#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""site.py — the pages, built from build/figs.json and build/facts.json.

    python3 tools/figures.py
    SITE_URL=https://nanobotco.github.io/indras-net python3 tools/site.py
"""
from __future__ import annotations

import html
import json
import os
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fleet  # noqa: E402
from css import CSS  # noqa: E402
import sources as S  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "build"
SITE = BUILD / "site"
SITE_URL = os.environ.get("SITE_URL", "https://nanobotco.github.io/indras-net").rstrip("/")
tail = SITE_URL.split("//", 1)[-1]
BASE = "/" + tail.split("/", 1)[1].rstrip("/") + "/" if "/" in tail else "/"
SELF = "indras-net"
NAME = "Indra's Net, Drawn"
TAG = ("A plain-spoken 'splainer of Indra's Net — the old picture of a net with a jewel at every knot, "
       "each jewel showin' all the others — read many ways, and drawn from the math of mirrors.")
TODAY = date.today().isoformat()
FLEET = fleet.load(ROOT / "data" / "fleet.json")
FACTS = json.loads((BUILD / "facts.json").read_text(encoding="utf-8"))
FIGS = json.loads((BUILD / "figs.json").read_text(encoding="utf-8"))
CREDIT = "Nan · hongdam.net · CC BY 4.0"
E = html.escape
URL = {s["id"]: s["url"] for s in FLEET["sites"]}

SIB = ("chaos", "three-body", "black-holes", "quantum-computing", "goin-fast", "exceptional-magic", "wichaa")

NAV = [("story/", "The story"), ("readings/", "Readings"), ("pearls/", "Pearls"),
       ("touch/", "Touch one"), ("code/", "Code"), ("words/", "Words"), ("sources/", "Sources")]

EXTRA = """
:root{--hot:#ffc861;--gold:#ffe3a3}
.reading{max-width:44rem;margin:.1rem 0 1.2rem;color:var(--ink);font-size:1rem}
.reading b{color:var(--gold);font-weight:700}
.eq var{font-style:italic}
.eq sub{font-size:.7em}
.eq .op{color:var(--mute);padding:0 .12em}
.win{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--hot);
 border-radius:12px;padding:1rem 1.1rem;margin:1.3rem 0;background-image:radial-gradient(120% 100% at 0% 0%,color-mix(in srgb,var(--hot) 12%,transparent),transparent 60%)}
.win h3{margin-top:.1rem}
.win p{max-width:none}
.srclist{padding-left:1.6rem;max-width:52rem}
.srclist li{margin:.5rem 0;font-size:.9rem;line-height:1.5;color:var(--ink)}
.srclist li a{color:var(--blue);text-decoration:none}
.dial{display:grid;grid-template-columns:auto 1fr;gap:.2rem 1rem;max-width:44rem;margin:1rem 0;font-size:.95rem}
.dial dt{font-family:var(--display);font-weight:800;color:var(--hot);text-transform:uppercase;font-size:.8rem;letter-spacing:.06em;padding-top:.35rem}
.dial dd{margin:0;padding:.25rem 0;border-bottom:1px solid var(--line)}
@media (max-width:36rem){.dial{grid-template-columns:1fr}.dial dt{padding-top:.8rem}}
figure.fig svg{display:block;width:100%;height:auto}
.next{display:flex;justify-content:space-between;gap:1rem;margin:2.4rem 0 0;flex-wrap:wrap}
.next a{font-family:var(--display);font-weight:800;text-transform:uppercase;letter-spacing:.04em;text-decoration:none;
 border:1px solid var(--line);padding:.6rem 1rem;border-radius:99px;color:var(--ink)}
