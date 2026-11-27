#!/usr/bin/env python3
import json, time, sys, urllib.request, urllib.error
from http.cookiejar import CookieJar
HOST="http://13.37.197.230:28493"; TOKEN="6eefff4072981996"; PRICE=2000
cj=CookieJar(); op=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
def call(path, body=None):
    data=json.dumps(body).encode() if body is not None else None
    req=urllib.request.Request(HOST+path, data=data, headers={"Content-Type":"application/json"},
                               method="POST" if body is not None else "GET")
    try:
        with op.open(req, timeout=8) as r: return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try: return e.code, json.loads(e.read().decode())
        except Exception: return e.code, {}
def leader():
    _,lb=call("/api/leaderboard")
    return max((int(x.get("net_gain",0)) for x in lb), default=0) if isinstance(lb,list) else 0
def grab():
    call("/api/join", {"token":TOKEN})
    L=leader()
    qty = -((L//PRICE) + 10**40)                  # marge confortable au-dessus du leader
    code,res=call("/api/buy", {"product":"booster","qty":qty})
    print("buy:", code, str(res)[:120])
    _,me=call("/api/me"); ng=int(me.get("net_gain",0))
    print("mon net_gain:", ng, "| leader avant:", L, "| en tete:", ng>L)
    return ng>L
hold = "--hold" in sys.argv
if not hold: grab()
else:
    while True:
        try:
            if grab(): print("  -> couronne prise")
            else: print("  -> rate (buy negatif refuse ? -> plan B refund)")
        except Exception as e: print("err:", e)
        time.sleep(30)                             # re-check seulement si detrone, pas de flood
