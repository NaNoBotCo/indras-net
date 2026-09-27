# -*- coding: utf-8 -*-
"""sources.py — every source the site cites, by id. A citation in the text is
cite("id"), which renders a numbered superscript link to /sources/#id."""

import html

SOURCES = [
    # ---- the old books
    ("av88", "Atharva Veda 8.8, a charm for beating an army with Indra's net; verse 8 calls this great world the net of great Indra. Ralph T. H. Griffith, trans., The Hymns of the Atharva-Veda (1895–96).", "https://www.sacred-texts.com/hin/av/av08008.htm"),
    ("mw", "Monier Monier-Williams, A Sanskrit-English Dictionary (Oxford, 1899), s.v. indra-jāla: “the net of Indra”; also a conjuring trick, sorcery, illusion.", "https://www.sanskrit-lexicon.uni-koeln.de/scans/MWScan/2020/web/webtc/indexcaller.php"),
    ("avatamsaka", "The Avataṃsaka (Flower Garland) Sūtra; Thomas Cleary, trans., The Flower Ornament Scripture (Shambhala, 1993) — the scripture the Huayan school grew from.", "https://en.wikipedia.org/wiki/Avatamsaka_Sutra"),
    ("dushun", "Dushun (557–640), Calming and Contemplation in the Five Teachings of Huayan, the text that sets out the jewel net in the form most retellings follow. Discussed in Cook 1977.", "https://en.wikipedia.org/wiki/Indra%27s_net"),
    ("cook1977", "Francis H. Cook, Hua-yen Buddhism: The Jewel Net of Indra (Pennsylvania State University Press, 1977) — the standard English account of the net and of the school built on it.", "https://en.wikipedia.org/wiki/Huayan"),
    ("chang1971", "Garma C. C. Chang, The Buddhist Teaching of Totality: The Philosophy of Hwa Yen Buddhism (Pennsylvania State University Press, 1971) — includes Fazang's room of mirrors, told for Empress Wu.", "https://en.wikipedia.org/wiki/Fazang"),
    ("fazang", "Fazang (643–712), Treatise on the Golden Lion; and the account in the Song Biographies of Eminent Monks of the mirror demonstration: mirrors on eight sides, above and below, a Buddha image and a lamp in the middle.", "https://en.wikipedia.org/wiki/Fazang"),
    # ---- Buddhist readings
    ("sn1221", "Saṃyutta Nikāya 12.21 (Dasabala Sutta): “When this is, that is; from the arising of this, that arises. When this is not, that is not; from the ceasing of this, that ceases.” Bhikkhu Sujato, trans.", "https://suttacentral.net/sn12.21/en/sujato"),
    ("mmk2418", "Nāgārjuna, Mūlamadhyamakakārikā 24.18 — whatever arises dependently is what is called emptiness. Jay L. Garfield, trans., The Fundamental Wisdom of the Middle Way (Oxford, 1995).", "https://en.wikipedia.org/wiki/M%C5%ABlamadhyamakak%C4%81rik%C4%81"),
    ("tnh1988", "Thích Nhất Hạnh, The Heart of Understanding: Commentaries on the Prajñaparamita Heart Sutra (Parallax Press, 1988) — the cloud in the sheet of paper, and the word “interbeing”.", "https://en.wikipedia.org/wiki/Interbeing"),
    ("dn21", "Dīgha Nikāya 21 (Sakkapañha Sutta) — Sakka, the Pāli name for Indra, lord of the Tāvatiṃsa heaven, puts his questions to the Buddha.", "https://suttacentral.net/dn21/en/sujato"),
    ("traiphum", "Frank E. Reynolds & Mani B. Reynolds, trans., Three Worlds According to King Ruang: A Thai Buddhist Cosmology (Berkeley, 1982) — the Traiphum, with Indra's city on the top of Mount Meru.", ""),
    ("inthakhin", "The Inthakhin city pillar of Chiang Mai, housed at Wat Chedi Luang, and the yearly Inthakhin festival; the founding legend has the pillar sent down by Indra.", "https://en.wikipedia.org/wiki/Wat_Chedi_Luang"),
    # ---- other folks' mirrors
    ("leibniz1714", "G. W. Leibniz, The Monadology (1714), §56: each simple substance is “a perpetual living mirror of the universe”. Robert Latta, trans. (Oxford, 1898).", "https://en.wikipedia.org/wiki/Monadology"),
    ("fox1656", "George Fox, letter from Launceston jail, 1656: “walk cheerfully over the world, answering that of God in every one.” The Journal of George Fox.", ""),
    ("muir1911", "John Muir, My First Summer in the Sierra (Boston, 1911), p. 110: “When we try to pick out anything by itself, we find it hitched to everything else in the Universe.”", "https://vault.sierraclub.org/john_muir_exhibit/writings/misquotes.aspx"),
    # ---- science rhymes
    ("gabor1948", "Dennis Gabor, “A New Microscopic Principle”, Nature 161 (1948) 777–778 — the invention of holography.", "https://doi.org/10.1038/161777a0"),
    ("bohm1980", "David Bohm, Wholeness and the Implicate Order (Routledge, 1980) — a physicist's picture of a whole folded into each part, with the hologram as his example.", "https://en.wikipedia.org/wiki/Implicate_and_explicate_order"),
    ("newton1687", "Isaac Newton, Philosophiæ Naturalis Principia Mathematica (1687), book III — every body in the universe pulls on every other.", "https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation"),
    ("bell1964", "John S. Bell, “On the Einstein Podolsky Rosen paradox”, Physics 1 (1964) 195–200 — the test that shows entangled particles keep a link no local story explains.", "https://doi.org/10.1103/PhysicsPhysiqueFizika.1.195"),
    ("nosignal", "The no-signalling theorem: entanglement cannot carry a message faster than light. G. C. Ghirardi, A. Rimini & T. Weber, Lettere al Nuovo Cimento 27 (1980) 293.", "https://en.wikipedia.org/wiki/No-communication_theorem"),
    ("johnson2020", "Michael D. Johnson et al., “Universal interferometric signatures of a black hole's photon ring”, Science Advances 6 (2020) eaaz1310 — the stack of ever-thinner rings, each a fresh image of the whole sky.", "https://doi.org/10.1126/sciadv.aaz1310"),
    ("sinai1970", "Yakov G. Sinai, “Dynamical systems with elastic reflections”, Russian Mathematical Surveys 25 (1970) 137 — a ball bouncing among round obstacles is chaotic.", "https://doi.org/10.1070/RM1970v025n02ABEH003794"),
    ("milgram1967", "Stanley Milgram, “The Small World Problem”, Psychology Today 1 (1967) 61–67 — letters passed hand to hand across the United States; the “six degrees”.", "https://en.wikipedia.org/wiki/Small-world_experiment"),
    ("watts1998", "Duncan J. Watts & Steven H. Strogatz, “Collective dynamics of ‘small-world’ networks”, Nature 393 (1998) 440–442 — a few long links shrink the whole world. The model the touch-one demo runs.", "https://doi.org/10.1038/30918"),
    # ---- the mathematics
    ("mumford2002", "David Mumford, Caroline Series & David Wright, Indra's Pearls: The Vision of Felix Klein (Cambridge University Press, 2002) — the mathematics of mirrors reflecting mirrors, named for the net.", "https://en.wikipedia.org/wiki/Indra%27s_Pearls_(book)"),
    ("klein1897", "Robert Fricke & Felix Klein, Vorlesungen über die Theorie der automorphen Functionen (Leipzig, 1897) — the first drawings of these nested circles, done by hand.", "https://en.wikipedia.org/wiki/Kleinian_group"),
    ("steiner", "Circle inversion, the reflection in a round mirror: the map that sends a point at distance d from the centre to distance R²/d along the same line. Worked out by Steiner, Plücker and others in the 1820s–30s.", "https://en.wikipedia.org/wiki/Inversive_geometry"),
    ("descartes", "The Apollonian gasket: circles packed into the gaps between touching circles, forever. Named for Apollonius of Perga (c. 200 BCE).", "https://en.wikipedia.org/wiki/Apollonian_gasket"),
]

BY_ID = {sid: (i + 1, text, url) for i, (sid, text, url) in enumerate(SOURCES)}


def cite(*ids, root="/"):
    out = []
    for sid in ids:
        n, _text, _url = BY_ID[sid]
        out.append(f'<a href="{root}sources/#{sid}">{n}</a>')
    return f'<sup class="src">{"".join(out)}</sup>'


def render_list(root="/"):
    rows = []
    for sid, text, url in SOURCES:
        n = BY_ID[sid][0]
        link = f' <a href="{html.escape(url)}" rel="noopener" target="_blank">↗</a>' if url else ""
        rows.append(f'<li id="{sid}" value="{n}">{html.escape(text)}{link}</li>')
    return '<ol class="srclist">' + "".join(rows) + "</ol>"