.next a:hover{border-color:var(--hot);color:var(--hot)}
.gen .read{font-family:var(--body);padding:.2rem 1rem .9rem;margin:0;font-size:.92rem;max-width:none;color:var(--ink)}
.gen .read b{color:var(--gold)}
.gen canvas{cursor:pointer}
#pearl-canvas{max-width:min(100%,680px);margin:0 auto}
.readings{display:grid;grid-template-columns:repeat(auto-fit,minmax(18rem,1fr));gap:1rem;margin:1rem 0 1.6rem}
.rd{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:.9rem 1rem;position:relative;overflow:hidden}
.rd::before{content:"";position:absolute;right:-18px;top:-18px;width:64px;height:64px;border-radius:50%;
 background:radial-gradient(circle at 35% 35%,#fff8,var(--jw,#ffc861) 30%,#000 75%);opacity:.55}
.rd h3{margin:.1rem 0 .1rem;padding-right:2.6rem}
.rd .who{font-size:.72rem;text-transform:uppercase;letter-spacing:.12em;color:var(--mute);font-weight:700;margin:0 0 .5rem}
.rd p{font-size:.95rem;margin:.4rem 0}
.rd .stop{color:var(--mute);font-size:.86rem;border-top:1px dashed var(--line);padding-top:.45rem;margin-top:.6rem}
.rd .stop b{color:var(--ink)}
.dirt{counter-reset:d;list-style:none;padding:0;max-width:44rem}
.dirt li{counter-increment:d;padding:.35rem 0 .35rem 2.4rem;position:relative;font-size:1.05rem}
.dirt li::before{content:counter(d);position:absolute;left:0;top:.3rem;width:1.7rem;height:1.7rem;border-radius:50%;
 background:radial-gradient(circle at 35% 35%,#fff,var(--hot) 35%,#6a3a00);color:#000;font-weight:800;font-size:.85rem;
 display:flex;align-items:center;justify-content:center;font-family:var(--display)}
.th{font-family:"Thonburi","Sukhumvit Set",sans-serif}
"""


def u(path=""):
    return BASE + path


def sib(id_, text):
    """A link to a sibling 'splainer, from inside the prose."""
    return f'<a href="{E(URL[id_])}">{text}</a>'


def head(title, desc, path):
    canon = SITE_URL + "/" + path
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title>
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{E(canon)}">
<meta property="og:type" content="website"><meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{E(canon)}">
<meta property="og:image" content="{SITE_URL}/card.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Round mirrors reflecting each other, over and over, under the title Indra's Net, Drawn">
<meta property="og:site_name" content="{E(NAME)}"><meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}">
<meta name="twitter:image" content="{SITE_URL}/card.jpg">
<meta name="theme-color" content="#07070b">
<link rel="icon" href="{u('icon.svg')}" type="image/svg+xml">
<style>{CSS}{EXTRA}</style></head><body>
<a class="sr" href="#main">Skip to the content</a>
<header class="top"><div class="in">
<a class="brand" href="{u()}"><i></i>Indra's Net, <b>Drawn</b></a>
<nav aria-label="Chapters">{"".join(f'<a href="{u(h)}"{" aria-current=page" if path.rstrip("/")+"/"==h else ""}>{E(t)}</a>' for h,t in NAV)}</nav>
</div></header><main id="main">"""


def foot(js=False):
    row = fleet.row_html(SELF, label="More 'splainers", roster=FLEET, ids=SIB)
    more = fleet.row_html(SELF, label="Also from NaNoBotCo", roster=FLEET)
    support = fleet.support_html(roster=FLEET, self_id=SELF)
    maker = fleet.maker_html(roster=FLEET)
    script = f'<script defer src="{u("net.js")}"></script>' if js else ""
    return f"""</main><footer class="bot"><div class="in">
<p><b>{E(NAME)}</b> — {E(TAG)}</p>
<p class="small">Text and pictures CC BY 4.0. The code that draws them is MIT. Every picture is
computed by <a href="{u('code/')}">the code on this site</a>, most of 'em live in your browser.
Built {E(TODAY)}.</p>
{row}
{more}
{support}
{maker}
</div></footer>{script}</body></html>"""


def cite(*ids):
    return S.cite(*ids, root=BASE)


def eq(body, reading=""):
    r = f'<p class="reading"><b>Readin\' it:</b> {reading}</p>' if reading else ""
    return f'<div class="eq">{body}</div>{r}'


def fig(key, caption, label=""):
    cap = f"<b>{label}.</b> {caption}" if label else caption
    return (f'<figure class="fig dark">{FIGS[key]}'
            f'<figcaption>{cap} <span class="small">· computed here · {CREDIT}</span></figcaption></figure>')


def slab(cells):
    out = []
    for v, l in cells:
        out.append(f"<div><b>{E(str(v))}</b><span>{E(l)}</span></div>")
    return '<div class="slab">' + "".join(out) + "</div>"


def toc(items):
    return '<div class="toc">' + "".join(f'<a href="{u(h)}">{E(t)}</a>' for h, t in items) + "</div>"


def nextlink(prev=None, nxt=None):
    a = f'<a href="{u(prev[0])}">← {E(prev[1])}</a>' if prev else "<span></span>"
    b = f'<a href="{u(nxt[0])}">{E(nxt[1])} →</a>' if nxt else "<span></span>"
    return f'<div class="next">{a}{b}</div>'


def rng(id_, lo, hi, step, val, label):
    return (f'<label for="{id_}">{label}<output id="{id_}-out"></output></label>'
            f'<input type="range" id="{id_}" min="{lo}" max="{hi}" step="{step}" value="{val}">')


def demo(stage, ctl="", row="", read_id=""):
    c = f'<div class="ctl">{ctl}</div>' if ctl else ""
    r = f'<div class="row">{row}</div>' if row else ""
    rd = f'<p class="read" id="{read_id}" aria-live="polite"></p>' if read_id else ""
    return f'<div class="gen"><div class="stage">{stage}</div>{c}{r}{rd}</div>'


def write(path, s):
    p = SITE / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")


def net_demo():
    return demo('<canvas id="net-canvas" width="900" height="560" aria-label="A net with a jewel at every knot; each jewel shows the whole net, which shows every jewel, and on down"></canvas>',
                rng("net-size", "10", "40", "1", "22", "how big the jewels are (px)"),
                row='<button id="net-pluck" type="button">Pluck one</button>'
                    '<span class="mute small">or tap any jewel and watch the tremble spread</span>',
                read_id="net-read")


# ============================================================================ pages
def page_home():
    sw = FACTS["small_world"]
    body = f"""
<h1><span class="kind">A 'splainer, drawn from the math</span>Every jewel<br>shows every jewel</h1>
<p class="lede">Way up yonder, over the palace of the old sky-god Indra, somebody strung a net. It
runs on out in every direction and don't quit. At every knot there hangs a jewel, polished so fine
you can see the whole rest of the net in it. And every one of <em>those</em> jewels you see is
showin' the whole net too. All the way down. That's the picture. Folks have been chewin' on it for
better'n thirteen hundred years, and it'll chew back.</p>

{net_demo()}

<div class="win">
<h3>The whole thing, dirt simple</h3>
<ol class="dirt">
<li>There's a net, and it goes on forever.</li>
<li>Every knot has a jewel. Every jewel shines back every other jewel.</li>
<li>So every jewel has the whole net inside it — and the net has every jewel.</li>
<li>Tug one knot and the whole thing trembles. Nothin' in it stands off by itself.</li>
<li>That's all. The rest is folks arguin' over what it <em>means</em> — and the math of mirrors that draws it.</li>
</ol>
</div>

{slab([(f"{FACTS['net_depth']}", "reflections deep you can see in the net up top"),
       (f"{FACTS['pearls_k4'][10]:,}", "pearls four round mirrors make on bounce ten"),
       (f"{FACTS['room']['10']}", "lamps in Fazang's mirror room within ten bounces"),
       (f"{sw['0.0']['hops']} → {sw['0.01']['hops']}", "average hops across 1,000 knots when 1 in 100 links goes long")])}

<h2>Walk it in order</h2>
{toc([("story/","1 · Where the picture comes from"),("readings/","2 · Many ways to read it"),
      ("pearls/","3 · The math: mirrors in mirrors"),("touch/","4 · Touch one, touch all"),
      ("code/","5 · Do it yourself"),("words/","Words"),("sources/","Sources")])}

<h2>Why it keeps comin' back</h2>
<p>The net is one of them pictures that fits whatever you hold it up to. A Buddhist teacher sees
how nothin' stands on its own. A Hindu storyteller sees a god's magic trick. A mathematician sees
round mirrors bouncin' circles off each other till they make lace. A fella who studies the internet
sees how your cousin's buddy's boss knows the President. Chaos folks see
{sib("chaos", "one little nudge that spreads to everything")}. They are all lookin' at the same
net. None of 'em is wrong about their jewel. <a href="{u('readings/')}">Here's sixteen of 'em, kept short.</a></p>

<div class="pair">
{fig("pearls4", "Four round mirrors, and every mirror seen in every other, nine bounces deep. Each color is one more bounce. This is the math folks named after the net.")}
{fig("room", "A square room with mirror walls and one lamp, unfolded. The gold square is the room. Every other lamp is that same lamp, seen in the mirrors — dimmer the more bounces it took.")}
</div>
{nextlink(None, ("story/", "Where the picture comes from"))}
"""
    write("index.html", head(NAME + " — every jewel shows every jewel",
                             "Indra's Net in plain words: the old picture of a net with a jewel at every knot, read many ways, and drawn live from the math of mirrors.", "") + body + foot(js=True))


def page_story():
    room = FACTS["room"]
    body = f"""
<h1><span class="kind">Chapter 1</span>Where the picture comes from</h1>
<p class="lede">The net's got two granddaddies — one a war charm, one a sermon — and a monk who
built it out of mirrors to show an empress what he meant.</p>

<h2>First, it was a weapon</h2>
<p>The oldest net of Indra shows up in the <strong>Atharva Veda</strong>, a book of Sanskrit charms
and spells from India near three thousand years back. Book eight has a charm for whippin' an enemy
army: throw Indra's net over 'em and tangle 'em up. Then it goes big and says this whole great world
is the net of great Indra{cite("av88")}. So from the start the net was two things at once — a trap
you throw, and the whole world you're standin' in.</p>
<p>The word stuck around. In later Sanskrit, <em>indrajāla</em> — Indra's net — came to mean a
conjurin' trick, magic, an illusion{cite("mw")}. Street magicians were doin' indrajāla. Hold on to
that; it comes back on the <a href="{u('readings/')}#maya">readings page</a>.</p>

<h2>Then it was a sermon</h2>
<p>A long Buddhist scripture called the <strong>Flower Garland Sūtra</strong> (the <em>Avataṃsaka</em>)
fills heaven with jewels and lights that shine into each other{cite("avatamsaka")}. In China, a
school of Buddhism grew up around that book called <strong>Huayan</strong> (say it
“hwah-yen”; Kegon in Japan, Hwaeom in Korea). One of its founders, a monk named <strong>Dushun</strong>,
around the year 600, took Indra's net and made it a teachin' picture: every jewel reflects every
other jewel, and every reflection holds all the others too, without end{cite("dushun", "cook1977")}.</p>
<p>His point was not about jewelry. It was that <em>every</em> thing is like that — it holds all the
rest inside it, and it is held inside all the rest.</p>

<h2>Then a monk built it</h2>
<p>A generation later, a Huayan teacher named <strong>Fazang</strong> had to explain all this to
Empress Wu Zetian, who was busy and wanted to see it, not hear it. So the story goes, he set up
mirrors on all eight sides of a room, plus one overhead and one underfoot, put a Buddha statue in the
middle, and lit a lamp. Step in, and there's the statue in every mirror, and in every mirror inside
every mirror, on out past countin'{cite("fazang", "chang1971")}.</p>
<p>You can draw his room with plain arithmetic. Squash it flat to a square with four mirror walls,
then do the trick every pool shark knows: instead of followin' the light as it bounces, <em>unfold</em>
the room. Flip it over each wall like a page. Then flip them copies. The bouncin' path turns into a
straight line out through a grid of rooms, and every lamp you see in the mirrors sits in one of
those rooms.</p>

{demo('<canvas id="room-canvas" width="900" height="620" aria-label="Fazang’s mirror room unfolded into a grid of rooms"></canvas>',
      rng("room-n", "1", "8", "1", "4", "how many bounces to show"),
      row='<button id="room-auto" type="button">Sweep around</button><span class="mute small">or tap any lamp to trace its path</span>',
      read_id="room-read")}

{eq('<var>lamps</var> <span class="op">=</span> 2<var>N</var>² <span class="op">+</span> 2<var>N</var> <span class="op">+</span> 1',
    f"count the lamps you can see that took <var>N</var> bounces or fewer. One bounce gives you {room['1']}: the lamp and its four reflections. Four bounces, {room['4']}. Ten, {room['10']}. A hundred, {room['100']:,}. Fazang had ten mirrors, not four, and in three directions, not two — the count climbs a whole lot faster, and it don't stop.")}

<div class="win"><h3>Why the lamps get dimmer</h3>
<p>No mirror sends back all the light it gets. A good household mirror keeps somethin' like nine
parts in ten, so a lamp ten bounces deep is down to about a third. The picture above dims each
bounce to 82%. The Huayan jewels are perfect mirrors, so in the story they don't dim — every
reflection is as bright as the thing itself. That's one place the story's net and a room you can
build part company.</p></div>

<p>And here's a thing Fazang didn't have to worry about: light takes time. Each bounce is a few
billionths of a second late, so every lamp in the mirrors is a lamp from a hair in the past. How
fast light goes, and why it won't go faster, is its own 'splainer: {sib("goin-fast", "Goin' Fast")}.</p>

{nextlink(("", "Home"), ("readings/", "Many ways to read it"))}
"""
    write("story/index.html", head("Where the picture comes from — " + NAME,
                                   "The Atharva Veda's war-net, the Flower Garland Sūtra, Dushun's jewel net, and Fazang's room of mirrors for Empress Wu — drawn live, with the arithmetic of the mirrors.", "story/") + body + foot(js=True))


READINGS = [
    # (anchor, title, who, color, body, where it stops)
    ("maya", "A god's magic trick", "Hindu reading", "#ff6a5e",
     lambda: f"""<p>In Sanskrit, Indra's net — <em>indrajāla</em> — got to be the word for a conjurin' trick{cite("mw")}.
     Read that way, the net is <em>māyā</em>: the world as a grand show put on by a god, dazzlin' and
     tangled, and easy to take for the whole story. The Atharva Veda calls the whole world Indra's
     net{cite("av88")}.</p>""",
     "The Veda's net traps an enemy; there's no jewel in it reflectin' anything. The mirrors come later."),
    ("huayan", "Everything holds everything", "Huayan Buddhism", "#ffc861",
     lambda: f"""<p>This is the one the picture was built for. Every thing contains all the others and is
     contained in all of them, the way each jewel holds the whole net. The Huayan word is
     <em>interpenetration</em>: the one in the many, the many in the one{cite("dushun", "cook1977")}.</p>""",
     "Huayan means it about <em>every</em> thing, not only the pretty ones. A mud puddle is a jewel too."),
    ("origin", "Nothin' stands by itself", "Early Buddhism", "#7fe0a8",
     lambda: f"""<p>Long before the net, the Buddha had a four-line rule: when this is, that is; when this
     comes up, that comes up; when this ain't, that ain't; when this quits, that quits{cite("sn1221")}.
     That's <em>dependent origination</em> — Pāli <em>paṭicca-samuppāda</em>, Thai
     <span class="th">ปฏิจจสมุปบาท</span> (<em>patitcha-samupbat</em>). The net is that rule, drawn.</p>""",
     "The old rule is mostly about how sufferin' gets started and stopped, one link at a time — a chain more than a net."),
    ("empty", "No jewel has its own light", "Madhyamaka", "#8fd0ff",
     lambda: f"""<p>Look close at one jewel. Everything you see in it came from somewhere else. Take away the
     other jewels and what's left to see? The philosopher Nāgārjuna said anything that comes up
     dependent on other things is what's meant by <em>empty</em>{cite("mmk2418")} — not nothin', but
     not standin' on its own either.</p>""",
     "The jewel's still there, hangin' on its knot. Empty ain't the same as gone."),
    ("interbeing", "There's a cloud in this paper", "Thích Nhất Hạnh", "#c8a6ff",
     lambda: f"""<p>The Vietnamese Zen teacher Thích Nhất Hạnh held up a sheet of paper and said if you look
     good, there's a cloud in it — no cloud, no rain; no rain, no tree; no tree, no paper. And the
     logger, and his breakfast. His word for it was <em>interbeing</em>{cite("tnh1988")}.</p>""",
     "He's talkin' about causes, one after another, back through time. The jewels shine all at once."),
    ("phrain", "Phra In and the city pillar", "Thai and Lanna", "#ffc861",
     lambda: f"""<p>In Thailand, Indra is <span class="th">พระอินทร์</span> (<em>Phra In</em>), known in the
     Pāli books as Sakka{cite("dn21")}, king of the heaven on top of Mount Meru in the Thai cosmology
     called the <em>Traiphum</em>{cite("traiphum")}. Chiang Mai's city pillar,
     <span class="th">เสาอินทขิล</span> (<em>Sao Inthakhin</em>), is told as sent down by him, and the
     city honors it every year{cite("inthakhin")}. More on the Lanna side at
     {sib("wichaa", "wichaa")}.</p>""",
     "In Thai tellin's Phra In is a helper god who shows up when good folks need him. The jewel net is mostly a Chinese Buddhist picture; it isn't a Thai temple story."),
    ("monads", "A living mirror of the universe", "Leibniz, 1714", "#8fd0ff",
     lambda: f"""<p>A German fella who'd never heard of Huayan came up with near the same picture. Gottfried
     Leibniz said the world is made of tiny simple things he called <em>monads</em>, and each one is
     “a perpetual living mirror of the universe”{cite("leibniz1714")}.</p>""",
     "His monads have “no windows” — nothin' goes in or out. The jewels are all window."),
    ("fox", "That of God in every one", "Quakers, 1656", "#7fe0a8",
     lambda: f"""<p>George Fox, who got the Quakers goin', wrote from a jail cell tellin' Friends to
     “walk cheerfully over the world, answering that of God in every one”{cite("fox1656")}. A light
     in every person, and you answer it by the light in yours. Jewel to jewel.</p>""",
     "Fox was talkin' about how to treat people, not how the world is built."),
    ("muir", "Hitched to everything else", "John Muir, 1911", "#7fe0a8",
     lambda: f"""<p>Up in the Sierra, John Muir wrote: “When we try to pick out anything by itself, we find
     it hitched to everything else in the Universe”{cite("muir1911")}. That's ecology in a sentence:
     pull the wolves and the elk eat the willows, and the creek bank caves in.</p>""",
     "A food web has a whole lot of knots with no string between 'em. The net ties every knot to every knot."),
    ("hologram", "Cut the picture, keep the whole", "Holograms", "#c8a6ff",
     lambda: f"""<p>Break a photo in half and you get half a photo. Break a hologram plate in half and each
     piece still shows the whole scene, a little fuzzier{cite("gabor1948")}. The physicist David Bohm
     built a whole picture of the universe out of that: the whole folded up in every part{cite("bohm1980")}.</p>""",
     "The smaller the piece, the blurrier the whole. The jewels don't lose a thing."),
    ("pull", "Everything pulls on everything", "Gravity", "#ffb347",
     lambda: f"""<p>Newton's gravity is a net: every lump of stuff tugs on every other lump, all the way
     across the universe{cite("newton1687")}. With two it's tidy. With three it goes wild — that's
     {sib("three-body", "the three-body problem")}, and it's why nobody can write down where three stars will be.</p>""",
     "The tug gets weaker with the square of the distance. The far jewels in the net shine as bright as the near ones."),
    ("entangle", "Two coins that always match", "Quantum", "#8fd0ff",
     lambda: f"""<p>Two particles can be <em>entangled</em>: measure one here and the other one, clear over
     yonder, matches it in a way no hidden plan could fix ahead of time{cite("bell1964")}. That's the
     trick {sib("quantum-computing", "quantum computers")} run on.</p>""",
     f"You can't send a message that way{cite('nosignal')}. The match only shows up when you compare notes, by regular mail."),
    ("rings", "A ring that shows the whole sky", "Black holes", "#ff6a5e",
     lambda: f"""<p>Light that skims a black hole gets bent clean around it. You see the sky once, then again in
     a thinner ring, then again thinner, on down — each ring a whole new picture of everything
     around{cite("johnson2020")}. A black hole is a jewel in the net, near enough. Drawn out at
     {sib("black-holes", "Black Holes, Drawn")}.</p>""",
     "Each ring's about 23 times thinner than the last, so you'd need a mighty good telescope past the second one."),
    ("chaos", "One nudge, and everything", "Chaos", "#ffb347",
     lambda: f"""<p>Pluck one knot and the whole net shivers. Put a ball bouncin' between round mirrors and a
     hair's difference in where it starts sends it somewhere else entirely, fast{cite("sinai1970")}.
     That's {sib("chaos", "chaos")}, and round mirrors are about the best chaos-maker there is.</p>""",
     "Chaos is about not bein' able to forecast. The net, in the story, is about everything showin' plain."),
    ("small", "Six handshakes", "Networks", "#ffc861",
     lambda: f"""<p>In the 1960s a fella named Milgram had folks pass a letter hand to hand across the country;
     the ones that made it took about six hops{cite("milgram1967")}. A few long links make the whole
     world small{cite("watts1998")}. <a href="{u('touch/')}">Try it yourself.</a></p>""",
     "Most letters never made it at all. Folks forget that part."),
    ("pearls", "Indra's Pearls", "Mathematics", "#c8a6ff",
     lambda: f"""<p>Put some round mirrors in a ring and look at each one in all the others. You get circles in
     circles in circles, crowdin' up into lace. Three mathematicians wrote a whole book on it and named it
     for the net: <em>Indra's Pearls</em>{cite("mumford2002")}. That's the next chapter. It's in the same
     family as the {sib("exceptional-magic", "odd, pretty math that turns up where nobody expected")}.</p>""",
     "It's the one readin' here you can draw exactly. Every picture on this site is that math."),
]


