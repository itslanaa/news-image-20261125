#!/usr/bin/env python3
"""Render the front page for Wednesday 25 November 2026.

Fresh renderer, written for this entry only. DejaVu fonts with a
resilient fallback chain; no network; deterministic output.
Usage: python3 draw_frontpage.py [output-path]
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 234)
INK = (20, 20, 20)
NAVY = (15, 42, 68)
NAVY_LT = (27, 68, 104)
RED = (180, 35, 24)
TEAL = (14, 107, 107)
GOLD = (176, 120, 20)
GREY = (90, 90, 90)
CARD = (255, 255, 255)
LINE = (200, 192, 175)
MAP_BG = (226, 236, 242)
LAND = (168, 188, 205)

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/TTF",
    "/usr/share/fonts",
]


def load_font(name, size):
    for d in FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()


def bold(size):
    return load_font("DejaVuSans-Bold.ttf", size)


def regular(size):
    return load_font("DejaVuSans.ttf", size)


def serif_bold(size):
    return load_font("DejaVuSerif-Bold.ttf", size)


def wrap(draw, text, font, max_w):
    """Greedy word wrap by pixel width; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, text, font, x, y, max_w, max_lines, lh, fill=INK):
    lines = wrap(draw, text, font, max_w)[:max_lines]
    if len(wrap(draw, text, font, max_w)) > max_lines and lines:
        last = lines[-1]
        while draw.textlength(last + "...", font=font) > max_w and len(last) > 3:
            last = last[:-1]
        lines[-1] = last + "..."
    for i, ln in enumerate(lines):
        draw.text((x, y + i * lh), ln, font=font, fill=fill)
    return y + len(lines) * lh


def draw_mixed(draw, head, body, x, y, max_w, max_lines, lh):
    """Bold head + regular body flowing as one wrapped paragraph."""
    bf, rf = bold(11), regular(11)
    tokens = [(t, bf) for t in head.split()] + [(t, rf) for t in body.split()]
    lines, cur, cur_w = [], [], 0
    space = draw.textlength(" ", font=rf)
    for tok, f in tokens:
        tw = draw.textlength(tok, font=f)
        add = tw if not cur else tw + space
        if cur_w + add <= max_w or not cur:
            cur.append((tok, f))
            cur_w += add
        else:
            lines.append(cur)
            cur, cur_w = [(tok, f)], tw
    if cur:
        lines.append(cur)
    shown = lines[:max_lines]
    if len(lines) > max_lines and shown:
        shown[-1] = shown[-1][:-1] + [("...", rf)] if len(shown[-1]) > 1 else shown[-1]
    for i, ln in enumerate(shown):
        cx = x
        for j, (tok, f) in enumerate(ln):
            draw.text((cx, y + i * lh), tok, font=f, fill=INK)
            cx += draw.textlength(tok, font=f) + (space if j < len(ln) - 1 else 0)
    return y + len(shown) * lh


# ---------------------------------------------------------------- leads art
def art_toll(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(24, 32, 44))
    bars = [38, 55, 48, 72, 66, 92, 118]
    bw = w // 9
    for i, v in enumerate(bars):
        bx = x + 14 + i * bw
        bh = int(v / 118.0 * (h - 34))
        draw.rectangle([bx, y + h - 12 - bh, bx + bw - 8, y + h - 12],
                       fill=RED if i == len(bars) - 1 else (120, 140, 165))
    draw.text((x + 14, y + 8), "RUSSIAN WAR DEAD SINCE 2022", font=bold(12),
              fill=(255, 255, 255))
    draw.text((x + 14, y + 26), "720,000", font=bold(30), fill=(255, 120, 100))


