import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

# Official Coolors Palette
C_MAHOGANY = hex_to_rgb('#310603')
C_RUST = hex_to_rgb('#7D1B05')
C_BRONZE = hex_to_rgb('#B6580B')
C_MARIGOLD = hex_to_rgb('#E09B17')
C_GOLD_VIVID = hex_to_rgb('#F5C538')
C_CHAMPAGNE = hex_to_rgb('#F7D160')
C_CANARY = hex_to_rgb('#FDF39D')
C_PLUM = hex_to_rgb('#360538')

def get_fonts():
    try:
        f_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 44)
        f_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 24)
        f_body = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 20)
        f_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 16)
        f_spec_val = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
    except Exception:
        f_title = f_sub = f_body = f_badge = f_spec_val = ImageFont.load_default()
    return f_title, f_sub, f_body, f_badge, f_spec_val

def create_studio_background(w, h, radial_col=(30, 36, 52)):
    bg = Image.new("RGBA", (w, h), (10, 13, 20, 255))
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    cx, cy = w // 2, h // 2
    max_r = int(math.hypot(w, h) / 2)
    for r in range(max_r, 0, -20):
        alpha = int((1 - r / max_r) ** 1.6 * 85)
        g_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(radial_col[0], radial_col[1], radial_col[2], alpha))
    return Image.alpha_composite(bg, glow)

