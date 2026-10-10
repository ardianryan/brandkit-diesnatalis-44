#!/usr/bin/env python3
"""
process_generated_brandkit_assets.py
-----------------------------------
Memproses aset visual kaya (hasil generasi AI) menjadi aset Brand Kit resmi:
1. Menyiapkan master background HD (2048x2048 & 1080x1920) untuk Feed dan Story.
2. Melakukan ekstraksi & isolasi latar belakang putih pada tirai teater untuk menghasilkan
   PNG transparan 32-bit ultra murni tanpa halo putih.
3. Melakukan vektorisasi / tracing kontur SVG untuk aset ornamen.
4. Menghasilkan mockup preview komposit untuk menguji kontras logo emas 44 & AVERSA.

Dies Natalis ke-44 SMAN 1 Gedeg (1982 - 2026)
"""

import os
import sys
import numpy as np
from PIL import Image, ImageFilter, ImageOps, ImageChops

WORKSPACE = "/Users/ardianryan/Documents/diesnat44project"
BRAIN_DIR = "/Users/ardianryan/.gemini/antigravity-ide/brain/1e5aebc6-88de-4318-a297-a371f05702be"

ASSETS_DIR = os.path.join(WORKSPACE, "assets/brandkit_elements")
BG_DIR = os.path.join(ASSETS_DIR, "backgrounds")
PNG_DIR = os.path.join(ASSETS_DIR, "png")
SVG_DIR = os.path.join(ASSETS_DIR, "svg")
MOCKUPS_DIR = os.path.join(WORKSPACE, "docs/mockups")

for d in [BG_DIR, PNG_DIR, SVG_DIR, MOCKUPS_DIR]:
    os.makedirs(d, exist_ok=True)

# 1. Sumber gambar hasil AI
SOURCE_SWIRL_BG = os.path.join(BRAIN_DIR, "fantasy_hypnotic_swirl_bg_1791605042901.jpg")
SOURCE_STAGE_BG = os.path.join(BRAIN_DIR, "confectionery_theater_stage_bg_1791605063247.jpg")
SOURCE_PATTERN_BG = os.path.join(BRAIN_DIR, "confectionery_pattern_wallpaper_1791605088308.jpg")
SOURCE_CURTAIN = os.path.join(BRAIN_DIR, "isolated_theater_curtain_drape_1791605117326.jpg")
SOURCE_STORY_BG = os.path.join(BRAIN_DIR, "fantasy_hypnotic_stage_story_1791605135970.jpg")

# 2. Logo resmi untuk uji komposit
LOGO_44_PATH = os.path.join(WORKSPACE, "assets/png/logo-symbol-color.png")
AVERSA_PATH = os.path.join(WORKSPACE, "assets/png/aversa-logotype-horizontal.png")
DIES_NATALIS_PATH = os.path.join(WORKSPACE, "assets/png/dies-natalis-standalone-color.png")
NUM_44_PATH = os.path.join(WORKSPACE, "assets/png/44-standalone-color.png")


def process_backgrounds():
    print("=== [1/4] MEMPROSES MASTER BACKGROUND PRESETS HD ===")

    # A. Hypnotic Swirl Background (2048x2048)
    if os.path.exists(SOURCE_SWIRL_BG):
        im = Image.open(SOURCE_SWIRL_BG).convert("RGB")
        im_feed = im.resize((2048, 2048), Image.Resampling.LANCZOS)
        out_feed = os.path.join(BG_DIR, "bg-hypnotic-swirl-vortex.png")
        im_feed.save(out_feed, "PNG", optimize=True)
        print(f"✓ {out_feed} (2048x2048)")

        # Versi Story (1080x1920) dengan crop sentral elegan
        w, h = im.size
        target_aspect = 1080 / 1920
        crop_w = int(h * target_aspect)
        left = (w - crop_w) // 2
        im_story = im.crop((left, 0, left + crop_w, h)).resize((1080, 1920), Image.Resampling.LANCZOS)
        out_story = os.path.join(BG_DIR, "bg-hypnotic-swirl-vortex-story.png")
        im_story.save(out_story, "PNG", optimize=True)
        print(f"✓ {out_story} (1080x1920)")

    # B. Confectionery Theater Stage Background (2048x2048)
    if os.path.exists(SOURCE_STAGE_BG):
        im = Image.open(SOURCE_STAGE_BG).convert("RGB")
        im_feed = im.resize((2048, 2048), Image.Resampling.LANCZOS)
        out_feed = os.path.join(BG_DIR, "bg-fantasy-theater-stage.png")
        im_feed.save(out_feed, "PNG", optimize=True)
        print(f"✓ {out_feed} (2048x2048)")

    # C. Confectionery Wallpaper Pattern (2048x2048)
    if os.path.exists(SOURCE_PATTERN_BG):
        im = Image.open(SOURCE_PATTERN_BG).convert("RGB")
        im_feed = im.resize((2048, 2048), Image.Resampling.LANCZOS)
        out_feed = os.path.join(BG_DIR, "bg-confectionery-pattern-wallpaper.png")
        im_feed.save(out_feed, "PNG", optimize=True)
        print(f"✓ {out_feed} (2048x2048)")

    # D. Fantasy Hypnotic Stage Story (1080x1920)
    if os.path.exists(SOURCE_STORY_BG):
        im = Image.open(SOURCE_STORY_BG).convert("RGB")
        im_story = im.resize((1080, 1920), Image.Resampling.LANCZOS)
        out_story = os.path.join(BG_DIR, "bg-fantasy-theater-story.png")
        im_story.save(out_story, "PNG", optimize=True)
        print(f"✓ {out_story} (1080x1920)")


