#!/usr/bin/env python3
"""Gold Berlin — automatic price collector (runs in GitHub Actions every 30 minutes).
Reads dealer price lists + world spot, validates every number, appends to gold/data/*.json.
Rule: a missing price is acceptable, a wrong price is not."""
import json, re, html, os, sys, time, datetime, requests
from zoneinfo import ZoneInfo
ROOT=os.path.join(os.path.dirname(__file__),'..'); BER=ZoneInfo('Europe/Berlin')
UA={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1','Accept-Language':'de-DE,de;q=0.9'}
N=r'(\d{1,3}(?:\.\d{3})*,\d{2})'
def num(s): return float(s.replace('.','').replace(',','.'))
def page(u):
    r=requests.get(u,headers=UA,timeout=40); r.raise_for_status()
    h=re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>',' ',r.text); h=re.sub(r'<[^>]+>',' ',h); h=html.unescape(h)
    return re.sub(r'\s+',' ',h.replace('-->',' ')).strip()
def find(t,pat):
    m=re.search(pat,t); return m
SIZES=[(1,'1g'),(5,'5g'),(10,'10g'),(100,'100g')]
def p_philoro(t):
    d={};raw=None
    for w,s in SIZES:
        m=find(t,r'Goldbarren '+str(w)+r' g - philoro [\d.,]+ g Verkaufspreis '+N+r' € Kaufpreis '+N+r' €')
        if m:
            d[f'philoro_{s}_sell']=num(m.group(1)); d[f'philoro_{s}_buy']=num(m.group(2))
            if w==1: raw=m.group(0)
    return d,raw,None
def p_proaurum(t):
    d={};raw=None
    for w,s in SIZES:
        name=f'Goldbarren {w} Gramm Heraeus'+(' geprägt' if w==100 else '')
        m=find(t,re.escape(name)+r' '+str(w)+r',00 g '+N+r' € '+N+r' €')
        if m:
            d[f'proaurum_{s}_sell']=num(m.group(1)); d[f'proaurum_{s}_buy']=num(m.group(2))
            if w==1: raw=m.group(0)
    st=find(t,r'Zuletzt aktualisiert am (\d\d\.\d\d\.\d{4}) um (\d\d:\d\d:\d\d)')
    return d,(raw+f' (page stamp {st.group(1)} {st.group(2)})' if raw and st else raw),None
def p_degussa(t):
    m=find(t,r'1 g Degussa Goldbarren \(geprägt\) '+N+r' €')
    return ({'degussa_1g_buy':num(m.group(1))} if m else {}),(m.group(0) if m else None),None
def p_ge(t):
    d={};raw=None
    for w,s in SIZES:
        m=find(t,r'Goldbarren '+str(w)+r' Gramm '+str(w)+r'g '+N+r' € '+N+r' €')
        if m:
            d[f'goldexchange_{s}_buy']=num(m.group(1)); d[f'goldexchange_{s}_sell']=num(m.group(2))
            if w==1: raw=m.group(0)
    return d,raw,None
def p_rs(t):
    names={'1g':'1 g Heraeus oder Umicore Goldbarren Neuware','5g':'5 g Heraeus Goldbarren Neuware','10g':'10 g Heraeus Goldbarren Neuware','100g':'100 g C. Hafner Goldbarren geprägt Neuware'}
    d={};raw=None
    for s,n in names.items():
        m=find(t,r'(?<![\d,.])'+re.escape(n)+r' '+N+r' €')
        if m:
            d[f'rs_{s}_buy']=num(m.group(1))
            if s=='1g': raw=m.group(0)
    return d,raw,None
def p_hatay(t):
    d={}
    for k,n in (('ceyrek','Çeyrek Resat'),('yarim','Yarim Resat'),('tam','Tam Resat')):
        m=find(t,r'(?:Münze '+n+r' )+'+N+r' €')
        if m: d[f'hatay_{k}_resat']=num(m.group(1))
    return d,(' | '.join(f'{k} {v:.2f} €' for k,v in d.items()) or None),None
DEALERS={'philoro':('https://philoro.de/preisliste/goldbarren',p_philoro),
 'proaurum':('https://www.proaurum.de/shop/preisliste-onlineshop/gold/',p_proaurum),
 'degussa':('https://www.degussa.com/de-de/1-g-degussa-goldbarren-gepraegt-p2546/',p_degussa),
 'goldexchange':('https://www.gold-exchange.de/Preisliste/',p_ge),
 'rs':('https://shop.rheinische-scheidestaette.de/gold/goldbarren/',p_rs),
 'hatay':('https://www.hatay.de',p_hatay)}
OZ=31.1035
def spot():
    out={};errs=[]
    try:
        t=page('https://www.gold.de/kurse/goldpreis/gramm/')
        m=find(t,r'Goldpreis in EUR je Gramm \(1 g\) '+N+r' EUR'); a=num(m.group(1)) if m else None
    except Exception as e: a=None; errs.append('gold.de '+str(e)[:80])
    b=pc=hi=lo=None
    try:
        t=page('https://www.goldpreis.de/')
        def oz(lbl):
            m=find(t,lbl+r' [\d.,]+ USD '+N+r' EUR'); return round(num(m.group(1))/OZ,2) if m else None
        b=oz(r'Heute \(\d\d\.\d\d\.\d{4}\)'); pc=oz(r'Vortag \(\d\d\.\d\d\.\d{4}\)'); lo=oz('Tagestief'); hi=oz('Tageshoch')
    except Exception as e: errs.append('goldpreis.de '+str(e)[:80])
    g=a if a else b
    if a and b and abs(a-b)/b>0.015: return None,'sources disagree %.2f vs %.2f'%(a,b)
    if not g or not (50<=g<=300): return None,'no valid spot '+'; '.join(errs)
    out={'g':round(g,2),'src':'gold.de/goldpreis.de'}
    if pc and 0.9*g<=pc<=1.1*g: out['prev_close']=pc
    if hi and lo and hi>=lo and abs(hi-g)/g<=0.05 and abs(lo-g)/g<=0.05: out['high']=hi; out['low']=lo
    return out,None
def rd(p,dflt):
    try: return json.load(open(p,encoding='utf-8'))
    except FileNotFoundError: return dflt
def wr(p,o):
    os.makedirs(os.path.dirname(p),exist_ok=True); json.dump(o,open(p,'w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
def last_prices(now):
    idx=rd(f'{ROOT}/data.json',{'months':[]}); out=[]
    for m in sorted(idx.get('months',[]))[-2:]: out+=rd(f'{ROOT}/data/prices-{m}.json',[])
    return sorted(out,key=lambda x:x.get('ts',''))
def validate(rec,S,prev):
    errs={}
    def drop(dealer,keys,why):
        for k in keys: rec.pop(k,None)
        errs[dealer]=(errs.get(dealer,'')+'; ' if dealer in errs else '')+why
    for dealer in ['philoro','proaurum','degussa','goldexchange','rs']:
        for w,s in SIZES:
            b=rec.get(f'{dealer}_{s}_buy'); se=rec.get(f'{dealer}_{s}_sell')
            if S:
                lo,hi=(1.00,1.45) if w==1 else (1.00,1.15)
                if b is not None and not (lo*S<=b/w<=hi*S): drop(dealer,[f'{dealer}_{s}_buy'],f'{s} buy out of range')
                if se is not None and not (0.85*S<=se/w<=1.02*S): drop(dealer,[f'{dealer}_{s}_sell'],f'{s} sell out of range')
            b=rec.get(f'{dealer}_{s}_buy'); se=rec.get(f'{dealer}_{s}_sell')
            if b is not None and se is not None and not b>se: drop(dealer,[f'{dealer}_{s}_buy',f'{dealer}_{s}_sell'],f'{s} buy<=sell')
        pg=[(w,rec.get(f'{dealer}_{s}_buy')) for w,s in SIZES if rec.get(f'{dealer}_{s}_buy') is not None]
        for (w1,b1),(w2,b2) in zip(pg,pg[1:]):
            if b2/w2>b1/w1+1e-9: drop(dealer,[f'{dealer}_{s}_buy' for _,s in SIZES]+[f'{dealer}_{s}_sell' for _,s in SIZES],'per-gram order inconsistent'); break
    return errs
def main():
    now=datetime.datetime.now(datetime.timezone.utc); nb=now.astimezone(BER)
    rid=nb.strftime('%Y%m%d-%H%M'); ym=nb.strftime('%Y-%m'); ts=now.replace(microsecond=0).isoformat().replace('+00:00','Z')
    sp,sperr=spot(); S=sp['g'] if sp else None
    hist=last_prices(now); prev=hist[-1] if hist else {}
    rec={'_id':rid,'ts':ts}; raws={}; errs={}
    for name,(url,fn) in DEALERS.items():
        try:
            d,raw,_=fn(page(url))
            if not d: errs[name]='rows not found on page'
            rec.update(d); 
            if raw: raws['raw_'+name]=raw[:160]
        except Exception as e: errs[name]='fetch failed: '+str(e)[:80]
    # >6% jump vs previous record -> confirm with a second read
    jumps={k for k,v in rec.items() if isinstance(v,(int,float)) and isinstance(prev.get(k),(int,float)) and prev[k] and abs(v-prev[k])/prev[k]>0.06}
    if jumps:
        time.sleep(20)
        for name,(url,fn) in DEALERS.items():
            ks=[k for k in jumps if k.startswith(name+'_')]
            if not ks: continue
            try: d2,_,_=fn(page(url))
            except Exception: d2={}
            for k in ks:
                if d2.get(k)!=rec.get(k): rec.pop(k,None); errs[name]=errs.get(name,'')+f' {k} jump not confirmed'
    if S: rec['spot_g']=S
    errs.update(validate(rec,S,prev))
    rec.update(raws)
    for k,v in errs.items(): rec['err_'+k]=v.strip('; ')
    nums=[k for k in rec if k.endswith('_buy') or k.endswith('_sell')]
    changed=[k for k in nums if rec.get(k)!=prev.get(k)]
    wrote=[]
    if nums and (changed or not prev):
        f=f'{ROOT}/data/prices-{ym}.json'; lst=rd(f,[]); lst.append(rec); wr(f,lst); wrote.append('prices')
    if sp:
        f=f'{ROOT}/data/spot-{ym}.json'; lst=rd(f,[]); lst.append(dict(_id=rid,ts=ts,**sp)); wr(f,lst); wrote.append('spot')
    idx=rd(f'{ROOT}/data.json',{'months':[],'alerts':[],'notifications':[]})
    idx['months']=sorted(set(idx.get('months',[]))|{ym}); idx['updated']=ts; idx['collector']={'ts':ts,'errors':errs,'spot_error':sperr,'wrote':wrote}
    wr(f'{ROOT}/data.json',idx)
    print(json.dumps({'id':rid,'spot':sp,'spot_err':sperr,'n_prices':len(nums),'changed':len(changed),'errors':errs,'wrote':wrote},ensure_ascii=False))
if __name__=='__main__': main()
