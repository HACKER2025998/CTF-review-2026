#!/usr/bin/env python3
"""
NCTF26 KOTH — Reseau Fortune (28493) : RECON posé, une seule passe.

Objectif de ce script : seulement COMPRENDRE l'économie (pas encore exploiter).
Il ouvre une session avec ton jeton, lit ton solde/score de départ, le
classement, et teste UN achat pour voir comment l'argent bouge.

Requêtes ESPACÉES (PAUSE s) pour respecter le rate-limit du hill et la règle
anti-flood. Aucune boucle. Si tu reprends "trop de requêtes", augmente PAUSE.
"""
import json, time, urllib.request, urllib.error
from http.cookiejar import CookieJar

HOST  = "http://13.37.197.230:28493"
TOKEN = "6eefff4072981996"     # jeton Reseau Fortune (secret)
PAUSE = 4                       # secondes entre deux requêtes

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

print("1) join")
call("/api/join", {"token": TOKEN});                  time.sleep(PAUSE)
print("2) état initial")
me = call("/api/me");                                 time.sleep(PAUSE)
print("3) classement")
call("/api/leaderboard");                             time.sleep(PAUSE)
print("4) un achat (pour voir le débit)")
buy = call("/api/buy", {"product": "booster", "qty": 1}); time.sleep(PAUSE)
print("5) état après achat")
call("/api/me");                                      time.sleep(PAUSE)
print("6) remboursement de cette commande (pour voir le crédit)")
if buy.get("order_id") is not None:
    call("/api/refund", {"order_id": buy["order_id"]}); time.sleep(PAUSE)
print("7) état après remboursement")
call("/api/me")
print("\n-> Colle TOUTE cette sortie. On repère où l'argent se crée.")
