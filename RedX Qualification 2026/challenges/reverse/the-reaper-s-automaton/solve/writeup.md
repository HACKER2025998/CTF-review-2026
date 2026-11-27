# The Reaper's Automaton — Write-up

- **Category:** Reverse
- **Flag:** `RxR{vm_wh1sp3rs_fr0m_th3_cryp7_0f_byt3s}`

## TL;DR

A stripped static x86-64 binary runs a tiny **byte-code VM**. The VM program is
decoded at runtime from `.rodata` using a keystream whose seed depends on an
**anti-debug** check. The program is a CBC-like stream cipher over the 35 inner
flag characters, checked against a 35-byte table. Recover the seed, lift the VM's
instruction set, then invert the cipher.

## Recon

- Prompt: `The reaper's automaton stirs. Speak the flag:`; success:
  `The grave accepts you. The flag is correct.`
- Input is validated: prefix `RxR{`, suffix `}`, **total length `0x28` = 40**
  (so 35 inner chars).
- Anti-debug: `fopen("/proc/self/status")` + `strtol` on `TracerPid:`, and an
  `int3` whose `SIGTRAP` handler sets a flag at `0x40c8`.

## The runtime-decoded program

A loop at `0x11a0` decodes 69 bytes from `0x2140` into `.bss` (`0x4080`):

```c
eax = seed;                       // seed derived from the anti-debug result
for (i = 0; i < 0x45; i++) {
    prog[i] = data2140[i] ^ (eax & 0xff);
    eax = (eax*0x6d) & 0xffffffff;
    eax = (eax + 0x3b) & 0xff;
}
```

Rather than untangle the exact seed arithmetic, brute all 256 seeds and keep the
one whose decoded program runs cleanly (valid opcodes, reaches `HALT`, performs
all 35 checks): **seed = `0x7c`**.

## The VM instruction set

Dispatch at `0x1290`: `op = prog[pc]; op -= 0x11; if (op > 0xd) fail;` then an
indexed jump (table at `0x20c0`). Operands `A = prog[pc+1]`, `B = prog[pc+2]`;
tape `T[256]`, input index `r9`, check index `r8`, error flag. Lifted opcodes:

| byte | mnemonic | effect | adv |
|---|---|---|---|
| 0x11 | SET  | `T[A] = B` | 3 |
| 0x12 | READ | `T[A] = input[r9++]` | 2 |
| 0x13 | XOR  | `T[A] ^= T[B]` | 3 |
| 0x14 | ADD  | `T[A] += T[B]` | 3 |
| 0x15 | ADDi | `T[A] += B` | 3 |
| 0x16 | ROL  | `T[A] = rol8(T[A], B)` | 3 |
| 0x17 | MOV  | `T[A] = T[B]` | 3 |
| 0x18 | MULi | `T[A] = T[A]*B` | 3 |
| 0x19 | DEC  | `T[A] -= 1` | 2 |
| 0x1a | CHECK| assert `T[A] == EXP[r8++]` else set error | 2 |
| 0x1b | JNZ  | if `T[A]!=0`: `pc += (int8)B` | 3 |
| 0x1c | HALT | success iff `r8==35 && error==0` | — |
| 0x1d | NOP  | — | 1 |
| 0x1e | SQ   | `T[A] = T[A]*T[A] + 1` | 2 |

`EXP` is the 35-byte table at `0x2100`.

## Disassembled program

```
SET T[1]=90 ; SET T[2]=165 ; SET T[3]=35 ; SET T[4]=0
loop (T[3] times, T[4] = round i = 0..34):
    READ  T[0] = input[i]
    XOR   T[0] ^= T[1]
    MOV   T[5]=T[4]; MULi T[5]*=7; ADDi T[5]+=13      # T[5] = i*7 + 13
    ADD   T[0] += T[5]
    ROL   T[0] <<<= 3
    XOR   T[0] ^= T[2]
    CHECK T[0] == EXP[i]
    MOV   T[6]=T[1]; MULi T[6]*=27; ADD T[6]+=T[0]; ADDi T[6]+=49; MOV T[1]=T[6]
    MOV   T[2]=T[0]                                   # chaining (prev output)
    T[4]+=1 ; DEC T[3] ; JNZ T[3] -> loop
HALT
```

So, per round `i` (state `T1=90, T2=165` initially):

```
t = input[i] ^ T1
t = (t + (i*7 + 13)) & 0xff
t = rol3(t)
t = t ^ T2
assert t == EXP[i]
T1 = (T1*27 + t + 49) & 0xff ;  T2 = t
```

## Inversion

Every step is invertible; `t` is just `EXP[i]`:

```python
EXP = bytes.fromhex("6c38f93294285285f7f3b11c1e5ef9eccd7bf1fe53e7c4cf50122124320d5014acebc0")
ror3 = lambda v: ((v>>3)|(v<<5)) & 0xff
T1, T2 = 90, 165
inner = []
for i in range(35):
    t = EXP[i]
    t ^= T2
    t = ror3(t)
    t = (t - (i*7 + 13)) & 0xff
    t ^= T1
    inner.append(t)
    T1 = (T1*27 + EXP[i] + 49) & 0xff
    T2 = EXP[i]
flag = "RxR{" + bytes(inner).decode() + "}"
```

Re-running the full VM emulator on this input gives `r8 == 35, error == 0` →
`ACCEPTED`, and the length is exactly 40.

## Flag

```
RxR{vm_wh1sp3rs_fr0m_th3_cryp7_0f_byt3s}
```
