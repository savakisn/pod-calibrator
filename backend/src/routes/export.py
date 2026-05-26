from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

SCALE = 2
W = 640 * SCALE
PAD = 28 * SCALE

BG       = (15, 23, 42)
SURFACE  = (30, 41, 59)
BORDER   = (51, 65, 85)
TEXT     = (226, 232, 240)
MUTED    = (100, 116, 139)
GOLD     = (245, 158, 11)

BRACKET_COLOR = {
    1: (20, 184, 166),   # teal  — red/green colorblind safe
    2: (59, 130, 246),   # blue
    3: (234, 179, 8),    # yellow
    4: (249, 115, 22),   # orange
    5: (217, 70, 239),   # fuchsia — red/green colorblind safe
}

SPEED_STYLE = {
    'Turbo':        {'bg': (45,8,8),    'border': (153,27,27),  'text': (252,165,165)},
    'Fast':         {'bg': (45,16,0),   'border': (154,52,18),  'text': (253,186,116)},
    'Steady':       {'bg': (45,26,0),   'border': (146,64,14),  'text': (253,230,138)},
    'Slow':         {'bg': (12,26,58),  'border': (29,78,216),  'text': (147,197,253)},
    'Battlecruiser':{'bg': (30,41,59),  'border': (71,85,105),  'text': (148,163,184)},
}

COLOR_BADGE = {
    'white':    {'bg': (254,243,199), 'text': (120,53,15),  'label': 'W'},
    'blue':     {'bg': (37,99,235),   'text': (255,255,255),'label': 'U'},
    'black':    {'bg': (71,85,105),   'text': (255,255,255),'label': 'B'},
    'red':      {'bg': (220,38,38),   'text': (255,255,255),'label': 'R'},
    'green':    {'bg': (22,163,74),   'text': (255,255,255),'label': 'G'},
    'colorless':{'bg': (100,116,139), 'text': (255,255,255),'label': 'C'},
}

FONT_REG   = '/usr/share/fonts/noto/NotoSans-Regular.ttf'
FONT_BOLD  = '/usr/share/fonts/noto/NotoSans-Bold.ttf'
FONT_BLACK = '/usr/share/fonts/noto/NotoSans-Black.ttf'

def font(path, size):
    return ImageFont.truetype(path, size * SCALE)

