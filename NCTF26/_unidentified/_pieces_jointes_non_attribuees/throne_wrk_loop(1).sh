#!/bin/bash
# Flood The Throne using wrk, refreshing the signed claim every 35s
# (signature window is 45s, so 35s gives margin).

TEAM="242cb7b1d3645528"
HILL_KEY="49f52b539ba95d2f68d632428f007371c78a984eb9011d2a"
URL="http://13.37.197.230:28490/throne"
LUA="$HOME/Téléchargements/throne.lua"
THREADS=16
CONNECTIONS=400
DURATION="35s"

while true; do
  TS=$(date +%s)
  SIG=$(python3 -c "
import hmac, hashlib
team='$TEAM'
ts=$TS
key='$HILL_KEY'
msg = f'{team}|{ts}'.encode()
print(hmac.new(key.encode(), msg, hashlib.sha1).hexdigest())
")
  export CLAIM_BODY="{\"team\":\"$TEAM\",\"ts\":$TS,\"sig\":\"$SIG\"}"
  echo "[*] $(date '+%H:%M:%S') claiming with ts=$TS sig=${SIG:0:12}..."
  wrk -t$THREADS -c$CONNECTIONS -d$DURATION "$URL" -s "$LUA"
done
