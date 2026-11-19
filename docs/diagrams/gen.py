#!/usr/bin/env python3
"""Generate the SVG diagrams used in the documentation.

Run from anywhere: ``python3 docs/diagrams/gen.py``. Output goes to
``docs/_static/diagrams/``. The SVGs are committed so that Read the Docs does
not need to run this script.

Cross-sections use roughly 1 px = 1 µm horizontally. Layer thicknesses are
exaggerated by a large factor, otherwise 1 µm of aluminium would be invisible
next to a 250 µm ball.
"""

import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parent.parent / "_static" / "diagrams"

# Colours.
SI = "#8d99a6"
AL = "#c9d6e2"
PASS = "#7fb77e"
NI = "#6f7f8f"
AU = "#e0b020"
TI = "#4a4a6a"
CU = "#c8763a"
SOLDER = "#d9dde2"
POLY = "#e8c98a"
IMC = "#8b3fa0"
ICA = "#5a5a5a"
PCB = "#3f7f4f"
INK = "#1d2733"
WARN = "#b3261e"

FONT = 'font-family="DejaVu Sans, Arial, Helvetica, sans-serif"'


class Svg:
    def __init__(self, w, h, title, shift=0):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}" role="img" aria-label="{title}">',
            f"<title>{title}</title>",
            '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>',
            f'<g transform="translate({shift},0)">',
        ]

    def add(self, s):
        self.parts.append(s)

    def rect(self, x, y, w, h, fill, stroke=INK, sw=1, rx=0, extra=""):
        self.add(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
        )

    def poly(self, pts, fill, stroke=INK, sw=1):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(
            f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{sw}" stroke-linejoin="round"/>'
        )

    def circle(self, cx, cy, r, fill, stroke=INK, sw=1):
        self.add(
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw}"/>'
        )

    def line(self, x1, y1, x2, y2, stroke=INK, sw=1, extra=""):
        self.add(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" '
            f'stroke-width="{sw}" {extra}/>'
        )

    def text(self, x, y, s, size=13, anchor="start", fill=INK, weight="normal"):
        lines = s.split("\n")
        for i, ln in enumerate(lines):
            self.add(
                f'<text x="{x}" y="{y + i * (size + 3)}" font-size="{size}" '
                f'text-anchor="{anchor}" fill="{fill}" font-weight="{weight}" '
                f"{FONT}>{ln}</text>"
            )

    def label(self, tx, ty, s, px, py, anchor="start", fill=INK):
        """Text at (tx, ty) with a leader line to the point (px, py)."""
        lines = s.split("\n")
        mid = ty - 4 + (len(lines) - 1) * 8
        lx = tx - 4 if anchor == "start" else tx + 4
        self.line(lx, mid, px, py, stroke=fill, sw=0.8)
        self.circle(px, py, 2, fill, stroke=fill)
        self.text(tx, ty, s, anchor=anchor, fill=fill)

    def dim(self, x1, x2, y, s):
        self.line(x1, y, x2, y, extra='marker-start="url(#arr)" marker-end="url(#arr)"')
        self.text((x1 + x2) / 2, y - 5, s, size=12, anchor="middle")

    def save(self, name):
        OUT.mkdir(parents=True, exist_ok=True)
        (OUT / name).write_text("\n".join(self.parts + ["</g>", "</svg>"]) + "\n")
        print("wrote", name)


# --- Shared pad geometry ---------------------------------------------------
W, H = 760, 450
CX = 380
OPEN = 100  # half passivation opening: 200 µm
PADHALF = 116  # half top metal pad: 232 µm
Y_SUB, Y_PAD, Y_PASS = 320, 300, 280
NOTE = "Horizontal: about 1 px per µm. Layer thicknesses greatly exaggerated."


def ball(s, chord_y, half_width, r=135, fill=SOLDER):
    """Solder ball truncated on a wetted area of the given half width."""
    d = math.sqrt(r * r - half_width * half_width)
    cy = chord_y - d
    s.circle(CX, cy, r, fill)
    s.add(
        f'<ellipse cx="{CX - 45}" cy="{cy - 55}" rx="26" ry="16" fill="#ffffff" '
        'opacity="0.6"/>'
    )
    return cy


def base(s, pad_fill=AL):
    """Substrate, passivation and top metal pad. Draw after the ball."""
    s.rect(60, Y_SUB, 640, 70, SI)
    s.rect(60, Y_PASS, CX - OPEN - 60, Y_SUB - Y_PASS, PASS)
    s.rect(CX + OPEN, Y_PASS, 700 - CX - OPEN, Y_SUB - Y_PASS, PASS)
    s.rect(CX - PADHALF, Y_PAD, 2 * PADHALF, Y_SUB - Y_PAD, pad_fill)
    s.text(380, 362, "inter-metal dielectric, lower metals, silicon", anchor="middle", fill="#ffffff")
    s.text(380, 436, NOTE, size=11, anchor="middle", fill="#555555")


def conformal(o, t, overlap=20):
    """Polygon for a thin film of thickness t at offset o over the opening."""
    def prof(k):
        return [
            (CX - OPEN - overlap, Y_PASS - k),
            (CX - OPEN + k, Y_PASS - k),
            (CX - OPEN + k, Y_PAD - k),
            (CX + OPEN - k, Y_PAD - k),
            (CX + OPEN - k, Y_PASS - k),
            (CX + OPEN + overlap, Y_PASS - k),
        ]
    return prof(o) + prof(o + t)[::-1]


