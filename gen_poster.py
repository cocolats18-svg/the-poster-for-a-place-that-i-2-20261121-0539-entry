#!/usr/bin/env python3
"""Draw the LUMARIS travel poster (1024x1024 PNG) for the make.fun bounty.

LUMARIS is an invented place: a dusk bay whose lagoon glows turquoise, a
striped lighthouse on the right cliff sweeping its beam across the sunset,
white cliff-houses on the left headland, lantern-lit sailboats, and the
name set large in the sky.

Deterministic: every coordinate, colour and random draw is fixed or seeded,
so repeated runs produce identical bytes. Pillow only, no network.
Run:  python3 gen_poster.py   -> writes entry.png beside this file.
"""
import random

from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

CREAM = (255, 243, 210)
NIGHT = (18, 22, 48)
CORAL = (216, 98, 68)


def blend(c1, c2, t):
    """Linear blend between two RGB triples."""
    return tuple(round(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def band(d, top, bottom, c_top, c_bottom):
    """Fill horizontal band [top, bottom) with a vertical gradient."""
    span = max(1, bottom - top - 1)
    for y in range(top, bottom):
        d.line([(0, y), (SIZE, y)], fill=blend(c_top, c_bottom, (y - top) / span))


def centred(d, cx, y, text, font, fill, tracking=0):
    """Draw text centred on cx; tracking adds extra space between letters."""
    if tracking:
        widths = [d.textlength(ch, font=font) for ch in text]
        total = sum(widths) + tracking * (len(text) - 1)
        x = cx - total / 2
        for ch, w in zip(text, widths):
            d.text((x, y), ch, font=font, fill=fill)
            x += w + tracking
        return
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)


def halo(d, cx, cy, radius, colour, alpha, steps=5):
    """Soft radial halo: concentric translucent discs, faintest outside."""
    for i in range(steps, 0, -1):
        r = radius * i / steps
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  fill=colour + (alpha // steps,))


def cliff_house(d, x, y, w, h):
    """One white cliff-house with a coral roof and a lit window."""
    d.rectangle([x, y, x + w, y + h], fill=(246, 238, 216))
    d.polygon([(x - 2, y), (x + w / 2, y - 10), (x + w + 2, y)],
              fill=CORAL)
    d.rectangle([x + w / 2 - 2, y + h / 2, x + w / 2 + 2, y + h / 2 + 6],
                fill=(255, 214, 110))


def sailboat(d, bx, by, scale, hull=NIGHT):
    """A small sailboat with cream sails and a glowing lantern."""
    s = scale
    d.polygon([(bx - 36 * s, by), (bx + 36 * s, by),
               (bx + 24 * s, by + 15 * s), (bx - 24 * s, by + 15 * s)], fill=hull)
    d.line([(bx, by), (bx, by - 54 * s)], fill=hull, width=max(2, int(3 * s)))
    d.polygon([(bx + 4, by - 52 * s), (bx + 4, by - 7 * s),
               (bx + 36 * s, by - 7 * s)], fill=CREAM)
    d.polygon([(bx - 4, by - 46 * s), (bx - 4, by - 7 * s),
               (bx - 28 * s, by - 7 * s)], fill=(244, 200, 158))
    halo(d, bx, by - 16 * s, 14 * s, (255, 214, 110), 90, steps=3)
    d.ellipse([bx - 5 * s, by - 21 * s, bx + 5 * s, by - 11 * s],
              fill=(255, 216, 112))


def main():
    img = Image.new("RGB", (SIZE, SIZE), NIGHT)
    d = ImageDraw.Draw(img, "RGBA")
    rng = random.Random(20261121)

    # -- Sky: deep indigo at the top, violet, then a coral sunset band. --
    band(d, 0, 320, (20, 24, 60), (72, 50, 102))
    band(d, 320, 510, (72, 50, 102), (236, 120, 80))
    band(d, 510, 556, (236, 120, 80), (255, 178, 112))

    # Stars in the upper sky only.
    for _ in range(150):
        x = rng.randint(24, SIZE - 24)
        y = rng.randint(26, 290)
        r = rng.choice([1, 1, 1, 2])
        a = rng.randint(90, 215)
        d.ellipse([x - r, y - r, x + r, y + r], fill=CREAM + (a,))

    # Low sun, just above the horizon, with a warm halo.
    sun_x, sun_y, sun_r = 512, 498, 90
    halo(d, sun_x, sun_y, 215, (255, 190, 110), 110)
    d.ellipse([sun_x - sun_r, sun_y - sun_r, sun_x + sun_r, sun_y + sun_r],
              fill=(255, 216, 142))

    # -- Sea: glowing turquoise at the horizon, deep teal below. --
    band(d, 556, SIZE, (66, 192, 180), (9, 50, 72))

    # Sun glint: a widening column of warm dashes down the water.
    for i in range(48):
        y = 564 + i * 9
        half = 24 + 135 * (i / 47)
        wobble = rng.uniform(-13, 13)
        fade = max(16, 148 - i * 3)
        d.line([(sun_x - half + wobble, y), (sun_x + half + wobble, y)],
               fill=(255, 206, 132, fade), width=3)

    # Turquoise shimmer streaks across the bay.
    for _ in range(95):
        x = rng.randint(60, SIZE - 60)
        y = rng.randint(578, 880)
        ln = rng.randint(18, 92)
        a = rng.randint(40, 128)
        d.line([(x, y), (x + ln, y)], fill=(142, 240, 220, a), width=2)

    # Distant headland silhouette across the bay.
    d.polygon([(0, 556), (140, 518), (290, 546), (430, 528), (560, 554),
               (700, 526), (860, 550), (SIZE, 530), (SIZE, 556), (0, 556)],
              fill=(36, 42, 84))

    # -- Left cliff with the white cliff-town. --
    d.polygon([(0, 556), (0, SIZE), (148, SIZE), (208, 762), (178, 638),
               (118, 578), (38, 556)], fill=(15, 19, 42))
    town = random.Random(11)
    for _ in range(15):
        hx = town.randint(38, 128)
        hy = town.randint(598, 782)
        hw = town.randint(16, 30)
        hh = town.randint(14, 24)
        cliff_house(d, hx, hy, hw, hh)

    # -- Right cliff and the lighthouse, the poster's landmark. --
    d.polygon([(SIZE, 556), (SIZE, SIZE), (878, SIZE), (828, 762),
               (858, 638), (918, 578), (988, 556)], fill=(15, 19, 42))
    lx = 906
    # Tapered tower, cream with two coral bands.
    d.polygon([(lx - 27, 640), (lx + 27, 640), (lx + 17, 468), (lx - 17, 468)],
              fill=(250, 240, 214))
    d.polygon([(lx - 24, 602), (lx + 24, 602), (lx + 22, 576), (lx - 22, 576)],
              fill=CORAL)
    d.polygon([(lx - 20, 542), (lx + 20, 542), (lx + 18, 516), (lx - 18, 516)],
              fill=CORAL)
    # Beam sweeping left across the dusk sky, then the lamp room.
    d.polygon([(lx - 9, 448), (lx + 9, 448), (252, 484), (252, 416)],
              fill=(255, 226, 140, 44))
    d.polygon([(lx - 9, 448), (lx + 9, 448), (252, 472), (252, 428)],
              fill=(255, 226, 140, 62))
    halo(d, lx, 450, 30, (255, 220, 130), 130)
    d.rectangle([lx - 25, 460, lx + 25, 472], fill=NIGHT)
    d.rectangle([lx - 16, 434, lx + 16, 460], fill=(255, 214, 110))
    d.polygon([(lx - 19, 434), (lx, 412), (lx + 19, 434)], fill=CORAL)
    d.ellipse([lx - 4, 404, lx + 4, 412], fill=(255, 214, 110))

    # -- Lantern sailboats on the glowing water. --
    sailboat(d, 326, 698, 1.0)
    sailboat(d, 644, 788, 0.72)

    # -- Pale sand crescent along the bottom. --
    d.polygon([(0, SIZE), (0, 928), (180, 904), (420, 916), (640, 898),
               (860, 914), (SIZE, 894), (SIZE, SIZE)], fill=(238, 214, 170))
    d.polygon([(0, SIZE), (0, 966), (300, 948), (620, 960), (SIZE, 944),
               (SIZE, SIZE)], fill=(224, 196, 150))
    for sx2, sy2 in [(706, 938), (764, 954), (296, 946)]:
        d.ellipse([sx2, sy2, sx2 + 8, sy2 + 6], fill=(255, 255, 255, 95))

    # -- Vintage double border. --
    d.rectangle([18, 18, SIZE - 19, SIZE - 19], outline=CREAM, width=3)
    d.rectangle([30, 30, SIZE - 31, SIZE - 31], outline=CREAM, width=1)

    # -- Type. --
    f_name = ImageFont.truetype(FONT_SERIF, 132)
    f_tag = ImageFont.truetype(FONT_SANS_BOLD, 34)
    f_foot = ImageFont.truetype(FONT_SANS, 25)

    # The name, cream on the dusk sky with a soft dark shadow.
    centred(d, 512 + 4, 96 + 5, "LUMARIS", f_name, (15, 19, 42, 165), tracking=10)
    centred(d, 512, 96, "LUMARIS", f_name, CREAM, tracking=10)

    # Subtitle with flanking rules and a centre dot.
    rule_y = 258
    d.line([(212, rule_y), (392, rule_y)], fill=CREAM, width=2)
    d.line([(632, rule_y), (812, rule_y)], fill=CREAM, width=2)
    d.ellipse([506, rule_y - 4, 518, rule_y + 4], fill=CREAM)
    centred(d, 512, 268, "THE GLOWING SHORE", f_tag, CREAM, tracking=8)

    # Bottom line, dark ink on the sand.
    centred(d, 512, 952, "WHERE THE SEA LIGHTS THE NIGHT", f_foot,
            NIGHT, tracking=4)

    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()
