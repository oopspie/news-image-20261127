"""Draw the front page for THE WORLD TODAY, Friday 27 November 2026.

Everything on the page is drawn from scratch with Pillow primitives:
no photos, no downloaded assets, no network, no clock, no randomness.
Running this module twice produces byte-identical output.
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

WIDTH = 1024
HEIGHT = 1024

PAPER = (247, 243, 232)   # off-white newsprint
INK = (17, 17, 17)        # near-black ink
RED = (178, 34, 34)       # single red accent
GREY = (90, 86, 76)       # muted grey for rules and captions

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, font_obj, max_width):
    """Split text into lines that fit max_width, word by word."""
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            trial = current + " " + word
            if draw.textlength(trial, font=font_obj) <= max_width:
                current = trial
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_text_block(draw, x, y, text, font_obj, max_width, fill=INK,
                    line_spacing=6):
    """Draw wrapped text starting at (x, y); return the y below the block."""
    for line in wrap(draw, text, font_obj, max_width):
        draw.text((x, y), line, font=font_obj, fill=fill)
        bbox = draw.textbbox((0, 0), line, font=font_obj)
        y += (bbox[3] - bbox[1]) + line_spacing
    return y


def star_points(cx, cy, outer, inner, points=5, rotation=-90):
    """Return the polygon points of a regular star."""
    coords = []
    for i in range(points * 2):
        radius = outer if i % 2 == 0 else inner
        angle = math.radians(rotation + i * 180.0 / points)
        coords.append((cx + radius * math.cos(angle),
                       cy + radius * math.sin(angle)))
    return coords


def draw_tanker(draw, x, y, w, h):
    """Lead pictogram: an oil tanker at sea beside a spiked naval mine."""
    # Sky band and sea.
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=3)
    sea_y = y + int(h * 0.62)
    draw.rectangle([x, sea_y, x + w, y + h], fill=(226, 220, 203))
    # Sun.
    draw.ellipse([x + w - 78, y + 22, x + w - 30, y + 70], outline=RED,
                 width=3)
    # Mine: spiked circle, upper right of the sea.
    mx, my, mr = x + int(w * 0.68), y + int(h * 0.30), 26
    for angle in range(0, 360, 30):
        rad = math.radians(angle)
        draw.line([(mx + (mr - 2) * math.cos(rad), my + (mr - 2) * math.sin(rad)),
                   (mx + (mr + 14) * math.cos(rad), my + (mr + 14) * math.sin(rad))],
                  fill=INK, width=3)
    draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=INK)
    draw.ellipse([mx - 9, my - 9, mx + 9, my + 9], outline=PAPER, width=2)
    # Red burst lines around the mine.
    for angle in (45, 135, 225, 315):
        rad = math.radians(angle)
        draw.line([(mx + (mr + 22) * math.cos(rad), my + (mr + 22) * math.sin(rad)),
                   (mx + (mr + 34) * math.cos(rad), my + (mr + 34) * math.sin(rad))],
                  fill=RED, width=3)
    # Tanker hull.
    hull_top = sea_y - 52
    hull = [(x + 26, hull_top), (x + w - 110, hull_top),
            (x + w - 70, sea_y + 26), (x + 52, sea_y + 26),
            (x + 26, sea_y + 6)]
    draw.polygon(hull, fill=INK)
    # Deck line and funnel.
    draw.rectangle([x + 40, hull_top - 26, x + w - 130, hull_top], fill=INK)
    draw.rectangle([x + w - 128, hull_top - 58, x + w - 96, hull_top],
                   fill=RED)
    draw.rectangle([x + w - 128, hull_top - 58, x + w - 96, hull_top - 44],
                   fill=INK)
    # Bridge tower.
    draw.rectangle([x + w - 92, hull_top - 40, x + w - 62, hull_top],
                   fill=INK)
    draw.rectangle([x + w - 88, hull_top - 34, x + w - 66, hull_top - 22],
                   fill=PAPER)
    # Waves.
    for wy in (sea_y + 44, sea_y + 62, sea_y + 80):
        for wx in range(x + 14, x + w - 30, 46):
            draw.arc([wx, wy, wx + 34, wy + 18], start=180, end=360,
                     fill=INK, width=3)


def draw_drone(draw, x, y, w, h):
    """Small pictogram: a quadcopter drone seen from above."""
    cx, cy = x + w // 2, y + h // 2
    # Four arms from the centre to the rotor hubs.
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        draw.line([(cx, cy), (cx + dx * 34, cy + dy * 30)], fill=INK, width=5)
    # Rotor discs.
    for dx, dy in ((-1, -1), (1, -1), (-1, 1), (1, 1)):
        rx, ry = cx + dx * 40, cy + dy * 34
        draw.ellipse([rx - 24, ry - 9, rx + 24, ry + 9], outline=INK, width=3)
        draw.ellipse([rx - 4, ry - 4, rx + 4, ry + 4], fill=INK)
    # Central body.
    draw.ellipse([cx - 22, cy - 14, cx + 22, cy + 14], fill=INK)
    draw.ellipse([cx - 8, cy - 5, cx + 8, cy + 5], fill=RED)
    # Camera dot underneath.
    draw.ellipse([cx - 4, cy + 14, cx + 4, cy + 22], outline=INK, width=2)


def draw_eu_stars(draw, x, y, w, h):
    """Small pictogram: a ring of twelve stars, as on the EU flag."""
    cx, cy = x + w // 2, y + h // 2
    draw.ellipse([x + 4, y + 4, x + w - 4, y + h - 4], outline=RED, width=3)
    for i in range(12):
        angle = math.radians(-90 + i * 30)
        sx = cx + 34 * math.cos(angle)
        sy = cy + 34 * math.sin(angle)
        draw.polygon(star_points(sx, sy, 9, 4), fill=INK)
    draw.text((cx - 7, cy - 8), "?", font=font(SANS_BOLD, 16), fill=RED)


def draw_missile(draw, x, y, w, h):
    """Small pictogram: a missile in flight, nose up, with motion lines."""
    # Motion lines trailing down-left.
    for i, offset in enumerate((0, 14, 28)):
        draw.line([(x + 8, y + h - 18 - offset),
                   (x + 34, y + h - 18 - offset)], fill=GREY, width=3)
    # Body: a long tapered shape pointing up-right.
    body = [(x + 44, y + h - 26), (x + 62, y + 22), (x + 76, y + 12),
            (x + 88, y + 44), (x + 70, y + h - 8)]
    draw.polygon(body, fill=INK)
    # Nose cone.
    draw.polygon([(x + 62, y + 22), (x + 76, y + 12), (x + 82, y + 30)],
                 fill=RED)
    # Fins at the tail.
    draw.polygon([(x + 44, y + h - 26), (x + 30, y + h - 6),
                  (x + 52, y + h - 12)], fill=INK)
    draw.polygon([(x + 70, y + h - 8), (x + 88, y + h - 4),
                  (x + 76, y + h - 24)], fill=INK)
    # Exhaust flame.
    draw.polygon([(x + 46, y + h - 18), (x + 30, y + h - 2),
                  (x + 56, y + h - 6)], fill=RED)


def draw_helmet_letter(draw, x, y, w, h):
    """Small pictogram: a soldier's helmet above a call-up letter."""
    cx = x + w // 2
    # Helmet dome.
    draw.pieslice([cx - 34, y + 6, cx + 34, y + 62], start=180, end=360,
                  fill=INK)
    draw.rectangle([cx - 42, y + 52, cx + 42, y + 60], fill=INK)
    # Helmet ridge.
    draw.line([(cx, y + 8), (cx, y + 52)], fill=PAPER, width=2)
    # Envelope below.
    ex0, ey0, ex1, ey1 = x + 16, y + 68, x + w - 16, y + h - 6
    draw.rectangle([ex0, ey0, ex1, ey1], outline=INK, width=3, fill=(255, 255, 255))
    draw.line([(ex0, ey0), ((ex0 + ex1) // 2, ey0 + 22)], fill=INK, width=2)
    draw.line([(ex1, ey0), ((ex0 + ex1) // 2, ey0 + 22)], fill=INK, width=2)
    # Red seal on the envelope.
    draw.ellipse([(ex0 + ex1) // 2 - 9, ey0 + 16, (ex0 + ex1) // 2 + 9,
                  ey0 + 34], fill=RED)
    draw.ellipse([(ex0 + ex1) // 2 - 4, ey0 + 21, (ex0 + ex1) // 2 + 4,
                  ey0 + 29], outline=(255, 255, 255), width=1)


PICTOGRAMS = {
    "tanker": draw_tanker,
    "drone": draw_drone,
    "eu": draw_eu_stars,
    "missile": draw_missile,
    "helmet": draw_helmet_letter,
}


def draw_card(draw, x, y, w, h, kicker, headline, body, pictogram,
              headline_size=23, body_size=16):
    """Draw one of the four grid stories: text left, pictogram right."""
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    text_w = w - 150
    tx = x + 16
    ty = y + 14
    draw.text((tx, ty), kicker, font=font(SANS_BOLD, 13), fill=RED)
    ty += 24
    ty = draw_text_block(draw, tx, ty, headline, font(SERIF_BOLD, headline_size),
                         text_w, line_spacing=3)
    ty += 4
    draw_text_block(draw, tx, ty, body, font(SERIF, body_size), text_w,
                    line_spacing=4)
    PICTOGRAMS[pictogram](draw, x + w - 132, y + h - 128, 116, 116)


def draw_entry():
    """Build the full 1024x1024 front page and return the Pillow image."""
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)

    margin = 36
    content_w = WIDTH - 2 * margin

    # --- Masthead -------------------------------------------------------
    title_font = font(SERIF_BOLD, 64)
    title = "THE WORLD TODAY"
    title_w = draw.textlength(title, font=title_font)
    draw.text(((WIDTH - title_w) / 2, 26), title, font=title_font, fill=INK)
    draw.line([(margin, 112), (WIDTH - margin, 112)], fill=INK, width=3)
    date_font = font(SANS, 17)
    date_text = "Friday, 27 November 2026"
    date_w = draw.textlength(date_text, font=date_font)
    draw.text(((WIDTH - date_w) / 2, 122), date_text, font=date_font, fill=INK)
    draw.line([(margin, 152), (WIDTH - margin, 152)], fill=INK, width=2)

    # --- Lead story -----------------------------------------------------
    lead_y = 168
    lead_h = 330
    kicker_font = font(SANS_BOLD, 14)
    draw.text((margin, lead_y), "LEAD STORY  —  ENERGY MARKETS",
              font=kicker_font, fill=RED)
    head_font = font(SERIF_BOLD, 33)
    hy = draw_text_block(draw, margin, lead_y + 30,
                         "Two tankers struck by mines in the Strait of Hormuz",
                         head_font, 560, line_spacing=4)
    body_font = font(SERIF, 20)
    draw_text_block(
        draw, margin, hy + 10,
        "Iran's Revolutionary Guards say two tankers struck mines in the "
        "Strait of Hormuz. Brent crude settles at $96.57, up about 8% over "
        "three sessions.",
        body_font, 560, line_spacing=6)
    draw_tanker(draw, 622, lead_y + 6, 366, 300)

    draw.line([(margin, 516), (WIDTH - margin, 516)], fill=INK, width=2)

    # --- Four stories in a 2 x 2 grid ----------------------------------
    grid_top = 534
    card_w = (content_w - 24) // 2
    card_h = 204
    gap = 24

    draw_card(
        draw, margin, grid_top, card_w, card_h,
        "KUWAIT  —  26 NOV",
        "Drone strike kills two Italian technicians",
        "A drone attack on 26 Nov hit a Kuwaiti air-defence site, killing "
        "two Italian technicians. Italy says the drones were of Iranian "
        "origin; Iran denies responsibility.",
        "drone")

    draw_card(
        draw, margin + card_w + gap, grid_top, card_w, card_h,
        "BRUSSELS  —  EU SUMMIT",
        "Summit ends early with no deal on Ukraine loan",
        "The special EU summit in Brussels ended early on 27 Nov with no "
        "decision on a \u20ac45 billion Ukraine loan, pushed to December. "
        "The 2028\u20132034 EU budget also unresolved.",
        "eu")

    draw_card(
        draw, margin, grid_top + card_h + gap, card_w, card_h,
        "UKRAINE  —  MISSILES",
        "North Korea halts missile deliveries to Russia",
        "Ukrainian intelligence says North Korea has suspended KN-23 "
        "missile deliveries to Russia.",
        "missile")

    draw_card(
        draw, margin + card_w + gap, grid_top + card_h + gap, card_w, card_h,
        "LONDON  —  READINESS",
        "UK contacts 100,000 retired troops",
        "The UK government is contacting 100,000 retired military "
        "personnel over military readiness, for the first time since the "
        "Cold War.",
        "helmet")

    # --- Footer ---------------------------------------------------------
    foot_font = font(SANS, 13)
    foot = "Five stories from Friday, 27 November 2026  \u00b7  THE WORLD TODAY"
    foot_w = draw.textlength(foot, font=foot_font)
    draw.text(((WIDTH - foot_w) / 2, 986), foot, font=foot_font, fill=GREY)

    return img


def save_entry(output_dir):
    """Render the page and write entry.png into output_dir."""
    os.makedirs(output_dir, exist_ok=True)
    img = draw_entry()
    path = os.path.join(output_dir, "entry.png")
    img.save(path, format="PNG")
    return path
