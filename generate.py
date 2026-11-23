#!/usr/bin/env python3
# news-image-20261123 — entry.png renderer.
#
# Hero story: PT Fonusa Agung Mulia confectionery factory fire, Cikande,
# Banten, Indonesia (Reuters, Mon 23 Nov 2026). 24 confirmed dead, ~30
# workers still missing, rescuers searching the burned wreckage.
#
# One hero subject, vertical drama (flame column + smoke + fire-truck
# spray), legible at thumbnail size. 960x960 PNG, DejaVu fonts, PIL only.
# Deterministic: fixed seed, so the output is byte-identical every run.
# The image is drawn, not photographed.
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))

# ~~~ configuration: every colour and size lives here, nothing is inline ~~~
CFG = {
    "canvas": 960,
    "seed": 20261123,
    "font_bold": "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "font_regular": "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "size_date": 46,
    "size_kicker": 20,
    "size_headline": 54,
    "size_sub": 23,
    "size_lead": 26,
    "size_body": 24,
    "size_footer": 18,
}

PALETTE = {
    "night": (7, 11, 22),
    "gold": (216, 178, 90),
    "white": (255, 255, 255),
    "asphalt": (16, 16, 20),
    "dash": (70, 70, 78),
    "wall": (24, 24, 30),
    "roof": (34, 34, 42),
    "window_fire": (255, 120, 20),
    "window_fire_top": (255, 190, 60),
    "office": (40, 42, 52),
    "office_lit": (255, 214, 130),
    "chimney": (52, 52, 60),
    "chimney_cap": (150, 60, 40),
    "smoke": (58, 58, 64),
    "flame_outer": (255, 88, 0),
    "flame_mid": (255, 165, 0),
    "flame_inner": (255, 216, 70),
    "flame_core": (255, 246, 180),
    "glow": (255, 110, 20),
    "ember": (255, 40),
    "truck_red": (198, 32, 28),
    "truck_dark": (178, 24, 22),
    "glass": (180, 220, 240),
    "panel": (220, 225, 230),
    "tyre": (12, 12, 14),
    "hub": (120, 120, 128),
    "ladder": (200, 200, 205),
    "spray": (190, 220, 240),
    "hi_vis": (255, 110, 20),
    "helmet": (255, 190, 60),
    "masthead": (7, 12, 24),
    "band": (10, 17, 32),
    "sub_text": (199, 210, 224),
    "story_body": (205, 214, 226),
    "rule": (90, 100, 118),
    "footer_text": (140, 150, 165),
}

W = H = CFG["canvas"]
GOLD = PALETTE["gold"]


# ~~~ text sections first: masthead, headline, briefs, footer ~~~

def paint_header(d):
    d.rectangle([0, 0, W, 92], fill=PALETTE["masthead"] + (255,))
    d.line([(0, 92), (W, 92)], fill=GOLD + (255,), width=3)
    f_date = ImageFont.truetype(CFG["font_bold"], CFG["size_date"])
    d.text((36, 22), "23 NOVEMBER 2026", font=f_date, fill=PALETTE["white"] + (255,))
    f_kick = ImageFont.truetype(CFG["font_bold"], CFG["size_kicker"])
    d.text((W - 36, 34), "WORLD NEWS IN ONE IMAGE", font=f_kick,
           fill=GOLD + (255,), anchor="ra")


def paint_headline_block(d):
    d.rectangle([0, 470, W, 604], fill=PALETTE["band"] + (255,))
    d.line([(0, 470), (W, 470)], fill=GOLD + (255,), width=2)
    f_head = ImageFont.truetype(CFG["font_bold"], CFG["size_headline"])
    d.text((36, 482), "FACTORY FIRE KILLS 24", font=f_head, fill=PALETTE["white"] + (255,))
    f_sub = ImageFont.truetype(CFG["font_regular"], CFG["size_sub"])
    d.text((36, 544), "Cikande candy plant ablaze — ~30 workers still missing", font=f_sub,
           fill=PALETTE["sub_text"] + (255,))
    d.text((36, 572), "Rescuers search the wreckage as hotspots smoulder on", font=f_sub,
           fill=PALETTE["sub_text"] + (255,))