def fig_bare():
    s = Svg(W + 120, H, "Bare GF180MCU bump pad cross-section", shift=60)
    base(s)
    s.dim(CX - OPEN, CX + OPEN, 262, "opening A = 200 µm")
    s.dim(CX - PADHALF, CX + PADHALF, 232, "top metal pad, A + 32 = 232 µm")
    s.line(CX - PADHALF, 236, CX - PADHALF, Y_PAD, sw=0.6, extra='stroke-dasharray="3 3"')
    s.line(CX + PADHALF, 236, CX + PADHALF, Y_PAD, sw=0.6, extra='stroke-dasharray="3 3"')
    s.label(560, 180, "native Al oxide, a few nm:\nsolder will not wet this", CX + 40, Y_PAD, fill=WARN)
    s.label(225, 180, "Al top metal,\nabout 1.1 µm (11 kÅ)", CX - 108, Y_PAD + 10, anchor="end")
    s.label(225, 250, "passivation", 250, Y_PASS + 10, anchor="end")
    s.text(380, 40, "Starting point: a bump pad in top metal", size=16, anchor="middle", weight="bold")
    s.save("pad-bare.svg")


def fig_enig():
    s = Svg(W + 120, H, "Electroless nickel immersion gold UBM with solder ball", shift=60)
    ball(s, 270, 108)
    base(s)
    ni = [
        (CX - OPEN, Y_PAD), (CX + OPEN, Y_PAD), (CX + OPEN, Y_PASS),
        (CX + OPEN + 8, Y_PASS), (CX + OPEN + 8, 272), (CX + OPEN + 5, 270),
        (CX - OPEN - 5, 270), (CX - OPEN - 8, 272), (CX - OPEN - 8, Y_PASS),
        (CX - OPEN, Y_PASS),
    ]
    s.poly(ni, NI)
    s.line(CX - OPEN - 6, 270, CX + OPEN + 6, 270, stroke=AU, sw=3)
    s.line(CX - OPEN + 2, Y_PAD - 1, CX + OPEN - 2, Y_PAD - 1, stroke=IMC, sw=2)
    s.label(560, 130, "SAC solder ball,\n250 µm", CX + 100, 170)
    s.label(570, 185, "immersion Au, 0.05 to 0.1 µm\n(dissolves into the solder)", CX + 104, 269)
    s.label(570, 234, "electroless Ni-P, about 5 µm:\nbarrier and wettable layer", CX + 80, 286)
    s.label(225, 200, "Ni mushrooms about 5 µm\nover the passivation edge", CX - OPEN - 6, 275, anchor="end")
    s.label(225, 250, "zincate seed layer on Al\n(0.3 to 0.4 µm of Al consumed)", CX - 70, Y_PAD - 1, anchor="end", fill=IMC)
    s.text(380, 30, "ENIG under bump metal on the Al pad", size=16, anchor="middle", weight="bold")
    s.save("enig-cross-section.svg")


def fig_stud():
    s = Svg(W + 120, H, "Gold stud bump used as under bump metal", shift=60)
    r = 125
    s.circle(CX, 298 - r, r, SOLDER)
    base(s)
    # AuSn4 halo, stud, Au-Al intermetallic.
    s.rect(CX - 50, 258, 100, 42, "#b9a7c9", stroke="none", rx=14)
    s.rect(CX - 20, 236, 40, 30, "#b9a7c9", stroke="none", rx=10)
    s.rect(CX - 40, 268, 80, 32, AU, rx=10)
    s.rect(CX - 12, 246, 24, 24, AU, rx=6)
    s.line(CX - 36, Y_PAD, CX + 36, Y_PAD, stroke=IMC, sw=3)
    s.label(560, 120, "solder ball", CX + 90, 150)
    s.label(570, 200, "Au stud from a ball bonder,\n60 to 120 µm across", CX + 30, 282)
    s.label(570, 250, "AuSn4 forms around the stud:\nbrittle when gold is plentiful", CX + 46, 266, fill=IMC)
    s.label(225, 180, "Au-Al intermetallic grows\nabove about 200 °C", CX - 20, Y_PAD, anchor="end", fill=IMC)
    s.label(225, 240, "bare Al beside the stud:\nnot wetted, not sealed", CX - 75, Y_PAD, anchor="end", fill=WARN)
    s.text(380, 30, "Gold stud bump as the solderable surface", size=16, anchor="middle", weight="bold")
    s.save("stud-bump-cross-section.svg")


