"""Draw the 27 November 2026 world-news front page.

Pure Pillow, no network, no randomness, no clock: the same code always
writes the same bytes. Newspaper front page: a navy masthead with the
date, one big lead story (the tankers hit by mines off Hormuz), and a
2x2 grid of four more stories, each with a small hand-drawn pictogram.
All numbers shown are the verified figures from the day's reporting.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 233)
NAVY = (30, 41, 66)
INK = (26, 26, 26)
RED = (178, 38, 29)
ORANGE = (230, 112, 40)
GOLD = (216, 164, 64)
TEAL = (46, 111, 106)
GREY = (118, 118, 112)
LIGHT = (255, 255, 255)
MIDGREY = (60, 60, 60)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
]


def load_font(bold, size):
    names = (
        ["DejaVuSans-Bold.ttf", "LiberationSans-Bold.ttf"]
        if bold
        else ["DejaVuSans.ttf", "LiberationSans-Regular.ttf"]
    )
    for d in FONT_DIRS:
        for n in names:
            p = os.path.join(d, n)
            if os.path.exists(p):
                return ImageFont.truetype(p, size)
    return ImageFont.load_default()


F_TITLE = load_font(True, 62)
F_DATE = load_font(False, 27)
F_KICKER = load_font(True, 20)
F_LEAD = load_font(True, 42)
F_LEAD_SUB = load_font(False, 25)
F_HEAD = load_font(True, 28)
F_SUB = load_font(False, 20)


def wrap(d, text, font, max_w):
    """Greedy word wrap to a pixel width; returns a list of lines."""
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if d.textlength(trial, font=font) <= max_w:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def center(d, cx, y, text, font, fill):
    d.text((cx - d.textlength(text, font=font) / 2, y), text,
           font=font, fill=fill)


def star(d, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -90 + i * 36
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(math.radians(ang)),
                    cy + rr * math.sin(math.radians(ang))))
    d.polygon(pts, fill=fill)


def waves(d, x0, x1, y):
    for wx in range(x0, x1 - 30, 44):
        d.arc([wx, y - 7, wx + 32, y + 7], 180, 360, fill=TEAL, width=3)


def draw_tanker_mine(d, x0, y0, x1, y1):
    """Oil tanker in the Strait of Hormuz, with a spiked sea mine.

    Drawn in a 96-tall reference box and scaled to the region given,
    so the same code serves the lead story and any smaller slot.
    """
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # reference box is 258 wide, 100 tall; fit inside the region given
    s = min((x1 - x0) / 258.0, (y1 - y0) / 100.0)

    def X(v):
        return cx + v * s

    def Y(v):
        return cy + v * s

    def R(v):
        return v * s

    # sea mine, floating ahead of the ship
    mx, my = X(-105), Y(2)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        d.line([(mx + 12 * s * math.cos(a), my + 12 * s * math.sin(a)),
                (mx + 23 * s * math.cos(a), my + 23 * s * math.sin(a))],
               fill=INK, width=max(2, int(4 * s)))
    d.ellipse([mx - R(13), my - R(13), mx + R(13), my + R(13)], fill=INK,
              outline=LIGHT, width=2)
    # tanker hull and bridge
    d.polygon([(X(-88), Y(-8)), (X(118), Y(-8)),
               (X(96), Y(26)), (X(-68), Y(26))], fill=NAVY)
    d.rectangle([X(-88), Y(-8), X(118), Y(0)], fill=RED)
    d.rectangle([X(82), Y(-34), X(114), Y(-8)], fill=LIGHT,
                outline=INK, width=2)
    # containers on deck
    for i, c in enumerate([TEAL, GOLD, RED]):
        d.rectangle([X(-62 + i * 42), Y(-30), X(-26 + i * 42), Y(-8)],
                    fill=c, outline=INK, width=2)
    # funnel with smoke
    d.rectangle([X(-76), Y(-28), X(-52), Y(-8)], fill=INK)
    for sx, sy, r in [(-66, -38, 9), (-78, -48, 11), (-56, -54, 8)]:
        d.ellipse([X(sx) - R(r), Y(sy) - R(r), X(sx) + R(r), Y(sy) + R(r)],
                  fill=(150, 150, 145))
    waves(d, x0 + 8, x1 - 8, Y(36))
    waves(d, x0 + 8, x1 - 8, Y(46))
    # oil price badge
    bx, by = x1 - 6, y1 - 8
    d.rounded_rectangle([bx - 108, by - 34, bx + 8, by + 8], radius=10,
                        fill=RED, outline=LIGHT, width=3)
    center(d, bx - 50, by - 27, "$96.57", load_font(True, 24), LIGHT)


def draw_drone(d, x0, y0, x1, y1):
    """Quadcopter drone over a radar site, two red warning flashes."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # radar arcs behind the drone
    for r in (26, 40, 54):
        d.arc([cx - r, cy + 8 - r, cx + r, cy + 8 + r], 200, 340,
              fill=GREY, width=3)
    # arms and rotors
    for sx, sy in [(cx - 46, cy - 22), (cx + 46, cy - 22),
                   (cx - 46, cy + 12), (cx + 46, cy + 12)]:
        d.line([(cx, cy - 8), (sx, sy)], fill=INK, width=5)
        d.line([(sx - 26, sy), (sx + 26, sy)], fill=INK, width=4)
        d.ellipse([sx - 8, sy - 8, sx + 8, sy + 8], fill=GREY,
                  outline=INK, width=2)
    # body and camera eye
    d.rounded_rectangle([cx - 34, cy - 18, cx + 34, cy + 8], radius=12,
                        fill=(90, 95, 105), outline=INK, width=3)
    d.ellipse([cx - 9, cy - 11, cx + 9, cy + 7], fill=RED, outline=INK,
              width=2)
    # warning flashes
    star(d, x0 + 26, y0 + 20, 12, RED)
    star(d, x1 - 26, y0 + 44, 9, ORANGE)
    # ground line
    d.line([x0 + 12, y1 - 18, x1 - 12, y1 - 18], fill=INK, width=3)
    # "2" badge: two technicians killed
    bx, by = x1 - 26, y1 - 26
    d.ellipse([bx - 22, by - 22, bx + 22, by + 22], fill=RED,
              outline=LIGHT, width=3)
    center(d, bx, by - 15, "2", load_font(True, 26), LIGHT)


