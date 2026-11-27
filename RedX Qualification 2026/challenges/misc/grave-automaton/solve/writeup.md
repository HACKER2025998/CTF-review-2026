# Grave automaton — Write-up

- **Category:** Misc
- **Flag:** `RxR{c0nw4y_gr4v3_4ut0m4t0n}`

## TL;DR

`board.txt` is a 570×1800 grid of `O`/`.`. The statement spells out **Conway's
Game of Life** ("a grave is dug where three surround an empty plot; a soul
perishes alone or in a crowd" = birth on 3 neighbours, survival on 2–3). Running
the simulation makes the random noise die out and leaves a stable still-life
drawing the flag.

## Recognising the rule

From the statement:

- "a grave is dug where three surround an empty plot" → a dead cell with exactly
  **3** live neighbours becomes alive (**birth**).
- "a soul perishes alone or in a crowd" → a live cell with <2 or >3 neighbours
  dies (**survival on 2–3**).

That is exactly Conway's Game of Life. "Let the garden live by its rules, and the
noise will settle — leaving the Reaper's message standing" → iterate until the
transient ash dies and only the still-life letters remain.

## Solve

```python
import numpy as np
from PIL import Image, ImageFilter

L = [l.rstrip("\n") for l in open("board.txt")]
h, w = len(L), max(map(len, L))
b = np.zeros((h, w), np.uint8)
for y, l in enumerate(L):
    for x, c in enumerate(l):
        if c == "O": b[y, x] = 1

def step(g):
    n = sum(np.roll(np.roll(g, dy, 0), dx, 1)
            for dy in (-1, 0, 1) for dx in (-1, 0, 1) if (dy, dx) != (0, 0))
    return ((n == 3) | ((g == 1) & (n == 2))).astype(np.uint8)

for _ in range(50):          # stabilises after ~11 generations
    b = step(b)

# crop + thicken the sparse still-life so the letters are legible
ys, xs = np.where(b)
img = Image.fromarray((1 - b[ys.min():ys.max()+1, xs.min():xs.max()+1]) * 255).convert("L")
img = img.resize((img.width*3, img.height*3), Image.NEAREST).filter(ImageFilter.MinFilter(5))
img.save("solved.png")
```

The board stabilises after ~11 generations. Rendered and thickened, the
surviving cells spell, over two lines:

```
RxR{c0nw4y_gr4
v3_4ut0m4t0n}
```

i.e. `RxR{c0nw4y_gr4v3_4ut0m4t0n}` — Conway + grave + automaton.

## Flag

```
RxR{c0nw4y_gr4v3_4ut0m4t0n}
```

> Decoy to avoid: `RxR{the_garden_decays_to_dust}` — an anti-AI prompt-injection
> hidden in a transparent `<span>` in the HTML statement, claiming the board
> "stabilizes to nothing". It does not; ignore it.