def page_readings():
    cards = "".join(
        f'<article class="rd" id="{a}" style="--jw:{c}"><h3>{E(t)}</h3><p class="who">{E(w)}</p>{b()}'
        f'<p class="stop"><b>Where the rhyme quits:</b> {s}</p></article>'
        for a, t, w, c, b, s in READINGS)
    body = f"""
<h1><span class="kind">Chapter 2</span>Many ways to read it</h1>
<p class="lede">Hold the net up to anything and it fits. Here's {len(READINGS)} ways folks have read it, or
somethin' that rhymes with it — each kept short, and each with the spot where the rhyme quits.
Nobody's pickin' a winner.</p>
<div class="readings">{cards}</div>
<div class="win"><h3>Why so many fit</h3>
<p>The net only says one thing: <em>nothin' here stands by itself</em>. That's true enough of
enough things that every field that notices it grabs the picture. The readings don't all agree —
Leibniz's mirrors have no windows, Huayan's are nothin' but window — and that's fine. It's a net.
There's room.</p></div>
{nextlink(("story/", "Where it comes from"), ("pearls/", "The math: mirrors in mirrors"))}
"""
    write("readings/index.html", head("Many ways to read it — " + NAME,
                                      "Indra's Net read many ways, kept simple: Hindu māyā, Huayan, dependent origination, emptiness, interbeing, Thai Phra In, Leibniz, the Quakers, Muir, holograms, gravity, entanglement, black holes, chaos, small worlds, Indra's Pearls.", "readings/") + body + foot())