def draw_eu_stars(d, x0, y0, x1, y1):
    """Circle of gold stars on navy, with a red euro badge."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.ellipse([cx - 48, cy - 48, cx + 48, cy + 48], fill=NAVY,
              outline=INK, width=3)
    for i in range(12):
        a = math.radians(-90 + i * 30)
        star(d, cx + 32 * math.cos(a), cy + 32 * math.sin(a), 7, GOLD)
    center(d, cx, cy - 14, "EU", load_font(True, 26), LIGHT)
    # red badge with the stalled loan figure
    bx, by = x1 - 30, y1 - 24
    d.rounded_rectangle([bx - 62, by - 24, bx + 44, by + 24], radius=12,
                        fill=RED, outline=LIGHT, width=3)
    center(d, bx - 9, by - 16, "€45bn", load_font(True, 22), LIGHT)


def draw_missile_pause(d, x0, y0, x1, y1):
    """KN-23 missile on its launcher, stopped by a red pause sign."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # launcher
    d.rectangle([x0 + 16, cy + 26, x1 - 16, cy + 34], fill=GREY,
                outline=INK, width=2)
    for wx in (x0 + 30, cx - 6, x1 - 46):
        d.ellipse([wx, cy + 34, wx + 12, cy + 44], fill=INK)
    # missile body, tilted upright
    d.rounded_rectangle([cx - 18, cy - 30, cx + 18, cy + 26], radius=9,
                        fill=(90, 95, 105), outline=INK, width=3)
    d.polygon([(cx - 18, cy - 28), (cx, cy - 46), (cx + 18, cy - 28)],
              fill=RED)
    d.ellipse([cx - 9, cy - 16, cx + 9, cy + 2], fill=(140, 190, 220),
              outline=INK, width=2)
    # red pause sign
    px, py = x1 - 34, y0 + 30
    d.ellipse([px - 24, py - 24, px + 24, py + 24], fill=RED,
              outline=LIGHT, width=3)
    d.rectangle([px - 11, py - 13, px - 2, py + 13], fill=LIGHT)
    d.rectangle([px + 2, py - 13, px + 11, py + 13], fill=LIGHT)


