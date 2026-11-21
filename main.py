from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
BG = (246, 242, 230)
INK = (20, 22, 24)
WHITE = (255, 255, 255)
RED = (190, 42, 42)
GOLD = (196, 154, 52)
BLUE = (58, 105, 160)
GREEN = (55, 139, 87)


def font(path, size, fallback_size):
    candidates = [
        path,
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


SERIF_BOLD = "C:/Windows/Fonts/timesbd.ttf"
SANS_BOLD = "C:/Windows/Fonts/arialbd.ttf"
SANS_REGULAR = "C:/Windows/Fonts/arial.ttf"

def fbold(size):
    return font(SANS_BOLD, size, size)

def fserif(size):
    return font(SERIF_BOLD, size, size)

def fregular(size):
    return font(SANS_REGULAR, size, size)


def text_size(draw, text, typeface):
    box = draw.textbbox((0, 0), text, font=typeface)
    return box[2] - box[0], box[3] - box[1]


def wrap_text(draw, text, typeface, max_width):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        trial = word if not line else line + " " + word
        if text_size(draw, trial, typeface)[0] <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def draw_wrapped(draw, box, text, typeface, fill, max_lines=None, align="left"):
    x, y, right, bottom = box
    max_width = right - x
    lines = wrap_text(draw, text, typeface, max_width)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        for i in range(len(lines)):
            probe = lines[i]
            while text_size(draw, probe + "...", typeface)[0] > max_width and len(probe) > 1:
                probe = probe[:-1]
            lines[i] = probe.rstrip() + "..."
    line_height = typeface.size + 5
    for i, line in enumerate(lines):
        line_width = text_size(draw, line, typeface)[0]
        tx = x if align == "left" else x + (max_width - line_width) // 2
        draw.text((tx, y + i * line_height), line, font=typeface, fill=fill)
    return y + len(lines) * line_height


def rounded_rectangle(draw, box, fill, outline=None, width=1, radius=0):
    draw.rectangle(box, fill=fill, outline=outline, width=width)


def summit_illustration(draw, box):
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h), fill=(232, 235, 239))
    cy = y + 38
    colors = ((69, 67, 122), (183, 54, 50), (48, 99, 154))
    labels = ("USA", "CHN", "RUS")
    xs = (x + w // 2 - 92, x + w // 2, x + w // 2 + 92)
    for cx, color, label in zip(xs, colors, labels):
        draw.ellipse((cx - 29, cy - 29, cx + 29, cy + 29), fill=color)
        lw = fbold(13)
        tw = text_size(draw, label, lw)[0]
        draw.text((cx - tw // 2, cy - 7), label, font=lw, fill=WHITE)
    table_y = y + h - 24
    draw.rectangle((x + 43, table_y - 7, x + w - 43, table_y), fill=(132, 94, 57))
    cx = x + w // 2
    badge_bottom = y + 8
    draw.ellipse((cx - 13, badge_bottom - 26, cx + 13, badge_bottom), fill=WHITE,
                 outline=(20, 22, 24), width=2)
    draw.line((cx, badge_bottom - 20, cx, badge_bottom - 6), fill=(20, 22, 24), width=2)
    draw.arc((cx - 8, badge_bottom - 18, cx + 8, badge_bottom - 4),
             20, 160, fill=(20, 22, 24), width=2)
    draw.arc((cx - 8, badge_bottom - 18, cx + 8, badge_bottom - 4),
             200, 340, fill=(20, 22, 24), width=2)


def justice_illustration(draw, box):
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h), fill=(239, 231, 190))
    cx = x + w // 2
    navy = (38, 47, 62)
    gold = GOLD
    draw.rectangle((cx - 5, y + 18, cx + 5, y + h - 18), fill=navy)
    draw.ellipse((cx - 12, y + 12, cx + 12, y + 36), fill=gold)
    draw.line((x + w // 2 - 112, y + 38, x + w // 2 + 112, y + 38), fill=navy, width=4)
    for side in (-1, 1):
        sx = cx + side * 112
        draw.line((cx, y + 38, sx, y + 66), fill=navy, width=3)
        draw.polygon([(sx - 34, y + 66), (sx + 34, y + 66), (sx + 21, y + h - 18),
                      (sx - 21, y + h - 18)], fill=(173, 128, 42), outline=navy)
        draw.line((sx - 38, y + 66, sx + 38, y + 66), fill=navy, width=3)
    draw.rectangle((cx - 48, y + h - 21, cx + 48, y + h - 11), fill=navy)


def kyiv_illustration(draw, box):
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h), fill=(20, 34, 61))
    for cx, cy in ((45, 32), (120, 22), (270, 38), (370, 26), (420, 56)):
        draw.line((cx - 8, cy - 8, cx + 8, cy + 8), fill=(255, 168, 63), width=3)
        draw.line((cx - 8, cy + 8, cx + 8, cy - 8), fill=(255, 168, 63), width=3)
        draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), fill=(255, 210, 105))
    draw.line((x + 20, y + 12, x + 175, y + 69), fill=(204, 55, 47), width=4)
    draw.polygon([(x + 168, y + 65), (x + 155, y + 62), (x + 174, y + 73)], fill=(204, 55, 47))
    draw.line((x + w - 20, y + 18, x + 330, y + 73), fill=(204, 55, 47), width=4)
    draw.polygon([(x + 338, y + 71), (x + 330, y + 61), (x + 324, y + 74)], fill=(204, 55, 47))
    base = y + h - 14
    draw.rectangle((x, base - 25, x + w, base), fill=(18, 24, 31))
    draw.rectangle((x + 30, base - 48, x + 70, base - 25), fill=(18, 24, 31))
    draw.rectangle((x + 90, base - 35, x + 160, base - 25), fill=(18, 24, 31))
    draw.rectangle((x + 190, base - 55, x + 245, base - 25), fill=(18, 24, 31))
    dome_cx = x + 216
    draw.polygon([(dome_cx - 28, base - 42), (dome_cx, base - 68), (dome_cx + 28, base - 42)],
                 fill=(184, 146, 58))
    draw.rectangle((dome_cx - 20, base - 42, dome_cx + 20, base - 25), fill=(184, 146, 58))
    draw.rectangle((x, y + h - 14, x + w, y + h), fill=(58, 105, 160))
    draw.rectangle((x, y + h - 7, x + w, y + h), fill=(244, 202, 55))