def page_pearls():
    ex = FACTS["inv_example"]
    pk = FACTS["pearls_k4"]
    body = f"""
<h1><span class="kind">Chapter 3</span>The math: mirrors in mirrors</h1>
<p class="lede">You can't build a net of jewels that goes on forever. But you can put a handful of
round mirrors on a table and do the arithmetic of what shows up in 'em. That arithmetic draws the
prettiest pictures on this site, and mathematicians named it for the net{cite("mumford2002")}.</p>

{demo('<canvas id="pearl-canvas" width="760" height="760" aria-label="Round mirrors reflecting each other, circles nested in circles"></canvas>',
      rng("pearl-k", "3", "6", "1", "4", "how many mirrors") +
      rng("pearl-size", "0.5", "1", "0.01", "0.96", "how big (1 = touchin')") +
      rng("pearl-depth", "1", "12", "1", "9", "how many bounces"),
      row='<button id="pearl-breathe" type="button" aria-pressed="false">Let it breathe</button>'
          '<span class="mute small">push the size to 1 and the gaps close into lace</span>',
      read_id="pearl-read")}

<h2>A flat mirror, then a round one</h2>
<p>Stand in front of a flat mirror and your reflection is as far behind the glass as you are in front
of it. Easy. A <strong>round mirror</strong> — here, a circle you reflect <em>through</em>, the way
mathematicians do it — flips near and far instead. Somethin' right up against the rim stays put.
Somethin' far outside lands close to the middle. Somethin' way off yonder lands right in the
center{cite("steiner")}.</p>

{eq('<var>d</var><sub>new</sub> <span class="op">=</span> <var>R</var>² <span class="op">÷</span> <var>d</var>',
    "take a point <var>d</var> away from the center of a round mirror of radius <var>R</var>. Its reflection sits on the same line out from the center, but at <var>R</var>² ÷ <var>d</var>. Twice as far out as the rim? Reflection's halfway in. Ten times out? A tenth of the way in.")}

<p>Do that to every point on a circle and — here's the sweet part — you get another circle, only
smaller. So circles in round mirrors stay circles. For a circle of radius <var>r</var> whose center
sits <var>d</var> from the mirror's center:</p>

{eq('<var>s</var> <span class="op">=</span> <var>R</var>² <span class="op">÷</span> (<var>d</var>² <span class="op">−</span> <var>r</var>²)'
    ' &nbsp;&nbsp; <var>d</var><sub>new</sub> <span class="op">=</span> <var>s</var>·<var>d</var>'
    ' &nbsp;&nbsp; <var>r</var><sub>new</sub> <span class="op">=</span> <var>s</var>·<var>r</var>',
    f"work out one squeeze factor <var>s</var>, then shrink both the distance and the radius by it. A circle of radius 0.5 centered 2 out, in a mirror of radius 1: <var>s</var> = 1 ÷ (4 − 0.25) = 0.267, so the reflection sits {ex[0]} out with radius {ex[2]}. That's the whole engine. Everything below is that, over and over.")}

<h2>Now put four of 'em in a ring</h2>
<p>Look at mirror one in mirror two, and you see a little circle. Look at <em>that</em> in mirror
three, a littler one. Keep goin'. The one rule is: don't bounce straight back into the mirror you
just came out of, 'cause that undoes the bounce and you're back where you started.</p>

{eq('<var>circles on bounce n</var> <span class="op">=</span> <var>k</var> <span class="op">×</span> (<var>k</var> <span class="op">−</span> 1)<sup><var>n</var></sup>',
    f"with <var>k</var> mirrors, each circle has <var>k</var> − 1 fresh mirrors to show up in. Four mirrors: {pk[0]}, then {pk[1]}, then {pk[2]}, {pk[3]}, {pk[4]} — by bounce ten, {pk[10]:,}. They pile up that fast and they don't overlap, so they have to get smaller and crowd in toward the edges. That crowdin' is the lace.")}

<div class="pair">
{fig("pearls3", "Three mirrors just touchin'. The gaps fill with smaller and smaller circles that also touch — near kin to the Apollonian gasket.")}
{fig("pearls6", "Six mirrors with a little air between 'em. Each bounce is a color; the dust of circles crowds up against a ring it never quite reaches.")}
</div>
<p class="mute small">These still pictures draw every circle bigger than a speck: {FACTS['pearls3_drawn']:,} and {FACTS['pearls6_drawn']:,} of 'em. The live one up top does the same arithmetic in your browser{cite("descartes")}.</p>

<div class="win"><h3>What the jewels are, in this math</h3>
<p>Each round mirror is a jewel. Each little circle is one jewel seen in another, seen in another.
The dust they pile up against — mathematicians call it the <strong>limit set</strong> — is the part
of the net you'd only reach after bouncin' forever. Felix Klein and his students drew the first of
these by hand in the 1890s{cite("klein1897")}; it took computers to see how fine they go.</p></div>

<p>Here's a thing to try: set the size to 1 so the mirrors touch, and watch the gaps fill in with
circles that also touch. Then back it off to 0.8 and the lace comes apart into dust. Same rule, a
hair's difference in the setup, a different world — which is the whole of {sib("chaos", "chaos")}
in one slider.</p>

{nextlink(("readings/", "Many ways to read it"), ("touch/", "Touch one, touch all"))}
"""
    write("pearls/index.html", head("Mirrors in mirrors — " + NAME,
                                    "Circle inversion, the math of round mirrors, drawn live: four mirrors in a ring make 4 × 3ⁿ circles on bounce n, crowding into the lace mathematicians call Indra's Pearls.", "pearls/") + body + foot(js=True))