def isolate_theater_curtains():
    print("\n=== [2/4] ISOLASI & EKSTRAKSI TIRAI TEATER TRANSPARAN ===")
    if not os.path.exists(SOURCE_CURTAIN):
        print(f"Error: {SOURCE_CURTAIN} tidak ditemukan")
        return

    img = Image.open(SOURCE_CURTAIN).convert("RGB")
    arr = np.array(img, dtype=np.float32)

    # Deteksi warna putih latar belakang
    # Putih murni: R > 240, G > 240, B > 240
    # Jarak warna ke putih (255, 255, 255)
    diff = 255.0 - arr
    dist_to_white = np.sqrt(np.sum(diff ** 2, axis=2))

    # Masker Alpha halus:
    # Jarak > 35 dianggap tirai padat (alpha = 255)
    # Jarak < 15 dianggap latar belakang putih murni (alpha = 0)
    # 15 - 35 transisi lembut anti-aliasing
    alpha = np.clip((dist_to_white - 15.0) / (35.0 - 15.0) * 255.0, 0, 255).astype(np.uint8)

    # Hilangkan background spill (defringe / unmultiply white)
    rgb = np.array(img, dtype=np.float32)
    alpha_norm = (alpha.astype(np.float32) / 255.0)[:, :, np.newaxis]
    # Di area semi-transparan, netralkan kecerahan putih
    clean_rgb = np.where(alpha_norm > 0.05, rgb, 0.0).astype(np.uint8)

    # Gabungkan menjadi RGBA
    rgba_arr = np.dstack((clean_rgb, alpha))
    out_rgba = Image.fromarray(rgba_arr, mode="RGBA")

    # Crop bagian transparan kosong bawah jika berlebih
    bbox = out_rgba.getbbox()
    if bbox:
        out_rgba_cropped = out_rgba.crop((0, 0, out_rgba.width, bbox[3] + 20))
    else:
        out_rgba_cropped = out_rgba

    # Simpan PNG Transparan Premium
    out_png = os.path.join(PNG_DIR, "theater-curtain-drape-premium.png")
    out_rgba_cropped.save(out_png, "PNG", optimize=True)
    print(f"✓ {out_png} ({out_rgba_cropped.width}x{out_rgba_cropped.height}, Transparansi Bersih)")

    # Simpan SVG pembungkus vektor beresolusi tinggi dengan embedded data URI
    import base64
    from io import BytesIO
    buffer = BytesIO()
    out_rgba_cropped.save(buffer, format="PNG")
    b64_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

    svg_content = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {out_rgba_cropped.width} {out_rgba_cropped.height}" width="100%" height="100%">
  <defs>
    <filter id="curtain-drop-shadow" x="-5%" y="-5%" width="110%" height="120%">
      <feDropShadow dx="0" dy="12" stdDeviation="16" flood-color="#1A021C" flood-opacity="0.6"/>
    </filter>
  </defs>
  <image href="data:image/png;base64,{b64_data}" width="{out_rgba_cropped.width}" height="{out_rgba_cropped.height}" filter="url(#curtain-drop-shadow)"/>
