import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 627

# Farver — NBB brand palette (fra logo: cyan → grøn → lime, navy tekst)
C_BG       = "#0D1E3A"   # Mørk navy baggrund
C_BG_STRIP = "#081629"   # Mørkere navy til bund-strip
C_BLUE     = "#00A8CC"   # Brand cyan-blå
C_GREEN    = "#4ABF6C"   # Brand grøn
C_LIME     = "#95C11F"   # Brand lime
C_WHITE    = "#FFFFFF"
C_MUTED    = "#A8C8D8"   # Lys blå-grå til sekundær tekst
C_BADGE_BG = "#0A2F52"   # Mørk blå til badge baggrund

FONT_PATH_BOLD = "/System/Library/Fonts/HelveticaNeue.ttc"
FONT_PATH_REG  = "/System/Library/Fonts/HelveticaNeue.ttc"
FONT_FALLBACK  = "/System/Library/Fonts/Supplemental/Arial.ttf"


def _font(size, bold=False):
    try:
        idx = 1 if bold else 0
        return ImageFont.truetype(FONT_PATH_BOLD, size, index=idx)
    except Exception:
        try:
            return ImageFont.truetype(FONT_FALLBACK, size)
        except Exception:
            return ImageFont.load_default()


def _hex(color):
    c = color.lstrip("#")
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))


def _draw_rounded_rect(draw, xy, radius, fill):
    x0, y0, x1, y1 = xy
    draw.rectangle([x0 + radius, y0, x1 - radius, y1], fill=fill)
    draw.rectangle([x0, y0 + radius, x1, y1 - radius], fill=fill)
    draw.ellipse([x0, y0, x0 + radius * 2, y0 + radius * 2], fill=fill)
    draw.ellipse([x1 - radius * 2, y0, x1, y0 + radius * 2], fill=fill)
    draw.ellipse([x0, y1 - radius * 2, x0 + radius * 2, y1], fill=fill)
    draw.ellipse([x1 - radius * 2, y1 - radius * 2, x1, y1], fill=fill)


