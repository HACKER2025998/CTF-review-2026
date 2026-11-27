#!/usr/bin/env python3
"""
NCTF26 KOTH — The Throne : TENUE active.

Re-plante à cadence courte pour être roi au maximum de ticks. Clé confirmée =
chaîne hex (key=str), donc 1 requête par cycle. Cadence 3 s = jeu normal du KOTH
(les autres équipes font pareil), PAS du flood volumétrique.

Si tu veux lever un peu la pression serveur, remonte INTERVAL ; si tu te fais
distancer, descends-le prudemment (ne vise pas < 1-2 s, ce serait du stress).
"""
import hmac, hashlib, time, json, urllib.request, urllib.error

HOST     = "http://13.37.197.230:28490"
TEAM     = "242cb7b1d3645528"
HILL_KEY = "d2e775a9aa7633e140a43cb6998778e7c63f7abeb4e3f583"
INTERVAL = 3

def claim():
    ts = int(time.time())
    sig = hmac.new(HILL_KEY.encode(), f"{TEAM}|{ts}".encode(), hashlib.sha1).hexdigest()
    body = json.dumps({"team": TEAM, "ts": ts, "sig": sig}).encode()
    req = urllib.request.Request(f"{HOST}/throne", data=body,
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            return r.status, r.read().decode(errors="replace")[:120]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode(errors="replace")[:120]
    except Exception as e:
        return 0, str(e)

print(f"[hold] The Throne — re-plante toutes les {INTERVAL}s (Ctrl-C pour arrêter)")
n = 0
while True:
    code, txt = claim()
    n += 1
    print(f"#{n} {code} {txt}")
    time.sleep(INTERVAL)
