# shell-lock — reversing a self-decrypting shell script

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/shell-lock/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — `lock.sh` derives a password from a hex string XORed with `0x2a`,
> then XOR-decrypts a base64 blob with that password to print the flag. Both
> transforms are static, so there is no need to brute or run anything.
> Flag: `NCTF{sh3l…}`.


## 1. Briefing
A self-decrypting shell script that prints the flag when run with the right
password.

```sh
#!/bin/sh
_k=5942194646755d1b504b584e
_b=PStnKhcsHwIWDS0XFgRVMwhsFEMDEQY7Aw0AAAk7Cg==
_p=$(printf '%s' "$_k" | perl -ne 'chomp;print chr(hex($1)^0x2a)while/(..)/g')
[ "$1" = "$_p" ] || { echo "access denied"; exit 1; }
printf '%s' "$_b" | base64 -d | perl -e '$k=shift;local $/;$d=<STDIN>;print join("",map{chr(ord(substr($d,$_,1))^ord(substr($k,$_%length($k),1)))}0..length($d)-1),"\n"' "$_p"
```

## 2. Analysis
Two static secrets:
- `_k` — hex bytes, each XORed with `0x2a` to produce the password `_p`.
- `_b` — base64 blob, XOR-decrypted with `_p` (repeating key) to get the flag.

Neither depends on runtime state, so both can be replicated directly.

## 3. Exploitation

```
# Password: hex pairs XOR 0x2a
59 42 19 46 46 75 5d 1b 50 4b 58 4e  →  sh3ll_w1zard
```

```js
const bin = atob('PStnKhcsHwIWDS0XFgRVMwhsFEMDEQY7Aw0AAAk7Cg==');
const k = 'sh3ll_w1zard';
let out = '';
for (let i = 0; i < bin.length; i++)
  out += String.fromCharCode(bin.charCodeAt(i) ^ k.charCodeAt(i % k.length));
// out === NCTF{sh3l…}
```

## 4. Flag
```
NCTF{sh3l…}
```

## 5. Lessons & remediation
XOR and base64 are obfuscation, not encryption. Any "password check" whose
expected value is derived from constants shipped alongside it can be recovered
by re-implementing the derivation offline.
