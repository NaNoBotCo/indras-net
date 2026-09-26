#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""figures.py — the pictures and the numbers, computed here.

Writes build/figs.json (inline SVG by name) and build/facts.json (every number the pages
quote), so the text reads its numbers from the arithmetic and cannot drift from it.

    python3 tools/figures.py
"""
from __future__ import annotations

import json
import math
import random
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"

GOLD = "#ffd27a"
HUES = ["#ffb347", "#8fd0ff", "#c8a6ff", "#ff6a5e", "#7fe0a8", "#ffd27a"]


# ---------------------------------------------------------------- circle mirrors
def invert(c, m):
    """Circle c=(x,y,r) seen in the round mirror m=(X,Y,R). Returns the reflected circle."""
    x, y, r = c
    X, Y, R = m
    dx, dy = x - X, y - Y
    d2 = dx * dx + dy * dy
    s = R * R / (d2 - r * r)
    return (X + s * dx, Y + s * dy, abs(s) * r)


def ring(k, size):
    """k round mirrors on a ring of radius 1; size=1 makes neighbours touch."""
    r = math.sin(math.pi / k) * size
    return [(math.cos(2 * math.pi * j / k - math.pi / 2), math.sin(2 * math.pi * j / k - math.pi / 2), r)
            for j in range(k)]


def pearls(mirrors, max_depth, min_r=0.0):
    """Every reflection of every mirror in every other, down to max_depth bounces.
    A mirror is never reflected straight back in the one it was just seen in —
    that would undo the step. Returns [(x, y, r, depth)]."""
    out = []

    def walk(c, last, depth):
        out.append((c[0], c[1], c[2], depth))
        if depth >= max_depth or c[2] < min_r:
            return
        for j, m in enumerate(mirrors):
            if j != last:
                walk(invert(c, m), j, depth + 1)

    for j, m in enumerate(mirrors):
        walk(m, j, 0)
    return out


def svg_pearls(k, size, depth, min_r, w=640, h=640, span=1.62):
    cs = pearls(ring(k, size), depth, min_r)
    sc = w / (2 * span)
    parts = []
    for x, y, r, d in sorted(cs, key=lambda t: -t[2]):
        px, py, pr = w / 2 + x * sc, h / 2 + y * sc, r * sc
        if pr < 0.35:
            continue
        col = HUES[d % len(HUES)]
        op = 0.95 if d == 0 else max(0.35, 0.9 - 0.07 * d)
        sw = 1.6 if d == 0 else max(0.4, 1.2 - 0.1 * d)
        parts.append(f'<circle cx="{px:.2f}" cy="{py:.2f}" r="{pr:.2f}" fill="none" stroke="{col}" '
                     f'stroke-opacity="{op:.2f}" stroke-width="{sw:.2f}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
           f'aria-label="{k} round mirrors and their reflections in each other, {depth} bounces deep">'
           f'<rect width="{w}" height="{h}" fill="#000"/>' + "".join(parts) + "</svg>")
    return svg, len(cs)


# ---------------------------------------------------------------- Fazang's mirror room
def fold(v, a):
    """Where a point in the unfolded plane lands back in the one real room [0,1]."""
    n = math.floor(v)
    f = v - n
    return f if n % 2 == 0 else 1 - f


def svg_room(N=4, w=640, h=640, lamp=(0.38, 0.62)):
    """The one room in the middle, and every mirror-room around it, each with its lamp
    dimmed by how many bounces it took to get there."""
    cells = 2 * N + 1
    sz = w / cells
    parts = []
    for i in range(-N, N + 1):
        for j in range(-N, N + 1):
            b = abs(i) + abs(j)
            if b > N:
                continue
            x0, y0 = (i + N) * sz, (N - j) * sz
            lx = i + (lamp[0] if i % 2 == 0 else 1 - lamp[0])
            ly = j + (lamp[1] if j % 2 == 0 else 1 - lamp[1])
            px, py = (lx + N) * sz, (N + 1 - ly) * sz
            op = 0.82 ** b
            stroke = GOLD if b == 0 else "#2a2a38"
            parts.append(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{sz:.1f}" height="{sz:.1f}" fill="none" '
                         f'stroke="{stroke}" stroke-width="{2 if b == 0 else 1}"/>')
            parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{sz * 0.13:.1f}" fill="#ffb347" opacity="{op:.3f}"/>')
            parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="{sz * 0.3:.1f}" fill="#ffb347" opacity="{op * 0.18:.3f}"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
           f'aria-label="A square room of mirrors, unfolded: one lamp and its reflections up to {N} bounces">'
           f'<rect width="{w}" height="{h}" fill="#000"/>' + "".join(parts) + "</svg>")
    return svg


def room_count(N):
    return sum(1 for i in range(-N, N + 1) for j in range(-N, N + 1) if abs(i) + abs(j) <= N)


# ---------------------------------------------------------------- small world
def small_world(n, k, p, seed=1):
    """Watts–Strogatz: a ring where each knot holds hands with its k nearest, then each
    hand-hold is moved to a random stranger with chance p."""
    rnd = random.Random(seed)
    adj = [set() for _ in range(n)]
    for i in range(n):
        for s in range(1, k // 2 + 1):
            j = (i + s) % n
            adj[i].add(j); adj[j].add(i)
    for i in range(n):
        for s in range(1, k // 2 + 1):
            j = (i + s) % n
            if rnd.random() < p and j in adj[i]:
                choices = [t for t in range(n) if t != i and t not in adj[i]]
                if not choices:
                    continue
                t = rnd.choice(choices)
                adj[i].discard(j); adj[j].discard(i)
                adj[i].add(t); adj[t].add(i)
    return adj


def mean_hops(adj):
    n = len(adj)
    tot = cnt = 0
    for s in range(n):
        dist = [-1] * n
        dist[s] = 0
        q = deque([s])
        while q:
            a = q.popleft()
            for b in adj[a]:
                if dist[b] < 0:
                    dist[b] = dist[a] + 1
                    q.append(b)
        tot += sum(d for d in dist if d > 0)
        cnt += sum(1 for d in dist if d > 0)
    return tot / cnt


def clustering(adj):
    cs = []
    for a in range(len(adj)):
        nb = list(adj[a])
        kk = len(nb)
        if kk < 2:
            cs.append(0.0); continue
        links = sum(1 for i in range(kk) for j in range(i + 1, kk) if nb[j] in adj[nb[i]])
        cs.append(links / (kk * (kk - 1) / 2))
    return sum(cs) / len(cs)


def main():
    BUILD.mkdir(parents=True, exist_ok=True)
    figs, facts = {}, {}

    # pearls: the count formula checked against the walk itself
    for k in (3, 4, 5):
        for d in range(1, 7):
            got = len([c for c in pearls(ring(k, 0.9), d) if c[3] == d])
            want = k * (k - 1) ** d
            assert got == want, (k, d, got, want)
    facts["pearls_k4"] = [4 * 3 ** d for d in range(0, 11)]

    figs["pearls4"], n4 = svg_pearls(4, 0.96, 9, 0.0015)
    figs["pearls3"], n3 = svg_pearls(3, 1.0, 11, 0.0015)
    figs["pearls6"], n6 = svg_pearls(6, 0.93, 7, 0.0015)
    facts["pearls4_drawn"], facts["pearls3_drawn"], facts["pearls6_drawn"] = n4, n3, n6

    # a worked inversion, printed on the pearls page
    m = (0.0, 0.0, 1.0)
    c = (2.0, 0.0, 0.5)
    ci = invert(c, m)
    facts["inv_example"] = [round(v, 4) for v in ci]

    # Fazang's room
    figs["room"] = svg_room(4)
    facts["room"] = {N: room_count(N) for N in (1, 2, 3, 4, 10, 100)}
    for N in (1, 2, 3, 4, 10, 100):
        assert facts["room"][N] == 2 * N * N + 2 * N + 1

    # the jewel net: how many reflections deep before a jewel is smaller than a pixel
    W, D = 900, 44
    facts["net_depth"] = round(math.log(W) / math.log(W / D), 2)

    # small world: 1,000 knots, 10 hands each
    sw = {}
    for p in (0.0, 0.001, 0.01, 0.1, 1.0):
        adj = small_world(1000, 10, p, seed=7)
        sw[str(p)] = {"hops": round(mean_hops(adj), 2), "clustering": round(clustering(adj), 3)}
        print(f"small world p={p}: hops {sw[str(p)]['hops']}, clustering {sw[str(p)]['clustering']}")
    facts["small_world"] = sw

    (BUILD / "figs.json").write_text(json.dumps(figs), encoding="utf-8")
    (BUILD / "facts.json").write_text(json.dumps(facts, indent=1), encoding="utf-8")
    print(f"figures: {len(figs)} · pearls drawn k4={n4} k3={n3} k6={n6} · inversion {ci} · net depth {facts['net_depth']}")


if __name__ == "__main__":
    main()