def generate(article, language, usp_index, output_path):
    img = Image.new("RGB", (W, H), C_BG)
    draw = ImageDraw.Draw(img, "RGBA")

    # Gradient-strip øverst (brand: cyan → grøn → lime)
    grad_h = 8
    colors_grad = [_hex(C_BLUE), _hex(C_GREEN), _hex(C_LIME)]
    stops = [0, W // 2, W]
    for x in range(W):
        if x <= stops[1]:
            t = x / stops[1]
            r = int(colors_grad[0][0] + t * (colors_grad[1][0] - colors_grad[0][0]))
            g = int(colors_grad[0][1] + t * (colors_grad[1][1] - colors_grad[0][1]))
            b = int(colors_grad[0][2] + t * (colors_grad[1][2] - colors_grad[0][2]))
        else:
            t = (x - stops[1]) / (stops[2] - stops[1])
            r = int(colors_grad[1][0] + t * (colors_grad[2][0] - colors_grad[1][0]))
            g = int(colors_grad[1][1] + t * (colors_grad[2][1] - colors_grad[1][1]))
            b = int(colors_grad[1][2] + t * (colors_grad[2][2] - colors_grad[1][2]))
        draw.line([(x, 0), (x, grad_h)], fill=(r, g, b))

    # Dekorative cirkler øverst til højre
    circles = [
        (1020, -50, 420, C_BLUE,  80, 3),
        (1110,  90, 300, C_GREEN, 60, 2),
        (890,  170, 190, C_LIME,  50, 2),
        (960,  300, 120, C_BLUE,  35, 1),
    ]
    for cx, cy, r, col, alpha, lw in circles:
        bbox = [cx - r, cy - r, cx + r, cy + r]
        draw.ellipse(bbox, outline=(*_hex(col), alpha), width=lw)

    # Top-venstre: NBB navn
    logo_font = _font(58, bold=True)
    draw.text((52, 38), "NBB", font=logo_font, fill=C_WHITE)

    sub_font = _font(17)
    draw.text((52, 106), "Nordic Big Bag · Industriel emballage", font=sub_font, fill=C_MUTED)

    # Kategori-badge med brand cyan-blå
    category = {"da": "CIRKULÆR ØKONOMI", "en": "CIRCULAR ECONOMY", "de": "KREISLAUFWIRTSCHAFT", "sv": "CIRKULÄR EKONOMI"}.get(language, "CIRCULAR ECONOMY")
    badge_font = _font(14, bold=True)
    badge_bbox = draw.textbbox((0, 0), category, font=badge_font)
    badge_w = badge_bbox[2] - badge_bbox[0] + 32
    badge_h = 32
    badge_x, badge_y = 52, 156
    _draw_rounded_rect(draw, [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], 6, C_BADGE_BG)
    draw.text((badge_x + 16, badge_y + 8), category, font=badge_font, fill=C_BLUE)

    # Separator-linje i lime (brand accent)
    draw.rectangle([52, 208, 52 + 60, 213], fill=C_LIME)

    # Hoved-overskrift (nyhedstitlen)
    headline_raw = article.get("title", "")
    # Fjern kildenavn fra slutningen hvis det er der
    source = article.get("source", "")
    if f"| {source}" in headline_raw:
        headline_raw = headline_raw.split(f"| {source}")[0].strip()
    if " - " in headline_raw and len(headline_raw) > 80:
        headline_raw = headline_raw.split(" - ")[0].strip()

    # Wrap teksten
    headline_font = _font(46, bold=True)
    max_chars = 38
    lines = textwrap.wrap(headline_raw, width=max_chars)[:3]
    if len(lines) == 3 and len(textwrap.wrap(headline_raw, width=max_chars)) > 3:
        lines[2] = lines[2][:30].rstrip() + "…"

    y_headline = 240
    line_height = 58
    for line in lines:
        draw.text((52, y_headline), line, font=headline_font, fill=C_WHITE)
        y_headline += line_height

    # Kilde-info
    pub_raw = article.get("published", "")
    try:
        from email.utils import parsedate_to_datetime
        pub_dt = parsedate_to_datetime(pub_raw)
        months = ["jan","feb","mar","apr","maj","jun","jul","aug","sep","okt","nov","dec"]
        pub = f"{pub_dt.day}. {months[pub_dt.month - 1]} {pub_dt.year}"
    except Exception:
        pub = pub_raw[:10]
    source_text = f"{source}  ·  {pub}" if pub else source
    source_font = _font(17)
    draw.text((52, y_headline + 18), source_text, font=source_font, fill=C_MUTED)

    # Bund-strip
    strip_y = H - 72
    draw.rectangle([0, strip_y, W, H], fill=C_BG_STRIP)
    draw.rectangle([0, strip_y, W, strip_y + 2], fill=C_BLUE)

    # Hashtags i bund (brand cyan-blå)
    tags = {
        "da": "#bigbags  #cirkulærøkonomi  #grønomstilling  #NordicBigBag",
        "en": "#bigbags  #circulareconomy  #greentransition  #NordicBigBag",
        "de": "#bigbags  #kreislaufwirtschaft  #grünerWandel  #NordicBigBag",
        "sv": "#bigbags  #cirkulärekonomi  #grönomställning  #NordicBigBag",
    }.get(language, "#bigbags  #circulareconomy  #NordicBigBag")
    tag_font = _font(17)
    draw.text((52, strip_y + 22), tags, font=tag_font, fill=C_BLUE)

    # nbb.dk i bund til højre (lime accent)
    nbb_small = _font(20, bold=True)
    nbb_text = "nbb.dk"
    nbb_bbox = draw.textbbox((0, 0), nbb_text, font=nbb_small)
    nbb_w = nbb_bbox[2] - nbb_bbox[0]
    draw.text((W - nbb_w - 52, strip_y + 20), nbb_text, font=nbb_small, fill=C_LIME)

    # Gem
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    img.save(output_path, "PNG", quality=95)
    return output_path
