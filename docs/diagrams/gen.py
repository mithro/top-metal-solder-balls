#!/usr/bin/env python3
"""Generate the SVG diagrams used in the documentation.

Run from anywhere: ``python3 docs/diagrams/gen.py``. Output goes to
``docs/_static/diagrams/``. The SVGs are committed so that Read the Docs does
not need to run this script.

Cross-sections use roughly 1 px = 1 um horizontally. Layer thicknesses are
exaggerated by a large factor, otherwise 1 um of aluminium would be invisible
next to a 250 um ball.
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
            f'<rect width="{w}" height="{h}" fill="#ffffff"/>',
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
OPEN = 100  # half passivation opening: 200 um
PADHALF = 116  # half top metal pad: 232 um
Y_SUB, Y_PAD, Y_PASS = 320, 300, 280
NOTE = "Horizontal: about 1 px per um. Layer thicknesses greatly exaggerated."


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
    s.dim(CX - OPEN, CX + OPEN, 262, "passivation opening A (200 um here)")
    s.dim(CX - PADHALF, CX + PADHALF, 232, "top metal bump pad, A + 32")
    s.line(CX - PADHALF, 236, CX - PADHALF, Y_PAD, sw=0.6, extra='stroke-dasharray="3 3"')
    s.line(CX + PADHALF, 236, CX + PADHALF, Y_PAD, sw=0.6, extra='stroke-dasharray="3 3"')
    s.label(560, 180, "native Al oxide, a few nm:\nsolder will not wet this", CX + 40, Y_PAD, fill=WARN)
    s.label(225, 180, "Al top metal,\nabout 1.1 um (11 kA)", CX - 108, Y_PAD + 10, anchor="end")
    s.label(225, 250, "passivation\n(nitride or polyimide)", 150, Y_PASS + 10, anchor="end")
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
    s.label(560, 150, "SAC solder ball,\n250 um", CX + 100, 190)
    s.label(570, 215, "immersion Au, 0.05 to 0.1 um\n(dissolves into the solder)", CX + 104, 269)
    s.label(570, 262, "electroless Ni-P, about 5 um:\nbarrier and wettable layer", CX + 80, 286)
    s.label(225, 200, "Ni mushrooms about 5 um\nover the passivation edge", CX - OPEN - 6, 275, anchor="end")
    s.label(225, 250, "zincate seed layer on Al\n(0.3 to 0.4 um of Al consumed)", CX - 70, Y_PAD - 1, anchor="end", fill=IMC)
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
    s.label(570, 200, "Au stud from a ball bonder,\n60 to 120 um across", CX + 30, 282)
    s.label(570, 250, "AuSn4 forms around the stud:\nbrittle when gold is plentiful", CX + 46, 266, fill=IMC)
    s.label(225, 180, "Au-Al intermetallic grows\nabove about 200 C", CX - 20, Y_PAD, anchor="end", fill=IMC)
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
    s.label(570, 222, "Au cap, 0.1 to 0.2 um", CX + 112, 271)
    s.label(570, 246, "Ni (or NiV, Cu) wettable layer", CX + 114, 275)
    s.label(570, 270, "Ti or TiW adhesion / barrier", CX + 116, 279)
    s.label(225, 200, "film overlaps the passivation,\nsealing the Al (10 um or more)", CX - OPEN - 12, 275, anchor="end")
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
    s.label(225, 200, "only about 1.1 um of Al to\nsurvive cavitation and tin", CX - 108, Y_PAD + 10, anchor="end")
    s.label(225, 255, "pad edge not sealed", CX - 98, Y_PAD - 2, anchor="end", fill=WARN)
    s.text(380, 30, "Direct soldering to the Al pad (no under bump metal)", size=16, anchor="middle", weight="bold")
    s.save("direct-to-al-cross-section.svg")


def fig_adhesive():
    s = Svg(W + 120, H, "Stud bump with conductive adhesive flip chip joint", shift=60)
    s.text(380, 30, "Flip chip with a gold stud and conductive adhesive", size=16, anchor="middle", weight="bold")
    # Die, face down.
    s.rect(60, 60, 640, 70, SI)
    s.text(380, 100, "die (face down)", anchor="middle", fill="#ffffff")
    s.rect(60, 130, 220, 30, PASS)
    s.rect(480, 130, 220, 30, PASS)
    s.rect(264, 130, 232, 16, AL)
    # Underfill, adhesive, stud.
    s.rect(60, 160, 640, 150, "#f3ead7", stroke="none")
    s.rect(280, 146, 200, 14, "#f3ead7", stroke="none")
    s.add(f'<ellipse cx="{CX}" cy="268" rx="78" ry="44" fill="{ICA}" stroke="{INK}"/>')
    s.rect(CX - 40, 146, 80, 44, AU, rx=10)
    s.rect(CX - 14, 186, 28, 60, AU, rx=8)
    # Board.
    s.rect(240, 300, 280, 16, CU)
    s.rect(60, 316, 640, 70, PCB)
    s.text(380, 356, "substrate / PCB", anchor="middle", fill="#ffffff")
    s.label(560, 200, "Au stud bump on the Al pad", CX + 38, 170)
    s.label(570, 262, "silver-filled conductive adhesive", CX + 70, 262)
    s.label(570, 296, "Cu pad with Au finish", 500, 306)
    s.label(225, 215, "underfill (often needed\nfor strength)", 200, 240, anchor="end")
    s.text(380, 436, "Not to scale.", size=11, anchor="middle", fill="#555555")
    s.save("adhesive-cross-section.svg")


def fig_wlcsp():
    s = Svg(W + 120, H, "Wafer level chip scale package with redistribution layer", shift=60)
    s.text(380, 30, "Commercial wafer-level bumping with redistribution", size=16, anchor="middle", weight="bold")
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
    s.label(130, 150, "small Al pad\n(any pad ring)", 155, 344, anchor="end")
    s.label(150, 215, "polymer repassivation,\ntwo layers", 210, 293, anchor="end")
    s.label(395, 190, "plated Cu redistribution\ntrace moves the ball\naway from the pad", 350, 307, anchor="end")
    s.label(650, 130, "solder ball on\nplated UBM", bx + 60, 190, anchor="start")
    s.text(380, 436, "Not to scale.", size=11, anchor="middle", fill="#555555")
    s.save("wlcsp-rdl-cross-section.svg")


def flow(name, title, steps, cols=4, note=None):
    bw, bh, gx, gy = 160, 64, 28, 40
    rows = math.ceil(len(steps) / cols)
    w = 40 + cols * bw + (cols - 1) * gx + 40
    h = 70 + rows * bh + (rows - 1) * gy + (50 if note else 24)
    s = Svg(w, h, title)
    s.text(w / 2, 30, title, size=16, anchor="middle", weight="bold")
    pos = []
    for i, st in enumerate(steps):
        r, c = divmod(i, cols)
        if r % 2:
            c = cols - 1 - c
        x = 40 + c * (bw + gx)
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
        ("Electroless Ni-P\n88 C, 15 min, 5 um", HOT),
        ("Immersion Au\n90 C, 1 min", HOT),
        ("Rinse, dry,\nrelease from carrier", DRY),
    ], note="DI water rinse between every wet step. Times from the Virginia Tech single-die thesis.")
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
    flow("ball-attach-flow.svg", "Ball attach by stencil: process flow", [
        ("Die with UBM\nin a nest", DRY),
        ("Apply tacky flux\nto the pads", WET),
        ("Align stencil,\nsweep balls into holes", DRY),
        ("Lift stencil,\ninspect, fix strays", DRY),
        ("Reflow\n(about 245 C for SAC)", HOT),
        ("Clean flux,\nshear test samples", WET),
    ], cols=3)
    flow("wafer-level-flow.svg", "Commercial wafer-level bumping: process flow", [
        ("Lay out pads to the\nbump house rules", DRY),
        ("Buy the\nundiced wafer", DRY),
        ("Repassivation and\nRDL (optional)", HOT),
        ("UBM: electroless Ni/Au\nor sputter and plate", WET),
        ("Ball place\nand reflow", HOT),
        ("Backgrind, dice,\ntape and reel", DRY),
    ], cols=3)


def fig_routes():
    s = Svg(820, 470, "Routes from bare aluminium pad to solder ball")
    s.text(410, 30, "Two steps: make the pad solderable, then add the solder", size=16, anchor="middle", weight="bold")
    s.text(170, 62, "Step 1: under bump metal", size=13, anchor="middle", weight="bold")
    s.text(650, 62, "Step 2: solder", size=13, anchor="middle", weight="bold")
    left = [
        ("Electroless Ni / Au (zincate)", DRY, 90),
        ("Sputtered Ti / Ni / Au", DRY, 150),
        ("Gold stud bump", HOT, 210),
        ("Commercial wafer bumping", DRY, 270),
    ]
    right = [
        ("Stencil ball placement", 90),
        ("Laser solder jetting", 170),
        ("Paste printing", 250),
    ]
    for t, c, y in left:
        s.rect(40, y, 260, 40, c, rx=8)
        s.text(170, y + 25, t, anchor="middle")
    for t, y in right:
        s.rect(540, y, 220, 40, "#e9f0f7", rx=8)
        s.text(650, y + 25, t, anchor="middle")
    for _, _, y in left[:2]:
        for _, ry in right:
            s.line(300, y + 20, 538, ry + 20, sw=1, extra='marker-end="url(#arr)"')
    s.line(300, 230, 538, 195, sw=1, extra='marker-end="url(#arr)" stroke-dasharray="5 4"')
    s.line(300, 290, 538, 115, sw=1, extra='marker-end="url(#arr)"')
    s.rect(40, 350, 260, 40, "#f6d5d2", rx=8)
    s.text(170, 375, "Ultrasonic / active solder, Sn-Zn", anchor="middle")
    s.rect(540, 350, 220, 40, "#f6d5d2", rx=8)
    s.text(650, 375, "Solder straight on Al", anchor="middle")
    s.line(300, 370, 538, 370, sw=1, extra='marker-end="url(#arr)" stroke-dasharray="5 4"')
    s.text(410, 425, "Solid arrows: established combinations. Dashed: works for prototypes or unproven on thin pads.", size=12, anchor="middle", fill="#555555")
    s.text(410, 445, "Green: gives a real barrier layer. Orange: no barrier. Red: no under bump metal at all.", size=12, anchor="middle", fill="#555555")
    s.save("routes.svg")


def fig_array():
    sc = 90  # px per mm
    dw, dh = 3.93, 5.12
    s = Svg(1040, 600, "Ball arrays drawn to scale on wafer.space slots")
    s.text(520, 30, "Ball arrays to scale: 250 um balls", size=16, anchor="middle", weight="bold")

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


if __name__ == "__main__":
    fig_bare()
    fig_enig()
    fig_stud()
    fig_sputter("sputtered-ubm-cross-section.svg", "Sputtered thin-film UBM with solder ball",
                "SAC solder ball,\n250 um")
    fig_direct()
    fig_adhesive()
    fig_wlcsp()
    fig_flows()
    fig_routes()
    fig_array()
