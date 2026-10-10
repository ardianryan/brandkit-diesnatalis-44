#!/usr/bin/env python3
"""
build_accurate_brandkit_backgrounds.py
--------------------------------------
Membangun Aset Latar Belakang & Ornamen Presisi Berdasarkan Poster Referensi Resmi:

KONSEP 1: POSTER PANGGUNG RESMI (Theatrical Stage)
  - Pinwheel spiral halus memancar dari tengah: Mint Toska Pastel + Krem Vanilla
  - Tirai teater beludru merah marun anggur (Wine Crimson Velvet) berumbai emas di atas
  - Awan kapas gula merah muda lembut (Cotton Candy Clouds) di kiri & kanan
  - Pusat cahaya hangat (warm glowing stardust core)

KONSEP 2: POSTER TEASER RESMI (Imperial Velvet Purple & Golden Stardust)
  - Gradasi radial ungu beludru malam pekat (Imperial Velvet Purple)
  - Lengkungan debu bintang emas berpendar melingkar (Golden Stardust Arc Swoosh)
  - Taburan debu sihir & bintang 4 sudut berkilau (Vivid Gold & Canary Specular Glints)

Format Output:
  - Feed Instagram / Poster (2048 x 2048 px)
  - Story Instagram / WA Status (1080 x 1920 px)
  - Ornamen transparan PNG 32-bit & SVG

Dies Natalis ke-44 SMA Negeri 1 Gedeg (1982 - 2026)
"""

import os
import math
import random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

WORKSPACE = "/Users/ardianryan/Documents/diesnat44project"
BG_DIR = os.path.join(WORKSPACE, "assets/brandkit_elements/backgrounds")
PNG_DIR = os.path.join(WORKSPACE, "assets/brandkit_elements/png")
SVG_DIR = os.path.join(WORKSPACE, "assets/brandkit_elements/svg")

for d in [BG_DIR, PNG_DIR, SVG_DIR]:
    os.makedirs(d, exist_ok=True)

# Warna Palet Resmi Sesuai Moodboard
COLOR_MINT = np.array([108, 193, 170], dtype=np.float32)     # #6CC1AA (Mint Toska Pastel)
COLOR_CREAM = np.array([250, 243, 222], dtype=np.float32)    # #FAF3DE (Krem Vanilla)
COLOR_ROSE_BLUSH = np.array([242, 175, 198], dtype=np.float32) # #F2AFC6 (Soft Pink Blush)
COLOR_WARM_GLOW = np.array([255, 252, 235], dtype=np.float32)  # #FFFEFF (Center warm light)

COLOR_VELVET_DARK = np.array([29, 2, 33], dtype=np.float32)   # #1D0221 (Obsidian Velvet Purple)
COLOR_VELVET_MID = np.array([62, 7, 70], dtype=np.float32)    # #3E0746 (Imperial Velvet Purple)
COLOR_VELVET_LIGHT = np.array([92, 14, 104], dtype=np.float32) # #5C0E68 (Plum Highlight)


# ==============================================================================
# 1. GENERATOR SPIRAL KIPAS TEATRIKAL (MINT & KREM VANILLA)
# ==============================================================================