def art_tower(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(30, 46, 66))
    for i, (bx, bw, bh) in enumerate([(20, 34, 70), (62, 26, 88), (96, 44, 118),
                                      (148, 30, 80), (186, 38, 96), (232, 28, 62)]):
        draw.rectangle([x + bx, y + h - bh, x + bx + bw, y + h], fill=(90, 110, 135))
        for wy in range(y + h - bh + 8, y + h - 6, 12):
            draw.rectangle([x + bx + 5, wy, x + bx + bw - 5, wy + 4],
                           fill=(240, 200, 90))
    cx, cy = x + 118, y + 30
    for ang in range(0, 360, 45):
        import math
        ex = cx + int(24 * math.cos(math.radians(ang)))
        ey = cy + int(24 * math.sin(math.radians(ang)))
        draw.line([cx, cy, ex, ey], fill=(255, 120, 60), width=3)
    draw.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(255, 90, 40))
    draw.rectangle([x, y + h - 22, x + w, y + h], fill=(15, 42, 68))
    draw.text((x + 14, y + h - 19), "PIF TOWER, RIYADH", font=bold(12),
              fill=(255, 255, 255))


def art_market(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(240, 238, 228))
    pts = [(14, 26), (52, 40), (92, 18), (132, 52), (172, 44), (212, 78),
           (252, 66), (288, 104)]
    pts = [(x + px, y + py) for px, py in pts]
    draw.line(pts, fill=RED, width=5, joint="curve")
    draw.line([(x + 14, y + 26), (x + 52, y + 40)], fill=TEAL, width=3)
    draw.text((x + 14, y + 8), "+31.5% MONDAY", font=bold(12), fill=TEAL)
    draw.text((x + 170, y + 8), "-6% TUESDAY", font=bold(12), fill=RED)
    draw.text((x + 14, y + h - 26), "NASDAQ -1.5%  •  DOW 50,000+", font=bold(12),
              fill=INK)


LEADS = [
    ("UKRAINE WAR  •  THE TOLL", "720,000 RUSSIAN DEAD",
     "Leaked official data put Russian war dead past 720,000 — one every "
     "four minutes since 2022.", art_toll),
    ("YEMEN  •  SAUDI ARABIA", "RIYADH TOWER HIT AGAIN",
     "A Houthi strike on the PIF tower wounds 11. The Saudi coalition orders "
     "Hodeidah port evacuated.", art_tower),
    ("MARKETS  •  AI", "NVIDIA RALLY FADES",
     "Shares fall 6% a day after a 31.5% surge on Huang's return. Nasdaq "
     "drops 1.5%; Dow tops 50,000.", art_market),
]

STATS = [
    ("720,000", "Russian soldiers killed since 2022, leaked data show"),
    ("11", "wounded in the Riyadh tower strike"),
    ("96", "Russian drones fired overnight — 73 shot down"),
    ("$8.7bn", "EU's largest-ever single payment to Ukraine"),
    ("50", "Boeing 737-8 jets ordered by Xiamen Airlines"),
]