def fig_sputter(name, title, top_label, ball_fill=SOLDER, r=135, layers=None):
    s = Svg(W + 120, H, title, shift=60)
    ball(s, 270, 118, r=r, fill=ball_fill)
    base(s)
    s.rect(CX - OPEN + 10, 270, 2 * OPEN - 20, 20, ball_fill, stroke="none")
    for o, t, c in layers or [(0, 3, TI), (3, 5, NI), (8, 2, AU)]:
        s.poly(conformal(o, t), c, sw=0.5)
    s.label(560, 150, top_label, CX + 100, 195)
    s.label(570, 222, "Au cap, 0.1 to 0.2 µm", CX + 112, 271)
    s.label(570, 246, "Ni (or NiV, Cu) wettable layer", CX + 114, 275)
    s.label(570, 270, "Ti or TiW adhesion / barrier", CX + 116, 279)
    s.label(225, 200, "film overlaps the passivation,\nsealing the Al (10 µm or more)", CX - OPEN - 12, 275, anchor="end")
    s.label(225, 250, "oxide removed in vacuum\nbefore deposition", CX - 60, Y_PAD - 1, anchor="end")
    s.text(380, 30, title, size=16, anchor="middle", weight="bold")
    s.save(name)


def fig_direct():
    s = Svg(W + 120, H, "Solder wetted directly onto aluminium", shift=60)
    ball(s, Y_PAD, 96)
    base(s)
    s.line(CX - 96, Y_PAD, CX + 96, Y_PAD, stroke=WARN, sw=3)
    s.label(560, 150, "Sn-based solder, wetted with\nultrasonic or active alloy", CX + 100, 200)
    s.label(570, 230, "Sn directly on Al: no barrier,\nAl dissolves, galvanic couple", CX + 60, Y_PAD, fill=WARN)
    s.label(225, 200, "only about 1.1 µm of Al to\nsurvive cavitation and tin", CX - 108, Y_PAD + 10, anchor="end")
    s.label(225, 255, "pad edge not sealed", CX - 98, Y_PAD - 2, anchor="end", fill=WARN)
    s.text(380, 30, "Direct soldering to the Al pad (no under bump metal)", size=16, anchor="middle", weight="bold")
    s.save("direct-to-al-cross-section.svg")


def fig_adhesive():
    s = Svg(W + 120, H, "Silver epoxy dot joining a bare aluminium pad to a board pad", shift=60)
    s.text(380, 30, "Silver epoxy dot straight on the aluminium pad", size=16, anchor="middle", weight="bold")
    # Die, face down.
    s.rect(60, 60, 640, 70, SI)
    s.text(380, 100, "die (face down)", anchor="middle", fill="#ffffff")
    s.rect(60, 130, 220, 30, PASS)
    s.rect(480, 130, 220, 30, PASS)
    s.rect(264, 130, 232, 16, AL)
    # Epoxy dot squeezed between the pad and the board.
    s.poly([(284, 147), (476, 147), (476, 160), (492, 176), (500, 230), (486, 300),
            (274, 300), (260, 230), (268, 176), (284, 160)], ICA)
    s.line(286, 147, 474, 147, stroke=WARN, sw=3)
    # Board.
    s.rect(240, 300, 280, 16, AU)
    s.rect(60, 316, 640, 70, PCB)
    s.text(380, 356, "board or flex circuit", anchor="middle", fill="#ffffff")
    s.label(570, 180, "native oxide stays under the epoxy:\nhigh, drifting contact resistance", CX + 60, 147, fill=WARN)
    s.label(570, 240, "silver-filled epoxy dot,\nabout 200 µm across", CX + 90, 240)
    s.label(570, 296, "gold-finished copper pad", 505, 308)
    s.label(225, 190, "Al pad, untreated or\nscrubbed while the epoxy is wet", 272, 139, anchor="end")
    s.label(225, 262, "air gap: no underfill, so the\ndots carry all the load", 200, 240, anchor="end")
    s.text(380, 436, "Not to scale.", size=11, anchor="middle", fill="#555555")
    s.save("adhesive-cross-section.svg")


def fig_flex():
    s = Svg(W + 120, H, "Bare die on a flex circuit with Z-axis adhesive", shift=60)
    s.text(380, 30, "Flex circuit as a home-made package", size=16, anchor="middle", weight="bold")
    s.rect(140, 60, 480, 60, SI)
    s.text(380, 96, "die (face down)", anchor="middle", fill="#ffffff")
    s.rect(140, 120, 480, 14, PASS)
    for x0 in (220, 460):
        s.rect(x0, 120, 80, 10, AL)
        s.rect(x0 + 6, 130, 68, 4, "#fbf3d0", stroke="none")
    s.rect(140, 134, 480, 22, "#fbf3d0", stroke="none")
    import random
    rnd = random.Random(4)
    for _ in range(70):
        s.circle(rnd.uniform(146, 614), rnd.uniform(138, 152), 3, "#b0b0b0", sw=0.5)
    for x0 in (220, 460):
        s.rect(x0, 142, 80, 14, AU)
        for k in range(6):
            s.circle(x0 + 10 + k * 12, 137, 4.5, "#d8d8d8", sw=0.6)
    s.rect(80, 156, 600, 40, POLY)
    s.text(600, 181, "polyimide flex", anchor="middle", size=12)
    for x0 in (220, 460):
        s.rect(x0 + 30, 156, 20, 40, CU)
        s.rect(x0 - 20, 196, 120, 12, AU)
        s.circle(x0 + 40, 250, 46, SOLDER)
        s.rect(x0 - 20, 196, 120, 12, AU)
    s.rect(60, 296, 640, 14, CU)
    s.rect(60, 310, 640, 50, PCB)
    s.text(380, 340, "main PCB", anchor="middle", fill="#ffffff")
    s.label(590, 240, "ordinary solder balls on the\nflex's gold-plated copper pads", 545, 250)
    s.label(190, 262, "plated via carries the\nsignal through the flex", 258, 180, anchor="end")
    s.label(120, 110, "Al pad, untreated", 226, 125, anchor="end")
    s.label(625, 105, "particles trapped between\nAl pad and flex pad", 538, 137)
    s.text(380, 436, "Not to scale. The join to aluminium is adhesive; the solder only ever touches the flex.", size=11, anchor="middle", fill="#555555")
    s.save("flex-ztape-cross-section.svg")


