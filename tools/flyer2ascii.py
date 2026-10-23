"""Convert the Halloween flyer's skull art into colored ASCII data for the site."""
import json, sys, colorsys
from PIL import Image, ImageDraw

src, out = sys.argv[1], sys.argv[2]
COLS = int(sys.argv[3]) if len(sys.argv) > 3 else 120
CHAR_ASPECT = 0.6  # monospace cell width / height at line-height 1
RAMP = " .,:;-~=+*ox%#@"
SMOKE, GAIN, GAMMA = 0.25, 1.35, 0.9
B64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"

im = Image.open(src).convert("RGB")
# Black out the flyer's lettering so only the art becomes ASCII (text is rendered as real text).
d = ImageDraw.Draw(im)
d.rectangle([0, 925, 275, 1130], fill=(0, 0, 0))
im = im.crop((0, 255, 1198, 1300))
w, h = im.size
ROWS = round(COLS * h / w * CHAR_ASPECT)
small = im.resize((COLS, ROWS), Image.BOX)

cells, boosted = [], Image.new("RGB", (COLS, ROWS))
for y in range(ROWS):
    for x in range(COLS):
        r, g, b = small.getpixel((x, y))
        hh, ss, vv = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
        # Saturated subjects (green skull, red eyes, blue hood) carry the image;
        # grey smoke is pushed back into the dark.
        v = max(0.0, min(1.0, (vv - 0.08) / 0.6)) * (SMOKE + (1 - SMOKE) * min(1, ss * 1.6))
        v = min(1.0, v * GAIN) ** GAMMA
        rr, gg, bb = colorsys.hsv_to_rgb(hh, min(1, ss * 1.25), min(1, 0.45 + 0.6 * vv))
        boosted.putpixel((x, y), (int(rr * 255), int(gg * 255), int(bb * 255)))
        eye = r > 150 and r > 1.9 * g and r > 1.9 * b
        cells.append((v, eye))

pal_img = boosted.quantize(colors=64, method=Image.Quantize.MEDIANCUT)
pal = pal_img.getpalette()[: 64 * 3]
palette = ["#%02x%02x%02x" % tuple(pal[i * 3 : i * 3 + 3]) for i in range(64)]

chars, colors, eyes = [], [], []
for y in range(ROWS):
    crow, colrow = "", ""
    for x in range(COLS):
        v, eye = cells[y * COLS + x]
        c = RAMP[min(len(RAMP) - 1, int(v * len(RAMP)))]
        if eye and c == " ":
            c = "o"
        crow += c
        colrow += B64[pal_img.getpixel((x, y))]
        if eye:
            eyes.append(y * COLS + x)
    chars.append(crow)
    colors.append(colrow)

import pyfiglet
def fig(text):
    return [l.rstrip() for l in pyfiglet.figlet_format(text, font="ansi_shadow").splitlines() if l.strip()]
data = {"cols": COLS, "rows": ROWS, "palette": palette, "chars": chars, "colors": colors, "eyes": eyes,
        "title": [fig("HALLOWEEN"), fig("PARTY")]}
with open(out, "w") as f:
    f.write("// Generated from the Halloween flyer by flyer2ascii.py. Do not hand-edit.\n")
    f.write("window.FLYERS = window.FLYERS || {};\nwindow.FLYERS.halloween = ")
    json.dump(data, f, separators=(",", ":"))
    f.write(";\n")
print(COLS, ROWS, "eyes:", len(eyes))

if len(sys.argv) > 4:  # colored preview PNG
    from PIL import ImageFont
    font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 14)
    cw, ch = 8.43, 14
    prev = Image.new("RGB", (int(COLS * cw) + 10, ROWS * ch + 10), (5, 8, 5))
    pd = ImageDraw.Draw(prev)
    for y in range(ROWS):
        for x in range(COLS):
            c = chars[y][x]
            if c != " ":
                pd.text((5 + x * cw, 5 + y * ch), c, font=font, fill=palette[B64.index(colors[y][x])])
    prev.save(sys.argv[4])
