
#!/usr/bin/env python3

import requests
import re
import time
from kpata_manger_core import manger, decode_candidates

URL = "https://l726eaofb7dbvwt4.t.ctf.tg"

session = requests.Session()
session.headers.update({"User-Agent": "NCTF26-Kpata-Solver"})

print("[+] Connexion à Kpata...", flush=True)

r = session.get(URL + "/challenge", timeout=15)
r.raise_for_status()

challenge = r.json()

n = int(challenge["n"])
e = int(challenge["e"])
c = int(challenge["c"])

print("[+] Paramètres RSA récupérés", flush=True)
print("[+] Bits du module :", n.bit_length(), flush=True)

count = 0

def oracle(ciphertext):
    global count

    for attempt in range(5):
        try:
            response = session.get(
                URL + "/oracle",
                params={"c": str(ciphertext)},
                timeout=15,
            )
            response.raise_for_status()

            result = response.json()
            if "valid" not in result:
                raise ValueError(f"Réponse inattendue : {result}")

            count += 1

            if count % 50 == 0:
                print(
                    f"[*] {count} requêtes effectuées",
                    flush=True
                )

            return result["valid"] is True

        except (requests.RequestException, ValueError) as ex:
            print(f"[!] Erreur réseau : {ex}", flush=True)
            time.sleep(min(2 ** attempt, 10))

    raise RuntimeError("Oracle indisponible après 5 essais")

# Vérifier la signification du booléen
print("[+] Test de l'oracle...", flush=True)

assert oracle(1), "L'oracle doit accepter c=1"
assert not oracle(n - 1), "L'oracle doit refuser c=n-1"
assert oracle(c), "Le ciphertext original doit être valide"

print("[+] Oracle opérationnel !", flush=True)
print("[+] Démarrage de Manger...", flush=True)

m, queries = manger(n, e, c, oracle)

print("[+] Bloc RSA récupéré !", flush=True)
print("[+] Requêtes :", count, flush=True)

em = decode_candidates(m, n)

matches = re.findall(rb"NCTF\{[^}]+\}", em)

for flag in matches:
    print("\n" + "=" * 50)
    print("FLAG :", flag.decode())
    print("=" * 50)

if not matches:
    print("[*] Bloc OAEP brut :", em.hex())