def draw_veterans(d, x0, y0, x1, y1):
    """Soldier's helmet with a star, and a 100,000 call-up badge."""
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    # helmet dome and brim
    d.pieslice([cx - 46, cy - 46, cx + 46, cy + 24], 180, 360,
               fill=(74, 94, 58), outline=INK, width=3)
    d.rectangle([cx - 54, cy - 2, cx + 54, cy + 10], fill=(74, 94, 58),
                outline=INK, width=3)
    d.line([cx - 46, cy - 10, cx + 46, cy - 10], fill=INK, width=2)
    # gold star on the helmet
    star(d, cx, cy - 22, 14, GOLD)
    # crossed rifles below
    d.line([cx - 40, cy + 22, cx + 40, cy + 42], fill=INK, width=5)
    d.line([cx + 40, cy + 22, cx - 40, cy + 42], fill=INK, width=5)
    # call-up badge
    bx, by = x1 - 12, y1 - 20
    d.rounded_rectangle([bx - 116, by - 26, bx + 12, by + 18], radius=10,
                        fill=NAVY, outline=LIGHT, width=3)
    center(d, bx - 52, by - 19, "100,000", load_font(True, 22), LIGHT)


def draw(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer border
    d.rectangle([24, 24, 1000, 1000], outline=NAVY, width=4)
    d.rectangle([30, 30, 994, 994], outline=NAVY, width=1)

    # masthead
    d.rectangle([36, 36, 988, 134], fill=NAVY)
    center(d, 512, 52, "THE WORLD TODAY", F_TITLE, LIGHT)
    center(d, 512, 142, "Friday, 27 November 2026", F_DATE, NAVY)
    d.line([36, 178, 988, 178], fill=NAVY, width=2)

    # ---- lead story: tankers hit mines off Hormuz ----
    d.rectangle([36, 192, 988, 452], outline=INK, width=2)
    draw_tanker_mine(d, 56, 210, 340, 434)
    d.text((368, 206), "STRAIT OF HORMUZ  ·  OIL", font=F_KICKER, fill=RED)
    lead = wrap(d, "TANKERS HIT MINES, OIL JUMPS", F_LEAD, 988 - 368 - 20)
    y = 236
    for line in lead:
        d.text((368, y), line, font=F_LEAD, fill=INK)
        y += 50
    sub = wrap(d, "Iran's Revolutionary Guards say two tankers struck "
                  "mines in the strait; Brent crude settles at $96.57, "
                  "up about 8% over three sessions.",
               F_LEAD_SUB, 988 - 368 - 20)
    y += 8
    for line in sub:
        d.text((368, y), line, font=F_LEAD_SUB, fill=MIDGREY)
        y += 32

    # ---- 2x2 grid ----
    cells = [
        (36, 466, 500, 716, draw_drone,
         "DRONE STRIKE KILLS TWO ITALIANS",
         "Drones hit a Kuwaiti air-defence site on 26 Nov, killing two "
         "Italian technicians; Italy blames Iran, Iran denies it"),
        (524, 466, 988, 716, draw_eu_stars,
         "EU SUMMIT STALLS ON €45BN LOAN",
         "Brussels summit ends early with no decision on a €45bn "
         "Ukraine loan, pushed to December; budget also unresolved"),
        (36, 730, 500, 980, draw_missile_pause,
         "NORTH KOREA PAUSES MISSILE AID",
         "Ukrainian intelligence says North Korea has suspended KN-23 "
         "missile deliveries to Russia"),
        (524, 730, 988, 980, draw_veterans,
         "BRITAIN CALLS UP 100,000 VETERANS",
         "The UK is contacting 100,000 retired personnel over military "
         "readiness, a first since the Cold War"),
    ]
    for x0, y0, x1, y1, icon, head, sub in cells:
        d.rectangle([x0, y0, x1, y1], outline=INK, width=2)
        icon(d, x0 + 14, y0 + 4, x1 - 14, y0 + 98)
        head_lines = wrap(d, head, F_HEAD, x1 - x0 - 28)
        hy = y0 + 102
        for line in head_lines:
            center(d, (x0 + x1) // 2, hy, line, F_HEAD, INK)
            hy += 33
        sub_lines = wrap(d, sub, F_SUB, x1 - x0 - 36)
        for line in sub_lines:
            center(d, (x0 + x1) // 2, hy, line, F_SUB, MIDGREY)
            hy += 24

    img.save(path, "PNG")
    return path
