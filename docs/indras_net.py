#!/usr/bin/env python3
"""indras_net.py — the math under Indra's Net, Drawn, in one file, nothing to install.

    python3 indras_net.py

Three things:
  1. round mirrors reflecting round mirrors (circle inversion) and how fast they pile up
  2. Fazang's square room of mirrors: how many lamps you see within N bounces
  3. the small world: touch one knot, and how many hops to reach the rest
"""
import math
import random
from collections import deque


# 1 ---------------------------------------------------------------- round mirrors
def invert(c, m):
    """The circle c = (x, y, r) as seen in the round mirror m = (X, Y, R)."""
    x, y, r = c
    X, Y, R = m
    dx, dy = x - X, y - Y
    s = R * R / (dx * dx + dy * dy - r * r)
    return (X + s * dx, Y + s * dy, abs(s) * r)


def ring(k, size=0.95):
    """k round mirrors on a ring; size 1 makes neighbours touch."""
    r = math.sin(math.pi / k) * size
    return [(math.cos(2 * math.pi * j / k), math.sin(2 * math.pi * j / k), r) for j in range(k)]


def pearls(mirrors, depth):
    """Every mirror seen in every other, `depth` bounces deep. Never straight back
    into the mirror you just came out of — that undoes the bounce."""
    out = []

    def walk(c, last, d):
        out.append((c, d))
        if d < depth:
            for j, m in enumerate(mirrors):
                if j != last:
                    walk(invert(c, m), j, d + 1)

    for j, m in enumerate(mirrors):
        walk(m, j, 0)
    return out


# 2 ---------------------------------------------------------------- Fazang's room
def lamps_within(N):
    """Lamps in the unfolded grid of mirror-rooms that take N bounces or fewer."""
    return sum(1 for i in range(-N, N + 1) for j in range(-N, N + 1) if abs(i) + abs(j) <= N)


# 3 ---------------------------------------------------------------- touch one
def small_world(n, k, p, seed=7):
    rnd = random.Random(seed)
    adj = [set() for _ in range(n)]
    for i in range(n):
        for s in range(1, k // 2 + 1):
            adj[i].add((i + s) % n); adj[(i + s) % n].add(i)
    for i in range(n):
        for s in range(1, k // 2 + 1):
            j = (i + s) % n
            if rnd.random() < p and j in adj[i]:
                t = rnd.choice([t for t in range(n) if t != i and t not in adj[i]])
                adj[i].discard(j); adj[j].discard(i); adj[i].add(t); adj[t].add(i)
    return adj


def hops_from(adj, s):
    dist = {s: 0}
    q = deque([s])
    while q:
        a = q.popleft()
        for b in adj[a]:
            if b not in dist:
                dist[b] = dist[a] + 1
                q.append(b)
    return dist


if __name__ == "__main__":
    print("A circle of radius 0.5, centred 2 out, seen in a round mirror of radius 1 (x, y, r):",
          tuple(round(v, 4) for v in invert((2, 0, 0.5), (0, 0, 1))))
    for d in range(6):
        n = sum(1 for _, dd in pearls(ring(4), d) if dd == d)
        print(f"4 mirrors, bounce {d}: {n} circles  (4 x 3^{d} = {4 * 3 ** d})")
    for N in (1, 2, 4, 10):
        print(f"Fazang's room, within {N} bounces: {lamps_within(N)} lamps  (2N^2+2N+1 = {2*N*N+2*N+1})")
    for p in (0.0, 0.01, 0.1):
        adj = small_world(1000, 10, p)
        d = hops_from(adj, 0)
        print(f"1,000 knots, {p:.0%} rewired: farthest knot from #0 is {max(d.values())} hops")