def fig_wlcsp():
    s = Svg(W + 120, H, "Wafer level chip scale package with redistribution layer", shift=60)
    s.text(380, 30, "Proprietary wafer-level bumping with redistribution", size=16, anchor="middle", weight="bold")
    bx, r = 520, 105
    s.circle(bx, 274 - math.sqrt(r * r - 70 * 70), r, SOLDER)
    s.rect(60, 350, 640, 60, SI)
    s.text(380, 386, "die", anchor="middle", fill="#ffffff")
    s.rect(60, 330, 640, 20, PASS)
    s.rect(110, 338, 90, 12, AL)
    s.rect(135, 330, 40, 8, "#ffffff", stroke="none")
    s.rect(60, 312, 640, 18, POLY)
    s.rect(138, 312, 34, 26, CU, stroke="none")
    s.rect(120, 302, 480, 10, CU)
    s.rect(60, 284, 640, 18, POLY)
    s.rect(60, 302, 60, 10, POLY, stroke="none")
    s.rect(600, 302, 100, 10, POLY, stroke="none")
    s.rect(450, 284, 140, 18, SOLDER, stroke="none")
    s.poly([(440, 284), (450, 284), (450, 302), (590, 302), (590, 284), (600, 284),
            (600, 276), (584, 276), (584, 296), (456, 296), (456, 276), (440, 276)], NI)
    s.label(120, 250, "small Al pad\n(any pad ring)", 155, 344, anchor="end")
    s.label(150, 170, "polymer repassivation,\ntwo layers", 210, 293, anchor="end")
    s.label(395, 190, "plated Cu redistribution\ntrace moves the ball\naway from the pad", 420, 307, anchor="end")
    s.label(650, 130, "solder ball on\nplated UBM", bx + 60, 190, anchor="start")
    s.text(380, 436, "Not to scale.", size=11, anchor="middle", fill="#555555")
    s.save("wlcsp-rdl-cross-section.svg")


def flow(name, title, steps, cols=4, note=None):
    bw, bh, gx, gy = 160, 64, 28, 40
    rows = math.ceil(len(steps) / cols)
    w = 880  # same canvas width as the cross-sections, so text renders at one size
    x_left = (w - cols * bw - (cols - 1) * gx) / 2
    h = 70 + rows * bh + (rows - 1) * gy + (50 if note else 24)
    s = Svg(w, h, title)
    s.text(w / 2, 30, title, size=16, anchor="middle", weight="bold")
    pos = []
    for i, st in enumerate(steps):
        r, c = divmod(i, cols)
        if r % 2:
            c = cols - 1 - c
        x = x_left + c * (bw + gx)
        y = 56 + r * (bh + gy)
        pos.append((x, y))
        text, fill = st if isinstance(st, tuple) else (st, "#e9f0f7")
        s.rect(x, y, bw, bh, fill, rx=8)
        lines = text.split("\n")
        y0 = y + bh / 2 - (len(lines) - 1) * 8 + 4
        s.text(x + bw / 2, y0, text, size=12, anchor="middle")
    for (x1, y1), (x2, y2) in zip(pos, pos[1:]):
        if y1 == y2:
            if x2 > x1:
                s.line(x1 + bw, y1 + bh / 2, x2 - 2, y2 + bh / 2, sw=1.4, extra='marker-end="url(#arr)"')
            else:
                s.line(x1, y1 + bh / 2, x2 + bw + 2, y2 + bh / 2, sw=1.4, extra='marker-end="url(#arr)"')
        else:
            s.line(x1 + bw / 2, y1 + bh, x2 + bw / 2, y2 - 2, sw=1.4, extra='marker-end="url(#arr)"')
    if note:
        s.text(w / 2, h - 18, note, size=12, anchor="middle", fill="#555555")
    s.save(name)


WET, HOT, DRY = "#dbeaf7", "#f9dfc8", "#e6f2de"


