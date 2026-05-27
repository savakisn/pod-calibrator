from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import httpx
import urllib.parse

SCALE = 2
W = 640 * SCALE
PAD = 28 * SCALE

BG      = (15, 23, 42)
SURFACE = (30, 41, 59)
BORDER  = (51, 65, 85)
TEXT    = (226, 232, 240)
MUTED   = (100, 116, 139)
GOLD    = (245, 158, 11)

import os as _os
_FONT_DIR = _os.path.join(_os.path.dirname(__file__), '../../fonts')
FONT_REG   = _os.path.join(_FONT_DIR, 'NotoSans-Regular.ttf')
FONT_BOLD  = _os.path.join(_FONT_DIR, 'NotoSans-Bold.ttf')
FONT_BLACK = _os.path.join(_FONT_DIR, 'NotoSans-Black.ttf')

# Protanopia: no red receptors — R appears dark; use orange for R, cyan for G
# Deuteranopia: no green receptors — G appears yellowish; use rose for R, violet for G
# Tritanopia: no blue receptors — U appears green-ish; use violet for U
PALETTES = {
    'protanopia': {
        'bracket': {
            1: (6, 182, 212),    # cyan-500
            2: (59, 130, 246),   # blue-500
            3: (139, 92, 246),   # violet-500
            4: (245, 158, 11),   # amber-500
            5: (217, 70, 239),   # fuchsia-500
        },
        'speed': {
            'Turbo':        {'bg': (45,26,0),   'border': (180,120,0),  'text': (253,230,138)},
            'Fast':         {'bg': (8,35,45),   'border': (14,116,144), 'text': (103,232,249)},
            'Steady':       {'bg': (12,26,58),  'border': (29,78,216),  'text': (147,197,253)},
            'Slow':         {'bg': (30,15,60),  'border': (109,40,217), 'text': (196,181,253)},
            'Battlecruiser':{'bg': (30,41,59),  'border': (71,85,105),  'text': (148,163,184)},
        },
        'color_badge': {
            'white':    {'bg': (254,243,199), 'text': (120,53,15),  'label': 'W'},
            'blue':     {'bg': (37,99,235),   'text': (255,255,255), 'label': 'U'},
            'black':    {'bg': (71,85,105),   'text': (255,255,255), 'label': 'B'},
            'red':      {'bg': (249,115,22),  'text': (255,255,255), 'label': 'R'},
            'green':    {'bg': (8,145,178),   'text': (255,255,255), 'label': 'G'},
            'colorless':{'bg': (100,116,139), 'text': (255,255,255), 'label': 'C'},
        },
    },
    'deuteranopia': {
        'bracket': {
            1: (20, 184, 166),   # teal-500
            2: (59, 130, 246),   # blue-500
            3: (167, 139, 250),  # violet-400
            4: (249, 115, 22),   # orange-500
            5: (244, 63, 94),    # rose-500
        },
        'speed': {
            'Turbo':        {'bg': (50,8,20),   'border': (190,18,60),  'text': (253,164,175)},
            'Fast':         {'bg': (45,16,0),   'border': (154,52,18),  'text': (253,186,116)},
            'Steady':       {'bg': (12,26,58),  'border': (29,78,216),  'text': (147,197,253)},
            'Slow':         {'bg': (30,15,50),  'border': (126,34,206), 'text': (216,180,254)},
            'Battlecruiser':{'bg': (30,41,59),  'border': (71,85,105),  'text': (148,163,184)},
        },
        'color_badge': {
            'white':    {'bg': (254,243,199), 'text': (120,53,15),  'label': 'W'},
            'blue':     {'bg': (37,99,235),   'text': (255,255,255), 'label': 'U'},
            'black':    {'bg': (71,85,105),   'text': (255,255,255), 'label': 'B'},
            'red':      {'bg': (244,63,94),   'text': (255,255,255), 'label': 'R'},
            'green':    {'bg': (124,58,237),  'text': (255,255,255), 'label': 'G'},
            'colorless':{'bg': (100,116,139), 'text': (255,255,255), 'label': 'C'},
        },
    },
    'tritanopia': {
        'bracket': {
            1: (34, 197, 94),    # green-500
            2: (251, 113, 133),  # rose-400
            3: (167, 139, 250),  # violet-400
            4: (249, 115, 22),   # orange-500
            5: (220, 38, 38),    # red-600
        },
        'speed': {
            'Turbo':        {'bg': (45,8,8),    'border': (153,27,27),  'text': (252,165,165)},
            'Fast':         {'bg': (45,16,0),   'border': (154,52,18),  'text': (253,186,116)},
            'Steady':       {'bg': (30,15,50),  'border': (109,40,217), 'text': (196,181,253)},
            'Slow':         {'bg': (50,10,20),  'border': (190,18,60),  'text': (253,164,175)},
            'Battlecruiser':{'bg': (30,41,59),  'border': (71,85,105),  'text': (148,163,184)},
        },
        'color_badge': {
            'white':    {'bg': (254,215,170), 'text': (124,45,18),  'label': 'W'},
            'blue':     {'bg': (109,40,217),  'text': (255,255,255), 'label': 'U'},
            'black':    {'bg': (71,85,105),   'text': (255,255,255), 'label': 'B'},
            'red':      {'bg': (225,29,72),   'text': (255,255,255), 'label': 'R'},
            'green':    {'bg': (22,163,74),   'text': (255,255,255), 'label': 'G'},
            'colorless':{'bg': (100,116,139), 'text': (255,255,255), 'label': 'C'},
        },
    },
}