def page_touch():
    sw = FACTS["small_world"]
    body = f"""
<h1><span class="kind">Chapter 4</span>Touch one, touch all</h1>
<p class="lede">In the net, every knot is tied to every other one. The world we live in ain't quite
that tight — you don't know everybody. But you know somebody who knows somebody, and it turns out
that's near as good.</p>

{demo('<canvas id="touch-canvas" width="900" height="620" aria-label="A ring of knots, each tied to its neighbours, with a few long ties across; the news spreads out hop by hop"></canvas>',
      rng("touch-p", "0", "40", "1", "5", "how many ties go long (%)"),
      row='<button id="touch-go" type="button">Touch one at random</button><span class="mute small">or tap any knot</span>',
      read_id="touch-read")}

<h2>A ring of neighbors</h2>
<p>Start with folks in a big circle, each one holdin' hands with the two on either side, and the two
past that. Tell one person some news. It goes one hop at a time around the ring, both directions.
With 1,000 people each holdin' ten hands, the average person is <strong>{sw['0.0']['hops']}</strong>
hops from any other. Slow goin'.</p>

<h2>Move a few hands</h2>
<p>Now take one handhold in a hundred and hook it to a stranger clear across the ring. That's all.
The average drops to <strong>{sw['0.01']['hops']}</strong> hops. One in ten, and it's
<strong>{sw['0.1']['hops']}</strong>. Your neighbors are still mostly your neighbors — the share of
your friends who know each other barely moves, from {sw['0.0']['clustering']} to
{sw['0.01']['clustering']} — but the world got small{cite("watts1998")}. Duncan Watts and Steven
Strogatz worked that out in 1998. Stanley Milgram had seen it with letters thirty years
before{cite("milgram1967")}.</p>

<dl class="dial">
<dt>0% long</dt><dd>{sw['0.0']['hops']} hops on average · friends-know-each-other {sw['0.0']['clustering']}</dd>
<dt>0.1% long</dt><dd>{sw['0.001']['hops']} hops · {sw['0.001']['clustering']}</dd>
<dt>1% long</dt><dd>{sw['0.01']['hops']} hops · {sw['0.01']['clustering']}</dd>
<dt>10% long</dt><dd>{sw['0.1']['hops']} hops · {sw['0.1']['clustering']}</dd>
<dt>All random</dt><dd>{sw['1.0']['hops']} hops · {sw['1.0']['clustering']}</dd>
</dl>
<p class="mute small">1,000 knots, ten hands each, computed on this site's own machine with a fixed seed.</p>

<div class="win"><h3>What this has to do with jewels</h3>
<p>Indra's net is the far end of that table: every knot tied straight to every other, zero hops. Our
world sits in the middle — mostly neighbors, a few long ties — and that's enough that a nudge in one
corner gets everywhere in a handful of steps. Gossip does it. So does a cold. So does a kindness.
Plucked one jewel, and the whole net trembled: that's the demo on the <a href="{u('')}">front
page</a>, and it's this.</p></div>

{nextlink(("pearls/", "Mirrors in mirrors"), ("code/", "Do it yourself"))}
"""
    write("touch/index.html", head("Touch one, touch all — " + NAME,
                                   "Small worlds, drawn live: a ring of neighbours where moving 1 in 100 ties to a stranger drops the average distance across 1,000 people from 50 hops to under 9.", "touch/") + body + foot(js=True))


