#!/usr/bin/env python3
"""Gold Berlin: publish validated records to the GitHub Pages app (Rezaei-Git/Rezaei-Git.github.io, folder gold/).
Usage:  python3 sync_data.py payload.json
payload = {"prices":[{"_id":"YYYYMMDD-HHMM","ts":"...Z",...}], "spot":[...], "notifications":[...], "alerts":[...]}
 - prices/spot records are upserted by _id into gold/data/<kind>-YYYY-MM.json
 - notifications are upserted (last 200 kept); "alerts" (if present) replaces the list in gold/data.json
Needs the repo attached to the session (add_repo, push access). Uses a sparse git clone + push."""
import json, sys, os, subprocess, datetime, tempfile
URL='https://github.com/Rezaei-Git/Rezaei-Git.github.io'
def sh(*a, cwd=None, ok=False):
    r=subprocess.run(list(a),cwd=cwd,capture_output=True,text=True)
    if r.returncode and not ok: raise SystemExit('FAILED: '+' '.join(a)+'\n'+(r.stderr or r.stdout)[-600:])
    return r
def rd(path, default):
    try: return json.load(open(path, encoding='utf-8'))
    except FileNotFoundError: return default
def wr(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path,'w',encoding='utf-8'), ensure_ascii=False, separators=(',',':'))
def upsert(lst, recs):
    m={x['_id']:x for x in lst}
    for r in recs: m[r['_id']]=r
    return sorted(m.values(), key=lambda x:x.get('ts',''))
def apply(root, p, now):
    months=set(); rep=[]
    for kind in ('prices','spot'):
        for r in p.get(kind) or []:
            if '_id' not in r or 'ts' not in r: raise SystemExit('record needs _id and ts: '+json.dumps(r)[:200])
            ym=r['_id'][:4]+'-'+r['_id'][4:6]; months.add(ym)
            f=f'{root}/gold/data/{kind}-{ym}.json'; wr(f, upsert(rd(f,[]), [r])); rep.append(f'{kind} {r["_id"]}')
    idxf=f'{root}/gold/data.json'; idx=rd(idxf, {'months':[],'alerts':[],'notifications':[]})
    idx['months']=sorted(set(idx.get('months',[]))|months)
    if 'alerts' in p: idx['alerts']=p['alerts']; rep.append(f'alerts {len(p["alerts"])}')
    if p.get('notifications'): idx['notifications']=upsert(idx.get('notifications',[]), p['notifications'])[-200:]; rep.append(f'notifications +{len(p["notifications"])}')
    if p.get('prices') or 'alerts' in p or p.get('notifications') or months: idx['updated']=now
    wr(idxf, idx)
    return rep
def main():
    p=json.load(open(sys.argv[1], encoding='utf-8'))
    now=datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00','Z')
    d=tempfile.mkdtemp(prefix='goldsync-')
    for attempt in range(3):
        sh('rm','-rf',d); sh('git','clone','-q','--depth','1','--filter=blob:none','--sparse',URL,d)
        sh('git','sparse-checkout','set','gold',cwd=d)
        rep=apply(d,p,now)
        sh('git','add','gold',cwd=d)
        if not sh('git','status','--porcelain',cwd=d).stdout.strip(): print('SYNC OK · nothing changed'); return
        sh('git','-c','user.name=Gold Berlin bot','-c','user.email=a.rezaei.official@gmail.com','commit','-q','-m','gold: '+', '.join(rep)[:200],cwd=d)
        r=sh('git','push','-q','origin','HEAD:main',cwd=d,ok=True)
        if r.returncode==0: print('SYNC OK · '+' · '.join(rep)); return
    raise SystemExit('FAILED: push rejected 3 times\n'+(r.stderr or '')[-400:])
if __name__=='__main__': main()
