# Dijkstra Relay — the cheapest path spells the flag

> 📖 **Public write-up by [alwil17](https://github.com/Alwil17)** — originally published at <https://alwil17.github.io/ctf-writeups/posts/dijkstra-relay/>  
> Source: <https://github.com/Alwil17/ctf-writeups> · MIT License, © 2026 alwil17 (see `THIRD_PARTY_LICENSES/alwil17-ctf-writeups.LICENSE`). Front matter removed, article body unmodified.

> **TL;DR** — A weighted directed graph is given as an edge list. The node labels
> along the shortest path from source to target, read in order, spell the flag. I
> run Dijkstra, walk the predecessor chain back, and concatenate the labels.
> **Flag:** `NCTF{…}`.

## 1. Briefing

`graph.txt` is a weighted digraph: the first line is `<node_count> <edge_count>`,
followed by `u v w` edges. The task says the cheapest path from the source to the
target, by its node labels, is the flag.

## 2. Approach

This is a straight shortest-path problem — Dijkstra with a min-heap. The only CTF
twist is that each node carries a label character, and the answer is the labels
concatenated along the optimal path, not the distance.

## 3. Exploitation

```python
import heapq, pathlib

lines = pathlib.Path("graph.txt").read_text().split("\n")
n, m = map(int, lines[0].split())
adj = {i: [] for i in range(n)}
for ln in lines[1:1+m]:
    u, v, w = map(int, ln.split())
    adj[u].append((v, w))

src, tgt = 0, n - 1                      # per the challenge's endpoints
dist = {src: 0}; prev = {}; pq = [(0, src)]
while pq:
    d, u = heapq.heappop(pq)
    if d > dist.get(u, 1e18): continue
    for v, w in adj[u]:
        nd = d + w
        if nd < dist.get(v, 1e18):
            dist[v] = nd; prev[v] = u
            heapq.heappush(pq, (nd, v))

path, cur = [], tgt
while cur != src:
    path.append(cur); cur = prev[cur]
path.append(src); path.reverse()

flag = "".join(labels[v] for v in path)  # labels: per-node character table
print(flag)                              # NCTF{…}
```

## 4. Flag

```text
NCTF{…}
```

## 5. Notes

- The grind is parsing and bookkeeping, not the algorithm. Keep a `prev[]` map so
  you can reconstruct the path, not just the cost.
- Watch the endpoints: source/target are fixed by the challenge, and the labels
  must be read in path order (source → target).
