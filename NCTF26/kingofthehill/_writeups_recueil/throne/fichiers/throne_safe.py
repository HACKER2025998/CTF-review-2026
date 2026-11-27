#!/usr/bin/env python3
"""NCTF The Throne: send a single signed claim, optionally at a low rate.

Reads TEAM/HILL_KEY/URL from an existing throne_wrk_loop.sh as plain text.
Does NOT execute the shell script or use wrk.
"""
import argparse
import hashlib
import hmac
import json
from pathlib import Path
import re
import sys
import time
from urllib import request, error
from urllib.parse import urlparse


def read_config(filename):
    content = Path(filename).read_text(encoding="utf-8")
    params = {}
    for key in ("TEAM", "HILL_KEY", "URL"):
        found = re.search(rf'(?m)^{key}="([^"]+)"\s*$', content)
        if not found:
            raise ValueError(f"Missing quoted {key}=... in {filename}")
        params[key] = found.group(1)
    parsed = urlparse(params["URL"])
    if parsed.scheme not in ("http", "https") or not parsed.hostname or parsed.path != "/throne":
        raise ValueError("Unexpected URL; expected http(s)://<host>:<port>/throne")
    return params


def claim(config, dry_run=False):
    timestamp = int(time.time())
    team = config["TEAM"]
    message = f"{team}|{timestamp}".encode("utf-8")
    signature = hmac.new(config["HILL_KEY"].encode("utf-8"), message, hashlib.sha1).hexdigest()
    payload = {"team": team, "ts": timestamp, "sig": signature}
    if dry_run:
        print(f"[DRY RUN] URL={config['URL']} team={team} timestamp={timestamp}")
        print("[DRY RUN] Payload validated, signature computed (not displayed). No network request sent.")
        return
    req = request.Request(
        config["URL"],
        data=json.dumps(payload, separators=(",", ":")).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": "NCTF-team-claim/1.0"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=12) as response:
            body = response.read(4096).decode("utf-8", errors="replace")
            print(f"[{time.strftime('%H:%M:%S')}] HTTP {response.status}: {body}", flush=True)
    except error.HTTPError as exc:
        body = exc.read(4096).decode("utf-8", errors="replace")
        print(f"[{time.strftime('%H:%M:%S')}] HTTP {exc.code}: {body}", flush=True)
    except error.URLError as exc:
        print(f"[{time.strftime('%H:%M:%S')}] Network error: {exc.reason}", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Send a low-rate HMAC claim to The Throne")
    parser.add_argument("config", help="Path to original throne_wrk_loop.sh (read only)")
    parser.add_argument("--dry-run", action="store_true", help="Check locally, without network access")
    parser.add_argument("--loop", action="store_true", help="Send one signed request every 35 seconds")
    args = parser.parse_args()
    try:
        config = read_config(args.config)
        if args.dry_run:
            claim(config, dry_run=True)
        elif args.loop:
            print("Starting bounded claim loop: one request every 35s. Ctrl+C to stop.", flush=True)
            while True:
                claim(config)
                time.sleep(35)
        else:
            claim(config)
    except KeyboardInterrupt:
        print("\nStopped.")
    except (ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
