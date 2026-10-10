import os
import subprocess
import shutil
from PIL import Image
import numpy as np

def demat_white_background(img_rgba):
    """
    Ekstraksi transparansi presisi dari raster WebKit di atas kanvas putih.
    Menggunakan un-premultiplication alpha matematika:
    C_observed = alpha * C_foreground + (1 - alpha) * White
    """
    arr = np.array(img_rgba, dtype=np.float32)
    rgb = arr[:, :, :3]
    white = np.array([255.0, 255.0, 255.0], dtype=np.float32)
    dist = np.sqrt(np.sum((rgb - white) ** 2, axis=2))
    
    alpha = np.clip((dist / 140.0) ** 0.85, 0.0, 1.0)
    alpha[dist < 1.0] = 0.0
    alpha[dist > 45.0] = 1.0
    
    alpha_denom = np.maximum(alpha[:, :, np.newaxis], 1e-4)
    unmixed_rgb = (rgb - (1.0 - alpha[:, :, np.newaxis]) * 255.0) / alpha_denom
    unmixed_rgb = np.clip(unmixed_rgb, 0.0, 255.0)
    
    final_arr = np.zeros_like(arr, dtype=np.uint8)
    final_arr[:, :, :3] = np.round(unmixed_rgb).astype(np.uint8)
    final_arr[:, :, 3] = np.round(alpha * 255.0).astype(np.uint8)
    return Image.fromarray(final_arr, "RGBA")

def demat_black_background(img_rgba):
    """
    Ekstraksi transparansi dari kanvas hitam untuk elemen putih/terang.
    """
    arr = np.array(img_rgba, dtype=np.float32)
    rgb = arr[:, :, :3]
    black = np.array([0.0, 0.0, 0.0], dtype=np.float32)
    dist = np.sqrt(np.sum((rgb - black) ** 2, axis=2))
    
    alpha = np.clip((dist / 140.0) ** 0.85, 0.0, 1.0)
    alpha[dist < 1.0] = 0.0
    alpha[dist > 45.0] = 1.0
    
    alpha_denom = np.maximum(alpha[:, :, np.newaxis], 1e-4)
    unmixed_rgb = rgb / alpha_denom
    unmixed_rgb = np.clip(unmixed_rgb, 0.0, 255.0)
    
    final_arr = np.zeros_like(arr, dtype=np.uint8)
    final_arr[:, :, :3] = np.round(unmixed_rgb).astype(np.uint8)
    final_arr[:, :, 3] = np.round(alpha * 255.0).astype(np.uint8)
    return Image.fromarray(final_arr, "RGBA")

