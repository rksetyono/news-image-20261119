"""Build entry.png for news-image-20261119 from scratch.

Draws a 1024x1024 newspaper-style front page with PIL only, using
DejaVu fonts. All text and icons are drawn by this script; nothing is
copied from the starter kit or from any earlier entry. Run:
    python3 render.py
writes entry.png next to this file. Output is deterministic.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (11, 26, 44)          # deep navy
TILE = (21, 42, 66)        # tile background
TILE_EDGE = (38, 66, 97)   # tile border
WHITE = (245, 247, 250)
SUMMARY = (199, 213, 228)
GOLD = (232, 180, 74)
MUTED = (148, 166, 188)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
BOLD = FONT_DIR + "DejaVuSans-Bold.ttf"
REG = FONT_DIR + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- icons
def icon_flags(d, x, y, s):
    """Three small flags on poles: US, China, Russia (left to right)."""
    pole_w = s // 3
    for i, colors in enumerate([
        [(200, 40, 40), (240, 240, 240), (200, 40, 40)],   # US stripes
        [(222, 41, 16)],                                     # China red
        [(240, 240, 240), (40, 90, 200), (200, 40, 40)],   # Russia stripes
    ]):
        px = x + i * pole_w + 4
        d.line([px, y + 6, px, y + s - 4], fill=(200, 210, 220), width=3)
        fw, fh = pole_w - 8, (s - 14) // 3
        fy = y + 8
        for c in colors:
            d.rectangle([px + 2, fy, px + 2 + fw, fy + fh], fill=c)
            fy += fh
        if i == 1:  # one gold star on the red flag
            cx, cy = px + 2 + fw // 3, y + 8 + fh // 2
            d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 215, 0))


def icon_waves(d, x, y, s):
    """Flood: rain above, three waves below."""
    for i in range(3):  # raindrops
        rx = x + 12 + i * 24
        d.line([rx, y + 4, rx - 5, y + 18], fill=(127, 196, 255), width=4)
    for j, yy in enumerate([y + s - 34, y + s - 20, y + s - 6]):
        d.arc([x, yy - 8, x + s, yy + 10], 0, 180, fill=(90, 170, 240), width=5)
    d.ellipse([x + s // 2 - 4, y + s // 2 - 4, x + s // 2 + 4, y + s // 2 + 4],
              fill=(127, 196, 255))


def icon_bridge(d, x, y, s):
    """Bridge deck with an arch, pillars, water, and a burst above."""
    mid = y + s // 2
    d.arc([x + 4, y + 6, x + s - 4, mid + 26], 180, 360, fill=(255, 209, 102), width=5)
    d.line([x + 2, mid + 4, x + s - 2, mid + 4], fill=(220, 228, 236), width=6)
    for px in (x + 12, x + s - 16):
        d.line([px, mid + 4, px, mid + 26], fill=(220, 228, 236), width=5)
    d.line([x + 4, mid + 34, x + s - 4, mid + 34], fill=(90, 170, 240), width=4)
    # burst star above the deck
    cx, cy = x + s // 2, y + 14
    for ang in range(0, 360, 45):
        import math
        r = 12 if ang % 90 == 0 else 6
        dx = int(cx + r * math.cos(math.radians(ang)))
        dy = int(cy + r * math.sin(math.radians(ang)))
        d.line([cx, cy, dx, dy], fill=(255, 120, 90), width=3)


def icon_euro(d, x, y, s):
    """Gold coin with a euro sign, plus two small coins."""
    cx, cy, r = x + s // 2 - 6, y + s // 2, s // 2 - 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(232, 180, 74))
    d.ellipse([cx - r + 5, cy - r + 5, cx + r - 5, cy + r - 5],
              outline=(120, 85, 20), width=2)
    f = font(BOLD, s // 2)
    d.text((cx, cy), "\u20ac", font=f, fill=(60, 42, 8), anchor="mm")
    d.ellipse([x + s - 20, y + s - 20, x + s - 6, y + s - 6], fill=(200, 150, 50))
    d.ellipse([x + s - 34, y + 6, x + s - 22, y + 18], fill=(200, 150, 50))


def icon_controller(d, x, y, s):
    """Game controller with D-pad, buttons and a VI badge."""
    d.rounded_rectangle([x + 2, y + s // 3, x + s - 2, y + s - 8],
                        radius=12, fill=(70, 60, 110), outline=(180, 170, 230), width=3)
    d.rectangle([x + 16, y + s // 2 + 2, x + 30, y + s // 2 + 16], fill=(220, 228, 236))
    d.rectangle([x + 10, y + s // 2 + 8, x + 36, y + s // 2 + 10], fill=(220, 228, 236))
    for bx, by, c in [(x + s - 34, y + s // 2 + 2, (255, 90, 90)),
                      (x + s - 24, y + s // 2 + 10, (90, 200, 120)),
                      (x + s - 44, y + s // 2 + 12, (90, 150, 255)),
                      (x + s - 34, y + s // 2 + 20, (255, 210, 90))]:
        d.ellipse([bx, by, bx + 8, by + 8], fill=c)
    f = font(BOLD, 22)
    d.text((x + s // 2, y + 4), "VI", font=f, fill=(255, 209, 102), anchor="ma")


def icon_voyager(d, x, y, s):
    """Probe with a dish antenna among stars."""
    import random
    rng = random.Random(19)
    for _ in range(14):
        sx = x + rng.randint(2, s - 2)
        sy = y + rng.randint(2, s - 2)
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(220, 228, 236))
    cx, cy = x + s // 2, y + s // 2 + 8
    d.line([cx, cy, cx + 22, cy - 22], fill=(200, 210, 220), width=3)
    d.polygon([(cx + 22, cy - 22), (cx + 34, cy - 34), (cx + 10, cy - 30)],
              fill=(232, 180, 74))
    d.rectangle([cx - 16, cy - 6, cx + 6, cy + 8], fill=(160, 175, 190))
    d.line([cx - 16, cy - 6, cx - 26, cy - 16], fill=(200, 210, 220), width=3)
    d.arc([cx + 18, cy - 40, cx + 44, cy - 14], -60, 60, fill=(127, 196, 255), width=3)


# ---------------------------------------------------------------- stories
STORIES = [
    ("DIPLOMACY \u00b7 SHENZHEN", (127, 196, 255),
     "Trump, Xi and Putin gather in Shenzhen",
     "Three leaders meet for rare trilateral talks as the APEC summit opens in China.",
     icon_flags),
    ("MIDDLE EAST \u00b7 GAZA", (255, 157, 122),
     "Floods deepen the Gaza crisis",
     "Australia, Canada, Italy and the UK urge Israel to let aid reach flooded Gaza.",
     icon_waves),
    ("UKRAINE WAR", (255, 209, 102),
     "Crimean Bridge attacked again",
     "Traffic is suspended after a fresh strike on the link to occupied Crimea.",
     icon_bridge),
    ("EUROPE \u00b7 ECONOMY", (143, 214, 160),
     "EU proposes \u20ac45bn loan for Ukraine",
     "Brussels seeks a loan to be repaid once Russia pays war reparations.",
     icon_euro),
    ("CULTURE \u00b7 GAMING", (201, 167, 255),
     "GTA VI begins global rollout",
     "Gamers enter Vice City as the long-awaited sequel launches worldwide.",
     icon_controller),
    ("SPACE \u00b7 SCIENCE", (127, 227, 208),
     "Voyager 1 reaches one light-day",
     "NASA's 49-year-old probe hits the milestone; confirmation is due today.",
     icon_voyager),
]

ALSO = ("ALSO TODAY \u2014 Van Gogh sells for a record $190.4m \u00b7 "
        "Anthropic poised for a $1.4tn stock-market debut \u00b7 "
        "Cyclone Akvan nears India's east coast")


def draw_tile(d, x, y, w, h, kicker, color, headline, summary, icon_fn):
    d.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=TILE, outline=TILE_EDGE, width=2)
    d.rounded_rectangle([x, y, x + 6, y + h], radius=3, fill=color)
    icon_fn(d, x + 20, y + 16, 76)
    f_kick = font(BOLD, 19)
    d.text((x + 110, y + 22), kicker, font=f_kick, fill=color)
    f_head = font(BOLD, 27)
    lines = wrap(d, headline, f_head, w - 110 - 16)[:2]
    yy = y + 50
    for ln in lines:
        d.text((x + 110, yy), ln, font=f_head, fill=WHITE)
        yy += 33
    f_sum = font(REG, 20)
    lines = wrap(d, summary, f_sum, w - 40)[:3]
    yy = y + 122
    for ln in lines:
        d.text((x + 20, yy), ln, font=f_sum, fill=SUMMARY)
        yy += 27


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # header
    f_title = font(BOLD, 56)
    d.text((W // 2, 34), "THURSDAY, 19 NOVEMBER 2026", font=f_title,
           fill=WHITE, anchor="ma")
    f_sub = font(REG, 25)
    d.text((W // 2, 104), "THE WORLD IN ONE DAY", font=f_sub,
           fill=GOLD, anchor="ma")
    d.line([24, 158, W - 24, 158], fill=GOLD, width=3)

    # story grid: 2 columns x 3 rows
    tw, th, gap, mx = 480, 232, 16, 24
    y0 = 180
    for i, (kicker, color, headline, summary, icon_fn) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x = mx + col * (tw + gap)
        y = y0 + row * (th + gap)
        draw_tile(d, x, y, tw, th, kicker, color, headline, summary, icon_fn)

    # "also today" strip
    f_also = font(REG, 20)
    lines = wrap(d, ALSO, f_also, W - 48)
    yy = 922
    for ln in lines:
        d.text((24, yy), ln, font=f_also, fill=MUTED)
        yy += 27

    # footer
    f_foot = font(REG, 16)
    d.text((W // 2, 996), "Events that happened or were first reported on 19 November 2026",
           font=f_foot, fill=MUTED, anchor="mb")

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
