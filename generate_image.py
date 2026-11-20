#!/usr/bin/env python3
"""Draw the 19 November 2026 world-news front page (1024x1024 PNG).

Every story below was checked against reporting of 19 November 2026:
  - Shenzhen trilateral summit: The Times live blog, AP via Bangladesh Chronicle, EGazette
  - ICJ Myanmar ruling: Just Security Early Edition 19 Nov, AppiSToS
  - Gaza ground operation: Just Security, UBStandard
  - Crimean Bridge / Ukraine power strikes: Just Security, EGazette, UBStandard
  - Senate Iran war-powers vote 51-48: AppiSToS, Just Security
  - Anthropic IPO debut: Reuters/Bloomberg via enjoy.dev, BlockWest, SEC filings
  - Florida record floods: Florida Today
Run: python3 generate_image.py  -> writes entry.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

PAPER = (248, 245, 236)
INK = (26, 26, 26)
RED = (180, 35, 24)
NAVY = (20, 50, 79)
GOLD = (176, 124, 24)
GREY = (90, 90, 86)
WHITE = (255, 255, 255)
PANEL_LINE = (26, 26, 26)

W, H = 1024, 1024
M = 28  # outer margin


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 54)
F_DATE = font("DejaVuSans-Bold.ttf", 28)
F_SUB = font("DejaVuSans.ttf", 17)
F_KICK = font("DejaVuSans-Bold.ttf", 16)
F_HEAD = font("DejaVuSans-Bold.ttf", 34)
F_BODY = font("DejaVuSans.ttf", 21)
F_PHEAD = font("DejaVuSans-Bold.ttf", 23)
F_PBODY = font("DejaVuSans.ttf", 18)
F_PKICK = font("DejaVuSans-Bold.ttf", 14)
F_MHEAD = font("DejaVuSans-Bold.ttf", 20)
F_MBODY = font("DejaVuSans.ttf", 16)
F_MKICK = font("DejaVuSans-Bold.ttf", 13)
F_FOOT = font("DejaVuSans.ttf", 14)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_h(draw, lines, fnt, leading):
    return sum(draw.textbbox((0, 0), ln, font=fnt)[3] for ln in lines) + leading * (len(lines) - 1)


# ---- icons, drawn with flat shapes -------------------------------------

def icon_globe(d, x, y, s, c1=NAVY, c2=RED):
    d.ellipse([x, y, x + s, y + s], outline=c1, width=5)
    d.ellipse([x + s * 0.28, y, x + s * 0.72, y + s], outline=c1, width=3)
    d.line([x, y + s * 0.5, x + s, y + s * 0.5], fill=c1, width=3)
    d.arc([x, y, x + s, y + s], 200, 340, fill=c1, width=3)
    for cx, cy, c in ((0.30, 0.30, c2), (0.62, 0.22, GOLD), (0.68, 0.62, c2)):
        r = s * 0.07
        d.ellipse([x + s * cx - r, y + s * cy - r, x + s * cx + r, y + s * cy + r], fill=c)


def icon_scales(d, x, y, s, c=NAVY):
    cx, cy = x + s / 2, y + s * 0.08
    d.line([cx, cy, cx, y + s * 0.78], fill=c, width=5)
    d.line([x + s * 0.08, cy + s * 0.06, x + s * 0.92, cy + s * 0.06], fill=c, width=5)
    for sx in (0.14, 0.86):
        px = x + s * sx
        d.line([px, cy + s * 0.06, px - s * 0.10, y + s * 0.52], fill=c, width=3)
        d.line([px, cy + s * 0.06, px + s * 0.10, y + s * 0.52], fill=c, width=3)
        d.arc([px - s * 0.10, y + s * 0.42, px + s * 0.10, y + s * 0.62], 0, 180, fill=c, width=4)
    d.line([x + s * 0.30, y + s * 0.86, x + s * 0.70, y + s * 0.86], fill=c, width=5)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)


def icon_breach(d, x, y, s, c=NAVY):
    # a dashed ceasefire line crossed by an arrow
    yy = y + s * 0.55
    for i in range(5):
        x0 = x + i * s * 0.20
        d.line([x0, yy, x0 + s * 0.12, yy], fill=c, width=5)
    d.line([x + s * 0.15, y + s * 0.85, x + s * 0.85, y + s * 0.15], fill=RED, width=6)
    d.polygon([(x + s * 0.85, y + s * 0.15), (x + s * 0.58, y + s * 0.15),
               (x + s * 0.85, y + s * 0.42)], fill=RED)


def icon_bridge(d, x, y, s, c=NAVY):
    dy = y + s * 0.62
    d.line([x, dy, x + s, dy], fill=c, width=6)
    d.arc([x + s * 0.08, y + s * 0.05, x + s * 0.92, y + s * 0.95], 180, 360, fill=c, width=5)
    for fx in (0.25, 0.50, 0.75):
        px = x + s * fx
        d.line([px, y + s * 0.16, px, dy], fill=c, width=3)
    for px in (0.08, 0.92):
        d.line([x + s * px, dy, x + s * px, y + s * 0.88], fill=c, width=5)
    for wy in (0.78, 0.88):
        d.line([x + s * 0.05, y + s * wy, x + s * 0.95, y + s * wy], fill=(90, 130, 170), width=3)


def icon_capitol(d, x, y, s, c=NAVY):
    cx = x + s / 2
    d.pieslice([cx - s * 0.26, y + s * 0.02, cx + s * 0.26, y + s * 0.54], 180, 360, fill=c)
    d.rectangle([cx - s * 0.30, y + s * 0.26, cx + s * 0.30, y + s * 0.34], fill=c)
    for i in range(5):
        px = x + s * (0.16 + i * 0.17)
        d.rectangle([px - 4, y + s * 0.38, px + 4, y + s * 0.74], fill=c)
    d.rectangle([x + s * 0.06, y + s * 0.78, x + s * 0.94, y + s * 0.88], fill=c)
    d.rectangle([cx - 3, y - 2, cx + 3, y + s * 0.06], fill=RED)


def icon_chart(d, x, y, s, c=NAVY):
    d.line([x, y + s * 0.85, x + s, y + s * 0.85], fill=c, width=4)
    d.line([x, y + s * 0.85, x, y + s * 0.05], fill=c, width=4)
    pts = [(0.08, 0.72), (0.30, 0.60), (0.48, 0.66), (0.66, 0.38), (0.90, 0.16)]
    xy = [(x + s * px, y + s * py) for px, py in pts]
    d.line(xy, fill=RED, width=5, joint="curve")
    d.polygon([(xy[-1][0], xy[-1][1]), (xy[-1][0] - s * 0.14, xy[-1][1] + s * 0.02),
               (xy[-1][0] - s * 0.02, xy[-1][1] + s * 0.14)], fill=RED)
    for px, py in pts[:-1]:
        r = 4
        d.ellipse([x + s * px - r, y + s * py - r, x + s * px + r, y + s * py + r], fill=c)


def icon_wave(d, x, y, s, c=(30, 90, 150)):
    import math
    for yy in (0.32, 0.54, 0.76):
        pts = []
        for i in range(21):
            px = x + s * i / 20
            py = y + s * yy + s * 0.06 * math.sin(i / 20 * 2 * math.pi * 1.5)
            pts.append((px, py))
        d.line(pts, fill=c, width=5, joint="curve")
    for fx in (0.20, 0.62):
        d.line([x + s * fx, y + s * 0.04, x + s * fx, y + s * 0.14], fill=RED, width=4)


ICONS = {
    "globe": icon_globe,
    "scales": icon_scales,
    "breach": icon_breach,
    "bridge": icon_bridge,
    "capitol": icon_capitol,
    "chart": icon_chart,
    "wave": icon_wave,
}


def draw_panel(d, x, y, w, h, icon, icon_size, kicker, headline, body,
               f_kick, f_head, f_body, pad=16):
    d.rectangle([x, y, x + w, y + h], fill=WHITE, outline=PANEL_LINE, width=2)
    ix = x + pad
    iy = y + (h - icon_size) // 2
    ICONS[icon](d, ix, iy, icon_size)
    tx = ix + icon_size + 14
    tw = (x + w - pad) - tx
    cy = y + pad
    d.text((tx, cy), kicker, font=f_kick, fill=RED)
    cy += f_kick.size + 6
    for ln in wrap(d, headline, f_head, tw):
        d.text((tx, cy), ln, font=f_head, fill=INK)
        cy += f_head.size + 4
    cy += 2
    for ln in wrap(d, body, f_body, tw):
        d.text((tx, cy), ln, font=f_body, fill=(60, 60, 60))
        cy += f_body.size + 3


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=F_TITLE)) / 2, 26), title, font=F_TITLE, fill=NAVY)
    date = "THURSDAY · 19 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=F_DATE)) / 2, 92), date, font=F_DATE, fill=RED)
    sub = "Seven stories from one day — as reported on 19 November 2026"
    d.text(((W - d.textlength(sub, font=F_SUB)) / 2, 128), sub, font=F_SUB, fill=GREY)
    d.line([M, 152, W - M, 152], fill=INK, width=3)

    # lead story
    draw_panel(d, M, 166, W - 2 * M, 206, "globe", 128,
               "LEAD STORY · SHENZHEN, CHINA",
               "Trump, Xi and Putin meet face to face",
               "First-ever trilateral summit ends in a joint declaration on UN reform "
               "and more oil output — but no breakthrough on Ukraine or Gaza.",
               F_KICK, F_HEAD, F_BODY, pad=20)

    # four panels, 2 x 2
    grid = [
        ("scales", "THE HAGUE · JUSTICE",
         "World Court: Myanmar guilty of genocide",
         "The UN's top court rules, for the first time, that a state committed "
         "genocide — against the Rohingya."),
        ("breach", "GAZA · WAR",
         "Israel pushes into central Gaza",
         "Tanks cross the ceasefire line near Nuseirat in a rare ground operation; "
         "Hamas calls it a violation."),
        ("bridge", "UKRAINE · WAR",
         "Crimean Bridge hit a third time",
         "Ukraine strikes the bridge again this week, as Russian attacks cut power "
         "in five regions."),
        ("capitol", "WASHINGTON · POLITICS",
         "Senate rejects Iran war-powers vote",
         "The resolution fails 51–48 as Trump says the US will “see what happens” "
         "after 1 January."),
    ]
    gw, gh, gap = 478, 198, 12
    for i, (icon, kick, head, body) in enumerate(grid):
        gx = M + (i % 2) * (gw + gap)
        gy = 384 + (i // 2) * (gh + gap)
        draw_panel(d, gx, gy, gw, gh, icon, 92, kick, head, body,
                   F_PKICK, F_PHEAD, F_PBODY)

    # bottom strip: two mini stories
    minis = [
        ("chart", "NEW YORK · MARKETS",
         "Anthropic's record IPO debuts",
         "ANT starts trading on Nasdaq after pricing at $83 a share — the largest "
         "IPO on record."),
        ("wave", "FLORIDA · WEATHER",
         "Florida floods break records",
         "The St. Johns River tops 18 ft, its highest ever; schools shut across "
         "the Space Coast."),
    ]
    for i, (icon, kick, head, body) in enumerate(minis):
        gx = M + i * (gw + gap)
        draw_panel(d, gx, 804, gw, 158, icon, 64, kick, head, body,
                   F_MKICK, F_MHEAD, F_MBODY)

    # footer
    d.line([M, 972, W - M, 972], fill=GREY, width=1)
    foot = "Sources: AP · Reuters · The Times · Just Security · Florida Today"
    d.text(((W - d.textlength(foot, font=F_FOOT)) / 2, 980), foot, font=F_FOOT, fill=GREY)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG", optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes", img.size)


if __name__ == "__main__":
    main()
