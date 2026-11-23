#!/usr/bin/env python3
"""Generate entry.png for news-image-20261123 — authored fresh in this session.

Hero: the PT Fonusa Agung Mulia confectionery factory fire in Cikande,
Banten, Indonesia (Reuters, Mon 23 Nov 2026) — 24 confirmed dead, ~30
workers still missing, rescuers searching the burned wreckage. One hero
subject, vertical drama (flame column + smoke + fire-truck spray), legible
at thumbnail size. 960x960 PNG, DejaVu fonts, PIL only. Deterministic
(random.seed fixed); the image is drawn, not photographed.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 960
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
GOLD = (216, 178, 90)

random.seed(20261123)

img = Image.new("RGB", (W, H), (7, 11, 22))
d = ImageDraw.Draw(img, "RGBA")

# ---------- night sky: deep navy up top, scorched-orange glow at the roofline ---
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

# ---------- ground: dark asphalt strip at the foot of the hero scene ----------
d.rectangle([0, 430, W, 470], fill=(16, 16, 20, 255))
for _ in range(40):
    x = random.randint(8, W - 40)
    d.line([(x, 452), (x + random.randint(12, 40), 452)],
           fill=(70, 70, 78, 90), width=2)

# ---------- factory shed: long low block, sawtooth roof, left of centre ----------
# main walls
d.rectangle([60, 340, 700, 430], fill=(24, 24, 30, 255))
# sawtooth roofline
roof = [(60, 340)]
x = 60
up = True
while x < 700:
    x += 80
    roof.append((x, 312 if up else 340))
    up = not up
roof.append((700, 340))
d.polygon(roof, fill=(34, 34, 42, 255))
# glowing broken windows where the fire is inside
for wx in (150, 210, 560, 620):
    d.rectangle([wx, 372, wx + 34, 402], fill=(255, 120, 20, 230))
    d.rectangle([wx, 372, wx + 34, 382], fill=(255, 190, 60, 240))
# office block on the left, untouched, lit windows
d.rectangle([60, 300, 190, 340], fill=(40, 42, 52, 255))
for wy in (312, 326):
    for wx in (74, 104, 134, 164):
        d.rectangle([wx, wy, wx + 16, wy + 8], fill=(255, 214, 130, 220))
# chimney stack on the right end
d.rectangle([668, 268, 692, 340], fill=(52, 52, 60, 255))
d.rectangle([664, 260, 696, 270], fill=(150, 60, 40, 255))

# ---------- smoke column: thick, drifting up-left, blurred ----------
smoke = Image.new("RGBA", (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(smoke)
sx, sy = 430, 300
for i in range(24):
    r = 32 + i * 9
    sd.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(58, 58, 64, 205))
    sx -= 13
    sy -= 13
img.paste(Image.alpha_composite(img.convert("RGBA"),
                                smoke.filter(ImageFilter.GaussianBlur(10))).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# ---------- flames: layered tongues bursting through the roof, mid-shed ----------
flame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
fd = ImageDraw.Draw(flame)


def tongue(x0, base, height, w, col):
    pts = [(x0, base),
           (x0 + w * 0.20, base - height * 0.55),
           (x0 + w * 0.45, base - height),
           (x0 + w * 0.65, base - height * 0.58),
           (x0 + w, base)]
    fd.polygon(pts, fill=col)


# outer orange, then gold, then pale core — tallest tongue near the centre
for x0, hgt, w in [(300, 150, 95), (355, 205, 115), (415, 175, 100), (470, 130, 75)]:
    tongue(x0, 344, hgt, w, (255, 88, 0, 235))
for x0, hgt, w in [(320, 120, 72), (370, 158, 88), (430, 130, 72)]:
    tongue(x0, 344, hgt, w, (255, 165, 0, 240))
for x0, hgt, w in [(345, 88, 52), (392, 108, 62), (435, 82, 46)]:
    tongue(x0, 344, hgt, w, (255, 216, 70, 245))
for x0, hgt, w in [(372, 58, 34), (408, 66, 38)]:
    tongue(x0, 344, hgt, w, (255, 246, 180, 250))
img.paste(Image.alpha_composite(img.convert("RGBA"),
                                flame.filter(ImageFilter.GaussianBlur(1.2))).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# fire glow washing the roof and the ground in front of the shed
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
for i in range(22):
    x0 = 330 + random.randint(-40, 140)
    y0 = 420 + random.randint(0, 42)
    gd.ellipse([x0, y0, x0 + random.randint(10, 30), y0 + random.randint(4, 10)],
               fill=(255, 110, 20, random.randint(50, 110)))
img.paste(Image.alpha_composite(img.convert("RGBA"),
                                glow.filter(ImageFilter.GaussianBlur(4))).convert("RGB"), (0, 0))
d = ImageDraw.Draw(img, "RGBA")

# embers rising out of the flames
for _ in range(46):
    x = random.randint(310, 540)
    y = random.randint(130, 330)
    r = random.randint(1, 3)
    d.ellipse([x - r, y - r, x + r, y + r],
              fill=(255, random.randint(140, 210), 40, 220))

# ---------- fire truck, right foreground, ladder up and water arcing ----------
# cab + body
d.rectangle([742, 408, 830, 452], fill=(198, 32, 28, 255))
d.rectangle([830, 398, 920, 452], fill=(178, 24, 22, 255))
d.rectangle([752, 414, 788, 432], fill=(180, 220, 240, 255))
d.rectangle([838, 406, 912, 420], fill=(220, 225, 230, 255))
# wheels
for wx in (768, 872):
    d.ellipse([wx - 14, 440, wx + 14, 466], fill=(12, 12, 14, 255))
    d.ellipse([wx - 6, 448, wx + 6, 460], fill=(120, 120, 128, 255))
# ladder rising toward the flames
d.line([(850, 400), (700, 300)], fill=(200, 200, 205, 255), width=6)
for i in range(6):
    t = i / 5
    lx = int(850 + (700 - 850) * t)
    ly = int(400 + (300 - 400) * t)
    d.line([(lx - 8, ly + 4), (lx + 8, ly - 4)], fill=(200, 200, 205, 255), width=2)
# water spray arcing from the ladder tip toward the fire
for _ in range(60):
    t = random.random()
    x = int(700 - t * 150 + random.randint(-14, 14))
    y = int(300 - 40 * t * (1 - t) * 4 + t * 44 + random.randint(-8, 8))
    d.ellipse([x, y, x + 3, y + 3], fill=(190, 220, 240, random.randint(140, 220)))

# ---------- BASARNAS rescuers in orange, small figures at the shed front ----------
for rx in (120, 165, 215, 262):
    d.rectangle([rx, 436, rx + 12, 462], fill=(255, 110, 20, 255))   # hi-vis body
    d.ellipse([rx + 1, 426, rx + 11, 436], fill=(255, 190, 60, 255))  # helmet
    d.rectangle([rx + 2, 446, rx + 10, 449], fill=(255, 255, 255, 220))

# ---------- masthead ----------
d.rectangle([0, 0, W, 92], fill=(7, 12, 24, 255))
d.line([(0, 92), (W, 92)], fill=GOLD + (255,), width=3)
f_date = ImageFont.truetype(BOLD, 46)
d.text((36, 22), "23 NOVEMBER 2026", font=f_date, fill=(255, 255, 255, 255))
f_kick = ImageFont.truetype(BOLD, 20)
d.text((W - 36, 34), "WORLD NEWS IN ONE IMAGE", font=f_kick,
       fill=GOLD + (255,), anchor="ra")

# ---------- headline band ----------
d.rectangle([0, 470, W, 604], fill=(10, 17, 32, 255))
d.line([(0, 470), (W, 470)], fill=GOLD + (255,), width=2)
f_head = ImageFont.truetype(BOLD, 54)
d.text((36, 482), "FACTORY FIRE KILLS 24", font=f_head, fill=(255, 255, 255, 255))
f_sub = ImageFont.truetype(REG, 23)
d.text((36, 544), "Cikande candy plant ablaze — ~30 workers still missing", font=f_sub,
       fill=(199, 210, 224, 255))
d.text((36, 572), "Rescuers search the wreckage as hotspots smoulder on", font=f_sub,
       fill=(199, 210, 224, 255))

# ---------- other stories ----------
labels = [
    ((200, 70, 60), "POLAND", "3 Russian Kh-101 missiles confirmed — NATO meets"),
    ((70, 130, 200), "COP31", "Climate talks collapse — no deal over fossil fuels"),
    ((210, 180, 40), "KYIV", "Boy, 7, pulled alive from rubble after Russian strike"),
    ((230, 120, 30), "LIBYA", "Blast on Russian ship at port — officials suspect drone attack"),
    ((46, 160, 90), "U.S.", "Democrats win largest House majority since 1992"),
    ((150, 90, 170), "MEXICO", "'El Chapo Isidro' captured — FBI most-wanted cartel boss"),
]
f_lead = ImageFont.truetype(BOLD, 26)
f_body = ImageFont.truetype(REG, 24)
y = 628
for col, lead, body in labels:
    d.rectangle([36, y + 4, 52, y + 20], fill=col + (255,))
    d.text((66, y), lead, font=f_lead, fill=(255, 255, 255, 255))
    lw = d.textlength(lead, font=f_lead)
    d.text((66 + lw + 14, y + 1), body, font=f_body, fill=(205, 214, 226, 255))
    y += 49

# ---------- footer ----------
d.line([(36, 928), (W - 36, 928)], fill=(90, 100, 118, 255), width=1)
f_foot = ImageFont.truetype(REG, 18)
d.text((36, 938), "Sources: Reuters  •  AP", font=f_foot, fill=(140, 150, 165, 255))
d.text((W - 36, 938), "23 November 2026", font=f_foot, fill=(140, 150, 165, 255), anchor="ra")

img.save(os.path.join(HERE, "entry.png"), optimize=True)
print("saved entry.png")