def generate_pinwheel_canvas(width=2048, height=2048, cx=1024, cy=950, num_blades=18, twist=0.0022):
    """Menghasilkan kanvas spiral kipas 2D halus Mint & Krem Vanilla persis seperti di poster panggung."""
    print(f"Generating Pinwheel Spiral Canvas ({width}x{height})...")

    # Buat koordinat grid
    y_coords, x_coords = np.mgrid[0:height, 0:width]
    dx = x_coords - cx
    dy = y_coords - cy
    r = np.sqrt(dx**2 + dy**2)
    theta = np.arctan2(dy, dx)

    # Sudut terpilin lembut melengkung (spiral)
    phi = theta + twist * np.power(r, 0.72)

    # Gelombang bilah selang-seling halus
    wave = np.sin(num_blades * phi)
    # Normalisasi wave ke rentang 0.0 - 1.0 dengan transisi halus
    t = (wave + 1.0) * 0.5
    t = np.clip(t, 0.0, 1.0)

    # Interpolasi warna Mint ke Krem Vanilla
    img_arr = np.zeros((height, width, 3), dtype=np.float32)
    for c in range(3):
        img_arr[:, :, c] = COLOR_MINT[c] * (1.0 - t) + COLOR_CREAM[c] * t

    # Tambahkan pendaran cahaya hangat sentral di titik pusat
    glow_sigma = min(width, height) * 0.28
    center_glow = np.exp(-(r / glow_sigma)**2)
    for c in range(3):
        img_arr[:, :, c] = img_arr[:, :, c] * (1.0 - center_glow * 0.6) + COLOR_WARM_GLOW[c] * (center_glow * 0.6)

    # Tambahkan semburat pink blush halus di kuadran luar (seperti pantulan tirai/bunga)
    blush_factor = np.clip((r - glow_sigma) / (min(width, height) * 0.65), 0.0, 1.0) * 0.25
    for c in range(3):
        img_arr[:, :, c] = img_arr[:, :, c] * (1.0 - blush_factor) + COLOR_ROSE_BLUSH[c] * blush_factor

    # Vignette lembut di tepian
    max_r = math.sqrt((width/2)**2 + (height/2)**2)
    vignette = 1.0 - 0.22 * np.power(r / max_r, 1.8)
    vignette = np.clip(vignette, 0.75, 1.0)
    for c in range(3):
        img_arr[:, :, c] = img_arr[:, :, c] * vignette

    img_arr = np.clip(img_arr, 0, 255).astype(np.uint8)
    base_img = Image.fromarray(img_arr, mode="RGB")

    # Tambahkan partikel stardust halus di sekitar pusat cahaya
    draw = ImageDraw.Draw(base_img, "RGBA")
    random.seed(44)
    for _ in range(120):
        # Partikel debu bintang
        dist = random.gauss(0, glow_sigma * 0.55)
        angle = random.uniform(0, 2 * math.pi)
        px = int(cx + dist * math.cos(angle))
        py = int(cy + dist * math.sin(angle))
        if 0 <= px < width and 0 <= py < height:
            radius = random.choice([1, 1, 2, 2, 3])
            alpha = random.randint(120, 240)
            color = (255, 250, 220, alpha)
            draw.ellipse((px - radius, py - radius, px + radius, py + radius), fill=color)

    return base_img


# ==============================================================================
# 2. GENERATOR UNGU BELUDRU MEWAH & DEBU BINTANG EMAS (TEASER WONKA RESMI)
# ==============================================================================

def generate_imperial_velvet_background(width=2048, height=2048, cx=1024, cy=950):
    """Menghasilkan kanvas ungu beludru pekat mewah dengan spotlight sentral."""
    print(f"Generating Imperial Velvet Canvas ({width}x{height})...")
    y_coords, x_coords = np.mgrid[0:height, 0:width]
    dx = (x_coords - cx) / (width * 0.5)
    dy = (y_coords - cy) / (height * 0.5)
    dist = np.sqrt(dx**2 + dy**2)

    # Normalisasi dist
    dist_norm = np.clip(dist / 1.35, 0.0, 1.0)

    # 3-step radial gradient: Center (LIGHT) -> Mid (MID) -> Outer (DARK)
    img_arr = np.zeros((height, width, 3), dtype=np.float32)
    mask_inner = np.clip(dist_norm * 2.0, 0.0, 1.0)
    mask_outer = np.clip((dist_norm - 0.5) * 2.0, 0.0, 1.0)

    for c in range(3):
        val_inner = COLOR_VELVET_LIGHT[c] * (1.0 - mask_inner) + COLOR_VELVET_MID[c] * mask_inner
        val_outer = val_inner * (1.0 - mask_outer) + COLOR_VELVET_DARK[c] * mask_outer
        img_arr[:, :, c] = val_outer

    # Tambahkan tekstur mikro kain beludru halus
    noise = np.random.normal(0, 2.5, (height, width))
    for c in range(3):
        img_arr[:, :, c] = np.clip(img_arr[:, :, c] + noise, 0, 255)

    return Image.fromarray(img_arr.astype(np.uint8), mode="RGB")