def fig_flows():
    flow("enig-flow.svg", "ENIG on loose die: process flow", [
        ("Mount die on carrier,\nprotect edges and back", DRY),
        ("Clean and\nlight etch", WET),
        ("First zincate\n30 s, room temp", WET),
        ("Strip zinc in\n50% nitric, 5 s", WET),
        ("Second zincate\n30 s, room temp", WET),
        ("Electroless Ni-P\n88 °C, 15 min, 5 µm", HOT),
        ("Immersion Au\n90 °C, 1 min", HOT),
        ("Rinse, dry,\nrelease from carrier", DRY),
    ], note="DI water rinse between every wet step. Times from the Virginia Tech single-die thesis.")
    flow("home-nickel-flow.svg", "Home zincate and electroless nickel: process flow", [
        ("Stick die to a holder,\npaint edges and back", DRY),
        ("Degrease\n(IPA, detergent)", WET),
        ("Zincate dip\n15 to 30 s, room temp", WET),
        ("Strip in nitric acid,\nzincate again (optional)", WET),
        ("Electroless nickel kit\n85 to 90 °C, 10 to 20 min", HOT),
        ("Rinse and dry", WET),
        ("Flux and reball\nthe same day", HOT),
        ("Test: continuity,\npush on the balls", DRY),
    ], note="Distilled water rinse between every wet step. Times are starting points, not a proven recipe.")
    flow("al-paste-flow.svg", "Aluminium solder paste: process flow", [
        ("Die in a nest\nunder a stencil", DRY),
        ("Print aluminium\nsolder paste", WET),
        ("Hot plate reflow,\nreach temperature fast", HOT),
        ("Rinse residue off\nin hot water", WET),
        ("Inspect bumps,\ncheck pad still there", DRY),
        ("Optional: reball on\ntop of the tinned pads", HOT),
    ], cols=3)
    flow("silver-mirror-flow.svg", "Silver mirror: process flow", [
        ("Mask everything\nexcept the pads", DRY),
        ("Mix fresh Tollens\nreagent, small batch", WET),
        ("Add glucose,\nimmerse die", WET),
        ("Rinse, remove mask\n(lifts stray silver)", WET),
        ("Destroy leftover\nreagent with acid", HOT),
        ("Join with silver epoxy\nor low-temp solder", DRY),
    ], cols=3, note="Never store Tollens reagent: it forms explosive silver nitride on standing.")
    flow("ball-attach-flow.svg", "Reballing a bare die: process flow", [
        ("Die with treated\npads in a nest", DRY),
        ("Thin smear of\ntacky flux", WET),
        ("Align stencil,\nbrush balls into holes", DRY),
        ("Lift stencil (or leave a\ndirect-heat stencil on)", DRY),
        ("Heat from below until\nballs go shiny and round", HOT),
        ("Clean flux,\nprod each ball", WET),
    ], cols=3)
    flow("stud-bump-flow.svg", "Stud bump route: process flow", [
        ("Mount die on\nheated chuck", DRY),
        ("Thermosonic\nball bond on pad", HOT),
        ("Break wire,\nleaving a stud", DRY),
        ("Coin studs flat\n(optional)", DRY),
        ("Add solder: jet,\ndip or place ball", HOT),
        ("Short, cool reflow\n(keep Au-Al cool)", HOT),
    ], cols=3)
    flow("sputter-flow.svg", "Sputtered UBM on loose die: process flow", [
        ("Mount die in\ncarrier pocket", DRY),
        ("Align shadow mask\nover the pads", DRY),
        ("Pump down,\nsputter-etch oxide", HOT),
        ("Deposit Ti,\nthen Ni, then Au", HOT),
        ("Remove mask,\ninspect", DRY),
        ("Ball attach", HOT),
    ], cols=3)
    flow("wafer-level-flow.svg", "Proprietary wafer-level bumping: process flow", [
        ("Lay out pads to the\nbump house rules", DRY),
        ("Buy the\nundiced wafer", DRY),
        ("Repassivation and\nRDL (optional)", HOT),
        ("UBM: electroless Ni/Au\nor sputter and plate", WET),
        ("Ball place\nand reflow", HOT),
        ("Backgrind, dice,\ntape and reel", DRY),
    ], cols=3)


def fig_routes():
    s = Svg(860, 500, "Home routes from bare aluminium pad to solder ball")
    s.text(430, 30, "Home routes: make the pad solderable, then add the solder", size=16, anchor="middle", weight="bold")
    s.text(180, 62, "Step 1: treat the Al pad", size=13, anchor="middle", weight="bold")
    s.text(680, 62, "Step 2: add the solder", size=13, anchor="middle", weight="bold")
    left = [
        ("Zincate + electroless nickel kit", DRY, 90),
        ("Aluminium solder paste or flux", HOT, 160),
        ("Silver: mirror or displacement", "#f6d5d2", 230),
    ]
    for t, c, y in left:
        s.rect(40, y, 280, 44, c, rx=8)
        s.text(180, y + 27, t, anchor="middle")
    s.rect(560, 90, 240, 44, "#e9f0f7", rx=8)
    s.text(680, 117, "Reballing stencil + 0.25 mm balls", anchor="middle")
    s.rect(560, 160, 240, 44, "#e9f0f7", rx=8)
    s.text(680, 187, "Paste already leaves a bump", anchor="middle")
    s.rect(560, 300, 240, 44, "#e9f0f7", rx=8)
    s.text(680, 327, "Silver epoxy dots (no solder)", anchor="middle")
    s.line(320, 112, 558, 112, sw=1.4, extra='marker-end="url(#arr)"')
    s.line(320, 182, 558, 182, sw=1.4, extra='marker-end="url(#arr)"')
    s.line(320, 176, 558, 120, sw=1, extra='marker-end="url(#arr)"')
    s.line(320, 252, 558, 126, sw=1, extra='marker-end="url(#arr)" stroke-dasharray="5 4"')
    s.line(320, 258, 558, 316, sw=1, extra='marker-end="url(#arr)"')
    s.rect(40, 300, 280, 44, "#eeeeee", rx=8)
    s.text(180, 327, "Nothing (bare Al, scratched)", anchor="middle")
    s.line(320, 322, 558, 322, sw=1, extra='marker-end="url(#arr)" stroke-dasharray="5 4"')
    s.text(430, 400, "Green: real nickel barrier, most steps. Orange: fewest steps, unproven on thin pads.", size=12, anchor="middle", fill="#555555")
    s.text(430, 420, "Red: silver dissolves in molten solder, so it suits epoxy better than solder.", size=12, anchor="middle", fill="#555555")
    s.text(430, 440, "Dashed arrows: expected to be marginal.", size=12, anchor="middle", fill="#555555")
    s.save("routes.svg")


