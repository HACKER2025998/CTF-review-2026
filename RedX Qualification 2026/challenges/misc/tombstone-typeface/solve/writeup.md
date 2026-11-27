# Tombstone typeface — Write-up

- **Category:** Misc
- **Author:** FBI_Soldier
- **Flag:** `RxR{gsub_st4t3_m4ch1n3_3p1t4ph}`

## TL;DR

The "judge" is **not** JavaScript — it is the font `reaper.ttf` itself. Its `GSUB`
table implements a **finite-state automaton** over OpenType contextual
substitutions (`calt`). Typing the one correct name drives the automaton into an
accept state, which makes the font carve `ACCEPTED`; anything else carves
`REJECTED`. Extracting the automaton and searching it for the accepting string
yields the flag.

## Recon

`epitaph.html` just mirrors the `<input>` into a `<div>`:

```js
i.addEventListener("input", () => { out.textContent = i.value; });
```

No judging logic — confirmed by the challenge text ("no server, no password
check, no JavaScript doing the judging. The only thing deciding your fate is
`reaper.ttf`"). So the verdict is produced entirely by font shaping.

The font's `name` table contains a tempting decoy:

```
nameID 0: "Carved by the Reaper. Mason's mark: RxR{t0mbst0n3_s4ys_n0th1ng}"
```

`t0mbst0n3_s4ys_n0th1ng` ("the tombstone says nothing") is the hint that this is
a trap — the real flag is in the shaping logic, not in metadata.

## Font structure

```python
from fontTools.ttLib import TTFont
f = TTFont("reaper.ttf")
# 8005 glyphs, cmap of 66 chars (0-9 A-Z a-z _ { }), single feature: calt
# GSUB lookups: 122 x type1 (single subst), 2 x type2 (multiple subst), 2 x type6 (chaining context)
```

Shaping a few strings with HarfBuzz shows the mechanism:

```
shape("R")    -> ['R','space', <8 glyphs>]          # REJECTED tail
shape("RxR{") -> [carved,carved,carved,'braceleft','space', <8 glyphs>]
```

The trailing 8 glyphs are the verdict. Decoding them by their repeated glyph IDs:

- `glyph03052 05000 05000 06055 01675 07626 06055 06483` = **A C C E P T E D**
- `glyph07853 06055 00075 06055 05000 07626 06055 06483` = **R E J E C T E D**

The two **multiple-subst** lookups append these:

- **lookup 122** → `… ACCEPTED`
- **lookup 123** → `… REJECTED`

The `calt` feature applies two **chaining-context** lookups in order: `[124, 125]`.

- **Lookup 124** (122 subtables) is the **transition function**: each subtable
  matches `(backtrack = previous transformed glyph, input = current glyph)` and
  fires a nested single-subst that rewrites the current glyph into the **next
  state glyph**. This walks a state left-to-right across the typed text.
- **Lookup 125** reads the final glyph and decides the verdict. Its subtables, in
  order:
  - sub0: 7930 glyphs → no-op (consumes non-final glyphs)
  - sub1: **65 glyphs → lookup 122 (ACCEPTED)** ← the accept-final states
  - sub2: everything else → lookup 123 (REJECTED)

So the string is accepted **iff** after running the automaton the last glyph is
one of the 65 accept-final glyphs.

## Solving: rebuild the automaton and search it

There is no per-character leak (every char maps to a unique carved glyph, so
guessing position-by-position doesn't work). Instead, extract the transition
table statically and BFS from the start state to any accept-final glyph:

```python
from fontTools.ttLib import TTFont
from collections import deque

f = TTFont("reaper.ttf")
cm = f.getBestCmap(); char2glyph = {chr(c): n for c, n in cm.items()}
charset = sorted(char2glyph)
lut = f["GSUB"].table.LookupList.Lookup

# single-subst maps
single = {i: {k: v for st in l.SubTable for k, v in st.mapping.items()}
          for i, l in enumerate(lut) if l.LookupType == 1}

def apply_records(g, recs):
    for r in sorted(recs, key=lambda r: r.SequenceIndex):
        li = r.LookupListIndex
        if li in single and g in single[li]:
            g = single[li][g]
    return g

# transitions from lookup 124
T = []
for st in lut[124].SubTable:
    inp  = set(st.InputCoverage[0].glyphs)
    back = set(st.BacktrackCoverage[0].glyphs) if st.BacktrackCoverage else None
    T.append((inp, back, st.SubstLookupRecord))

def transition(state, cg):
    for inp, back, recs in T:
        if cg in inp and ((back is None and state is None) or
                          (back is not None and state in back)):
            return apply_records(cg, recs)
    return None  # no rule -> dead

ACCEPT = set(lut[125].SubTable[1].InputCoverage[0].glyphs)  # the 65 accept-final glyphs

seen, q = {}, deque()
for ch in charset:
    ns = transition(None, char2glyph[ch])
    if ns and ns not in seen:
        seen[ns] = ch; q.append((ns, ch))
while q:
    state, s = q.popleft()
    if state in ACCEPT:
        print("FLAG:", s); break
    for ch in charset:
        ns = transition(state, char2glyph[ch])
        if ns and ns not in seen:
            seen[ns] = s + ch; q.append((ns, s + ch))
```

The automaton has 185 reachable states and exactly **one** accepting string:

```
RxR{gsub_st4t3_m4ch1n3_3p1t4ph}
```

## Verification

Shaping it with HarfBuzz produces the `ACCEPTED` glyph run, and only this string
does:

```python
import uharfbuzz as hb
face = hb.Face(open("reaper.ttf", "rb").read())
def shape(s):
    font = hb.Font(face); buf = hb.Buffer(); buf.add_str(s)
    buf.guess_segment_properties(); hb.shape(font, buf, {"calt": True})
    return [g.codepoint for g in buf.glyph_infos]
# tail == ACCEPTED glyph ids only for RxR{gsub_st4t3_m4ch1n3_3p1t4ph}
```

## Flag

```
RxR{gsub_st4t3_m4ch1n3_3p1t4ph}
```

> Decoy to avoid: `RxR{t0mbst0n3_s4ys_n0th1ng}` (in the font's `name` table).
