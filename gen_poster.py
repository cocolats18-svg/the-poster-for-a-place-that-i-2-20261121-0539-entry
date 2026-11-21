#!/usr/bin/env python3
"""Generate the travel poster for LUMARIS, a place that isn't there.

Deterministic: fixed palette, fixed geometry, fixed seeded stars.
Writes entry.png (1024x1024) next to this script. Pillow only, no network.
"""
import random
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

CREAM = (255, 244, 214)
INK = (24, 28, 54)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vgrad(draw, y0, y1, c0, c1):
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        draw.line([(0, y), (W, y)], fill=lerp(c0, c1, t))


def text_center(draw, cx, y, s, font, fill, spacing=0):
    if spacing:
        widths = [draw.textlength(ch, font=font) for ch in s]
        total = sum(widths) + spacing * (len(s) - 1)
        x = cx - total / 2
        for ch, w in zip(s, widths):
            draw.text((x, y), ch, font=font, fill=fill)
            x += w + spacing
        return total
    w = draw.textlength(s, font=font)
    draw.text((cx - w / 2, y), s, font=font, fill=fill)
    return w


def main():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img, "RGBA")

    # ---- sky: indigo dusk -> violet -> coral band at the horizon ----
    vgrad(d, 0, 330, (22, 26, 62), (74, 52, 104))
    vgrad(d, 330, 520, (74, 52, 104), (238, 122, 82))
    vgrad(d, 520, 560, (238, 122, 82), (255, 176, 110))

    # ---- stars, upper sky only (seeded, deterministic) ----
    rng = random.Random(20261121)
    for _ in range(140):
        x = rng.randint(20, W - 20)
        y = rng.randint(24, 300)
        r = rng.choice([1, 1, 1, 2])
        a = rng.randint(90, 220)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 244, 214, a))

    # ---- low sun, big and warm, just above the horizon ----
    sx, sy, sr = 512, 500, 92
    for r, a in [(210, 26), (170, 40), (135, 60)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 190, 110, a))
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 214, 140))

    # ---- sea: glowing turquoise at the horizon, deep teal below ----
    vgrad(d, 560, 1024, (64, 190, 178), (10, 52, 74))

    # sun reflection column on the water
    for i in range(46):
        y = 566 + i * 9
        half = 26 + 130 * (i / 45) * rng.uniform(0.55, 1.0) if False else 26 + 130 * (i / 45)
        wob = rng.uniform(-14, 14)
        d.line([(sx - half + wob, y), (sx + half + wob, y)],
               fill=(255, 205, 130, max(18, 150 - i * 3)), width=3)

    # glow shimmer streaks across the bay
    for _ in range(90):
        x = rng.randint(60, W - 60)
        y = rng.randint(580, 880)
        ln = rng.randint(18, 90)
        a = rng.randint(40, 130)
        d.line([(x, y), (x + ln, y)], fill=(140, 240, 220, a), width=2)

    # ---- distant headland silhouette across the bay ----
    d.polygon([(0, 560), (150, 520), (300, 548), (430, 530), (560, 556),
               (700, 528), (860, 552), (1024, 532), (1024, 560), (0, 560)],
              fill=(38, 44, 86))

    # ---- left cliff with a white cliff-town ----
    d.polygon([(0, 560), (0, 1024), (150, 1024), (210, 760), (180, 640),
               (120, 580), (40, 560)], fill=(16, 20, 44))
    # little white houses stacked on the cliff
    rng2 = random.Random(7)
    for _ in range(14):
        hx = rng2.randint(8, 120)
        hy = rng2.randint(600, 780)
        hw, hh = rng2.randint(16, 30), rng2.randint(14, 24)
        d.rectangle([hx, hy, hx + hw, hy + hh], fill=(244, 236, 214))
        d.polygon([(hx, hy), (hx + hw / 2, hy - 9), (hx + hw, hy)],
                  fill=(214, 96, 66))
        d.rectangle([hx + hw / 2 - 2, hy + hh / 2, hx + hw / 2 + 2, hy + hh / 2 + 5],
                    fill=(255, 214, 110))

    # ---- right cliff with the lighthouse (the landmark) ----
    d.polygon([(1024, 560), (1024, 1024), (880, 1024), (830, 760), (860, 640),
               (920, 580), (990, 560)], fill=(16, 20, 44))
    # lighthouse tower, slightly tapered, cream with coral bands
    lx = 905
    d.polygon([(lx - 26, 640), (lx + 26, 640), (lx + 16, 470), (lx - 16, 470)],
              fill=(250, 240, 214))
    d.polygon([(lx - 23, 600), (lx + 23, 600), (lx + 21, 575), (lx - 21, 575)],
              fill=(214, 96, 66))
    d.polygon([(lx - 19, 540), (lx + 19, 540), (lx + 17, 515), (lx - 17, 515)],
              fill=(214, 96, 66))
    # gallery + lamp room + dome
    d.rectangle([lx - 24, 462, lx + 24, 472], fill=(24, 28, 54))
    d.rectangle([lx - 15, 436, lx + 15, 462], fill=(255, 214, 110))
    d.polygon([(lx - 18, 436), (lx, 414), (lx + 18, 436)], fill=(214, 96, 66))
    d.ellipse([lx - 4, 406, lx + 4, 414], fill=(255, 214, 110))
    # light beam fanning left across the dusk sky
    d.polygon([(lx - 8, 446), (lx + 8, 446), (260, 492), (260, 408)],
              fill=(255, 226, 140, 46))
    d.polygon([(lx - 8, 446), (lx + 8, 446), (260, 478), (260, 424)],
              fill=(255, 226, 140, 64))
    # lamp glow
    d.ellipse([lx - 26, 424, lx + 26, 476], fill=(255, 220, 130, 60))

    # ---- two sailboats with lanterns on the glowing water ----
    def boat(bx, by, s, hull=(24, 28, 54)):
        d.polygon([(bx - 34 * s, by), (bx + 34 * s, by), (bx + 22 * s, by + 14 * s),
                   (bx - 22 * s, by + 14 * s)], fill=hull)
        d.line([(bx, by), (bx, by - 52 * s)], fill=hull, width=max(2, int(3 * s)))
        d.polygon([(bx + 3, by - 50 * s), (bx + 3, by - 6 * s), (bx + 34 * s, by - 6 * s)],
                  fill=(255, 244, 214))
        d.polygon([(bx - 3, by - 44 * s), (bx - 3, by - 6 * s), (bx - 26 * s, by - 6 * s)],
                  fill=(244, 200, 160))
        d.ellipse([bx - 5, by - 20 * s, bx + 5, by - 10 * s], fill=(255, 214, 110))
        d.ellipse([bx - 9, by - 24 * s, bx + 9, by - 6 * s], fill=(255, 214, 110, 50))

    boat(330, 700, 1.0)
    boat(640, 790, 0.72)

    # ---- pale sand crescent, bottom foreground ----
    d.polygon([(0, 1024), (0, 930), (180, 905), (420, 918), (640, 900),
               (860, 916), (1024, 896), (1024, 1024)], fill=(238, 214, 170))
    d.polygon([(0, 1024), (0, 968), (300, 950), (620, 962), (1024, 946), (1024, 1024)],
              fill=(224, 196, 150))
    # a few small shells and footprints on the sand
    for sx2, sy2 in [(700, 940), (760, 956), (300, 948)]:
        d.ellipse([sx2, sy2, sx2 + 8, sy2 + 6], fill=(255, 255, 255, 90))

    # ---- vintage double border ----
    d.rectangle([18, 18, W - 19, H - 19], outline=CREAM, width=3)
    d.rectangle([30, 30, W - 31, H - 31], outline=CREAM, width=1)

    # ---- type ----
    f_name = ImageFont.truetype(SERIF_B, 132)
    f_sub = ImageFont.truetype(SANS_B, 34)
    f_bot = ImageFont.truetype(SANS, 25)

    # soft shadow, then the name in cream
    for dx, dy in [(4, 5)]:
        text_center(d, 512 + dx, 96 + dy, "LUMARIS", f_name, (16, 20, 44, 160), spacing=10)
    text_center(d, 512, 96, "LUMARIS", f_name, CREAM, spacing=10)

    # rule lines flanking the subtitle
    y_rule = 258
    d.line([(212, y_rule), (392, y_rule)], fill=CREAM, width=2)
    d.line([(632, y_rule), (812, y_rule)], fill=CREAM, width=2)
    d.ellipse([506, y_rule - 4, 518, y_rule + 4], fill=CREAM)
    text_center(d, 512, 268, "THE GLOWING SHORE", f_sub, CREAM, spacing=8)

    # bottom line on the sand, dark ink
    text_center(d, 512, 952, "WHERE THE SEA LIGHTS THE NIGHT", f_bot, INK, spacing=4)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
