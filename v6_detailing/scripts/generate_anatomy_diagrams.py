import os
from typing import TypedDict
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

class Callout(TypedDict):
    num: str
    title: str
    tag: str
    desc: list[str]
    color: tuple[int, int, int]
    target: tuple[int, int]
    card_box: tuple[int, int, int, int]
    dot_pos: tuple[int, int]
    anchor: str

# Official Colors
C_PURPLE_BASE = (28, 5, 33)        # #1C0521 (Deep Imperial Purple)
C_PURPLE_VIOLET = (66, 8, 78)      # #42084E (Center Velvet Glow)
C_PURPLE_CARD = (40, 8, 48, 240)   # High-contrast Velvet Card Panel
C_GOLD_PRIMARY = (245, 197, 56)    # #F5C538
C_GOLD_BRIGHT = (255, 234, 160)    # #FFEAA0
C_GOLD_DEEP = (224, 157, 23)       # #E09D17
C_WHITE = (248, 250, 252)
C_MUTED = (220, 195, 230)

def create_purple_canvas(w: int, h: int, cx: int, cy: int, glow_r: int = 800) -> Image.Image:
    """Membuat latar belakang ungu velvet mewah dengan radial glow ungu violet."""
    canvas = Image.new("RGBA", (w, h), (C_PURPLE_BASE[0], C_PURPLE_BASE[1], C_PURPLE_BASE[2], 255))
    
    # Radial Violet Glow
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    
    steps = 45
    for i in range(steps, 0, -1):
        frac = i / steps
        r = int(glow_r * frac)
        alpha = int(145 * (1.0 - frac) ** 1.6)
        glow_draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=(C_PURPLE_VIOLET[0], C_PURPLE_VIOLET[1], C_PURPLE_VIOLET[2], alpha)
        )
    canvas = Image.alpha_composite(canvas, glow)
    
    # Ambient Gold Dust Sparkles
    np.random.seed(44)
    dust = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    dust_draw = ImageDraw.Draw(dust)
    for _ in range(90):
        px = np.random.randint(40, w - 40)
        py = np.random.randint(40, h - 40)
        sz = np.random.randint(1, 4)
        alpha = np.random.randint(35, 150)
        dust_draw.ellipse([px - sz, py - sz, px + sz, py + sz], fill=(255, 234, 160, alpha))
    
    return Image.alpha_composite(canvas, dust)

def get_fonts():
    """Memuat font sistem dengan fallback aman."""
    font_bold_path = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
    font_reg_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
    
    def load(path, size):
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            return ImageFont.load_default()
            
    return {
        "header_title": load(font_bold_path, 48),
        "header_sub": load(font_bold_path, 24),
        "badge": load(font_bold_path, 18),
        "num": load(font_bold_path, 26),
        "title": load(font_bold_path, 25),
        "tag": load(font_bold_path, 17),
        "desc": load(font_reg_path, 19),
        "desc_lg": load(font_reg_path, 22),
        "footer": load(font_reg_path, 15)
    }

def extract_logo_components(logo_cv):
    """Mengekstrak kedua komponen figur utama dari logo master."""
    alpha = (logo_cv[:, :, 3] > 20).astype(np.uint8)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(alpha)
    
    # Component 1: Figur Kiri (Kepala Rajawali & Sayap Kiri = Figur 4 Pertama)
    c1 = logo_cv.copy()
    c1[labels != 1] = 0
    y1, x1 = np.where(labels == 1)
    crop_c1 = c1[y1.min():y1.max()+1, x1.min():x1.max()+1]
    
    # Component 2: Figur Kanan (Kobaran Lidah Api & Sayap Kanan = Figur 4 Kedua)
    c2 = logo_cv.copy()
    c2[labels != 2] = 0
    y2, x2 = np.where(labels == 2)
    crop_c2 = c2[y2.min():y2.max()+1, x2.min():x2.max()+1]
    
    # Component 2 with outer wing highlighted (dim inner flames)
    c2_highlight_wing = c2.copy()
    # Region of inner flames: x < 1220
    inner_mask = (labels == 2) & (np.arange(logo_cv.shape[1])[None, :] < 1220)
    c2_highlight_wing[inner_mask, 3] = (c2_highlight_wing[inner_mask, 3] * 0.35).astype(np.uint8)
    crop_wing = c2_highlight_wing[y2.min():y2.max()+1, x2.min():x2.max()+1]

    return (
        Image.fromarray(cv2.cvtColor(crop_c1, cv2.COLOR_BGRA2RGBA)),
        Image.fromarray(cv2.cvtColor(crop_c2, cv2.COLOR_BGRA2RGBA)),
        Image.fromarray(cv2.cvtColor(crop_wing, cv2.COLOR_BGRA2RGBA))
    )