def page_code():
    code = (ROOT / "indras_net.py").read_text(encoding="utf-8")
    body = f"""
<h1><span class="kind">Chapter 5</span>Do it yourself</h1>
<p class="lede">The mirrors, the room and the small world, in one file of plain Python with nothin'
to install. Copy it, run it, change the numbers, break it.</p>
<p><a class="btn solid" href="{u('indras_net.py')}" download>Download indras_net.py</a> &nbsp;
<a class="btn" href="https://github.com/NaNoBotCo/indras-net">The full source on GitHub</a></p>
<pre><code>{E(code)}</code></pre>
<h2>What it prints</h2>
<p>Run <code>python3 indras_net.py</code> and you get one circle seen in a round mirror; the count of
circles four mirrors make on each bounce, checked against 4 × 3<sup>n</sup>; the lamps in Fazang's
room within 1, 2, 4 and 10 bounces, checked against 2N² + 2N + 1; and how far the farthest person
is in a ring of 1,000 once you move a few handholds.</p>
<div class="win"><h3>Things worth breakin'</h3>
<p>Let the mirrors overlap — <code>ring(4, 1.3)</code> — and watch the circle count stay the same
while the picture goes to mush. Put five mirrors in the ring and the count goes as 5 × 4<sup>n</sup>.
Set the rewire chance to 1 and see what a world with no neighbors looks like. The moving pictures
live in <a href="{u('net.js')}">net.js</a>, same math, in the language your browser speaks.</p></div>
{nextlink(("touch/", "Touch one, touch all"), ("words/", "Words"))}
"""
    write("code/index.html", head("Do it yourself — " + NAME, "The math under Indra's Net, Drawn in one dependency-free Python file: circle inversion, Fazang's mirror room, and the small world.", "code/") + body + foot())
    write("indras_net.py", code)