def paint_briefs(d):
    labels = [
        ((200, 70, 60), "POLAND", "3 Russian Kh-101 missiles confirmed — NATO meets"),
        ((70, 130, 200), "COP31", "Climate talks collapse — no deal over fossil fuels"),
        ((210, 180, 40), "KYIV", "Boy, 7, pulled alive from rubble after Russian strike"),
        ((230, 120, 30), "LIBYA", "Blast on Russian ship at port — officials suspect drone attack"),
        ((46, 160, 90), "U.S.", "Democrats win largest House majority since 1992"),
        ((150, 90, 170), "MEXICO", "'El Chapo Isidro' captured — FBI most-wanted cartel boss"),
    ]
    f_lead = ImageFont.truetype(CFG["font_bold"], CFG["size_lead"])
    f_body = ImageFont.truetype(CFG["font_regular"], CFG["size_body"])
    y = 628
    for col, lead, body in labels:
        d.rectangle([36, y + 4, 52, y + 20], fill=col + (255,))
        d.text((66, y), lead, font=f_lead, fill=PALETTE["white"] + (255,))
        lw = d.textlength(lead, font=f_lead)
        d.text((66 + lw + 14, y + 1), body, font=f_body, fill=PALETTE["story_body"] + (255,))
        y += 49


def paint_colophon(d):
    d.line([(36, 928), (W - 36, 928)], fill=PALETTE["rule"] + (255,), width=1)
    f_foot = ImageFont.truetype(CFG["font_regular"], CFG["size_footer"])
    d.text((36, 938), "Sources: Reuters  •  AP", font=f_foot, fill=PALETTE["footer_text"] + (255,))
    d.text((W - 36, 938), "23 November 2026", font=f_foot, fill=PALETTE["footer_text"] + (255,), anchor="ra")


# ~~~ scene sections: sky, ground, shed, smoke, fire, truck, crew ~~~

def paint_night_sky(d):
    # gradient: deep navy up top, scorched-orange glow at the roofline
    for y in range(92, 372):
        t = (y - 92) / (372 - 92)
        d.line([(0, y), (W, y)], fill=(
            int(8 + 138 * t * t),
            int(12 + 52 * t * t),
            int(26 + 10 * t),
        ))
    # stars, kept out of the smoke column
    for _ in range(64):
        x = random.randint(10, W - 10)
        y = random.randint(100, 220)
        r = random.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r],
                  fill=(255, 255, 255, random.randint(80, 190)))
    # distant town glow, low on the horizon
    for _ in range(30):
        x = random.randint(20, W - 20)
        y = random.randint(330, 362)
        d.ellipse([x, y, x + 3, y + 2], fill=(255, 170, 60, random.randint(50, 120)))


def paint_asphalt(d):
    d.rectangle([0, 430, W, 470], fill=PALETTE["asphalt"] + (255,))
    for _ in range(40):
        x = random.randint(8, W - 40)
        d.line([(x, 452), (x + random.randint(12, 40), 452)],
               fill=PALETTE["dash"] + (90,), width=2)


def paint_shed(d):
    # main walls
    d.rectangle([60, 340, 700, 430], fill=PALETTE["wall"] + (255,))
    # sawtooth roofline
    roof = [(60, 340)]
    x = 60
    up = True
    while x < 700:
        x += 80
        roof.append((x, 312 if up else 340))
        up = not up
    roof.append((700, 340))
    d.polygon(roof, fill=PALETTE["roof"] + (255,))
    # glowing broken windows where the fire is inside
    for wx in (150, 210, 560, 620):
        d.rectangle([wx, 372, wx + 34, 402], fill=PALETTE["window_fire"] + (230,))
        d.rectangle([wx, 372, wx + 34, 382], fill=PALETTE["window_fire_top"] + (240,))
    # office block on the left, untouched, lit windows
    d.rectangle([60, 300, 190, 340], fill=PALETTE["office"] + (255,))
    for wy in (312, 326):
        for wx in (74, 104, 134, 164):
            d.rectangle([wx, wy, wx + 16, wy + 8], fill=PALETTE["office_lit"] + (220,))
    # chimney stack on the right end
    d.rectangle([668, 268, 692, 340], fill=PALETTE["chimney"] + (255,))
    d.rectangle([664, 260, 696, 270], fill=PALETTE["chimney_cap"] + (255,))


def _composite_blurred_layer(img, layer, radius):
    # paste a blurred RGBA layer over the canvas and hand back a fresh draw
    img.paste(Image.alpha_composite(img.convert("RGBA"),
                                    layer.filter(ImageFilter.GaussianBlur(radius))).convert("RGB"), (0, 0))
    return ImageDraw.Draw(img, "RGBA")


def paint_smoke_plume(img, d):
    smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(smoke)
    sx, sy = 430, 300
    for i in range(24):
        r = 32 + i * 9
        sd.ellipse([sx - r, sy - r, sx + r, sy + r], fill=PALETTE["smoke"] + (205,))
        sx -= 13
        sy -= 13
    return _composite_blurred_layer(img, smoke, 10)


