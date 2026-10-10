import os
from typing import TypedDict
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

def create_anatomy_diagrams():
    os.makedirs("assets/anatomy", exist_ok=True)
    
    # Load 2048x2048 logo
    logo_path = "assets/png/logo-color-2048.png"
    if not os.path.exists(logo_path):
        print(f"Error: {logo_path} not found")
        return

    logo_rgba = Image.open(logo_path).convert("RGBA")
    
    # Canvas dimensions for master diagram: 2400 x 1800 px (Ultra-HD 4:3 presentation)
    W, H = 2400, 1800
    
    # Background: Luxury Deep Space Obsidian with subtle warm radial glow
    bg = Image.new("RGBA", (W, H), (7, 9, 15, 255))
    
    # Radial glow layer in center
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    cx, cy = W // 2, H // 2 - 20
    for r in range(700, 0, -25):
        alpha = int((1 - r / 700) ** 1.8 * 65)
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(245, 197, 56, alpha))
    bg = Image.alpha_composite(bg, glow)
    
    # Resize and place logo in center
    logo_size = 1180
    logo_scaled = logo_rgba.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
    
    logo_pos_x = (W - logo_size) // 2
    logo_pos_y = (H - logo_size) // 2 - 10
    
    # Subtle drop shadow for logo
    shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shadow.paste((0, 0, 0, 160), (logo_pos_x + 10, logo_pos_y + 18), mask=logo_scaled.split()[3])
    shadow = shadow.filter(ImageFilter.GaussianBlur(radius=28))
    bg = Image.alpha_composite(bg, shadow)
    
    # Paste logo
    bg.paste(logo_scaled, (logo_pos_x, logo_pos_y), mask=logo_scaled.split()[3])
    
    draw = ImageDraw.Draw(bg)
    
    # Fonts setup (fallback to default if specific fonts missing)
    try:
        font_header_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 52)
        font_header_sub = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 26)
        font_badge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
        font_num = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 28)
        font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 26)
        font_tag = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 18)
        font_desc = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 19)
    except Exception:
        font_header_title = ImageFont.load_default()
        font_header_sub = ImageFont.load_default()
        font_badge = font_num = font_title = font_tag = font_desc = ImageFont.load_default()

    # Draw Header at top
    draw.text((cx, 80), "DIAGNOSTIK ANATOMI & FILOSOFI LAMBANG", fill=(248, 250, 252), font=font_header_title, anchor="mt")
    draw.text((cx, 145), "DIES NATALIS KE-44 SMA NEGERI 1 GEDEG • VERSI MASTER V6 FINAL", fill=(245, 197, 56), font=font_header_sub, anchor="mt")
    
    # 5 Anatomical Callout Points
    # Format: target_x, target_y, card_x, card_y, align, num, title, tag, desc_lines
    callouts: list[Callout] = [
        {
            "num": "01",
            "title": "Kepala & Tatapan Rajawali",
            "tag": "VISI VISIONER & KEWIBAWAAN",
            "desc": [
                "Siluet paruh dan tatapan tajam burung",
                "rajawali yang menghadap ke kanan atas.",
                "Simbol ketajaman visi intelektual dan",
                "keberanian moral menegakkan integritas."
            ],
            "color": (253, 243, 157),
            "target": (logo_pos_x + 580, logo_pos_y + 245),
            "card_box": (160, 260, 680, 500),
            "dot_pos": (680, 360),
            "anchor": "right"
        },
        {
            "num": "02",
            "title": "Figur Kembar Angka 44",
            "tag": "FONDASI ALMAMATER & 44 TAHUN",
            "desc": [
                "Dua figur angka 4 yang saling bertaut erat.",
                "Menandai kedewasaan perjalanan 44 tahun",
                "SMA Negeri 1 Gedeg dalam mendidik insan",
                "unggul dan mempererat ikatan antargenerasi."
            ],
            "color": (224, 155, 23),
            "target": (logo_pos_x + 360, logo_pos_y + 680),
            "card_box": (160, 750, 680, 990),
            "dot_pos": (680, 850),
            "anchor": "right"
        },
        {
            "num": "03",
            "title": "Lidah Api Abadi Berkobar",
            "tag": "SEMANGAT JUANG PANTANG PADAM",
            "desc": [
                "Sulur api dinamis yang meliuk membubung",
                "tinggi dari dasar hingga puncak lambang.",
                "Melambangkan gairah menuntut ilmu, daya",
                "lenting (resiliensi), dan kreativitas tanpa batas."
            ],
            "color": (182, 88, 11),
            "target": (logo_pos_x + 520, logo_pos_y + 980),
            "card_box": (160, 1240, 680, 1480),
            "dot_pos": (680, 1340),
            "anchor": "right"
        },
        {
            "num": "04",
            "title": "Akselerasi Sayap Aerodinamis",
            "tag": "MOMENTUM MELESAT KE MASA DEPAN",
            "desc": [
                "Sayap aerodinamis luar yang menyapu cepat",
                "ke kuadran kanan atas (masa depan).",
                "Simbol percepatan prestasi siswa, inovasi",
                "teknologi cerdas, dan gerak progresif almamater."
            ],
            "color": (212, 137, 17),
            "target": (logo_pos_x + 850, logo_pos_y + 440),
            "card_box": (1720, 360, 2240, 600),
            "dot_pos": (1720, 460),
            "anchor": "left"
        },
        {
            "num": "05",
            "title": "Symmetrical Medial Spine",
            "tag": "PRESI KONSENTRIS MASTER V6",
            "desc": [
                "Penyempurnaan radikal versi V6 berupa tulang",
                "punggung simetris murni 100% konsentris.",
                "Menciptakan kedalaman trimatra (3D) faset",
                "yang harmonis dan bebas distorsi sudut."
            ],
            "color": (245, 197, 56),
            "target": (logo_pos_x + 640, logo_pos_y + 730),
            "card_box": (1720, 1020, 2240, 1260),
            "dot_pos": (1720, 1120),
            "anchor": "left"
        }
    ]

    for item in callouts:
        tx, ty = item["target"]
        dx, dy = item["dot_pos"]
        x1, y1, x2, y2 = item["card_box"]
        col = item["color"]
        
        # 1. Draw glowing target ring on logo
        draw.ellipse([tx - 18, ty - 18, tx + 18, ty + 18], fill=(col[0], col[1], col[2], 50), outline=col, width=3)
        draw.ellipse([tx - 6, ty - 6, tx + 6, ty + 6], fill=(255, 255, 255, 240))
        
        # 2. Draw connector pointer line
        # Elbow routing: tx,ty -> midx, ty -> dx, dy
        mid_x = (tx + dx) // 2
        draw.line([(tx, ty), (mid_x, ty), (dx, dy)], fill=col, width=2)
        
        # Target node ring on card edge
        draw.ellipse([dx - 5, dy - 5, dx + 5, dy + 5], fill=col)
        
        # 3. Draw Card Background Box
        card_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        c_draw = ImageDraw.Draw(card_img)
        # Rounded rectangle
        c_draw.rounded_rectangle([x1, y1, x2, y2], radius=16, fill=(16, 23, 40, 220), outline=(col[0], col[1], col[2], 120), width=2)
        bg = Image.alpha_composite(bg, card_img)
        draw = ImageDraw.Draw(bg)
        
        # 4. Card Content
        pad = 26
        # Number pill
        draw.rounded_rectangle([x1 + pad, y1 + pad - 2, x1 + pad + 48, y1 + pad + 34], radius=8, fill=(col[0], col[1], col[2], 40), outline=col, width=1)
        draw.text((x1 + pad + 24, y1 + pad + 16), item["num"], fill=col, font=font_num, anchor="mm")
        
        # Title & Tag
        draw.text((x1 + pad + 60, y1 + pad + 3), item["title"], fill=(248, 250, 252), font=font_title)
        draw.text((x1 + pad + 60, y1 + pad + 32), item["tag"], fill=col, font=font_tag)
        
        # Separator line
        draw.line([(x1 + pad, y1 + pad + 56), (x2 - pad, y1 + pad + 56)], fill=(255, 255, 255, 25), width=1)
        
        # Description lines
        curr_y = y1 + pad + 70
        for line in item["desc"]:
            draw.text((x1 + pad, curr_y), line, fill=(203, 213, 225), font=font_desc)
            curr_y += 28

    # Footer note at bottom
    footer_text = "DOKUMEN RESMI IDENTITAS VISUAL • SMA NEGERI 1 GEDEG • HAK CIPTA DILINDUNGI UNDANG-UNDANG"
    draw.text((cx, H - 70), footer_text, fill=(148, 163, 184), font=font_badge, anchor="mt")

    output_master = "assets/anatomy/diagram_anatomi_lengkap.png"
    bg.convert("RGB").save(output_master, "PNG", quality=95)
    print(f"Master anatomy diagram saved to: {output_master}")

    # Generate 5 isolated focus images
    # We create high-resolution focused crops highlighting each specific area
    for idx, item in enumerate(callouts, 1):
        focus_canvas = Image.new("RGBA", (1200, 900), (13, 17, 30, 255))
        f_draw = ImageDraw.Draw(focus_canvas)
        
        # Center the focus on target with a nice crop
        crop_size = 850
        tx, ty = item["target"]
        
        # Paste scaled logo
        l_x = 600 - (tx - logo_pos_x)
        l_y = 450 - (ty - logo_pos_y)
        
        # Dim background logo slightly
        dim_logo = logo_scaled.copy()
        alpha_data = np.array(dim_logo.split()[3])
        alpha_data = (alpha_data * 0.45).astype(np.uint8)
        dim_logo.putalpha(Image.fromarray(alpha_data))
        
        focus_canvas.paste(dim_logo, (l_x, l_y), mask=dim_logo.split()[3])
        
        # Highlight circle around target
        for r in range(160, 0, -10):
            al = int((1 - r / 160) * 120)
            f_draw.ellipse([600 - r, 450 - r, 600 + r, 450 + r], fill=(item["color"][0], item["color"][1], item["color"][2], al))
        
        # Paste un-dimmed section on top
        mask_circle = Image.new("L", logo_scaled.size, 0)
        m_draw = ImageDraw.Draw(mask_circle)
        target_in_logo_x = tx - logo_pos_x
        target_in_logo_y = ty - logo_pos_y
        m_draw.ellipse([target_in_logo_x - 180, target_in_logo_y - 180, target_in_logo_x + 180, target_in_logo_y + 180], fill=255)
        # Combine with original alpha
        orig_alpha = logo_scaled.split()[3]
        final_mask = Image.fromarray(np.minimum(np.array(orig_alpha), np.array(mask_circle)))
        focus_canvas.paste(logo_scaled, (l_x, l_y), mask=final_mask)
        
        # Text Overlay Header & Description
        f_draw.rounded_rectangle([40, 40, 1160, 180], radius=16, fill=(7, 9, 15, 230), outline=item["color"], width=2)
        f_draw.text((70, 70), f"ANATOMI 0{idx}: {item['title'].upper()}", fill=(248, 250, 252), font=font_title)
        f_draw.text((70, 105), item["tag"], fill=item["color"], font=font_tag)
        desc_text = " ".join(item["desc"])
        f_draw.text((70, 138), desc_text[:110] + "...", fill=(203, 213, 225), font=font_desc)
        
        f_name = f"assets/anatomy/fokus_0{idx}_{item['title'].lower().replace(' ', '_').replace('&_', '')}.png"
        focus_canvas.convert("RGB").save(f_name, "PNG", quality=95)
        print(f"Focus image saved: {f_name}")

if __name__ == "__main__":
    create_anatomy_diagrams()