def fig_home_nickel():
    s = Svg(W + 120, H, "Home zincate and electroless nickel with solder ball", shift=60)
    ball(s, 270, 108)
    base(s)
    ni = [
        (CX - OPEN, Y_PAD), (CX + OPEN, Y_PAD), (CX + OPEN, Y_PASS),
        (CX + OPEN + 8, Y_PASS), (CX + OPEN + 8, 272), (CX + OPEN + 5, 270),
        (CX - OPEN - 5, 270), (CX - OPEN - 8, 272), (CX - OPEN - 8, Y_PASS),
        (CX - OPEN, Y_PASS),
    ]
    s.poly(ni, NI)
    s.line(CX - OPEN + 2, Y_PAD - 1, CX + OPEN - 2, Y_PAD - 1, stroke=IMC, sw=2)
    s.label(560, 130, "0.25 mm solder ball from\na reballing stencil", CX + 100, 170)
    s.label(570, 185, "no gold at home: solder soon,\nwith an active flux", CX + 104, 270, fill=WARN)
    s.label(570, 234, "electroless nickel from a\nhobby kit, a few µm", CX + 80, 286)
    s.label(225, 200, "nickel grows only on metal,\nso no mask is needed", CX - OPEN - 6, 275, anchor="end")
    s.label(225, 250, "zincate dip: eats 0.3 to 0.4 µm\nof a 1.1 µm pad", CX - 70, Y_PAD - 1, anchor="end", fill=IMC)
    s.text(380, 30, "Home zincate and electroless nickel", size=16, anchor="middle", weight="bold")
    s.save("home-nickel-cross-section.svg")


def fig_al_paste():
    s = Svg(W + 120, H, "Aluminium solder paste reflowed directly on the pad", shift=60)
    r, hw = 115, 96
    d = math.sqrt(r * r - hw * hw)
    s.add(f'<path d="M{CX - hw},{Y_PAD} A{r},{r} 0 0 1 {CX + hw},{Y_PAD} z" '
          f'fill="{SOLDER}" stroke="{INK}"/>')
    base(s)
    s.line(CX - 96, Y_PAD, CX + 96, Y_PAD, stroke=IMC, sw=3)
    s.label(560, 170, "Sn-Ag solder dome left\nby the printed paste", CX + 40, 262)
    s.label(570, 230, "silver-aluminium intermetallic\nmakes the bond (seen on bulk Al)", CX + 60, Y_PAD, fill=IMC)
    s.label(225, 190, "aggressive flux removes the oxide:\nmust be rinsed off afterwards", CX - 90, 285, anchor="end", fill=WARN)
    s.label(225, 250, "unknown: does a 1.1 µm pad\nsurvive the flux and the tin?", CX - 108, Y_PAD + 10, anchor="end", fill=WARN)
    s.text(380, 30, "Aluminium solder paste straight on the pad", size=16, anchor="middle", weight="bold")
    s.save("al-paste-cross-section.svg")


def fig_silver():
    s = Svg(W + 120, H, "Silver mirror deposit covering pads and passivation", shift=60)
    s.text(380, 30, "Silver mirror: the silver goes everywhere", size=16, anchor="middle", weight="bold")
    s.rect(60, Y_SUB, 640, 70, SI)
    s.text(380, 362, "inter-metal dielectric, lower metals, silicon", anchor="middle", fill="#ffffff")
    for x0 in (150, 430):
        s.rect(x0, Y_PAD, 180, 20, AL)
    for x0, w in ((60, 110), (310, 140), (590, 110)):
        s.rect(x0, Y_PASS, w, 40, PASS)
    pts = [(60, Y_PASS), (170, Y_PASS), (170, Y_PAD), (310, Y_PAD), (310, Y_PASS),
           (450, Y_PASS), (450, Y_PAD), (590, Y_PAD), (590, Y_PASS), (700, Y_PASS)]
    up = [(x, y - 5) for x, y in pts]
    up[1] = (175, Y_PASS - 5); up[2] = (175, Y_PAD - 5); up[3] = (305, Y_PAD - 5); up[4] = (305, Y_PASS - 5)
    up[5] = (455, Y_PASS - 5); up[6] = (455, Y_PAD - 5); up[7] = (585, Y_PAD - 5); up[8] = (585, Y_PASS - 5)
    s.poly(pts + up[::-1], "#f2f2f2", sw=0.8)
    s.label(560, 150, "silver film about 0.1 µm, on\npads and passivation alike", 520, Y_PAD - 4)
    s.label(570, 215, "bridge between pads: must be\nmasked or removed", 380, Y_PASS - 4, fill=WARN)
    s.label(225, 160, "alkaline bath also etches\nthe aluminium", 240, Y_PAD + 6, anchor="end", fill=WARN)
    s.label(180, 228, "oxide stays under the silver\nunless removed first", 200, Y_PAD - 1, anchor="end", fill=WARN)
    s.text(380, 436, "Two neighbouring pads. Not to scale.", size=11, anchor="middle", fill="#555555")
    s.save("silver-mirror-cross-section.svg")


