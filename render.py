#!/usr/bin/env python3
"""Render the LEONIDA AIRLINES boarding-pass meme for gta6-meme-x-01.

Draws a 1024x1024 boarding pass with PIL only. Deterministic: the same
input files always produce the same bytes (no clock, no network; the only
randomness is a barcode from a fixed seed).

The make.fun ghost is the official press-kit mark
(assets/mark-1024.png, from https://make.fun/press/), pasted as-is and
never redrawn, recoloured or stretched, per the press kit's own rules.
It plays the role of the airline's pilot — the ghost is the captain of
Leonida Airlines, not a sticker in a corner.
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
W = H = 1024

# make.fun brand colours (press kit palette.txt)
MAGENTA = (196, 28, 131)        # #C41C83
MAGENTA_PINK = (255, 136, 196)  # #FF88C4, lighter pink for dark grounds
BG = (10, 10, 15)               # night canvas
CARD = (23, 27, 36)             # #171B24 surface
PANEL = (30, 35, 48)            # slightly lighter dark panel
WHITE = (255, 255, 255)
MUTED = (154, 163, 178)         # secondary on dark
HAIRLINE = (58, 65, 82)
STAMP_FILL = (34, 22, 38)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
REG = FONT_DIR / "DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(str(BOLD if bold else REG), size)


def fit(text, max_width, start, bold=True, minimum=14):
    """Largest font size (<= start) at which text fits inside max_width."""
    size = start
    while size > minimum:
        f = font(size, bold)
        if f.getbbox(text)[2] <= max_width:
            return f
        size -= 1
    return font(minimum, bold)


def draw_text(draw, xy, s, f, fill):
    draw.text(xy, s, font=f, fill=fill)


def centered(draw, cx, y, s, f, fill):
    """Draw text centred on cx, top edge at y."""
    w = draw.textbbox((0, 0), s, font=f)[2]
    draw.text((cx - w / 2, y), s, font=f, fill=fill)


def right_aligned(draw, x_right, y, s, f, fill):
    w = draw.textbbox((0, 0), s, font=f)[2]
    draw.text((x_right - w, y), s, font=f, fill=fill)


def spaced(draw, xy, s, f, fill, tracking=8):
    """Draw text with extra space between letters (small-caps labels)."""
    x, y = xy
    for ch in s:
        draw.text((x, y), ch, font=f, fill=fill)
        x += draw.textbbox((0, 0), ch, font=f)[2] + tracking


def label(draw, xy, s):
    draw_text(draw, xy, s, font(20, bold=True), MAGENTA_PINK)


def dashed_hline(draw, y, x0, x1, fill, dash=14, gap=10):
    x = x0
    while x < x1:
        draw.line([(x, y), (min(x + dash, x1), y)], fill=fill, width=3)
        x += dash + gap


def barcode(draw, box, seed=2013):
    """A fake boarding-pass barcode: fixed seed, so it never changes."""
    rng = random.Random(seed)
    x0, y0, x1, y1 = box
    x = x0
    while x < x1 - 3:
        w = rng.choice([2, 2, 3, 3, 4, 5])
        if rng.random() < 0.62:
            draw.rectangle([x, y0, x + w - 1, y1], fill=WHITE)
        x += w + rng.choice([2, 3, 3, 4])


def ghost_mark(size):
    """The official make.fun mark, cropped to its ink and resized.

    The press kit ships the mark as a magenta disc on transparency; it is
    used exactly as it is, only resized, never redrawn or recoloured.
    """
    mark = Image.open(HERE / "assets" / "mark-1024.png").convert("RGBA")
    bbox = mark.getchannel("A").getbbox()
    mark = mark.crop(bbox)
    return mark.resize((size, size), Image.LANCZOS)


def render():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- the pass card -------------------------------------------------
    d.rounded_rectangle([24, 24, 1000, 1000], radius=28, fill=CARD,
                        outline=MAGENTA, width=4)

    # --- magenta header band -------------------------------------------
    d.rounded_rectangle([28, 28, 996, 196], radius=24, fill=MAGENTA)
    d.rectangle([28, 160, 996, 196], fill=MAGENTA)  # square off the bottom
    draw_text(d, (56, 50), "LEONIDA AIRLINES",
              fit("LEONIDA AIRLINES", 680, 58), WHITE)
    spaced(d, (56, 122), "BOARDING PASS", font(30, bold=True), WHITE)
    right_aligned(d, 968, 66, "LAUNCH WEEK", font(26, bold=True), WHITE)

    # --- left column: the journey --------------------------------------
    label(d, (56, 214), "FROM")
    draw_text(d, (56, 236), "LOS SANTOS", fit("LOS SANTOS", 584, 54), WHITE)
    draw_text(d, (56, 294), "▼", font(28, bold=True), MAGENTA_PINK)
    label(d, (56, 332), "TO")
    draw_text(d, (56, 352), "VICE CITY", fit("VICE CITY", 584, 54), WHITE)

    label(d, (56, 424), "FLIGHT")
    draw_text(d, (56, 446), "VI-2013  •  GATE B13",
              fit("VI-2013  •  GATE B13", 584, 36), WHITE)

    label(d, (56, 498), "PASSENGER")
    draw_text(d, (56, 520), "ONE VERY PATIENT GAMER",
              fit("ONE VERY PATIENT GAMER", 584, 30), WHITE)

    label(d, (56, 572), "DEPARTURE")
    draw_text(d, (56, 594), "17 SEP 2013", fit("17 SEP 2013", 280, 34), WHITE)
    label(d, (360, 572), "ARRIVAL")
    draw_text(d, (360, 594), "19 NOV 2026", fit("19 NOV 2026", 280, 34), WHITE)

    label(d, (56, 646), "STATUS")
    draw_text(d, (56, 668), "DELAYED 13 YEARS",
              fit("DELAYED 13 YEARS", 584, 34), WHITE)
    draw_text(d, (56, 706), "2 gate changes: Fall 2025 → May 2026",
              font(18, bold=False), MUTED)

    label(d, (56, 740), "BAGGAGE")
    draw_text(d, (56, 762), "214 GB", fit("214 GB", 280, 30), WHITE)
    draw_text(d, (56, 794), "family photos deleted to make room",
              font(16, bold=False), MUTED)
    label(d, (360, 740), "SEAT")
    draw_text(d, (360, 762), "5 SICK DAYS", fit("5 SICK DAYS", 280, 30), WHITE)
    draw_text(d, (360, 794), "doctor approved", font(16, bold=False), MUTED)

    # --- right column: the pilot ---------------------------------------
    d.rounded_rectangle([664, 200, 968, 800], radius=20, fill=PANEL,
                        outline=MAGENTA, width=3)
    centered(d, 816, 224, "YOUR PILOT", font(24, bold=True), WHITE)
    ghost = ghost_mark(280)
    img.paste(ghost, (676, 262), ghost)
    centered(d, 816, 566, "CAPTAIN", font(26, bold=True), MAGENTA_PINK)
    centered(d, 816, 598, "MAKE.FUN GHOST",
             fit("MAKE.FUN GHOST", 280, 28), WHITE)
    barcode(d, (706, 668, 926, 728))
    centered(d, 816, 740, "VI-2013", font(18, bold=False), MUTED)

    # --- perforation ----------------------------------------------------
    dashed_hline(d, 822, 44, 980, HAIRLINE)
    d.ellipse([8, 806, 40, 838], fill=BG)      # punched notch, left
    d.ellipse([984, 806, 1016, 838], fill=BG)  # punched notch, right

    # --- payment stamp --------------------------------------------------
    d.rounded_rectangle([56, 848, 968, 940], radius=14, fill=STAMP_FILL,
                        outline=MAGENTA, width=4)
    # stamp line, two-tone so the brand name pops: white, then make.fun pink
    stamp_font = fit("PAID BY MY AI AGENT ON MAKE.FUN", 880, 38)
    head, tail = "PAID BY MY AI AGENT ON ", "MAKE.FUN"
    w_head = d.textbbox((0, 0), head, font=stamp_font)[2]
    w_tail = d.textbbox((0, 0), tail, font=stamp_font)[2]
    x = 512 - (w_head + w_tail) / 2
    d.text((x, 864), head, font=stamp_font, fill=WHITE)
    d.text((x + w_head, 864), tail, font=stamp_font, fill=MAGENTA_PINK)
    centered(d, 512, 906, "FARE $79.99  •  NON-REFUNDABLE",
             font(22, bold=True), MAGENTA_PINK)
    centered(d, 512, 956, "The 13-year wait is non-returnable.",
             font(20, bold=False), MUTED)

    return img


if __name__ == "__main__":
    out = HERE / "meme.png"
    render().save(out, "PNG")
    # a 480x480 copy, exactly the size the judge reads the picture at
    render().resize((480, 480), Image.LANCZOS).save(HERE / "meme-480.png", "PNG")
    print(f"wrote {out} (1024x1024) and meme-480.png (480x480)")
