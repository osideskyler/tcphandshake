"""Render the link-preview image (og.jpg, 1200x630) from a flyer's ASCII data.

usage: og_image.py flyers/halloween.js og.jpg

Left: terminal lettering and event details. Right: the ASCII skull with glowing eyes.
"""
import json, sys
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageChops
import pyfiglet

B64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
S = 2  # supersample, downscaled at the end
W, H = 1200 * S, 630 * S
GREEN, DIM, RED, EMBER = (57, 255, 122), (31, 138, 69), (255, 59, 36), (255, 176, 46)
MENLO = "/System/Library/Fonts/Menlo.ttc"

src = open(sys.argv[1]).read()
art = json.loads(src[src.index("halloween = ") + 12 : src.rindex(";")])

base = Image.new("RGB", (W, H), (5, 8, 5))
glow = Image.new("RGB", (W, H), (0, 0, 0))
bd, gd = ImageDraw.Draw(base), ImageDraw.Draw(glow)


def font(px, bold=False):
    return ImageFont.truetype(MENLO, int(px), index=1 if bold else 0)


def block(lines, x, y, px, color, glow_amt=0.5):
    f = font(px, bold=True)
    lh = px * 1.02
    for i, line in enumerate(lines):
        bd.text((x, y + i * lh), line, font=f, fill=color)
        gd.text((x, y + i * lh), line, font=f, fill=tuple(int(c * glow_amt) for c in color))
    return y + len(lines) * lh


def fig(text):
    return [l.rstrip() for l in pyfiglet.figlet_format(text, font="ansi_shadow").splitlines() if l.strip()]


# Skull on the right, full height.
cols, rows = art["cols"], art["rows"]
ch = (H - 40 * S) / rows
cw = ch * 0.6
sx, sy = W - cols * cw - 30 * S, 20 * S
f = font(ch, bold=True)
eyes = set(art["eyes"])
for y in range(rows):
    for x in range(cols):
        c = art["chars"][y][x]
        if c == " ":
            continue
        i = y * cols + x
        px, py = sx + x * cw, sy + y * ch
        if i in eyes:
            bd.text((px, py), c, font=f, fill=(255, 241, 224) if c in "%#@" else (255, 42, 18))
            gd.text((px, py), "@", font=f, fill=(255, 30, 0))
        else:
            v = " .,:;-~=+*ox%#@".index(c) / 14
            col = tuple(int(int(art["palette"][B64.index(art["colors"][y][x])][k : k + 2], 16) * (0.35 + 0.65 * v)) for k in (1, 3, 5))
            bd.text((px, py), c, font=f, fill=col)
            gd.text((px, py), c, font=f, fill=tuple(int(k * 0.35) for k in col))
# Fade the skull's left edge into the dark so the text column reads cleanly.
fade = Image.linear_gradient("L").rotate(90).resize((int(160 * S), H))
mask = Image.new("L", (W, H), 255)
mask.paste(Image.eval(fade, lambda p: 255 - p), (int(sx), 0))
mask.paste(0, (0, 0, int(sx), H))
skull_only = Image.composite(base, Image.new("RGB", (W, H), (5, 8, 5)), mask)
base = skull_only
bd = ImageDraw.Draw(base)

# Text column on the left.
x0, y = 46 * S, 48 * S
bd.text((x0, y), "guest@tcphandshake:~$ cat halloween.flyer", font=font(17 * S), fill=DIM)
y += 52 * S
y = block(fig("TCP"), x0, y, 13 * S, GREEN) + 8 * S
y = block(fig("HANDSHAKE"), x0, y, 7.4 * S, GREEN) + 46 * S
y = block(fig("HALLOWEEN"), x0, y, 6.9 * S, RED, 0.8) + 6 * S
y = block(fig("PARTY"), x0, y, 6.9 * S, RED, 0.8) + 40 * S
bd.text((x0, y), "OCT 31 · 7:30PM", font=font(38 * S, True), fill=RED)
gd.text((x0, y), "OCT 31 · 7:30PM", font=font(38 * S, True), fill=(150, 30, 15))
y += 56 * S
bd.text((x0, y), "COSTUMES REQUIRED · LIVE MUSIC & DJ", font=font(19 * S, True), fill=EMBER)
y += 34 * S
bd.text((x0, y), "3675 N TIMPVIEW DR, PROVO, UT", font=font(19 * S, True), fill=EMBER)

# Bloom, then CRT scanlines.
bloom = glow.filter(ImageFilter.GaussianBlur(9 * S))
out = ImageChops.add(base, bloom)
out = ImageChops.add(out, glow.filter(ImageFilter.GaussianBlur(3 * S)))
lines = Image.new("L", (W, H), 0)
ld = ImageDraw.Draw(lines)
for yy in range(0, H, 3 * S):
    ld.rectangle([0, yy, W, yy + S - 1], fill=70)
out = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), out, lines)
out.resize((1200, 630), Image.LANCZOS).save(sys.argv[2], quality=88, optimize=True, progressive=True)
print("wrote", sys.argv[2])