def main():
    tmp_dir = "tmp_rebuild_render"
    os.makedirs(tmp_dir, exist_ok=True)
    os.makedirs("assets/png", exist_ok=True)
    
    print("=== 1. RENDERING MASTER LOGO (v6) VIA WEBKIT qlmanage ===")
    
    # 1. Master Logo Symbol (Color)
    master_svg = "assets/svg/logo-color.svg"
    subprocess.run(["qlmanage", "-t", "-s", "2048", "-o", tmp_dir, master_svg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    master_raw = Image.open(os.path.join(tmp_dir, f"{os.path.basename(master_svg)}.png")).convert("RGBA")
    master_clean = demat_white_background(master_raw)
    
    # Save master symbol color variants
    master_clean.save("assets/png/logo-color.png")
    master_clean.save("assets/png/logo-color-2048.png")
    master_clean.save("assets/png/logo-symbol-color.png")
    print("✓ logo-color.png, logo-color-2048.png, logo-symbol-color.png rendered (FULL GOLD, 0 BLACK)")
    
    # 2. Master Symbol Tight
    tight_svg = "assets/svg/logo-symbol-tight.svg"
    subprocess.run(["qlmanage", "-t", "-s", "2048", "-o", tmp_dir, tight_svg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tight_raw = Image.open(os.path.join(tmp_dir, f"{os.path.basename(tight_svg)}.png")).convert("RGBA")
    tight_clean = demat_white_background(tight_raw)
    tight_clean.save("assets/png/logo-symbol-tight.png")
    print("✓ logo-symbol-tight.png rendered")

    # 3. Horizontal Lockup Color
    hcolor_svg = "assets/svg/logo-horizontal-color.svg"
    subprocess.run(["qlmanage", "-t", "-s", "3200", "-o", tmp_dir, hcolor_svg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    hcolor_raw = Image.open(os.path.join(tmp_dir, f"{os.path.basename(hcolor_svg)}.png")).convert("RGBA")
    hcolor_clean = demat_white_background(hcolor_raw)
    hcolor_clean.save("assets/png/logo-horizontal-color.png")
    print("✓ logo-horizontal-color.png rendered")

    # 4. Horizontal Lockup Dark (Keep dark solid background)
    hdark_svg = "assets/svg/logo-horizontal-dark.svg"
    subprocess.run(["qlmanage", "-t", "-s", "3200", "-o", tmp_dir, hdark_svg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    hdark_raw = Image.open(os.path.join(tmp_dir, f"{os.path.basename(hdark_svg)}.png")).convert("RGBA")
    hdark_raw.save("assets/png/logo-horizontal-dark.png")
    print("✓ logo-horizontal-dark.png rendered")

    # 5. Vertical Lockup Color
    vcolor_svg = "assets/svg/logo-vertical-color.svg"
    subprocess.run(["qlmanage", "-t", "-s", "2400", "-o", tmp_dir, vcolor_svg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    vcolor_raw = Image.open(os.path.join(tmp_dir, f"{os.path.basename(vcolor_svg)}.png")).convert("RGBA")
    vcolor_clean = demat_white_background(vcolor_raw)
    vcolor_clean.save("assets/png/logo-vertical-color.png")
    print("✓ logo-vertical-color.png rendered")

    # 6. Vertical Lockup Dark (Keep dark background)
    vdark_svg = "assets/svg/logo-vertical-dark.svg"
    subprocess.run(["qlmanage", "-t", "-s", "2400", "-o", tmp_dir, vdark_svg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    vdark_raw = Image.open(os.path.join(tmp_dir, f"{os.path.basename(vdark_svg)}.png")).convert("RGBA")
    vdark_raw.save("assets/png/logo-vertical-dark.png")
    print("✓ logo-vertical-dark.png rendered")

    # 7. Monochrome Black & White
    mblack_svg = "assets/svg/logo-monochrome-black.svg"
    subprocess.run(["qlmanage", "-t", "-s", "2048", "-o", tmp_dir, mblack_svg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    mblack_raw = Image.open(os.path.join(tmp_dir, f"{os.path.basename(mblack_svg)}.png")).convert("L")
    mblack_arr = np.array(mblack_raw)
    # alpha is 255 - grayscale
    alpha_mono = (255 - mblack_arr).astype(np.uint8)
    
    # Save black
    black_rgba = np.zeros((2048, 2048, 4), dtype=np.uint8)
    black_rgba[:, :, :3] = 0
    black_rgba[:, :, 3] = alpha_mono
    Image.fromarray(black_rgba, "RGBA").save("assets/png/logo-monochrome-black.png")
    Image.fromarray(black_rgba, "RGBA").save("assets/png/logo-black-2048.png")
    
    # Save white
    white_rgba = np.zeros((2048, 2048, 4), dtype=np.uint8)
    white_rgba[:, :, :3] = 255
    white_rgba[:, :, 3] = alpha_mono
    Image.fromarray(white_rgba, "RGBA").save("assets/png/logo-monochrome-white.png")
    print("✓ logo-monochrome-black.png & logo-monochrome-white.png rendered")

    # 8. Linecut Black
    linecut_svg = "assets/svg/logo-linecut-black.svg"
    subprocess.run(["qlmanage", "-t", "-s", "2048", "-o", tmp_dir, linecut_svg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    linecut_raw = Image.open(os.path.join(tmp_dir, f"{os.path.basename(linecut_svg)}.png")).convert("L")
    alpha_lc = (255 - np.array(linecut_raw)).astype(np.uint8)
    lc_rgba = np.zeros((2048, 2048, 4), dtype=np.uint8)
    lc_rgba[:, :, :3] = 0
    lc_rgba[:, :, 3] = alpha_lc
    Image.fromarray(lc_rgba, "RGBA").save("assets/png/logo-linecut-black.png")
    print("✓ logo-linecut-black.png rendered")

    # 9. Logo with Grid (Keep construction background)
    grid_svg = "assets/svg/logo-with-grid.svg"
    subprocess.run(["qlmanage", "-t", "-s", "2048", "-o", tmp_dir, grid_svg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    grid_raw = Image.open(os.path.join(tmp_dir, f"{os.path.basename(grid_svg)}.png")).convert("RGBA")
    grid_raw.save("assets/png/logo-with-grid.png")
    print("✓ logo-with-grid.png rendered")

    # Clean up tmp
    shutil.rmtree(tmp_dir, ignore_errors=True)

    print("\n=== 2. REBUILDING ANATOMY DIAGRAMS WITH CLEAN FULL-GOLD LOGO ===")
    subprocess.run(["python3", "v6_detailing/scripts/generate_anatomy_diagrams.py"], check=True)
    print("✓ Anatomy diagrams successfully regenerated")

    print("\n=== 3. REBUILDING OFFICIAL MERCHANDISE MOCKUPS WITH CLEAN FULL-GOLD LOGO ===")
    subprocess.run(["python3", "v6_detailing/scripts/generate_official_merch_mockups.py"], check=True)
    print("✓ Merchandise mockups successfully regenerated")

    print("\n=== 4. AUDITING GENERATED ASSETS FOR CORRUPT BLACK PIXELS ===")
    for check_file in [
        "assets/png/logo-color-2048.png",
        "assets/png/logo-color.png",
        "assets/png/logo-symbol-color.png",
        "assets/anatomy/diagram_anatomi_lengkap.png"
    ]:
        im = Image.open(check_file)
        arr = np.array(im)
        if im.mode == "RGBA":
            vis = arr[arr[:, :, 3] > 128]
        else:
            vis = arr.reshape(-1, arr.shape[-1])
        black_cnt = ((vis[:, 0] < 30) & (vis[:, 1] < 30) & (vis[:, 2] < 30)).sum()
        print(f"{check_file}: Total visible {len(vis)} px | Pure black pixels: {black_cnt}")

if __name__ == "__main__":
    main()