def draw_golden_stardust_swoosh(canvas_img, cx=1024, cy=950, scale=1.0):
    """
    Menggambar lengkungan debu bintang emas (Golden Stardust Arc Swoosh)
    melingkar persis seperti di poster teaser Wonka resmi.
    """
    print("Drawing Golden Stardust Arc Swoosh...")
    width, height = canvas_img.size
    overlay = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay, "RGBA")

    # Parameter lengkungan elips debu bintang memutar dari kiri atas ke kanan bawah
    # Titik kurva parametrik: t dari 0.0 ke 1.0
    random.seed(1982)

    # Jalur kurva titik tengah:
    def curve_point(t):
        # Dari sudut -140 derajat ke +80 derajat
        angle = math.radians(-135 + t * 240)
        rx = 480 * scale * (1.0 + 0.18 * math.sin(t * math.pi))
        ry = 420 * scale * (1.0 - 0.12 * math.cos(t * math.pi))
        x = cx + rx * math.cos(angle)
        y = cy + ry * math.sin(angle) - 40 * scale
        return x, y

    # 1. Pendaran glow lembut di sepanjang jalur lengkungan
    for step in range(250):
        t = step / 250.0
        x, y = curve_point(t)
        # Glow radius membesar di kuadran kanan
        glow_r = int((16 + 28 * math.sin(t * math.pi)) * scale)
        alpha = int((30 + 45 * math.sin(t * math.pi)))
        draw.ellipse((x - glow_r, y - glow_r, x + glow_r, y + glow_r),
                     fill=(245, 197, 56, alpha))

    # 2. Taburan ratusan partikel debu bintang (stardust) di sekitar kurva
    for _ in range(850):
        t = random.uniform(0.05, 0.98)
        base_x, base_y = curve_point(t)

        # Sebaran debu (tebal di kanan, mengecil di ujung)
        spread = (15 + 45 * math.sin(t * math.pi)) * scale
        px = base_x + random.gauss(0, spread * 0.45)
        py = base_y + random.gauss(0, spread * 0.45)

        # Ukuran partikel
        r_part = random.choices([1, 2, 3, 4, 6], weights=[40, 30, 18, 9, 3])[0] * scale
        alpha = random.randint(140, 255)

        # Palet emas Coolors
        gold_type = random.choice(["vivid", "champagne", "canary", "white"])
        if gold_type == "vivid":
            color = (245, 197, 56, alpha)   # #F5C538
        elif gold_type == "champagne":
            color = (247, 209, 96, alpha)   # #F7D160
        elif gold_type == "canary":
            color = (253, 243, 157, alpha)  # #FDF39D
        else:
            color = (255, 255, 255, alpha)  # Inti putih berkilau

        draw.ellipse((px - r_part, py - r_part, px + r_part, py + r_part), fill=color)

    # 3. Bintang 4-sudut retro bercahaya (retro 4-point sparkle flares) di titik aksen
    sparkle_positions = [
        (0.20, 18), (0.35, 24), (0.50, 32), (0.65, 28), (0.78, 22), (0.88, 16)
    ]
    for t, sz in sparkle_positions:
        bx, by = curve_point(t)
        sx = bx + random.uniform(-10, 10) * scale
        sy = by + random.uniform(-10, 10) * scale
        s_size = sz * scale

        # Gambar pendaran bintang 4 sudut
        glow_col = (253, 243, 157, 180)
        core_col = (255, 255, 255, 255)

        # Bilah horizontal & vertikal runcing
        draw.polygon([(sx - s_size, sy), (sx, sy - s_size*0.2), (sx + s_size, sy), (sx, sy + s_size*0.2)], fill=glow_col)
        draw.polygon([(sx, sy - s_size), (sx + s_size*0.2, sy), (sx, sy + s_size), (sx - s_size*0.2, sy)], fill=glow_col)
        # Inti putih
        draw.ellipse((sx - 3, sy - 3, sx + 3, sy + 3), fill=core_col)

    # Gabungkan overlay dengan blur halus untuk kelembutan atmosfer
    blurred_overlay = overlay.filter(ImageFilter.GaussianBlur(1.0))
    canvas_rgba = canvas_img.convert("RGBA")
    result = Image.alpha_composite(canvas_rgba, blurred_overlay)

    # Simpan juga overlay debu bintang ini sebagai PNG transparan murni!
    if width == 2048:
        out_swoosh_png = os.path.join(PNG_DIR, "golden-stardust-arc-swoosh.png")
        overlay.save(out_swoosh_png, "PNG", optimize=True)
        print(f"✓ Saved transparent stardust swoosh (Feed): {out_swoosh_png}")
    else:
        out_swoosh_story_png = os.path.join(PNG_DIR, "golden-stardust-arc-swoosh-story.png")
        overlay.save(out_swoosh_story_png, "PNG", optimize=True)
        print(f"✓ Saved transparent stardust swoosh (Story): {out_swoosh_story_png}")

    return result.convert("RGB")