def fig_array():
    sc = 90  # px per mm
    dw, dh = 3.93, 5.12
    s = Svg(1040, 600, "Ball arrays drawn to scale on wafer.space slots")
    s.text(520, 30, "Ball arrays to scale: 250 µm balls", size=16, anchor="middle", weight="bold")

    def die(x0, y0, w, h, nx, ny, cap):
        s.rect(x0, y0, w * sc, h * sc, "#dfe5ec")
        px, py = w * 0.95 / nx, h * 0.95 / ny
        for i in range(nx):
            for j in range(ny):
                cx = x0 + (w / 2 + (i - (nx - 1) / 2) * px) * sc
                cy = y0 + (h / 2 + (j - (ny - 1) / 2) * py) * sc
                s.circle(cx, cy, 0.125 * sc, SOLDER)
        s.text(x0 + w * sc / 2, y0 + h * sc + 20,
               f"{cap}\n{nx} x {ny} = {nx * ny} balls\npitch {px:.2f} x {py:.2f} mm",
               size=12, anchor="middle")

    die(40, 60, dw, dh, 8, 10, "3.93 x 5.12 mm slot")
    die(430, 60, dw, dh, 9, 12, "3.93 x 5.12 mm slot")
    die(820, 60, 1.94, 2.53, 4, 5, "1.94 x 2.53 mm quarter slot")
    s.save("ball-arrays.svg")


def fig_fc01():
    sc = 0.2  # px per µm
    s = Svg(820, 620, "Sketch of the FC01 flip chip pad test die")
    s.text(410, 30, "FC01 on Run 2: pad layout as estimated from the public render", size=16, anchor="middle", weight="bold")
    x0, y0 = 60, 60
    s.rect(x0, y0, 1940 * sc, 2530 * sc, "#dfe5ec")
    big = [(675 + i * 400, 1155 + j * 400) for j in range(3) for i in range(2)]
    small = [(225, 335 + k * 150) for k in range(3)] + [(225, 790 + k * 110) for k in range(3)]
    for bx, by in big:
        s.rect(x0 + bx * sc, y0 + by * sc, 220 * sc, 220 * sc, AL)
    for sx, sy in small:
        s.rect(x0 + sx * sc, y0 + sy * sc, 120 * sc, 60 * sc, AL)
    s.label(500, 150, "6 small pads, roughly 120 x 60 µm,\nfor probing or wire bonding", x0 + 345 * sc, y0 + 365 * sc)
    s.label(500, 330, "6 large pads, roughly 220 µm square\non a 0.4 mm grid (2 x 3)", x0 + 1295 * sc, y0 + 1265 * sc)
    s.text(500, 430, "traces join large pads to small pads\n(not drawn: pairing not verified)", fill="#8a6fb0")
    s.label(500, 520, "die 1.94 x 2.53 mm, no transistors", x0 + 1940 * sc, y0 + 2300 * sc)
    s.text(410, 600, "Dimensions are measured off an image at about 2.5 µm per pixel, so treat them as plus or minus 10%.", size=11, anchor="middle", fill="#555555")
    s.save("fc01-layout.svg")


def fig_caravel_bumps():
    sc = 90  # px per mm
    dw, dh = 3.88, 5.07
    s = Svg(1060, 600, "Caravel bump layout from the open_pdks Micross generator")
    s.text(500, 30, "Caravel on GF180MCU: 6 x 10 bumps at 0.5 mm pitch", size=16, anchor="middle", weight="bold")
    x0, y0 = 60, 60
    s.rect(x0, y0, dw * sc, dh * sc, "#dfe5ec")

    def pt(x, y):  # die coordinates in µm, origin bottom left
        return x0 + x * sc / 1000, y0 + (dh * 1000 - y) * sc / 1000

    pad = 60 * sc / 1000
    for i in range(21):
        cx, cy = pt(100, 462.5 + 205 * i)
        s.rect(cx - pad / 2, cy - pad / 2, pad, pad, AL, sw=0.5)
    for i in range(20):
        cx, cy = pt(3780, 482.5 + 215 * i)
        s.rect(cx - pad / 2, cy - pad / 2, pad, pad, AL, sw=0.5)
    for i in range(11):
        cx, cy = pt(562.5 + 275 * i, 100)
        s.rect(cx - pad / 2, cy - pad / 2, pad, pad, AL, sw=0.5)
        cx, cy = pt(557.5 + 275 * i, 4970)
        s.rect(cx - pad / 2, cy - pad / 2, pad, pad, AL, sw=0.5)
    for i in range(6):
        for j in range(10):
            cx, cy = pt(1940 + (i - 2.5) * 500, 2535 + (j - 4.5) * 500)
            s.circle(cx, cy, 0.135 * sc, CU, sw=0.5)
            s.circle(cx, cy, 0.125 * sc, SOLDER, sw=0.5)
    s.text(x0 + dw * sc / 2, y0 + dh * sc + 20, "die 3.88 x 5.07 mm, 63 wire bond pads, 60 bumps",
           size=12, anchor="middle")
    px, py = pt(3780, 482.5 + 215 * 19)
    s.label(470, 100, "wire bond pads, 60 x 60 µm openings,\n205 to 275 µm pitch (inset from\nthe edge is not to scale)", px, py)
    px, py = pt(1940 + 2.5 * 500, 2535 + 2.5 * 500)
    s.label(470, 185, "bump sites on a 0.5 mm grid, joined to the\npads by 15 µm wide copper traces (not drawn)", px, py)

    # One bump site, enlarged: 1 px = 1 µm.
    cx, cy = 720, 400
    s.text(cx, 262, "One bump site, enlarged", size=13, anchor="middle", weight="bold")
    s.circle(cx, cy, 135, CU)
    s.circle(cx, cy, 125, NI)
    s.circle(cx, cy, 110, POLY)
    s.label(880, 300, "copper pad,\n270 µm", cx + 92, cy - 96)
    s.label(880, 370, "under-bump metal,\n250 µm", cx + 118, cy - 30)
    s.label(880, 440, "opening in top\npolymer, 220 µm", cx + 60, cy + 40)
    s.text(cx, 560, "A 250 µm ball sits on the under-bump metal.", size=11, anchor="middle", fill="#555555")
    s.save("caravel-bump-layout.svg")