def ipo_illustration(draw, box):
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h), fill=(224, 238, 226))
    bars = [(x + 55, 52), (x + 118, 67), (x + 181, 82)]
    bottoms = y + h - 25
    for bx, bh in bars:
        draw.rectangle((bx, bottoms - bh, bx + 38, bottoms), fill=(55, 139, 87))
    lw = fbold(14)
    draw.text((x + w - 58, y + 8), "$81B", font=lw, fill=(25, 84, 52))
    pts = [(x + 260, y + 28), (x + 290, y + 42), (x + 320, y + 34),
           (x + 350, y + 59), (x + 380, y + 49), (x + 414, y + 68)]
    draw.line(pts, fill=(190, 42, 42), width=5)
    dx, dy = pts[-2], pts[-1]
    draw.polygon([(dx[0] + 4, dy[1] - 2), (dy[0] - 5, dy[1] - 12), (dy[0] + 4, dy[1] + 8)],
                 fill=(190, 42, 42))


def globe_cloud_illustration(draw, box):
    x, y, w, h = box
    draw.rectangle((x, y, x + w, y + h), fill=(226, 232, 238))
    cx = x + 83
    cy = y + h // 2
    r = 53
    draw.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(58, 105, 160), width=3)
    draw.ellipse((cx-r//2, cy-r, cx+r//2, cy+r), outline=(58, 105, 160), width=2)
    draw.line((cx-r, cy, cx+r, cy), fill=(58, 105, 160), width=2)
    draw.line((cx, cy-r, cx, cy+r), fill=(58, 105, 160), width=2)
    draw.arc((cx-r, cy-r//2, cx+r, cy+r//2), 0, 180, fill=(58, 105, 160), width=2)
    nodes = [(cx-r+10, cy-10), (cx-30, cy-r+16), (cx+r-12, cy-25),
             (cx+22, cy+r-14), (cx-r+18, cy+r-28)]
    for nx, ny in nodes:
        draw.ellipse((nx-5, ny-5, nx+5, ny+5), fill=(85, 91, 98))
    cloud_x = x + w - 112
    cloud_y = y + h // 2 - 18
    draw.ellipse((cloud_x-48, cloud_y-20, cloud_x+22, cloud_y+34), fill=(180, 184, 188))
    draw.ellipse((cloud_x-18, cloud_y-38, cloud_x+52, cloud_y+34), fill=(180, 184, 188))
    draw.ellipse((cloud_x+18, cloud_y-18, cloud_x+72, cloud_y+34), fill=(180, 184, 188))
    draw.rectangle((cloud_x-38, cloud_y+5, cloud_x+54, cloud_y+34), fill=(180, 184, 188))
    draw.line((cloud_x+8, cloud_y-24, cloud_x-4, cloud_y+4, cloud_x+12, cloud_y+18),
              fill=(190, 42, 42), width=5)


def tile(draw, x, y, w, h, accent, headline, caption, illustrator, headline_size=31):
    draw.rectangle((x, y, x+w, y+h), fill=WHITE, outline=(47, 49, 50), width=2)
    draw.rectangle((x+1, y+1, x+w-1, y+10), fill=accent)
    inner_x = x + 12
    strip_y = y + 12
    strip_w = w - 24
    strip_h = 82
    illustrator(draw, (inner_x, strip_y, strip_w, strip_h))
    headline_y = strip_y + strip_h + 10
    draw_wrapped(draw, (x+18, headline_y, x+w-18, headline_y+58),
                 headline, fbold(headline_size), INK, max_lines=2)
    caption_y = headline_y + 58
    draw_wrapped(draw, (x+18, caption_y, x+w-18, y+h-10),
                 caption, fregular(20), (46, 49, 51), max_lines=4)


def main():
    image = Image.new("RGB", (SIZE, SIZE), BG)
    draw = ImageDraw.Draw(image)

    # Header
    draw.rectangle((0, 0, 1024, 128), fill=INK)
    draw.rectangle((0, 128, 1024, 134), fill=RED)
    masthead = fserif(55)
    masthead_text = "THE WORLD IN ONE DAY"
    mw = text_size(draw, masthead_text, masthead)[0]
    draw.text(((1024-mw)//2, 15), masthead_text, font=masthead, fill=WHITE)
    date_text = "FRIDAY, NOVEMBER 20, 2026 · WORLD NEWS FRONT PAGE"
    date_font = fbold(22)
    dw = text_size(draw, date_text, date_font)[0]
    draw.text(((1024-dw)//2, 91), date_text, font=date_font, fill=(229, 192, 92))

    margin = 28
    gap = 16
    tile_w = (1024 - 2*margin - gap) // 2
    tile_h = 262
    top = 150
    tile(draw, margin, top, tile_w, tile_h, RED,
         "SHENZHEN SUMMIT",
         "Trump, Xi & Putin hold first trilateral meeting; joint peace declaration pledges nuclear dialogue",
         summit_illustration)
    tile(draw, margin+tile_w+gap, top, tile_w, tile_h, GOLD,
         "MYANMAR: GENOCIDE RULING",
         "World Court (ICJ) finds Myanmar responsible for genocide against the Rohingya",
         justice_illustration, headline_size=26)
    tile(draw, margin, top+tile_h+gap, tile_w, tile_h, BLUE,
         "RUSSIA POUNDS KYIV",
         "Major missile and drone barrage damages embassies and a cathedral in Ukraine's capital",
         kyiv_illustration)
    tile(draw, margin+tile_w+gap, top+tile_h+gap, tile_w, tile_h, GREEN,
         "ANTHROPIC'S RECORD IPO",
         "$81 billion Nasdaq debut, the largest IPO ever — as AI and tech stocks tumble",
         ipo_illustration)

    wide_y = 704
    wide_h = 146
    draw.rectangle((margin, wide_y, 1024-margin, wide_y+wide_h),
                   fill=WHITE, outline=(47, 49, 50), width=2)
    draw.rectangle((margin+1, wide_y+1, 1024-margin-1, wide_y+10), fill=BLUE)
    globe_cloud_illustration(draw, (margin+12, wide_y+12, 250, wide_h-24))
    right_x = margin+278
    right_w = 1024-margin-right_x-18
    draw_wrapped(draw, (right_x, wide_y+29, right_x+right_w, wide_y+72),
                 "GLOBAL TECH OUTAGE", fbold(35), INK, max_lines=2)
    draw_wrapped(draw, (right_x, wide_y+82, right_x+right_w, wide_y+wide_h-12),
                 "Microsoft 365 down for 9+ hours worldwide; US cyber chief steps down",
                 fregular(21), (46, 49, 51), max_lines=3)

    # Footer
    draw.rectangle((0, 878, 1024, 1024), fill=INK)
    footer = "ALSO: EU–UK summit in Brussels · Houthi missile hits Riyadh skyscraper · Denmark approves Greenland security deal"
    footer_font = fbold(21)
    lines = wrap_text(draw, footer, footer_font, 948)
    if len(lines) > 2:
        mid = len(lines)//2
        lines = [" ".join(lines[:mid]), " ".join(lines[mid:])]
    footer_y = 925 - ((len(lines)-1)*27)//2
    for i, line in enumerate(lines):
        lw = text_size(draw, line, footer_font)[0]
        draw.text(((1024-lw)//2, footer_y+i*27), line, font=footer_font, fill=WHITE)

    # Final header pass ensures the header band contains only the masthead and date line.
    draw.rectangle((0, 0, 1024, 128), fill=INK)
    draw.rectangle((0, 128, 1024, 134), fill=RED)
    masthead = fserif(55)
    masthead_text = "THE WORLD IN ONE DAY"
    mw = text_size(draw, masthead_text, masthead)[0]
    draw.text(((1024-mw)//2, 15), masthead_text, font=masthead, fill=WHITE)
    date_text = "FRIDAY, NOVEMBER 20, 2026 · WORLD NEWS FRONT PAGE"
    date_font = fbold(22)
    dw = text_size(draw, date_text, date_font)[0]
    draw.text(((1024-dw)//2, 91), date_text, font=date_font, fill=(229, 192, 92))

    next_to_script = Path(__file__).resolve().parent / "entry.png"
    image.save(next_to_script, "PNG", optimize=True)

    output_dir = Path("/output")
    if output_dir.is_dir():
        image.save(output_dir / "entry.png", "PNG", optimize=True)


if __name__ == "__main__":
    main()