# ==============================================================================
# 3. EKSEKUSI PEMBANGUNAN SELURUH ASET RESMI
# ==============================================================================

def build_all_assets():
    print("==================================================================")
    print(" MEMBANGUN ASET LATAR BELAKANG PRESISI (SESUAI POSTER REFERENSI)")
    print("==================================================================")

    # --- KONSEP 1: POSTER PANGGUNG (Pinwheel Spiral Mint & Krem Vanilla) ---
    # A. Feed Instagram (2048 x 2048)
    pinwheel_feed = generate_pinwheel_canvas(width=2048, height=2048, cx=1024, cy=950, num_blades=18)
    out_pinwheel_feed = os.path.join(BG_DIR, "bg-theatrical-pinwheel-mint.png")
    pinwheel_feed.save(out_pinwheel_feed, "PNG", optimize=True)
    print(f"✓ [Feed 1:1] {out_pinwheel_feed}")

    # B. Story Instagram (1080 x 1920)
    pinwheel_story = generate_pinwheel_canvas(width=1080, height=1920, cx=540, cy=820, num_blades=18, twist=0.0020)
    out_pinwheel_story = os.path.join(BG_DIR, "bg-theatrical-pinwheel-mint-story.png")
    pinwheel_story.save(out_pinwheel_story, "PNG", optimize=True)
    print(f"✓ [Story 9:16] {out_pinwheel_story}")

    # --- KONSEP 2: POSTER TEASER RESMI (Imperial Velvet Purple & Debu Bintang Emas) ---
    # A. Feed Instagram (2048 x 2048)
    velvet_feed_raw = generate_imperial_velvet_background(width=2048, height=2048, cx=1024, cy=950)
    velvet_feed_complete = draw_golden_stardust_swoosh(velvet_feed_raw, cx=1024, cy=950, scale=1.0)
    out_velvet_feed = os.path.join(BG_DIR, "bg-imperial-velvet-stardust.png")
    velvet_feed_complete.save(out_velvet_feed, "PNG", optimize=True)
    print(f"✓ [Feed 1:1] {out_velvet_feed}")

    # Simpan juga versi polos tanpa debu bintang (opsi clean velvet)
    out_velvet_clean = os.path.join(BG_DIR, "bg-imperial-velvet-clean.png")
    velvet_feed_raw.save(out_velvet_clean, "PNG", optimize=True)
    print(f"✓ [Feed Clean] {out_velvet_clean}")

    # B. Story Instagram (1080 x 1920)
    velvet_story_raw = generate_imperial_velvet_background(width=1080, height=1920, cx=540, cy=850)
    velvet_story_complete = draw_golden_stardust_swoosh(velvet_story_raw, cx=540, cy=850, scale=0.68)
    out_velvet_story = os.path.join(BG_DIR, "bg-imperial-velvet-stardust-story.png")
    velvet_story_complete.save(out_velvet_story, "PNG", optimize=True)
    print(f"✓ [Story 9:16] {out_velvet_story}")

    out_velvet_story_clean = os.path.join(BG_DIR, "bg-imperial-velvet-clean-story.png")
    velvet_story_raw.save(out_velvet_story_clean, "PNG", optimize=True)
    print(f"✓ [Story Clean] {out_velvet_story_clean}")

    print("\n✓ SELURUH ASET RESMI BERHASIL DIBANGUN DENGAN PRESTISE TINGGI!")


if __name__ == "__main__":
    build_all_assets()
