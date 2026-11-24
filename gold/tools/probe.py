import json, re, html, requests, datetime
UA={'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1','Accept-Language':'de-DE,de;q=0.9'}
T={'philoro':('https://philoro.de/preisliste/goldbarren',['Goldbarren 1 g - philoro','Goldbarren 100 g - philoro']),
 'proaurum':('https://www.proaurum.de/shop/preisliste-onlineshop/gold/',['Goldbarren 1 Gramm Heraeus','Zuletzt aktualisiert']),
 'degussa':('https://www.degussa.com/de-de/1-g-degussa-goldbarren-gepraegt-p2546/',['1 g Degussa Goldbarren']),
 'goldexchange':('https://www.gold-exchange.de/Preisliste/',['Goldbarren 1 Gramm','Goldbarren 100 Gramm']),
 'rs':('https://shop.rheinische-scheidestaette.de/gold/goldbarren/',['1 g Heraeus oder Umicore','100 g C. Hafner']),
 'hatay':('https://www.hatay.de',['Çeyrek','Tam Resat']),
 'golddе':('https://www.gold.de/kurse/goldpreis/gramm/',['Gramm','EUR']),
 'goldpreis':('https://www.goldpreis.de/',['Vortag','Tageshoch']),
 'goldapi':('https://api.gold-api.com/price/XAU',[]),
 'ecb':('https://api.frankfurter.app/latest?from=USD&to=EUR',[]),
}
def text(h):
    h=re.sub(r'(?is)<(script|style)[^>]*>.*?</\1>',' ',h); h=re.sub(r'<[^>]+>',' ',h); h=html.unescape(h); return re.sub(r'\s+',' ',h)
out={'ts':datetime.datetime.utcnow().isoformat()+'Z'}
for k,(u,keys) in T.items():
    try:
        r=requests.get(u,headers=UA,timeout=30); t=text(r.text)
        e={'status':r.status_code,'len':len(r.text),'textlen':len(t)}
        if not keys: e['body']=r.text[:600]
        for key in keys:
            i=t.find(key); e[key]=t[max(0,i-60):i+400] if i>=0 else None
        out[k]=e
    except Exception as ex: out[k]={'error':str(ex)[:200]}
import os; os.makedirs('gold/debug',exist_ok=True)
json.dump(out,open('gold/debug/probe.json','w'),ensure_ascii=False,indent=1)