# ==============================================================================
# MOCKUP 1: KAOS POLO & T-SHIRT RESMI (DENGAN LOGO ASLI V6)
# ==============================================================================
def generate_mockup_kaos():
    W, H = 2000, 1500
    bg = create_studio_background(W, H, (28, 22, 38))
    f_title, f_sub, f_body, f_badge, f_spec_val = get_fonts()
    
    # Load Real Logo
    logo = Image.open("assets/png/logo-symbol-color.png").convert("RGBA")
    
    # Draw Stage Surface (Matte Studio Table)
    stage = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(stage)
    s_draw.polygon([(0, 1050), (W, 1050), (W, H), (0, H)], fill=(14, 18, 28, 255))
    s_draw.line([(0, 1050), (W, 1050)], fill=(40, 48, 70, 255), width=2)
    bg = Image.alpha_composite(bg, stage)
    
    # 1. POLO SHIRT (Left) in Obsidian Mahogany (#310603)
    polo_x, polo_y, polo_w, polo_h = 240, 360, 680, 840
    polo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    p_draw = ImageDraw.Draw(polo)
    
    # Shadow
    p_draw.rounded_rectangle([polo_x - 10, polo_y + 30, polo_x + polo_w + 10, polo_y + polo_h + 30], radius=32, fill=(0, 0, 0, 140))
    polo = polo.filter(ImageFilter.GaussianBlur(radius=20))
    p_draw = ImageDraw.Draw(polo)
    
    # Body
    p_draw.rounded_rectangle([polo_x, polo_y, polo_x + polo_w, polo_y + polo_h], radius=24, fill=(35, 10, 8, 255), outline=(75, 25, 20, 255), width=3)
    
    # Collar & Placket
    col_cx = polo_x + polo_w // 2
    # Collar wings
    p_draw.polygon([(col_cx - 160, polo_y), (col_cx, polo_y + 110), (col_cx + 160, polo_y), (col_cx, polo_y + 35)], fill=(24, 6, 5, 255), outline=(90, 30, 24, 255))
    # Placket
    p_draw.rectangle([col_cx - 36, polo_y + 110, col_cx + 36, polo_y + 340], fill=(28, 8, 7, 255), outline=(80, 26, 20, 255), width=2)
    # Buttons
    p_draw.ellipse([col_cx - 8, polo_y + 160, col_cx + 8, polo_y + 176], fill=(50, 40, 30, 255), outline=C_GOLD_VIVID, width=1)
    p_draw.ellipse([col_cx - 8, polo_y + 240, col_cx + 8, polo_y + 256], fill=(50, 40, 30, 255), outline=C_GOLD_VIVID, width=1)
    
    # Embroidered REAL Logo on Left Chest (Chest position)
    chest_x = polo_x + 130
    chest_y = polo_y + 340
    emb_size = 175
    logo_emb = logo.resize((emb_size, emb_size), Image.Resampling.LANCZOS)
    
    # Add subtle golden embroidery halo/shadow
    emb_shadow = Image.new("RGBA", (emb_size, emb_size), (0, 0, 0, 0))
    emb_shadow.paste(C_GOLD_VIVID, (0, 0), mask=logo_emb.split()[3])
    emb_shadow = emb_shadow.filter(ImageFilter.GaussianBlur(radius=3))
    
    polo.paste(emb_shadow, (chest_x, chest_y), mask=emb_shadow.split()[3])
    polo.paste(logo_emb, (chest_x, chest_y), mask=logo_emb.split()[3])
    
    # Text under logo: SMAN 1 GEDEG
    p_draw.text((chest_x + emb_size // 2, chest_y + emb_size + 16), "SMAN 1 GEDEG", fill=C_GOLD_VIVID, font=f_badge, anchor="mt")
    p_draw.text((chest_x + emb_size // 2, chest_y + emb_size + 36), "PANITIA RESMI DIES NATALIS 44", fill=(210, 180, 140), font=ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 13) if hasattr(ImageFont, "truetype") else f_badge, anchor="mt")

    # 2. T-SHIRT (Right) in Jet Black (#07090F)
    t_x, t_y, t_w, t_h = 1080, 360, 680, 840
    # Shadow
    p_draw.rounded_rectangle([t_x - 10, t_y + 30, t_x + t_w + 10, t_y + t_h + 30], radius=32, fill=(0, 0, 0, 140))
    
    # Body
    p_draw.rounded_rectangle([t_x, t_y, t_x + t_w, t_y + t_h], radius=24, fill=(14, 16, 24, 255), outline=(45, 50, 70, 255), width=3)
    
    # Crewneck Rib
    t_cx = t_x + t_w // 2
    p_draw.ellipse([t_cx - 130, t_y - 45, t_cx + 130, t_y + 85], fill=(8, 10, 16, 255), outline=(60, 68, 90, 255), width=4)
    
    # Center Big Chest Print of REAL Logo
    big_size = 280
    logo_big = logo.resize((big_size, big_size), Image.Resampling.LANCZOS)
    big_x = t_cx - big_size // 2
    big_y = t_y + 240
    
    # Metallic Gold Sheen
    polo.paste(logo_big, (big_x, big_y), mask=logo_big.split()[3])
    
    p_draw.text((t_cx, big_y + big_size + 24), "DIES NATALIS KE-44", fill=(248, 250, 252), font=f_sub, anchor="mt")
    p_draw.text((t_cx, big_y + big_size + 60), "SMA NEGERI 1 GEDEG", fill=C_GOLD_VIVID, font=f_spec_val, anchor="mt")
    
    bg = Image.alpha_composite(bg, polo)
    draw = ImageDraw.Draw(bg)
    
    # Header Banner
    draw.rounded_rectangle([60, 50, 720, 150], radius=16, fill=(16, 22, 38, 240), outline=C_GOLD_VIVID, width=2)
    draw.text((90, 72), "STANDAR KAOS & POLO SHIRT RESMI", fill=(248, 250, 252), font=f_sub)
    draw.text((90, 110), "Penerapan Bordir & Sablon Lambang Master V6", fill=C_CHAMPAGNE, font=f_body)
    
    # Specs Card Bottom Left
    draw.rounded_rectangle([240, 1240, 920, 1420], radius=16, fill=(16, 22, 38, 230), outline=(60, 70, 95, 255), width=1)
    draw.text((270, 1262), "Polo Panitia: Lacoste Cotton Pique • Obsidian Mahogany (#310603)", fill=(245, 197, 56), font=f_badge)
    draw.text((270, 1295), "Bordir Dada Kiri: Benang Rayon Emas 10.000 Stitches • Ø 65 mm", fill=(220, 225, 235), font=f_badge)
    draw.text((270, 1328), "Akurasi Desain: 100% Menggunakan Vektor Master V6 Asli", fill=(148, 163, 184), font=f_badge)
    draw.text((270, 1360), "Status: Standar Resmi Civitas Akademika SMAN 1 Gedeg", fill=C_CANARY, font=f_badge)
    
    # Specs Card Bottom Right
    draw.rounded_rectangle([1080, 1240, 1760, 1420], radius=16, fill=(16, 22, 38, 230), outline=(60, 70, 95, 255), width=1)
    draw.text((1110, 1262), "T-Shirt Peserta: Cotton Combed 30s Reaktif • Jet Black (#0B0F19)", fill=(245, 197, 56), font=f_badge)
    draw.text((1110, 1295), "Sablon Dada: Sablon Plastisol Emas Metalik Berkilau • Lebar 20 cm", fill=(220, 225, 235), font=f_badge)
    draw.text((1110, 1328), "Gradasi Warna: Mengikuti Spektrum Resmi Coolors Palette", fill=(148, 163, 184), font=f_badge)
    draw.text((1110, 1360), "Status: Siap Produksi Massal Kepanitiaan", fill=C_CANARY, font=f_badge)

    out_file = "assets/mockups/mockup_kaos_polo.jpg"
    bg.convert("RGB").save(out_file, "JPEG", quality=95)
    print(f"Mockup Kaos Polo saved to: {out_file}")

# ==============================================================================
# MOCKUP 2: TUMBLER STAINLESS STEEL (DENGAN LOGO ASLI V6)
# ==============================================================================
def generate_mockup_tumbler():
    W, H = 2000, 1500
    bg = create_studio_background(W, H, (40, 20, 45))
    f_title, f_sub, f_body, f_badge, f_spec_val = get_fonts()
    
    # Load Real Logo
    logo = Image.open("assets/png/logo-symbol-color.png").convert("RGBA")
    
    # Surface
    stage = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(stage)
    s_draw.polygon([(0, 1100), (W, 1100), (W, H), (0, H)], fill=(12, 14, 22, 255))
    s_draw.line([(0, 1100), (W, 1100)], fill=(50, 40, 65, 255), width=2)
    bg = Image.alpha_composite(bg, stage)
    
    # Tumbler Cylinder dimensions
    t_cx = 900
    t_top = 340
    t_w = 420
    t_h = 820
    t_x1 = t_cx - t_w // 2
    t_x2 = t_cx + t_w // 2
    t_bot = t_top + t_h
    
    tumbler = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tumbler)
    
    # Drop Shadow
    t_draw.ellipse([t_cx - 260, t_bot - 40, t_cx + 260, t_bot + 60], fill=(0, 0, 0, 180))
    tumbler = tumbler.filter(ImageFilter.GaussianBlur(radius=25))
    t_draw = ImageDraw.Draw(tumbler)
    
    # Cap / Lid
    lid_top = t_top - 140
    # Handle loop
    t_draw.rounded_rectangle([t_cx - 80, lid_top - 60, t_cx + 80, lid_top + 40], radius=30, fill=(35, 38, 48, 255), outline=(70, 75, 95, 255), width=5)
    # Lid main body
    t_draw.rounded_rectangle([t_x1 + 40, lid_top, t_x2 - 40, t_top], radius=18, fill=(28, 30, 40, 255), outline=(65, 70, 88, 255), width=3)
    
    # Shaded Metallic Body with Cylindrical Gradient
    # Matte Black to Midnight Plum tint (#360538)
    for col in range(t_x1, t_x2):
        u = (col - t_x1) / t_w
        # Cylindrical lighting profile
        light = math.sin(u * math.pi) ** 1.8
        specular = math.exp(-((u - 0.32) ** 2) / 0.015) * 0.4
        
        # Base color blend: midnight plum / dark slate
        r_val = int(22 * light + 200 * specular + 15 * (1 - u))
        g_val = int(14 * light + 190 * specular + 8 * (1 - u))
        b_val = int(32 * light + 210 * specular + 20 * (1 - u))
        
        r_val = min(255, max(0, r_val))
        g_val = min(255, max(0, g_val))
        b_val = min(255, max(0, b_val))
        
        t_draw.line([(col, t_top), (col, t_bot)], fill=(r_val, g_val, b_val, 255), width=1)
        
    # Rounded base
    t_draw.ellipse([t_x1, t_bot - 30, t_x2, t_bot + 30], fill=(22, 18, 30, 255), outline=(65, 70, 90, 255), width=2)
    
    # Overlay Laser Engraved REAL Logo on Tumbler
    logo_tumbler_size = 260
    logo_t = logo.resize((logo_tumbler_size, logo_tumbler_size), Image.Resampling.LANCZOS)
    
    # Gold Laser Sheen
    lt_x = t_cx - logo_tumbler_size // 2
    lt_y = t_top + 210
    
    tumbler.paste(logo_t, (lt_x, lt_y), mask=logo_t.split()[3])
    
    # Typography Engraved underneath
    t_draw.text((t_cx, lt_y + logo_tumbler_size + 24), "DIES NATALIS 44", fill=C_GOLD_VIVID, font=f_sub, anchor="mt")
    t_draw.text((t_cx, lt_y + logo_tumbler_size + 62), "SMA NEGERI 1 GEDEG", fill=C_CHAMPAGNE, font=f_spec_val, anchor="mt")
    t_draw.text((t_cx, lt_y + logo_tumbler_size + 98), "EST. 1980 • MOJOKERTO", fill=(190, 195, 205), font=f_badge, anchor="mt")
    
    bg = Image.alpha_composite(bg, tumbler)
    draw = ImageDraw.Draw(bg)
    
    # Header Banner
    draw.rounded_rectangle([60, 50, 780, 150], radius=16, fill=(16, 22, 38, 240), outline=C_GOLD_VIVID, width=2)
    draw.text((90, 72), "TUMBLER TERMAL STAINLESS STEEL RESMI", fill=(248, 250, 252), font=f_sub)
    draw.text((90, 110), "Laser Engraving Logam & UV Foil Emas Master V6", fill=C_CHAMPAGNE, font=f_body)
    
    # Specifications Side Card (Right)
    draw.rounded_rectangle([1320, 360, 1920, 880], radius=20, fill=(16, 22, 38, 240), outline=C_GOLD_VIVID, width=2)
    draw.text((1360, 400), "SPESIFIKASI PRODUKSI RESMI", fill=(248, 250, 252), font=f_sub)
    draw.line([(1360, 445), (1880, 445)], fill=(60, 70, 95, 255), width=1)
    
    specs = [
        ("Material Bodi:", "Double-Wall Vacuum Insulated SUS 304"),
        ("Kapasitas Volume:", "500 ml • Tahan Panas / Dingin 12 Jam"),
        ("Warna Tabung:", "Matte Black & Midnight Plum (#360538)"),
        ("Teknik Aplikasi:", "Fiber Laser Engraving / UV Gold Foil"),
        ("Tinggi Lambang:", "80 mm (Proporsi Presisi Master V6)"),
        ("Keunggulan Desain:", "Garis Medial Spine 100% Simetris"),
        ("Peruntukan:", "Cendera Mata Tamu VIP & Panitia Inti")
    ]
    cur_y = 470
    for label, val in specs:
        draw.text((1360, cur_y), label, fill=C_GOLD_VIVID, font=f_badge)
        draw.text((1360, cur_y + 24), val, fill=(225, 230, 240), font=f_body)
        cur_y += 58

    out_file = "assets/mockups/mockup_tumbler.jpg"
    bg.convert("RGB").save(out_file, "JPEG", quality=95)
    print(f"Mockup Tumbler saved to: {out_file}")

# ==============================================================================
# MOCKUP 3: LANYARD & ID CARD PANITIA (DENGAN LOGO ASLI V6)
# ==============================================================================
def generate_mockup_lanyard():
    W, H = 2000, 1500
    bg = create_studio_background(W, H, (45, 15, 45))
    f_title, f_sub, f_body, f_badge, f_spec_val = get_fonts()
    
    logo = Image.open("assets/png/logo-symbol-color.png").convert("RGBA")
    
    # Wooden/Slate Tabletop
    stage = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(stage)
    s_draw.rectangle([0, 0, W, H], fill=(18, 16, 22, 255))
    bg = Image.alpha_composite(bg, stage)
    
    lanyard = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    l_draw = ImageDraw.Draw(lanyard)
    
    # 1. LANYARD STRAP (Midnight Plum #360538 Satin Ribbon)
    # Curved Path for realistic strap
    strap_w = 90
    pts_left = [(200, -50), (450, 280), (700, 560), (900, 760), (1000, 840)]
    pts_right = [(1800, -50), (1550, 280), (1300, 560), (1100, 760), (1000, 840)]
    
    # Draw Ribbon shadow
    l_draw.line(pts_left, fill=(0, 0, 0, 160), width=strap_w + 20)
    l_draw.line(pts_right, fill=(0, 0, 0, 160), width=strap_w + 20)
    lanyard = lanyard.filter(ImageFilter.GaussianBlur(radius=18))
    l_draw = ImageDraw.Draw(lanyard)
    
    # Draw Midnight Plum Satin Ribbon Body
    l_draw.line(pts_left, fill=C_PLUM, width=strap_w)
    l_draw.line(pts_right, fill=C_PLUM, width=strap_w)
    
    # Highlights along ribbon edges
    l_draw.line(pts_left, fill=(120, 25, 110, 180), width=4)
    l_draw.line(pts_right, fill=(120, 25, 110, 180), width=4)
    
    # Repeating Logo & Text on Ribbon
    small_logo_size = 60
    logo_small = logo.resize((small_logo_size, small_logo_size), Image.Resampling.LANCZOS)
    
    lanyard.paste(logo_small, (380, 220), mask=logo_small.split()[3])
    lanyard.paste(logo_small, (1540, 220), mask=logo_small.split()[3])
    
    l_draw.text((470, 240), "DIES NATALIS 44 • SMAN 1 GEDEG", fill=C_GOLD_VIVID, font=f_badge)
    l_draw.text((1200, 240), "DIES NATALIS 44 • SMAN 1 GEDEG", fill=C_GOLD_VIVID, font=f_badge)
    
    # Metal Clip & Swivel Hook at (1000, 840)
    l_draw.rounded_rectangle([960, 820, 1040, 880], radius=12, fill=(180, 185, 200, 255), outline=(230, 235, 245, 255), width=3)
    l_draw.ellipse([980, 870, 1020, 920], fill=(130, 135, 150, 255), outline=(210, 215, 230, 255), width=3)
    
    # 2. PVC ID CARD
    id_w, id_h = 560, 840
    id_x = 1000 - id_w // 2
    id_y = 910
    
    # Card Shadow
    l_draw.rounded_rectangle([id_x - 12, id_y + 15, id_x + id_w + 12, id_y + id_h + 15], radius=28, fill=(0, 0, 0, 160))
    lanyard = lanyard.filter(ImageFilter.GaussianBlur(radius=20))
    l_draw = ImageDraw.Draw(lanyard)
    
    # Card Body (Dark Obsidian with Gold Border)
    l_draw.rounded_rectangle([id_x, id_y, id_x + id_w, id_y + id_h], radius=24, fill=(16, 22, 38, 255), outline=C_GOLD_VIVID, width=4)
    
    # Card Top Header
    l_draw.rounded_rectangle([id_x + 10, id_y + 10, id_x + id_w - 10, id_y + 130], radius=16, fill=(28, 12, 34, 255), outline=C_BRONZE, width=1)
    
    # Real Logo on ID Card Top
    id_logo_size = 85
    logo_id = logo.resize((id_logo_size, id_logo_size), Image.Resampling.LANCZOS)
    lanyard.paste(logo_id, (id_x + 30, id_y + 25), mask=logo_id.split()[3])
    
    l_draw.text((id_x + 130, id_y + 40), "SMA NEGERI 1 GEDEG", fill=(248, 250, 252), font=f_sub)
    l_draw.text((id_x + 130, id_y + 75), "PANITIA DIES NATALIS KE-44", fill=C_GOLD_VIVID, font=f_badge)
    
    # Participant Photo Box
    p_box_w, p_box_h = 240, 290
    p_bx = id_x + id_w // 2 - p_box_w // 2
    p_by = id_y + 160
    l_draw.rounded_rectangle([p_bx, p_by, p_bx + p_box_w, p_by + p_box_h], radius=16, fill=(24, 30, 48, 255), outline=C_GOLD_VIVID, width=2)
    l_draw.text((id_x + id_w // 2, p_by + p_box_h // 2 - 10), "PAS FOTO 3X4", fill=(148, 163, 184), font=f_badge, anchor="mm")
    
    # Participant Info
    l_draw.text((id_x + id_w // 2, id_y + 480), "ARDIAN RYAN SANTOSO", fill=(248, 250, 252), font=f_sub, anchor="mt")
    l_draw.rounded_rectangle([id_x + 100, id_y + 530, id_x + id_w - 100, id_y + 575], radius=12, fill=C_GOLD_VIVID)
    l_draw.text((id_x + id_w // 2, id_y + 552), "KOORDINATOR PELAKSANA", fill=(10, 12, 20), font=f_spec_val, anchor="mm")
    
    l_draw.text((id_x + id_w // 2, id_y + 605), "DIVISI PUBLIKASI & DOKUMENTASI", fill=C_CHAMPAGNE, font=f_body, anchor="mt")
    l_draw.text((id_x + id_w // 2, id_y + 640), "ID: DN44-SMAN1G-2024-001", fill=(148, 163, 184), font=f_badge, anchor="mt")
    
    # Barcode representation
    l_draw.rectangle([id_x + 80, id_y + 700, id_x + id_w - 80, id_y + 760], fill=(240, 245, 255, 255))
    for b in range(id_x + 95, id_x + id_w - 95, 8):
        l_draw.line([(b, id_y + 705), (b, id_y + 755)], fill=(15, 18, 25, 255), width=3 if b % 16 == 0 else 1)
        
    bg = Image.alpha_composite(bg, lanyard)
    draw = ImageDraw.Draw(bg)
    
    # Title Top Left
    draw.rounded_rectangle([60, 50, 760, 150], radius=16, fill=(16, 22, 38, 240), outline=C_GOLD_VIVID, width=2)
    draw.text((90, 72), "LANYARD & ID CARD KEPANITIAAN", fill=(248, 250, 252), font=f_sub)
    draw.text((90, 110), "Pita Satin Midnight Plum & Kartu PVC Master V6", fill=C_CHAMPAGNE, font=f_body)

    out_file = "assets/mockups/mockup_lanyard_idcard.jpg"
    bg.convert("RGB").save(out_file, "JPEG", quality=95)
    print(f"Mockup Lanyard saved to: {out_file}")

# ==============================================================================
# MOCKUP 4: TOTE BAG KANVAS & ENAMEL PIN 24K (DENGAN LOGO ASLI V6)
# ==============================================================================
def generate_mockup_totebag():
    W, H = 2000, 1500
    bg = create_studio_background(W, H, (35, 30, 25))
    f_title, f_sub, f_body, f_badge, f_spec_val = get_fonts()
    
    logo = Image.open("assets/png/logo-symbol-color.png").convert("RGBA")
    
    # Table surface
    stage = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(stage)
    s_draw.rectangle([0, 0, W, H], fill=(22, 18, 16, 255))
    bg = Image.alpha_composite(bg, stage)
    
    item_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(item_layer)
    
    # 1. CANVAS TOTE BAG (Left) in Natural Cream Off-White
    tb_x, tb_y, tb_w, tb_h = 180, 420, 760, 880
    
    # Handles
    i_draw.rounded_rectangle([tb_x + 160, 180, tb_x + 220, tb_y + 60], radius=30, fill=(235, 230, 220, 255), outline=(190, 180, 165, 255), width=2)
    i_draw.rounded_rectangle([tb_x + tb_w - 220, 180, tb_x + tb_w - 160, tb_y + 60], radius=30, fill=(235, 230, 220, 255), outline=(190, 180, 165, 255), width=2)
    
    # Shadow
    i_draw.rounded_rectangle([tb_x - 15, tb_y + 25, tb_x + tb_w + 15, tb_y + tb_h + 25], radius=28, fill=(0, 0, 0, 140))
    item_layer = item_layer.filter(ImageFilter.GaussianBlur(radius=20))
    i_draw = ImageDraw.Draw(item_layer)
    
    # Canvas Body (Natural Broken White)
    i_draw.rounded_rectangle([tb_x, tb_y, tb_x + tb_w, tb_y + tb_h], radius=20, fill=(245, 240, 230, 255), outline=(210, 200, 185, 255), width=3)
    # Stitches border
    i_draw.rounded_rectangle([tb_x + 18, tb_y + 18, tb_x + tb_w - 18, tb_y + tb_h - 18], radius=16, outline=(200, 190, 175, 255), width=1)
    
    # Print Real Master Logo in Center of Tote Bag
    tb_logo_size = 380
    logo_tb = logo.resize((tb_logo_size, tb_logo_size), Image.Resampling.LANCZOS)
    tb_lx = tb_x + tb_w // 2 - tb_logo_size // 2
    tb_ly = tb_y + 160
    
    item_layer.paste(logo_tb, (tb_lx, tb_ly), mask=logo_tb.split()[3])
    
    # Typography Screenprint underneath
    tb_cx = tb_x + tb_w // 2
    i_draw.text((tb_cx, tb_ly + tb_logo_size + 24), "DIES NATALIS KE-44", fill=C_MAHOGANY, font=f_sub, anchor="mt")
    i_draw.text((tb_cx, tb_ly + tb_logo_size + 64), "SMA NEGERI 1 GEDEG", fill=C_BRONZE, font=f_spec_val, anchor="mt")
    i_draw.text((tb_cx, tb_ly + tb_logo_size + 104), "1980 – 2024 • MOJOKERTO", fill=(120, 100, 90), font=f_badge, anchor="mt")

    # 2. ENAMEL PIN 24K ON VELVET CARD (Right)
    pin_cx = 1480
    pin_cy = 780
    
    # Midnight Plum Velvet Display Card
    card_w, card_h = 580, 580
    c_x1 = pin_cx - card_w // 2
    c_y1 = pin_cy - card_h // 2
    
    # Velvet card shadow
    i_draw.rounded_rectangle([c_x1 - 10, c_y1 + 20, c_x1 + card_w + 10, c_y1 + card_h + 20], radius=28, fill=(0, 0, 0, 160))
    # Velvet card body in Midnight Plum (#360538)
    i_draw.rounded_rectangle([c_x1, c_y1, c_x1 + card_w, c_y1 + card_h], radius=24, fill=C_PLUM, outline=C_GOLD_VIVID, width=3)
    
    # Velvet Card Text
    i_draw.text((pin_cx, c_y1 + 45), "LENCANA PIN KEHORMATAN 24K", fill=C_CHAMPAGNE, font=f_spec_val, anchor="mt")
    i_draw.text((pin_cx, c_y1 + 80), "EDISI TERBATAS DIES NATALIS 44", fill=(210, 175, 220), font=f_badge, anchor="mt")
    
    # Enamel Pin Badge: REAL LOGO die-struck in 24K Gold
    pin_size = 320
    logo_pin = logo.resize((pin_size, pin_size), Image.Resampling.LANCZOS)
    p_lx = pin_cx - pin_size // 2
    p_ly = pin_cy - pin_size // 2 + 30
    
    # Glowing gold rim behind pin
    for r in range(pin_size // 2 + 25, pin_size // 2, -3):
        i_draw.ellipse([pin_cx - r, pin_cy + 30 - r, pin_cx + r, pin_cy + 30 + r], fill=(245, 197, 56, 12))
        
    item_layer.paste(logo_pin, (p_lx, p_ly), mask=logo_pin.split()[3])
    
    # Bottom Note on card
    i_draw.text((pin_cx, c_y1 + card_h - 60), "SMA NEGERI 1 GEDEG • 24K GOLD ELECTROPLATED", fill=C_GOLD_VIVID, font=f_badge, anchor="mt")
    
    bg = Image.alpha_composite(bg, item_layer)
    draw = ImageDraw.Draw(bg)
    
    # Title Banner
    draw.rounded_rectangle([60, 50, 780, 150], radius=16, fill=(16, 22, 38, 240), outline=C_GOLD_VIVID, width=2)
    draw.text((90, 72), "TAS JINJING KANVAS & PIN EMAS 24K", fill=(248, 250, 252), font=f_sub)
    draw.text((90, 110), "Cendera Mata Ramah Lingkungan & Tanda Kehormatan", fill=C_CHAMPAGNE, font=f_body)

    out_file = "assets/mockups/mockup_totebag_pin.jpg"
    bg.convert("RGB").save(out_file, "JPEG", quality=95)
    print(f"Mockup Tote Bag & Pin saved to: {out_file}")

if __name__ == "__main__":
    generate_mockup_kaos()
    generate_mockup_tumbler()
    generate_mockup_lanyard()
    generate_mockup_totebag()