WORDS = [
    ("Indra", "The old Vedic king of the gods, wielder of thunder. Sakka in Pāli; Phra In (พระอินทร์) in Thai."),
    ("Indra's net", "A net over Indra's palace, going on forever, with a jewel at every knot; each jewel reflects every other, and every reflection holds all the rest."),
    ("Indrajāla", "Sanskrit, “Indra's net” — and, later, a conjuring trick or illusion."),
    ("Māyā", "The world as a dazzling show, easy to take for the whole of what is."),
    ("Huayan", "A school of Chinese Buddhism (Kegon in Japan, Hwaeom in Korea) built on the Flower Garland Sūtra; the net is its teaching picture."),
    ("Interpenetration", "The Huayan idea that every thing contains all others and is contained in them, without getting in their way."),
    ("Dependent origination", "The Buddha's rule that things come up because of other things: when this is, that is. Pāli paṭicca-samuppāda; Thai ปฏิจจสมุปบาท (patitcha-samupbat)."),
    ("Emptiness", "In Madhyamaka Buddhism, the lack of any standing-on-its-own in a thing that arises from others. Not the same as nothing."),
    ("Interbeing", "Thích Nhất Hạnh's word for dependent origination: the cloud is in the paper."),
    ("Monad", "Leibniz's simplest unit of what exists; each one mirrors the whole universe from its own spot."),
    ("Circle inversion", "Reflection in a round mirror: a point at distance d from the center goes to R²/d along the same line. Circles go to circles."),
    ("Limit set", "The dust that reflections of reflections crowd toward, reached only after bouncing forever. The lace in the pearls pictures."),
    ("Apollonian gasket", "Circles packed into the gaps between touching circles, and into those gaps, forever."),
    ("Unfolding", "Following a light ray in a mirror room by flipping the room over each wall instead of bouncing the ray; the path turns into a straight line."),
    ("Small world", "A network where most ties are local but a few go long, so anyone is a handful of hops from anyone."),
    ("Clustering", "The share of your friends who are also friends with each other."),
    ("Entanglement", "A link between particles that makes their measurements match in ways no plan made ahead of time explains; it carries no message."),
    ("Hologram", "A recording of light where every piece of the plate holds the whole scene, blurrier the smaller the piece."),
]


