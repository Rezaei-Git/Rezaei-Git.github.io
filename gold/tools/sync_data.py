#!/usr/bin/env python3
"""Gold Berlin: push validated records to GitHub Pages (Rezaei-Git/Rezaei-Git.github.io, folder gold/).
Usage: python3 sync_data.py payload.json
payload = {"prices":[{"_id":"YYYYMMDD-HHMM","ts":...,...}], "spot":[...], "notifications":[...], "alerts":[...]}
- prices/spot records are upserted by _id into gold/data/<kind>-YYYY-MM.json
- notifications are upserted (last 200 kept); alerts (if the key is present) replace the list
Uses the GitHub contents API through the gh CLI. Prints a short report."""
import json, sys, base64, subprocess, datetime
REPO='repos/Rezaei-Git/Rezaei-Git.github.io/contents/gold/'
def gh(args, inp=None):
    r=subprocess.run(['gh','api']+args,input=inp,capture_output=True,text=True)
    return r.returncode, r.stdout, r.stderr
def get(path):
    c,o,e=gh([REPO+path,'--jq','.sha'])
    if c!=0:
        if '404' in e or 'Not Found' in e or 'Not Found' in o: return None, None
        raise SystemExit('GET failed '+path+': '+e.strip()[:300])
    sha=o.strip()
    c,raw,e=gh([REPO+path,'-H','Accept: application/vnd.github.raw'])
    if c!=0: raise SystemExit('GET raw failed '+path+': '+e.strip()[:300])
    return json.loads(raw), sha
def put(path, obj, sha, msg):
    body={'message':msg,'branch':'main','content':base64.b64encode(json.dumps(obj,ensure_ascii=False,separators=(',',':')).encode()).decode()}
    if sha: body['sha']=sha
    return gh(['-X','PUT',REPO+path,'--input','-'], json.dumps(body))
def upsert(lst, recs):
    m={x['_id']:x for x in lst}
    for r in recs: m[r['_id']]=r
    return sorted(m.values(), key=lambda x:x.get('ts',''))
def save(path, mutate, msg):
    for attempt in range(3):
        cur, sha = get(path)
        new = mutate(cur)
        if new is None: return 'unchanged'
        c,o,e = put(path, new, sha, msg)
        if c==0: return 'ok'
        if '409' in e or '422' in e or 'does not match' in e: continue
        raise SystemExit('PUT failed '+path+': '+e.strip()[:300])
    raise SystemExit('PUT failed after retries '+path)
def main():
    p=json.load(open(sys.argv[1]))
    now=datetime.datetime.utcnow().replace(microsecond=0).isoformat()+'Z'
    rep=[]; months=set()
    for kind in ('prices','spot'):
        recs=p.get(kind) or []
        for r in recs:
            assert '_id' in r and 'ts' in r, 'record needs _id and ts'
        bym={}
        for r in recs: bym.setdefault(r['_id'][:4]+'-'+r['_id'][4:6],[]).append(r)
        for ym,rs in bym.items():
            months.add(ym)
            rep.append(f'{kind}-{ym}: '+save(f'data/{kind}-{ym}.json', lambda cur,rs=rs: upsert(cur or [], rs), f'gold: {kind} {rs[-1]["_id"]}'))
    touch = 'notifications' in p or 'alerts' in p or bool(p.get('prices'))
    def mut(cur):
        cur = cur or {'months':[], 'alerts':[], 'notifications':[]}
        ms=set(cur.get('months',[]))
        if not touch and months <= ms: return None
        cur['months']=sorted(ms|months)
        if 'alerts' in p: cur['alerts']=p['alerts']
        if p.get('notifications'): cur['notifications']=upsert(cur.get('notifications',[]), p['notifications'])[-200:]
        cur['updated']=now
        return cur
    rep.append('data.json: '+save('data.json', mut, 'gold: update index'))
    print('SYNC OK · '+' · '.join(rep))
if __name__=='__main__': main()