def fig_sky130_probe_pads():
    sc = 1.6  # px per µm
    s = Svg(900, 520, "Probe pad grid of the open sky130 test tile")
    s.text(450, 30, "Open sky130 test tile: probe pad grid", size=16, anchor="middle", weight="bold")
    x0, y0 = 60, 90
    for i in range(6):
        for j in range(3):
            x, y = x0 + i * 60 * sc, y0 + j * 80 * sc
            s.rect(x, y, 40 * sc, 40 * sc, AL)
            s.text(x + 20 * sc, y + 20 * sc + 4, f"{i + 1},{3 - j}", size=11, anchor="middle")
    s.dim(x0, x0 + 40 * sc, y0 - 12, "40 µm")
    s.dim(x0, x0 + 60 * sc, y0 + 200 * sc + 30, "60 µm pitch")
    bx = x0 + 4 * 60 * sc
    s.rect(bx + 4, y0 + 40 * sc + 6, 40 * sc - 8, 40 * sc - 12, "none", stroke=WARN, sw=1.2,
           extra='stroke-dasharray="5 3"')
    s.label(680, 150, "device under test\nsits between rows", bx + 40 * sc - 8, y0 + 60 * sc)
    px = x0 + 5 * 60 * sc + 40 * sc + 14
    s.line(px, y0 + 80 * sc, px, y0 + 160 * sc, extra='marker-start="url(#arr)" marker-end="url(#arr)"')
    s.text(px + 10, y0 + 120 * sc + 4, "80 µm pitch between rows", size=12)
    s.text(450, 490, "A 250 µm solder ball would cover a block of about 4 x 3 of these pads.",
           size=11, anchor="middle", fill="#555555")
    s.save("sky130-probe-pads.svg")


def fig_notes_flows():
    flow("plated-rdl-flow.svg", "Plated redistribution and under-bump metal: process flow", [
        ("Finished wafer, Al pads\nunder nitride", DRY),
        ("Spin, pattern and cure\npolyimide or PBO", HOT),
        ("Sputter seed: 100 nm Ti,\n200 to 500 nm Cu", DRY),
        ("Thick resist mould,\n5 to 50 µm", DRY),
        ("Electroplate Cu,\n5 to 10 µm traces", WET),
        ("Strip resist, etch\nseed Cu and Ti", WET),
        ("Repeat for UBM: Cu,\n2 to 3 µm Ni, Au flash", WET),
        ("Drop balls through a\nstencil and reflow", HOT),
        ("Backgrind, mark,\ndice, tape and reel", DRY),
    ], cols=3, note="Unverified: from the notes of 2026-11-10.")
    flow("zincate-mechanism-flow.svg", "What a zincate dip does to an aluminium pad", [
        ("Alkaline bath\ndissolves the oxide", WET),
        ("Zinc swaps places\nwith bare aluminium", WET),
        ("Film stops growing at\ntens of nanometres", WET),
        ("Zinc shields the pad\nthrough the rinse", WET),
        ("Nickel bath: nickel\nreplaces the zinc", HOT),
    ], cols=3, note="2 Al + 3 Zn(2+) gives 2 Al(3+) + 3 Zn. Nickel then keeps growing on itself.")


if __name__ == "__main__":
    fig_bare()
    fig_enig()
    fig_stud()
    fig_sputter("sputtered-ubm-cross-section.svg", "Sputtered thin-film UBM with solder ball",
                "SAC solder ball,\n250 µm")
    fig_home_nickel()
    fig_al_paste()
    fig_silver()
    fig_adhesive()
    fig_flex()
    fig_wlcsp()
    fig_flows()
    fig_routes()
    fig_array()
    fig_fc01()
    fig_caravel_bumps()
    fig_sky130_probe_pads()
    fig_notes_flows()