def paint_fire(img, d):
    flame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    fd = ImageDraw.Draw(flame)

    def flame_tongue(x0, base, height, w, col):
        pts = [(x0, base),
               (x0 + w * 0.20, base - height * 0.55),
               (x0 + w * 0.45, base - height),
               (x0 + w * 0.65, base - height * 0.58),
               (x0 + w, base)]
        fd.polygon(pts, fill=col)

    # outer orange, then gold, then pale core — tallest tongue near the centre
    for x0, hgt, w in [(300, 150, 95), (355, 205, 115), (415, 175, 100), (470, 130, 75)]:
        flame_tongue(x0, 344, hgt, w, PALETTE["flame_outer"] + (235,))
    for x0, hgt, w in [(320, 120, 72), (370, 158, 88), (430, 130, 72)]:
        flame_tongue(x0, 344, hgt, w, PALETTE["flame_mid"] + (240,))
    for x0, hgt, w in [(345, 88, 52), (392, 108, 62), (435, 82, 46)]:
        flame_tongue(x0, 344, hgt, w, PALETTE["flame_inner"] + (245,))
    for x0, hgt, w in [(372, 58, 34), (408, 66, 38)]:
        flame_tongue(x0, 344, hgt, w, PALETTE["flame_core"] + (250,))
    return _composite_blurred_layer(img, flame, 1.2)


def paint_glow(img, d):
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for i in range(22):
        x0 = 330 + random.randint(-40, 140)
        y0 = 420 + random.randint(0, 42)
        gd.ellipse([x0, y0, x0 + random.randint(10, 30), y0 + random.randint(4, 10)],
                   fill=PALETTE["glow"] + (random.randint(50, 110),))
    return _composite_blurred_layer(img, glow, 4)


def paint_sparks(d):
    for _ in range(46):
        x = random.randint(310, 540)
        y = random.randint(130, 330)
        r = random.randint(1, 3)
        d.ellipse([x - r, y - r, x + r, y + r],
                  fill=(255, random.randint(140, 210), 40, 220))


def paint_engine(d):
    # cab + body
    d.rectangle([742, 408, 830, 452], fill=PALETTE["truck_red"] + (255,))
    d.rectangle([830, 398, 920, 452], fill=PALETTE["truck_dark"] + (255,))
    d.rectangle([752, 414, 788, 432], fill=PALETTE["glass"] + (255,))
    d.rectangle([838, 406, 912, 420], fill=PALETTE["panel"] + (255,))
    # wheels
    for wx in (768, 872):
        d.ellipse([wx - 14, 440, wx + 14, 466], fill=PALETTE["tyre"] + (255,))
        d.ellipse([wx - 6, 448, wx + 6, 460], fill=PALETTE["hub"] + (255,))
    # ladder rising toward the flames
    d.line([(850, 400), (700, 300)], fill=PALETTE["ladder"] + (255,), width=6)
    for i in range(6):
        t = i / 5
        lx = int(850 + (700 - 850) * t)
        ly = int(400 + (300 - 400) * t)
        d.line([(lx - 8, ly + 4), (lx + 8, ly - 4)], fill=PALETTE["ladder"] + (255,), width=2)
    # water spray arcing from the ladder tip toward the fire
    for _ in range(60):
        t = random.random()
        x = int(700 - t * 150 + random.randint(-14, 14))
        y = int(300 - 40 * t * (1 - t) * 4 + t * 44 + random.randint(-8, 8))
        d.ellipse([x, y, x + 3, y + 3], fill=PALETTE["spray"] + (random.randint(140, 220),))


def paint_crew(d):
    for rx in (120, 165, 215, 262):
        d.rectangle([rx, 436, rx + 12, 462], fill=PALETTE["hi_vis"] + (255,))   # hi-vis body
        d.ellipse([rx + 1, 426, rx + 11, 436], fill=PALETTE["helmet"] + (255,))  # helmet
        d.rectangle([rx + 2, 446, rx + 10, 449], fill=(255, 255, 255, 220))


# ~~~ entry point: same draw order as the original script ~~~

def main():
    random.seed(CFG["seed"])
    img = Image.new("RGB", (W, H), PALETTE["night"])
    d = ImageDraw.Draw(img, "RGBA")

    paint_night_sky(d)
    paint_asphalt(d)
    paint_shed(d)
    d = paint_smoke_plume(img, d)
    d = paint_fire(img, d)
    d = paint_glow(img, d)
    paint_sparks(d)
    paint_engine(d)
    paint_crew(d)
    paint_header(d)
    paint_headline_block(d)
    paint_briefs(d)
    paint_colophon(d)

    img.save(os.path.join(HERE, "entry.png"), optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
