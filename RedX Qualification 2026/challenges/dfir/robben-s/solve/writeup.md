# Robben's — Write-up

- **Category:** DFIR
- **Flag:** `RxR{+05:00_156688_0x54_Sora}`

## Flag format

`RxR{offset_BytesTotal_key_name}`. Same Mirai-style infection as *Phantom*, but
the sensor log and the pcap "don't agree", so every answer must be proven from
the ground-truth capture, not the honeypot log.

## Files

- `cowrie.json` — honeypot log (timestamps end in `Z`).
- `capture.pcap` — ground-truth network capture.
- `robben.rodata.bin` — a dump of the deleted payload's read-only data section.

## 1. Real UTC offset of the sensor clock

Match one event in both sources. The first `GET /phantom.sh`:

- pcap (true UTC): `2026-07-23T23:48:38.289Z`
- cowrie log:      `2026-07-24T04:48:38.309Z` (labelled `Z`)

The sensor stamps `04:48:38` for an event that truly happened at `23:48:38` the
day before → the clock is running **5 hours ahead** of UTC while pretending to be
UTC.

→ **+05:00**

## 2. Bytes of payload builds actually received

The log claims some downloads failed, but the pcap shows what really arrived.
Successful HTTP transfers of the **arch builds** (the `.sh` dropper is not a
"build"), with every transfer counted:

```bash
tshark -r capture.pcap -Y http.response \
  -T fields -e http.content_length -e http.request.uri
```

```
24828  /bins/phantom.x86    (×2)
26236  /bins/phantom.mips   (×2)
27280  /bins/phantom.mpsl   (×2)
```

`2 × (24828 + 26236 + 27280) = 2 × 78344 =` **156688** bytes. (The `ftp://`
attempts the log marks failed never transferred payload bytes.)

→ **156688**

## 3. Single-byte key hiding the data section

`robben.rodata.bin` starts with the cleartext C2 IP `198.51.100.7`, then
obfuscated strings. The separator byte decodes to `0x00`, so XOR each byte and
score for known Mirai strings:

```python
d = open("robben.rodata.bin","rb").read()
for k in range(1,256):
    x = bytes(b ^ k for b in d)
    if b"/bin/busybox" in x:
        print(hex(k)); break   # 0x54
```

Key **0x54** reveals the credential table and strings like
`/bin/busybox SORA`, `SORA: applet not found`, `Connected To CNC`.

→ **0x54**

## 4. What the botnet calls itself

The classic Mirai self-check uses `/bin/busybox <NAME>`; the decoded strings show
`/bin/busybox SORA` and `SORA: applet not found`.

→ **Sora** (a Mirai variant)

## Flag

```
RxR{+05:00_156688_0x54_Sora}
```

> If the checker is picky about formatting, try the equivalents: offset `+5` /
> `UTC+5`, key `84`, name `SORA`.