def add_contour_glow(canvas: Image.Image, piece_pil: Image.Image, pos_x: int, pos_y: int, glow_color: tuple[int, int, int], radius: int = 24):
    """Menambahkan pendaran emas halus mengikuti kontur asli objek (bukan bulatan lingkaran datar)."""
    alpha_mask = piece_pil.split()[3]
    glow_img = Image.new("RGBA", piece_pil.size, (glow_color[0], glow_color[1], glow_color[2], 0))
    # Fill with color where alpha exists
    g_arr = np.array(glow_img)
    g_arr[:, :, 3] = (np.array(alpha_mask) * 0.65).astype(np.uint8)
    glow_pil = Image.fromarray(g_arr).filter(ImageFilter.GaussianBlur(radius=radius))
    
    # Layer di kanvas
    canvas.paste(glow_pil, (pos_x, pos_y), mask=glow_pil.split()[3])

def create_anatomy_diagrams():
    os.makedirs("assets/anatomy", exist_ok=True)
    
    logo_path = "assets/png/logo-color-2048.png"
    if not os.path.exists(logo_path):
        print(f"Error: {logo_path} tidak ditemukan")
        return

    logo_cv = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
    logo_raw = Image.open(logo_path).convert("RGBA")
    fonts = get_fonts()

    # Ekstraksi komponen vektor terisolasi
    left_eagle_pil, right_flames_pil, outer_wing_pil = extract_logo_components(logo_cv)

    # =========================================================================
    # 1. DIAGRAM MASTER UTAMA (2400 x 1800 - Ultra-HD)
    # =========================================================================
    W, H = 2400, 1800
    cx, cy = W // 2, H // 2 - 20
    
    # Latar belakang ungu velvet mewah (BUKAN hitam!)
    bg = create_purple_canvas(W, H, cx, cy, glow_r=850)
    bg_draw = ImageDraw.Draw(bg)
    bg_draw.rounded_rectangle([32, 32, W - 32, H - 32], radius=24, outline=(C_GOLD_PRIMARY[0], C_GOLD_PRIMARY[1], C_GOLD_PRIMARY[2], 55), width=2)
    bg_draw.rounded_rectangle([38, 38, W - 38, H - 38], radius=20, outline=(C_GOLD_BRIGHT[0], C_GOLD_BRIGHT[1], C_GOLD_BRIGHT[2], 25), width=1)

    # Resize dan letakkan logo di tengah
    logo_size = 1180
    logo_scaled = logo_raw.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    logo_pos_x = (W - logo_size) // 2
    logo_pos_y = (H - logo_size) // 2 - 10
    
    # Ambient Gold Aura & Shadow di belakang logo
    aura = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    aura_draw = ImageDraw.Draw(aura)
    for r in range(560, 0, -20):
        a = int((1.0 - r / 560) ** 2.0 * 85)
        aura_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 197, 56, a))
    bg = Image.alpha_composite(bg, aura)

    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow.paste((10, 2, 14, 210), (logo_pos_x + 12, logo_pos_y + 24), mask=logo_scaled.split()[3])
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=32))
    bg = Image.alpha_composite(bg, shadow)
    
    # Tempel Logo Utama
    bg.paste(logo_scaled, (logo_pos_x, logo_pos_y), mask=logo_scaled.split()[3])
    draw = ImageDraw.Draw(bg)

    # Header Master
    draw.text((cx, 75), "DIAGNOSTIK ANATOMI & FILOSOFI LAMBANG", fill=C_WHITE, font=fonts["header_title"], anchor="mt")
    draw.text((cx, 138), "DIES NATALIS KE-44 SMAN 1 GEDEG • PEDOMAN IDENTITAS VISUAL RESMI", fill=C_GOLD_PRIMARY, font=fonts["header_sub"], anchor="mt")

    # 5 ELEMEN ANATOMI RESMI (100% KONSISTEN DENGAN PDF GUIDELINE BAB 3)
    callouts: list[Callout] = [
        {
            "num": "01",
            "title": "FIGUR KEMBAR ANGKA 44",
            "tag": "FONDASI TRADISI & INOVASI MASA DEPAN",
            "desc": [
                "Menandai usia ke-44 tahun almamater.",
                "Angka 4 pertama berdiri kokoh sebagai",
                "fondasi tradisi; angka 4 kedua melesat maju",
                "sebagai pilar inovasi masa depan."
            ],
            "color": C_GOLD_PRIMARY,
            "target": (logo_pos_x + 360, logo_pos_y + 680),
            "card_box": (140, 740, 680, 990),
            "dot_pos": (680, 850),
            "anchor": "right"
        },
        {
            "num": "02",
            "title": "TATAPAN BURUNG RAJAWALI",
            "tag": "PANDANGAN VISIONER & KEBERANIAN MORAL",
            "desc": [
                "Siluet kepala rajawali menatap mantap",
                "ke arah kanan atas, menyimbolkan pandangan",
                "visioner, ketajaman intelektual, dan",
                "keberanian moral menegakkan integritas."
            ],
            "color": C_GOLD_BRIGHT,
            "target": (logo_pos_x + 580, logo_pos_y + 245),
            "card_box": (140, 250, 680, 500),
            "dot_pos": (680, 360),
            "anchor": "right"
        },
        {
            "num": "03",
            "title": "KOBARAN LIDAH API ABADI",
            "tag": "SEMANGAT BELAJAR PANTANG PADAM",
            "desc": [
                "Tiga sulur api yang menyala melambangkan",
                "semangat belajar pantang padam, ketangguhan",
                "menghadapi tantangan, dan daya cipta",
                "yang senantiasa memberi kemanfaatan."
            ],
            "color": C_GOLD_DEEP,
            "target": (logo_pos_x + 520, logo_pos_y + 980),
            "card_box": (140, 1230, 680, 1480),
            "dot_pos": (680, 1340),
            "anchor": "right"
        },
        {
            "num": "04",
            "title": "SAYAP MELESAT AERODINAMIS",
            "tag": "AKSELERASI PRESTASI & CITA-CITA MULIA",
            "desc": [
                "Sapuan sayap melengkung ke atas mencerminkan",
                "percepatan prestasi sekolah serta tekad teguh",
                "untuk terus terbang tinggi meraih cita-cita",
                "mulia almamater menuju era keemasan."
            ],
            "color": C_GOLD_PRIMARY,
            "target": (logo_pos_x + 850, logo_pos_y + 440),
            "card_box": (1720, 350, 2260, 600),
            "dot_pos": (1720, 460),
            "anchor": "left"
        },
        {
            "num": "05",
            "title": "GARIS TENGAH SIMETRIS",
            "tag": "KESERASIAN BENTUK KONSENTRIS",
            "desc": [
                "Garis tengah simetris konsentris menyatukan",
                "seluruh elemen dalam keserasian bentuk",
                "yang bersih, anggun, dan berwibawa",
                "bebas dari distorsi faset sudut."
            ],
            "color": (230, 175, 30),
            "target": (logo_pos_x + 640, logo_pos_y + 730),
            "card_box": (1720, 1010, 2260, 1260),
            "dot_pos": (1720, 1120),
            "anchor": "left"
        }
    ]

    for item in callouts:
        tx, ty = item["target"]
        dx, dy = item["dot_pos"]
        x1, y1, x2, y2 = item["card_box"]
        col = item["color"]
        
        # 1. Target Pin on Logo
        draw.ellipse([tx - 18, ty - 18, tx + 18, ty + 18], fill=(col[0], col[1], col[2], 55), outline=col, width=3)
        draw.ellipse([tx - 6, ty - 6, tx + 6, ty + 6], fill=(255, 255, 255, 240))
        
        # 2. Connector Pointer Line
        mid_x = (tx + dx) // 2
        draw.line([(tx, ty), (mid_x, ty), (dx, dy)], fill=col, width=2)
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=col)
        
        # 3. Card Background Box (Velvet Card Style)
        card_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        c_draw = ImageDraw.Draw(card_img)
        c_draw.rounded_rectangle([x1, y1, x2, y2], radius=16, fill=C_PURPLE_CARD, outline=(col[0], col[1], col[2], 140), width=2)
        bg = Image.alpha_composite(bg, card_img)
        draw = ImageDraw.Draw(bg)
        
        # 4. Card Content
        pad = 24
        # Number Pill (Dark purple fill + gold outline + visible text)
        pill_box = [x1 + pad, y1 + pad - 2, x1 + pad + 48, y1 + pad + 34]
        draw.rounded_rectangle(pill_box, radius=8, fill=(50, 10, 60), outline=col, width=1)
        draw.text((x1 + pad + 24, y1 + pad + 16), item["num"], fill=C_GOLD_BRIGHT, font=fonts["num"], anchor="mm")
        
        # Title & Tag
        draw.text((x1 + pad + 60, y1 + pad + 3), item["title"], fill=C_WHITE, font=fonts["title"])
        draw.text((x1 + pad + 60, y1 + pad + 32), item["tag"], fill=col, font=fonts["tag"])
        
        # Separator line
        draw.line([(x1 + pad, y1 + pad + 56), (x2 - pad, y1 + pad + 56)], fill=(255, 255, 255, 30), width=1)
        
        # Description lines
        curr_y = y1 + pad + 68
        for line in item["desc"]:
            draw.text((x1 + pad, curr_y), line, fill=C_MUTED, font=fonts["desc"])
            curr_y += 27

    # Footer Master
    footer_text = "BUKU PEDOMAN IDENTITAS VISUAL RESMI • DIES NATALIS KE-44 SMAN 1 GEDEG • VERSI V6 FINAL"
    draw.text((cx, H - 70), footer_text, fill=(180, 150, 195), font=fonts["badge"], anchor="mt")

    output_master = "assets/anatomy/diagram_anatomi_lengkap.png"
    bg.convert("RGB").save(output_master, "PNG", quality=95)
    print(f"[ANATOMI MASTER] Berhasil disimpan ke: {output_master}")

    # =========================================================================
    # 2. GAMBAR FOKUS ANATOMI PER ELEMEN (1920 x 1080 - FULL HD)
    # FOKUS PADA POTONGAN ASLI ELEMEN LOGO DENGAN LATAR UNGU VELVET
    # =========================================================================
    FW, FH = 1920, 1080
    fcx, fcy = FW // 2, FH // 2

    filenames = [
        "fokus_01_figur_kembar_angka_44.png",
        "fokus_02_tatapan_burung_rajawali.png",
        "fokus_03_kobaran_lidah_api_abadi.png",
        "fokus_04_sayap_melesat_aerodinamis.png",
        "fokus_05_garis_tengah_simetris.png"
    ]

    for idx, (item, fname) in enumerate(zip(callouts, filenames), 1):
        fcanvas = create_purple_canvas(FW, FH, fcx, fcy, glow_r=750)
        fdraw = ImageDraw.Draw(fcanvas)
        
        # Outer Gold Border Inset
        fdraw.rounded_rectangle([24, 24, FW - 24, FH - 24], radius=18, outline=(C_GOLD_PRIMARY[0], C_GOLD_PRIMARY[1], C_GOLD_PRIMARY[2], 45), width=2)

        # ---------------------------------------------------------------------
        # HEADER SLIDE
        # ---------------------------------------------------------------------
        fdraw.text((60, 48), f"BAB 3 • ANATOMI LAMBANG RESMI DIES NATALIS KE-44", fill=C_GOLD_PRIMARY, font=fonts["badge"])
        fdraw.text((60, 80), f"ANATOMI 0{idx}: {item['title']}", fill=C_WHITE, font=fonts["header_title"])
        fdraw.text((60, 140), f"DOKTRIN FILOSOFI: {item['tag']}", fill=item["color"], font=fonts["header_sub"])

        # ---------------------------------------------------------------------
        # KOTAK KIRI (X: 60 - 640): KONTEKS POSISI PADA LAMBANG LENGKAP
        # ---------------------------------------------------------------------
        k_box = (60, 195, 640, 840)
        fdraw.rounded_rectangle(k_box, radius=14, fill=C_PURPLE_CARD, outline=(item["color"][0], item["color"][1], item["color"][2], 100), width=2)
        fdraw.text((k_box[0] + 20, k_box[1] + 16), "POSISI PADA LAMBANG LENGKAP", fill=C_GOLD_BRIGHT, font=fonts["badge"])
        
        # Render ghosted context logo
        ghost_sz = 520
        ghost_logo = logo_raw.resize((ghost_sz, ghost_sz), Image.Resampling.LANCZOS)
        g_arr = np.array(ghost_logo)
        g_arr[:, :, 3] = (g_arr[:, :, 3] * 0.32).astype(np.uint8)
        ghost_faded = Image.fromarray(g_arr)
        
        gx = k_box[0] + (k_box[2] - k_box[0] - ghost_sz) // 2
        gy = k_box[1] + 55 + (k_box[3] - k_box[1] - 55 - ghost_sz) // 2
        fcanvas.paste(ghost_faded, (gx, gy), mask=ghost_faded.split()[3])

        # Target spotlight ring on ghost logo
        scale_f = ghost_sz / 2048.0
        orig_tx = (item["target"][0] - logo_pos_x) * (2048.0 / logo_size)
        orig_ty = (item["target"][1] - logo_pos_y) * (2048.0 / logo_size)
        gtx = int(gx + orig_tx * scale_f)
        gty = int(gy + orig_ty * scale_f)
        
        # Spotlight pulse
        fdraw.ellipse([gtx - 24, gty - 24, gtx + 24, gty + 24], fill=(item["color"][0], item["color"][1], item["color"][2], 70), outline=item["color"], width=3)
        fdraw.ellipse([gtx - 8, gty - 8, gtx + 8, gty + 8], fill=(255, 255, 255, 230))

        # ---------------------------------------------------------------------
        # KOTAK KANAN (X: 670 - 1860): HERO CUT-OUT ELEMEN ANATOMI ASLI
        # ---------------------------------------------------------------------
        h_box = (670, 195, 1860, 840)
        fdraw.rounded_rectangle(h_box, radius=14, fill=C_PURPLE_CARD, outline=(item["color"][0], item["color"][1], item["color"][2], 120), width=2)
        fdraw.text((h_box[0] + 28, h_box[1] + 18), "ISOLASI POTONGAN GEOMETRI ELEMEN (HERO CUT-OUT)", fill=C_GOLD_BRIGHT, font=fonts["badge"])

        if idx == 1:
            # 01: DUAL FIGUR 44 BERDAMPINGAN
            th = 480
            lw = int(left_eagle_pil.width * (th / left_eagle_pil.height))
            l_scaled = left_eagle_pil.resize((lw, th), Image.Resampling.LANCZOS)
            rw = int(right_flames_pil.width * (th / right_flames_pil.height))
            r_scaled = right_flames_pil.resize((rw, th), Image.Resampling.LANCZOS)
            
            total_w = lw + rw + 70
            start_x = h_box[0] + (h_box[2] - h_box[0] - total_w) // 2
            pos_y = h_box[1] + 75
            
            # Contour glow
            add_contour_glow(fcanvas, l_scaled, start_x, pos_y, C_GOLD_PRIMARY, radius=20)
            fcanvas.paste(l_scaled, (start_x, pos_y), mask=l_scaled.split()[3])
            fdraw.text((start_x + lw // 2, pos_y + th + 15), "FIGUR 4 PERTAMA (FONDASI & TRADISI)", fill=C_GOLD_BRIGHT, font=fonts["badge"], anchor="mt")
            
            sep_x = start_x + lw + 35
            fdraw.text((sep_x, pos_y + th // 2), "+", fill=C_WHITE, font=fonts["header_title"], anchor="mm")
            
            rx = start_x + lw + 70
            add_contour_glow(fcanvas, r_scaled, rx, pos_y, C_GOLD_PRIMARY, radius=20)
            fcanvas.paste(r_scaled, (rx, pos_y), mask=r_scaled.split()[3])
            fdraw.text((rx + rw // 2, pos_y + th + 15), "FIGUR 4 KEDUA (INOVASI & MASA DEPAN)", fill=C_GOLD_PRIMARY, font=fonts["badge"], anchor="mt")

        elif idx == 2:
            # 02: KEPALA & TATAPAN RAJAWALI (Clean Cutout Left Eagle)
            th = 520
            tw = int(left_eagle_pil.width * (th / left_eagle_pil.height))
            p_scaled = left_eagle_pil.resize((tw, th), Image.Resampling.LANCZOS)
            
            px = h_box[0] + (h_box[2] - h_box[0] - tw) // 2
            py = h_box[1] + 65
            
            add_contour_glow(fcanvas, p_scaled, px, py, C_GOLD_BRIGHT, radius=24)
            fcanvas.paste(p_scaled, (px, py), mask=p_scaled.split()[3])
            fdraw = ImageDraw.Draw(fcanvas)
            fdraw.text((px + tw // 2, py + th + 18), "POTONGAN RESMI: SILUET PARUH & KEPALA VISIONER", fill=C_GOLD_BRIGHT, font=fonts["badge"], anchor="mt")

        elif idx == 3:
            # 03: KOBARAN LIDAH API ABADI (Clean Cutout Right Flames)
            th = 520
            tw = int(right_flames_pil.width * (th / right_flames_pil.height))
            p_scaled = right_flames_pil.resize((tw, th), Image.Resampling.LANCZOS)
            
            px = h_box[0] + (h_box[2] - h_box[0] - tw) // 2
            py = h_box[1] + 65
            
            add_contour_glow(fcanvas, p_scaled, px, py, C_GOLD_DEEP, radius=24)
            fcanvas.paste(p_scaled, (px, py), mask=p_scaled.split()[3])
            fdraw = ImageDraw.Draw(fcanvas)
            fdraw.text((px + tw // 2, py + th + 18), "POTONGAN RESMI: 3 SULUR LIDAH API BERKOBAR MENJULANG", fill=C_GOLD_DEEP, font=fonts["badge"], anchor="mt")

        elif idx == 4:
            # 04: SAYAP MELESAT AERODINAMIS (Highlight Outer Sweeping Wing)
            th = 520
            tw = int(outer_wing_pil.width * (th / outer_wing_pil.height))
            p_scaled = outer_wing_pil.resize((tw, th), Image.Resampling.LANCZOS)
            
            px = h_box[0] + (h_box[2] - h_box[0] - tw) // 2
            py = h_box[1] + 65
            
            add_contour_glow(fcanvas, p_scaled, px, py, C_GOLD_PRIMARY, radius=24)
            fcanvas.paste(p_scaled, (px, py), mask=p_scaled.split()[3])
            fdraw = ImageDraw.Draw(fcanvas)
            fdraw.text((px + tw // 2, py + th + 18), "POTONGAN RESMI: SAPUAN SAYAP AERODINAMIS KUADRAN KANAN ATAS", fill=C_GOLD_PRIMARY, font=fonts["badge"], anchor="mt")

        elif idx == 5:
            # 05: GARIS TENGAH SIMETRIS (Kedua figur dengan aksis simetri konsentris bersinar)
            th = 510
            tw = int(logo_raw.width * (th / logo_raw.height))
            p_scaled = logo_raw.resize((tw, th), Image.Resampling.LANCZOS)
            
            px = h_box[0] + (h_box[2] - h_box[0] - tw) // 2
            py = h_box[1] + 75
            
            add_contour_glow(fcanvas, p_scaled, px, py, (230, 175, 30), radius=22)
            fcanvas.paste(p_scaled, (px, py), mask=p_scaled.split()[3])
            fdraw = ImageDraw.Draw(fcanvas)
            
            # Aksis Garis Simetri Emas Bersinar
            axis_x = px + int(tw * 0.495)
            fdraw.line([(axis_x, py), (axis_x, py + th)], fill=C_GOLD_BRIGHT, width=3)
            fdraw.text((axis_x, py - 18), "AKSIS SIMETRI KONSENTRIS", fill=C_GOLD_BRIGHT, font=fonts["badge"], anchor="mm")
            fdraw.text((axis_x, py + th + 18), "KESELARASAN BIDANG FASET KIRI DAN KANAN MURNI SIMETRIS", fill=C_GOLD_PRIMARY, font=fonts["badge"], anchor="mt")

        # ---------------------------------------------------------------------
        # FOOTER CARD (X: 60 - 1860, Y: 865 - 1030): DESKRIPSI RESMI PDF
        # ---------------------------------------------------------------------
        info_box = (60, 865, 1860, 1030)
        fdraw.rounded_rectangle(info_box, radius=12, fill=(24, 4, 30, 245), outline=(C_GOLD_PRIMARY[0], C_GOLD_PRIMARY[1], C_GOLD_PRIMARY[2], 95), width=2)
        
        # Pill Nomor (Dark purple fill + gold outline + visible text)
        fdraw.rounded_rectangle([info_box[0] + 20, info_box[1] + 18, info_box[0] + 75, info_box[1] + 62], radius=8, fill=(50, 10, 60), outline=item["color"], width=1)
        fdraw.text((info_box[0] + 47, info_box[1] + 40), f"0{idx}", fill=C_GOLD_BRIGHT, font=fonts["num"], anchor="mm")
        
        # Judul & Uraian Filosofis Resmi
        fdraw.text((info_box[0] + 90, info_box[1] + 18), f"{item['title']} — {item['tag']}", fill=C_WHITE, font=fonts["title"])
        full_desc = " ".join(item["desc"])
        fdraw.text((info_box[0] + 90, info_box[1] + 58), full_desc, fill=C_MUTED, font=fonts["desc_lg"])
        
        # Metadata almamater
        fdraw.text((info_box[2] - 25, info_box[1] + 115), "DOKUMEN RESMI IDENTITAS VISUAL • SMA NEGERI 1 GEDEG", fill=(170, 140, 185), font=fonts["footer"], anchor="ra")

        out_path = f"assets/anatomy/{fname}"
        fcanvas.convert("RGB").save(out_path, "PNG", quality=95)
        print(f"[ANATOMI FOKUS 0{idx}] Berhasil disimpan ke: {out_path}")

if __name__ == "__main__":
    create_anatomy_diagrams()