def draw_badge(draw, x, y, text, bg, border, fg, fnt):
    pad_x, pad_y = 10 * SCALE, 5 * SCALE
    bbox = draw.textbbox((0, 0), text, font=fnt, anchor='lt')
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    bw = tw + pad_x * 2
    bh = th + pad_y * 2
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=4, fill=bg, outline=border, width=1)
    # vertically center text in badge
    draw.text((x + pad_x, y + bh // 2), text, font=fnt, fill=fg, anchor='lm')
    return bw

def generate_export_jpeg(analysis):
    bracket_data = analysis.get('bracket')
    bracket = bracket_data if bracket_data and not bracket_data.get('error') else None
    mana_curve = analysis.get('mana_curve', {})
    max_count = max([int(v) for v in mana_curve.values()] + [1])

    # --- estimate height ---
    combos_preview = (bracket_data.get('combos') or []) if bracket_data and not bracket_data.get('error') else []
    h = PAD
    h += 30 * SCALE              # commander name
    h += 18 * SCALE              # card count + speed info
    h += 10 * SCALE              # gap
    h += 18 * SCALE              # badges row
    h += 14 * SCALE              # gap + divider
    h += 46 * SCALE              # interaction stats
    h += 14 * SCALE              # gap + divider
    if combos_preview:
        h += 16 * SCALE                          # COMBOS header
        for c in combos_preview:
            h += 14 * SCALE                      # produces line per combo
            h += len(c.get('lines', [])) * 12 * SCALE  # each card-pair line
            h += 4 * SCALE                       # gap after combo
        h += 4 * SCALE                           # trailing gap
        h += 14 * SCALE                          # divider
    h += 100 * SCALE             # mana curve
    h += 14 * SCALE              # gap + divider
    h += 30 * SCALE              # footer
    h += PAD

    img = Image.new('RGB', (W, h), color=BG)
    draw = ImageDraw.Draw(img)

    f_name   = font(FONT_BOLD,  22)
    f_sub    = font(FONT_REG,   11)
    f_tiny   = font(FONT_REG,    9)
    f_badge  = font(FONT_BOLD,  11)
    f_stat   = font(FONT_BLACK, 26)
    f_label  = font(FONT_BOLD,   9)
    f_brack  = font(FONT_BLACK, 38)
    f_brack_label = font(FONT_BOLD, 11)
    f_bar    = font(FONT_REG,    9)

    CONTENT_W = W - PAD * 2

    y = PAD

    # --- HEADER ---
    commander = analysis.get('commander', {}).get('name', 'Deck')
    draw.text((PAD, y), commander, font=f_name, fill=GOLD)
    y += int(f_name.size * 1.3)

    draw.text((PAD, y), f"{analysis['card_count']} cards · avg CMC {analysis['avg_cmc']}", font=f_sub, fill=MUTED)
    y += int(f_sub.size * 1.4)

    if analysis.get('speed'):
        spd = analysis['speed']
        draw.text((PAD, y), f"{spd['avg_nonland_cmc']} non-land avg · {spd['ramp_count']} ramp", font=f_tiny, fill=MUTED)
        y += int(f_tiny.size * 1.4)

    # Bracket on the right — draw alongside header
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

    y += 10 * SCALE

    # --- BADGES ---
    bx = PAD
    if analysis.get('speed'):
        s = SPEED_STYLE.get(analysis['speed']['label'], SPEED_STYLE['Battlecruiser'])
        bw = draw_badge(draw, bx, y, analysis['speed']['label'], s['bg'], s['border'], s['text'], f_badge)
        bx += bw + 6 * SCALE
    for wc in (analysis.get('win_conditions') or []):
        bw = draw_badge(draw, bx, y, wc, SURFACE, BORDER, TEXT, f_badge)
        bx += bw + 6 * SCALE

    y += 28 * SCALE

    # --- DIVIDER ---
    draw.line([(PAD, y), (W - PAD, y)], fill=BORDER, width=1)
    y += 16 * SCALE

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
            # draw number centered vertically in top half, label in bottom half
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

            # produces header for this combo group
            prod_text = '-> ' + produces
            while draw.textbbox((0,0), prod_text, font=f_combo_text)[2] > max_w:
                prod_text = prod_text[:max(0, len(prod_text)-4)] + '...'
            draw.text((PAD, y), prod_text, font=f_combo_text, fill=MUTED)
            y += int(f_combo_text.size * 1.4)

            # each line is a distinct card combination
            for line in lines:
                cards_text = ' + '.join(line)
                while draw.textbbox((0,0), cards_text, font=f_combo_text)[2] > max_w:
                    parts = cards_text.rsplit(' + ', 1)
                    if len(parts) == 1:
                        cards_text = cards_text[:max(0, len(cards_text)-4)] + '...'
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

    BAR_GAP = 5 * SCALE
    BAR_W = (CONTENT_W - BAR_GAP * 7) // 8
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

    # --- FOOTER ---
    fx = PAD
    deck_colors = analysis.get('colors', {})
    is_colorless_only = all(c == 'colorless' for c in deck_colors)
    # fixed badge size based on 'W' so all color badges are identical dimensions
    ref_bbox = draw.textbbox((0, 0), 'W', font=f_badge, anchor='lt')
    pad_x, pad_y = 7 * SCALE, 5 * SCALE
    badge_w = (ref_bbox[2] - ref_bbox[0]) + pad_x * 2
    badge_h = (ref_bbox[3] - ref_bbox[1]) + pad_y * 2
    for color, data in COLOR_BADGE.items():
        if color not in deck_colors:
            continue
        if color == 'colorless' and not is_colorless_only:
            continue
        draw.rounded_rectangle([fx, y, fx + badge_w, y + badge_h], radius=4, fill=data['bg'])
        draw.text((fx + pad_x, y + badge_h // 2), data['label'], font=f_badge, fill=data['text'], anchor='lm')
        fx += badge_w + 5 * SCALE

    branding = 'pod-calibrator'
    bbbox = draw.textbbox((0, 0), branding, font=font(FONT_REG, 11))
    bw = bbbox[2] - bbbox[0]
    draw.text((W - PAD - bw, y + 3), branding, font=font(FONT_REG, 11), fill=(30, 58, 95))

    # Crop to actual content
    final_h = y + 30 * SCALE
    img = img.crop((0, 0, W, final_h))

    output = BytesIO()
    img.save(output, format='JPEG', quality=92)
    output.seek(0)
    return output