def font(path, size):
    return ImageFont.truetype(path, size * SCALE)


def draw_badge(draw, x, y, text, bg, border, fg, fnt):
    pad_x, pad_y = 10 * SCALE, 5 * SCALE
    bbox = draw.textbbox((0, 0), text, font=fnt, anchor='mm')
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    bw = tw + pad_x * 2
    bh = th + pad_y * 2
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=4, fill=bg, outline=border, width=1)
    draw.text((x + bw // 2, y + bh // 2), text, font=fnt, fill=fg, anchor='mm')
    return bw


def generate_export_jpeg(analysis, color_mode='deuteranopia'):
    palette = PALETTES.get(color_mode, PALETTES['deuteranopia'])
    BRACKET_COLOR = palette['bracket']
    SPEED_STYLE   = palette['speed']
    COLOR_BADGE   = palette['color_badge']

    bracket_data = analysis.get('bracket')
    bracket = bracket_data if bracket_data and not bracket_data.get('error') else None
    mana_curve = analysis.get('mana_curve', {})
    max_count = max([int(v) for v in mana_curve.values()] + [1])

    combos_preview = (bracket_data.get('combos') or []) if bracket_data and not bracket_data.get('error') else []
    _badge_h = int(11 * SCALE) + 10 * SCALE * 2  # matches draw_badge: font size + 2x pad_y
    h = PAD
    h += 30 * SCALE
    h += 18 * SCALE
    h += 10 * SCALE
    h += _badge_h + 10 * SCALE  # badge row advance (was 18*SCALE, now matches actual)
    h += 14 * SCALE
    h += 46 * SCALE
    h += 14 * SCALE
    if combos_preview:
        h += 16 * SCALE
        for c in combos_preview:
            h += 14 * SCALE
            h += len(c.get('lines', [])) * 12 * SCALE
            h += 4 * SCALE
        h += 4 * SCALE
        h += 14 * SCALE
    h += 100 * SCALE
    h += 14 * SCALE
    h += 30 * SCALE
    h += PAD

    img = Image.new('RGB', (W, h), color=BG)
    draw = ImageDraw.Draw(img)

    # Commander art thumbnail
    ART_W = 90 * SCALE
    ART_H = 63 * SCALE
    TEXT_X = PAD
    commander_data = analysis.get('commander') or {}
    art_url = (commander_data.get('image_uris') or {}).get('art_crop')
    if not art_url and commander_data.get('name'):
        art_url = f"https://api.scryfall.com/cards/named?exact={urllib.parse.quote(commander_data['name'])}&format=image&version=art_crop"
    if art_url:
        try:
            resp = httpx.get(art_url, follow_redirects=True, timeout=6, headers={'User-Agent': 'pod-calibrator/1.0'})
            resp.raise_for_status()
            art = Image.open(BytesIO(resp.content)).convert('RGB').resize((ART_W, ART_H), Image.LANCZOS)
            img.paste(art, (PAD, PAD))
            draw.rectangle([PAD, PAD, PAD + ART_W, PAD + ART_H], outline=BORDER, width=1)
            TEXT_X = PAD + ART_W + 10 * SCALE
        except Exception:
            pass

    f_name        = font(FONT_BOLD,  22)
    f_sub         = font(FONT_REG,   11)
    f_tiny        = font(FONT_REG,    9)
    f_badge       = font(FONT_BOLD,  11)
    f_stat        = font(FONT_BLACK, 26)
    f_label       = font(FONT_BOLD,   9)
    f_brack       = font(FONT_BLACK, 38)
    f_brack_label = font(FONT_BOLD,  11)
    f_bar         = font(FONT_REG,    9)

    CONTENT_W = W - PAD * 2
    y = PAD

    # --- HEADER ---
    commander = commander_data.get('name', 'Deck')
    draw.text((TEXT_X, y), commander, font=f_name, fill=GOLD)
    y += int(f_name.size * 1.3)

    draw.text((TEXT_X, y), f"{analysis['card_count']} cards, avg CMC {analysis['avg_cmc']}", font=f_sub, fill=MUTED)
    y += int(f_sub.size * 1.4)

    if analysis.get('speed'):
        spd = analysis['speed']
        draw.text((TEXT_X, y), f"{spd['avg_nonland_cmc']} non-land avg, {spd['ramp_count']} ramp pieces", font=f_tiny, fill=MUTED)
        y += int(f_tiny.size * 1.4)

    # Ensure y clears the commander art thumbnail
    if TEXT_X > PAD:
        y = max(y, PAD + ART_H + 4 * SCALE)

    if bracket:
        bc = BRACKET_COLOR.get(bracket['bracket'], GOLD)
        bx = W - PAD - 80 * SCALE
        by = PAD
        line_h = int(f_brack.size * 1.15)
        bar_x = bx - 10 * SCALE
        draw.rectangle([bar_x, by, bar_x + 4 * SCALE, by + line_h + 40 * SCALE], fill=bc)
        draw.text((bx, by), 'BRACKET', font=font(FONT_BOLD, 9), fill=MUTED)
        draw.text((bx, by + 6 * SCALE), str(bracket['bracket']), font=f_brack, fill=bc)
        draw.text((bx, by + 6 * SCALE + line_h), bracket['bracket_label'], font=f_brack_label, fill=TEXT)
        draw.text((bx, by + 6 * SCALE + line_h + 16 * SCALE), f"{bracket['game_changer_count']} GC{'s' if bracket['game_changer_count'] != 1 else ''}", font=font(FONT_REG, 9), fill=MUTED)

    y += 4 * SCALE

    # --- BADGES ---
    bx = PAD
    if analysis.get('speed'):
        s = SPEED_STYLE.get(analysis['speed']['label'], SPEED_STYLE['Battlecruiser'])
        bw = draw_badge(draw, bx, y, analysis['speed']['label'], s['bg'], s['border'], s['text'], f_badge)
        bx += bw + 6 * SCALE
    for wc in (analysis.get('win_conditions') or []):
        bw = draw_badge(draw, bx, y, wc, SURFACE, BORDER, TEXT, f_badge)
        bx += bw + 6 * SCALE

    badge_h = int(f_badge.size) + 10 * SCALE * 2  # font height + top+bottom padding
    y += badge_h + 10 * SCALE  # clear badge + gap before divider

    # --- DIVIDER ---
    draw.line([(PAD, y), (W - PAD, y)], fill=BORDER, width=1)
    y += 12 * SCALE

    # --- INTERACTION STATS ---
    if analysis.get('interaction'):
        stats = [
            ('Removal',  analysis['interaction']['removal']),
            ('Wipes',    analysis['interaction']['board_wipes']),
            ('Counters', analysis['interaction']['counterspells']),
            ('Tutors',   analysis['interaction']['tutors']),
        ]
        col_w = CONTENT_W // 4
        row_h = int(f_stat.size * 1.0) + int(f_label.size * 1.5) + 12 * SCALE
        mid_y = y + row_h // 2
        for i, (label, value) in enumerate(stats):
            cx = PAD + i * col_w + col_w // 2
            draw.text((cx, mid_y - 4 * SCALE), str(value), font=f_stat, fill=TEXT, anchor='mb')
            draw.text((cx, mid_y + 6 * SCALE), label.upper(), font=f_label, fill=MUTED, anchor='mt')
            if i > 0:
                line_x = PAD + i * col_w
                draw.line([(line_x, y), (line_x, y + row_h)], fill=BORDER, width=1)
        y += row_h

    # --- COMBOS ---
    combos = (bracket.get('combos') or []) if bracket else []
    if combos:
        draw.line([(PAD, y), (W - PAD, y)], fill=BORDER, width=1)
        y += 12 * SCALE

        f_combo_label = font(FONT_BOLD, 8)
        f_combo_text  = font(FONT_REG, 9)

        draw.text((PAD, y), f'COMBOS ({len(combos)})', font=f_combo_label, fill=MUTED)
        y += int(f_combo_label.size * 1.5)

        for combo in combos:
            lines = combo.get('lines', [])
            produces = ', '.join(combo.get('produces', []))
            max_w = CONTENT_W - 20 * SCALE

            prod_text = '-> ' + produces
            while draw.textbbox((0, 0), prod_text, font=f_combo_text)[2] > max_w:
                prod_text = prod_text[:max(0, len(prod_text) - 4)] + '...'
            draw.text((PAD, y), prod_text, font=f_combo_text, fill=MUTED)
            y += int(f_combo_text.size * 1.4)

            for line in lines:
                cards_text = ' + '.join(line)
                while draw.textbbox((0, 0), cards_text, font=f_combo_text)[2] > max_w:
                    parts = cards_text.rsplit(' + ', 1)
                    if len(parts) == 1:
                        cards_text = cards_text[:max(0, len(cards_text) - 4)] + '...'
                        break
                    cards_text = parts[0] + ' + ...'
                draw.text((PAD + 8 * SCALE, y), cards_text, font=f_combo_text, fill=TEXT)
                y += int(f_combo_text.size * 1.3)

            y += 4 * SCALE

        y += 4 * SCALE

    # --- DIVIDER ---
    draw.line([(PAD, y), (W - PAD, y)], fill=BORDER, width=1)
    y += 14 * SCALE

    # --- MANA CURVE ---
    draw.text((PAD, y), 'MANA CURVE', font=f_label, fill=MUTED)
    y += int(f_label.size * 1.6)

    BAR_GAP   = 5 * SCALE
    BAR_W     = (CONTENT_W - BAR_GAP * 7) // 8
    BAR_MAX_H = 60 * SCALE
    bar_base_y = y + BAR_MAX_H + 14 * SCALE

    for i in range(8):
        count = int(mana_curve.get(str(i), 0))
        bar_h = max(4, int(count / max_count * BAR_MAX_H)) if count > 0 else 0
        bx = PAD + i * (BAR_W + BAR_GAP)

        if bar_h > 0:
            draw.rounded_rectangle([bx, bar_base_y - bar_h, bx + BAR_W, bar_base_y], radius=3, fill=GOLD)

        if count > 0:
            cbbox = draw.textbbox((0, 0), str(count), font=f_bar)
            cw = cbbox[2] - cbbox[0]
            draw.text((bx + BAR_W // 2 - cw // 2, bar_base_y - bar_h - int(f_bar.size * 1.4)), str(count), font=f_bar, fill=MUTED)

        label = '7+' if i == 7 else str(i)
        lbbox = draw.textbbox((0, 0), label, font=f_bar)
        lw = lbbox[2] - lbbox[0]
        draw.text((bx + BAR_W // 2 - lw // 2, bar_base_y + 4), label, font=f_bar, fill=MUTED)

    y = bar_base_y + int(f_bar.size * 1.6) + 8 * SCALE

    # --- DIVIDER ---
    draw.line([(PAD, y), (W - PAD, y)], fill=BORDER, width=1)
    y += 12 * SCALE

    # --- FOOTER: color badges ---
    fx = PAD
    deck_colors = analysis.get('colors', {})
    is_colorless_only = all(c == 'colorless' for c in deck_colors)
    # Fixed square badge size so all color symbols are identical
    badge_w = 22 * SCALE
    badge_h = 22 * SCALE

    for color, data in COLOR_BADGE.items():
        if color not in deck_colors:
            continue
        if color == 'colorless' and not is_colorless_only:
            continue
        draw.rounded_rectangle([fx, y, fx + badge_w, y + badge_h], radius=4, fill=data['bg'])
        draw.text((fx + badge_w // 2, y + badge_h // 2), data['label'], font=f_badge, fill=data['text'], anchor='mm')
        fx += badge_w + 5 * SCALE

    branding = 'pod-calibrator'
    bbbox = draw.textbbox((0, 0), branding, font=font(FONT_REG, 11))
    bw = bbbox[2] - bbbox[0]
    draw.text((W - PAD - bw, y + 3), branding, font=font(FONT_REG, 11), fill=(30, 58, 95))

    final_h = y + badge_h + 6 * SCALE
    img = img.crop((0, 0, W, final_h))

    output = BytesIO()
    img.save(output, format='JPEG', quality=92)
    output.seek(0)
    return output