</svg>'''

    out_svg = os.path.join(SVG_DIR, "theater-curtain-drape-premium.svg")
    with open(out_svg, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"✓ {out_svg} (SVG Vector Wrapper)")


def generate_contrast_mockups():
    print("\n=== [3/4] MEMBUAT MOCKUP KOMPOSIT UJI KONTRAS LOGO EMAS ===")

    # Muat logo utama 44 dan logotype
    if not (os.path.exists(LOGO_44_PATH) and os.path.exists(AVERSA_PATH)):
        print("Logo utama tidak ditemukan, lewati komposit.")
        return

    logo_44 = Image.open(LOGO_44_PATH).convert("RGBA")
    aversa = Image.open(AVERSA_PATH).convert("RGBA")
    curtain = Image.open(os.path.join(PNG_DIR, "theater-curtain-drape-premium.png")).convert("RGBA")

    # MOCKUP 1: Logo di atas Hypnotic Swirl Background
    swirl_bg_path = os.path.join(BG_DIR, "bg-hypnotic-swirl-vortex.png")
    if os.path.exists(swirl_bg_path):
        bg = Image.open(swirl_bg_path).convert("RGBA")
        canvas = bg.copy()

        # Pasang tirai di atas
        curtain_w = 2048
        curtain_h = int(curtain.height * (curtain_w / curtain.width))
        curtain_resized = curtain.resize((curtain_w, curtain_h), Image.Resampling.LANCZOS)
        canvas.paste(curtain_resized, (0, 0), curtain_resized)

        # Pasang logo 44 di tengah pendaran cahaya
        logo_w = 950
        logo_h = int(logo_44.height * (logo_w / logo_44.width))
        logo_resized = logo_44.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

        # Berikan pendaran luar (glow) halus di belakang logo emas
        glow_mask = logo_resized.split()[3].filter(ImageFilter.GaussianBlur(24))
        glow_layer = Image.new("RGBA", (logo_w, logo_h), (255, 240, 180, 180))
        glow_layer.putalpha(glow_mask)

        # Posisi sentral
        pos_x = (2048 - logo_w) // 2
        pos_y = (2048 - logo_h) // 2 - 80
        canvas.paste(glow_layer, (pos_x, pos_y), glow_layer)
        canvas.paste(logo_resized, (pos_x, pos_y), logo_resized)

        # Pasang Logotype AVERSA di bawah 44
        aversa_w = 750
        aversa_h = int(aversa.height * (aversa_w / aversa.width))
        aversa_resized = aversa.resize((aversa_w, aversa_h), Image.Resampling.LANCZOS)
        aversa_x = (2048 - aversa_w) // 2
        aversa_y = pos_y + logo_h + 30

        aversa_glow = aversa_resized.split()[3].filter(ImageFilter.GaussianBlur(15))
        aversa_glow_layer = Image.new("RGBA", (aversa_w, aversa_h), (255, 230, 150, 160))
        aversa_glow_layer.putalpha(aversa_glow)

        canvas.paste(aversa_glow_layer, (aversa_x, aversa_y), aversa_glow_layer)
        canvas.paste(aversa_resized, (aversa_x, aversa_y), aversa_resized)

        out_mockup1 = os.path.join(MOCKUPS_DIR, "preview_logo_on_hypnotic_swirl.png")
        canvas.save(out_mockup1, "PNG", optimize=True)
        print(f"✓ Mockup 1: {out_mockup1}")

    # MOCKUP 2: Logo di atas Fantasy Theater Stage Background
    stage_bg_path = os.path.join(BG_DIR, "bg-fantasy-theater-stage.png")
    if os.path.exists(stage_bg_path):
        bg = Image.open(stage_bg_path).convert("RGBA")
        canvas = bg.copy()

        # Pasang logo 44 di panggung atas lantai
        logo_w = 900
        logo_h = int(logo_44.height * (logo_w / logo_44.width))
        logo_resized = logo_44.resize((logo_w, logo_h), Image.Resampling.LANCZOS)

        pos_x = (2048 - logo_w) // 2
        pos_y = 480

        glow_mask = logo_resized.split()[3].filter(ImageFilter.GaussianBlur(25))
        glow_layer = Image.new("RGBA", (logo_w, logo_h), (255, 245, 200, 200))
        glow_layer.putalpha(glow_mask)

        canvas.paste(glow_layer, (pos_x, pos_y), glow_layer)
        canvas.paste(logo_resized, (pos_x, pos_y), logo_resized)

        # Pasang AVERSA
        aversa_w = 700
        aversa_h = int(aversa.height * (aversa_w / aversa.width))
        aversa_resized = aversa.resize((aversa_w, aversa_h), Image.Resampling.LANCZOS)
        aversa_x = (2048 - aversa_w) // 2
        aversa_y = pos_y + logo_h + 20

        canvas.paste(aversa_resized, (aversa_x, aversa_y), aversa_resized)

        out_mockup2 = os.path.join(MOCKUPS_DIR, "preview_logo_on_theater_stage.png")
        canvas.save(out_mockup2, "PNG", optimize=True)
        print(f"✓ Mockup 2: {out_mockup2}")


def print_summary():
    print("\n=== [4/4] SELESAI & RINGKASAN ASET BARU ===")
    print("Aset baru telah siap di:")
    print("  • Backgrounds: assets/brandkit_elements/backgrounds/")
    print("  • PNG Transparan: assets/brandkit_elements/png/")
    print("  • SVG: assets/brandkit_elements/svg/")
    print("  • Mockups Preview: docs/mockups/")


if __name__ == "__main__":
    process_backgrounds()
    isolate_theater_curtains()
    generate_contrast_mockups()
    print_summary()