REGIONS = [
    ("EUROPE", NAVY, [
        ("Gulf ship hit — ", "Zelensky confirms Ukraine struck a Russian ship in the Gulf of Finland."),
        ("Putin warns — ", "retaliation 'inevitable' as Ukraine keeps hitting Russian oil plants."),
        ("NATO watch — ", "AWACS early-warning planes to deploy in Poland after missile landings."),
        ("Sarkozy trial — ", "ex-president and wife Carla Bruni to stand trial over Libya funds."),
        ("EU sanctions — ", "bloc targets ~50 Russian banks; Kallas slams Putin's 'maximalist' demands."),
        ("Sweden vote — ", "parliament to vote on Kristersson staying PM after election gridlock."),
    ]),
    ("MIDDLE EAST", RED, [
        ("Hormuz squeeze — ", "oil traffic down 40% as Iran steps up tanker attacks; 3 tankers hit mines."),
        ("Gaza strikes — ", "Israeli strikes kill 9, including Hamas security chief Naim Abu Nahal."),
        ("US warning — ", "Americans in the Middle East told to stay vigilant over Houthi, Iran threats."),
        ("Hodeidah alert — ", "Saudi coalition orders port evacuated; Houthis threaten Saudi ports."),
        ("Iraq oil grab — ", "Baghdad orders federal forces to seize Kurdish-held oilfields."),
        ("Iran's bill — ", "Tehran seeks $290bn in US damages; rial slides past 2.8m to the dollar."),
    ]),
    ("ASIA-PACIFIC", TEAL, [
        ("Sea code stalls — ", "ASEAN and China fail to agree a South China Sea code of conduct."),
        ("Shenzhou-24 — ", "China unveils crew for Tiangong station, including first foreign astronaut."),
        ("Nepal quake — ", "5.3-magnitude tremor shakes Nepal; felt in India and China."),
        ("Punjab pact — ", "BJP and Akali Dal reunite for 2027 polls after six years apart."),
        ("Nepal in Delhi — ", "PM Balendra Shah ends first state visit to India (22–23 Nov)."),
        ("Pacific pact — ", "Philippines and Australia sign updated defence deal amid China pressure."),
    ]),
    ("AFRICA", GOLD, [
        ("Benghazi sinking — ", "Ukraine sank a Russian warship in Libya's Benghazi harbour."),
        ("Congo pullback — ", "rebel group withdraws from areas of DR Congo after clashes."),
        ("AFCON restored — ", "Senegal gets its 2025 title back after a CAS ruling."),
        ("Emir suspended — ", "Nigerian emir suspended after sexual-assault allegation."),
        ("Norway trial — ", "Cameroon separatist leader faces war-crimes charges in Norway."),
    ]),
    ("AMERICAS", NAVY_LT, [
        ("Iran war funds — ", "Trump: war 'funded' through January; warns Democrats not to end it."),
        ("'Not corrupt' — ", "Trump denies corruption, points at 'real grift' in Minnesota and states."),
        ("Death Row row — ", "Trump condemns Newsom's commutation of hundreds of death sentences."),
        ("Abrego flies — ", "Salvadoran migrant Abrego Garcia to fly to Europe on Tuesday."),
        ("Fort Hood plea — ", "shooter Hasan seeks a stay of execution set for next week."),
    ]),
    ("BUSINESS, SPORT & SCIENCE", (90, 60, 110), [
        ("Dell lifts outlook — ", "raises revenue and profit forecasts a third time on AI demand."),
        ("$41bn pharma deal — ", "Sanofi to buy US biotech Insmed in a $41bn takeover."),
        ("Madrid rout — ", "Real Madrid beat PSV 5–1; Bellingham stunner, Mbappe brace."),
        ("England level — ", "England beat Australia by 8 wickets in the 2nd T20I."),
        ("Asteroid eclipse — ", "a spacecraft catches one asteroid's shadow falling on another."),
    ]),
]

MAP_DOTS = [
    # (name, fx, fy, label dx, label dy) — offsets stagger labels so none collide.
    ("Kyiv", 0.56, 0.30, 6, -14), ("Warsaw", 0.525, 0.20, -52, -14),
    ("Benghazi", 0.545, 0.58, 6, 6), ("Riyadh", 0.60, 0.48, 6, -14),
    ("Hormuz", 0.635, 0.42, 6, 6), ("Delhi", 0.70, 0.40, 6, -14),
    ("Beijing", 0.80, 0.28, 6, -14),
]