def page_words():
    rows = "".join(f'<dt>{E(t)}</dt><dd>{E(d)}</dd>' for t, d in sorted(WORDS))
    body = f"""
<h1><span class="kind">Words</span>The words</h1>
<p class="lede">Every term on this site in one place, plain. {len(WORDS)} of 'em.</p>
<dl class="dial">{rows}</dl>
{nextlink(("code/", "Do it yourself"), ("sources/", "Sources"))}
"""
    write("words/index.html", head("Words — " + NAME, "A plain glossary of Indra's Net: Huayan, interpenetration, dependent origination, emptiness, interbeing, circle inversion, limit sets, small worlds.", "words/") + body + foot())


def page_sources():
    body = f"""
<h1><span class="kind">Sources</span>Sources</h1>
<p class="lede">{len(S.SOURCES)} of 'em — the old books, the teachers, and the papers behind the math.
The pictures are computed by <a href="{u('code/')}">the code</a>, not copied from any of these.</p>
{S.render_list(root=BASE)}
{nextlink(("words/", "Words"), ("", "Home"))}
"""
    write("sources/index.html", head("Sources — " + NAME, "The Atharva Veda, the Flower Garland Sūtra, Dushun, Fazang, Nāgārjuna, Thích Nhất Hạnh, Leibniz, Fox, Muir, Gabor, Watts & Strogatz, and Indra's Pearls.", "sources/") + body + foot())


ICON = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#07070b"/><path d="M8 20H56M8 44H56M20 8V56M44 8V56" stroke="#ffc861" stroke-opacity=".5" stroke-width="2"/><g fill="#07070b" stroke-width="3"><circle cx="20" cy="20" r="7" stroke="#ffc861"/><circle cx="44" cy="20" r="7" stroke="#8fd0ff"/><circle cx="20" cy="44" r="7" stroke="#c8a6ff"/><circle cx="44" cy="44" r="7" stroke="#ff6a5e"/></g></svg>'''


def page_404():
    body = f"""
<h1><span class="kind">404</span>No jewel at this knot</h1>
<p class="lede">This spot in the net's empty. Every other one's still shinin'.</p>
<p><a class="btn solid" href="{u()}">Back to the start</a></p>
"""
    write("404.html", head("Not found — " + NAME, "Page not found.", "404.html") + body + foot())


def machine_files():
    (SITE / ".nojekyll").write_text("", encoding="utf-8")
    (SITE / ".basepath").write_text(BASE + "\n", encoding="utf-8")
    (SITE / "icon.svg").write_text(ICON + "\n", encoding="utf-8")
    (SITE / "net.js").write_text((ROOT / "js" / "net.js").read_text(encoding="utf-8"), encoding="utf-8")
    (SITE / "manifest.webmanifest").write_text(json.dumps({
        "name": NAME, "short_name": "Indra's Net", "start_url": BASE, "display": "standalone",
        "background_color": "#07070b", "theme_color": "#07070b",
        "icons": [{"src": u("icon.svg"), "sizes": "any", "type": "image/svg+xml"}]}, indent=2) + "\n", encoding="utf-8")
    pages = ["", "story/", "readings/", "pearls/", "touch/", "code/", "words/", "sources/"]
    urls = "".join(f"<url><loc>{SITE_URL}/{p}</loc><lastmod>{TODAY}</lastmod></url>" for p in pages)
    (SITE / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n', encoding="utf-8")
    (SITE / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (SITE / "llms.txt").write_text(
        f"# {NAME}\n\n> {TAG}\n\n"
        f"Indra's Net: its sources (Atharva Veda 8.8, the Avatamsaka Sutra, Dushun, Fazang's room of mirrors), "
        f"{len(READINGS)} short readings (Hindu, Huayan, early Buddhist, Madhyamaka, Thich Nhat Hanh, Thai/Lanna, "
        f"Leibniz, Quaker, Muir, holography, gravity, entanglement, black holes, chaos, small worlds, Indra's Pearls), "
        f"and the mathematics of circle inversion, drawn live.\n\n## Pages\n"
        f"- [Where the picture comes from]({SITE_URL}/story/)\n- [Many ways to read it]({SITE_URL}/readings/)\n"
        f"- [Mirrors in mirrors]({SITE_URL}/pearls/): circle inversion, k(k-1)^n\n"
        f"- [Touch one, touch all]({SITE_URL}/touch/): small-world networks\n"
        f"- [Code]({SITE_URL}/code/) · [Words]({SITE_URL}/words/) · [Sources]({SITE_URL}/sources/)\n", encoding="utf-8")
    (SITE / "ai.txt").write_text(
        f"Publisher: {FLEET['publisher']} · {FLEET['contact']}\nSite: {NAME} — {SITE_URL}/\n"
        f"Licence: text and figures CC BY 4.0; code MIT.\n", encoding="utf-8")
    (SITE / "humans.txt").write_text(f"/* {NAME} */\n{TAG}\n\nBuilt {TODAY}.\nText & figures CC BY 4.0 · code MIT.\n", encoding="utf-8")
    return fleet.decorate(SITE, SELF, roster=FLEET)


def build_all():
    SITE.mkdir(parents=True, exist_ok=True)
    page_home(); page_story(); page_readings(); page_pearls(); page_touch()
    page_code(); page_words(); page_sources(); page_404()
    touched = machine_files()
    n = len(list(SITE.rglob("index.html")))
    print(f"built {n} pages into {SITE}  ·  base {BASE}  ·  machine files: {', '.join(touched)}")


if __name__ == "__main__":
    build_all()