def draw_map(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=MAP_BG, outline=LINE)
    draw.text((x + 10, y + 6), "WHERE THE DAY HAPPENED — MAP IS SCHEMATIC",
              font=bold(11), fill=NAVY)
    # Stylised landmasses (rough continents, not cartography).
    blobs = [
        [(0.03, 0.30), (0.10, 0.22), (0.20, 0.24), (0.24, 0.38), (0.18, 0.55),
         (0.10, 0.58), (0.04, 0.45)],
        [(0.22, 0.60), (0.28, 0.58), (0.30, 0.72), (0.26, 0.86), (0.22, 0.74)],
        [(0.46, 0.22), (0.55, 0.18), (0.62, 0.26), (0.60, 0.38), (0.50, 0.40),
         (0.45, 0.30)],
        [(0.48, 0.44), (0.56, 0.42), (0.60, 0.56), (0.56, 0.72), (0.50, 0.62)],
        [(0.62, 0.24), (0.74, 0.18), (0.88, 0.22), (0.92, 0.38), (0.84, 0.52),
         (0.72, 0.50), (0.64, 0.38)],
        [(0.84, 0.66), (0.90, 0.64), (0.92, 0.74), (0.86, 0.78), (0.83, 0.72)],
    ]
    for b in blobs:
        pts = [(x + fx * w, y + 12 + fy * (h - 14)) for fx, fy in b]
        draw.polygon(pts, fill=LAND)
    for name, fx, fy, ldx, ldy in MAP_DOTS:
        dx, dy = x + fx * w, y + 12 + fy * (h - 14)
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=RED,
                     outline=(255, 255, 255))
        lx, ly = dx + ldx, dy + ldy
        for ox, oy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            draw.text((lx + ox, ly + oy), name, font=bold(10), fill=MAP_BG)
        draw.text((lx, ly), name, font=bold(10), fill=INK)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead.
    d.rectangle([0, 0, W, 100], fill=NAVY)
    d.text((24, 14), "THE WORLD IN ONE DAY", font=serif_bold(44), fill=(255, 255, 255))
    d.text((24, 66), "WEDNESDAY 25 NOVEMBER 2026  •  ONE DAY, ONE IMAGE  •  36 STORIES",
           font=bold(15), fill=(240, 200, 90))
    d.text((W - 24 - d.textlength("No. 25-11-25", font=bold(13)), 66),
           "No. 25-11-25", font=bold(13), fill=(180, 200, 220))

    # Three leads.
    for i, (kicker, head, summ, art) in enumerate(LEADS):
        lx = 24 + i * 328
        lw = 320
        d.rectangle([lx, 112, lx + lw, 400], fill=CARD, outline=LINE, width=1)
        art(d, lx, 112, lw, 118)
        d.text((lx + 12, 238), kicker, font=bold(11), fill=RED)
        draw_wrapped(d, head, bold(23), lx + 12, 256, lw - 24, 2, 27)
        draw_wrapped(d, summ, regular(13), lx + 12, 316, lw - 24, 3, 17)

    # Stats bar.
    sw, gap = 187, 11
    for i, (num, lab) in enumerate(STATS):
        sx = 24 + i * (sw + gap)
        wbox = sw + (1 if i == 4 else 0)
        d.rectangle([sx, 410, sx + wbox, 478], fill=(255, 255, 255), outline=LINE)
        d.text((sx + 10, 416), num, font=bold(24), fill=NAVY)
        draw_wrapped(d, lab, regular(10), sx + 10, 444, wbox - 20, 2, 12)

    # Six regions, 3 x 2.
    for i, (name, colour, stories) in enumerate(REGIONS):
        col, row = i % 3, i // 3
        rx, ry = 24 + col * 328, 484 + row * 220
        rw, rh = 320, 208
        d.rectangle([rx, ry, rx + rw, ry + rh], fill=CARD, outline=LINE)
        d.rectangle([rx, ry, rx + rw, ry + 30], fill=colour)
        d.text((rx + 10, ry + 7), name, font=bold(14), fill=(255, 255, 255))
        yy = ry + 38
        for head, body in stories:
            yy = draw_mixed(d, head, body, rx + 10, yy, rw - 20, 2, 14)
            yy += 2

    # Map strip + footer.
    draw_map(d, 24, 920, 976, 72)
    d.text((24, 998),
           "Sources: Reuters, CNN, AP, Al Jazeera, RFE/RL — reporting from 25 November 2026. "
           "All figures as reported that day.",
           font=regular(11), fill=GREY)

    img.save(out, "PNG", optimize=True)
    print(out, img.size, os.path.getsize(out))


if __name__ == "__main__":
    main()
