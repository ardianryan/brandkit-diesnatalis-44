import os
import subprocess
import cv2
import numpy as np
from scipy.interpolate import splprep, splev
from PIL import Image

PALETTE = {
    "mahogany": "#310603",
    "rust": "#7D1B05",
    "bronze": "#B6580B",
    "marigold": "#E09B17",
    "gold_vivid": "#F5C538",
    "champagne": "#F7D160",
    "canary": "#FDF39D",
    "plum": "#360538"
}

def smooth_contour(cnt, s_factor=3.0, num_points=240):
    epsilon = 2.0
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    pts = approx.reshape(-1, 2)
    
    dx = np.diff(pts[:, 0])
    dy = np.diff(pts[:, 1])
    dist = np.hypot(dx, dy)
    keep = np.where(dist > 0.5)[0]
    pts = pts[np.append(keep, len(pts)-1)]
    
    if len(pts) < 4:
        return pts
        
    try:
        tck, u = splprep([pts[:, 0], pts[:, 1]], s=len(pts) * s_factor, per=True)
        u_new = np.linspace(0, 1, num_points)
        xs, ys = splev(u_new, tck)
        return np.column_stack([xs, ys])
    except Exception:
        return pts

def points_to_svg_path(pts):
    n = len(pts)
    if n < 3:
        return ""
    d = [f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"]
    for i in range(n):
        p0 = pts[(i - 1) % n]
        p1 = pts[i]
        p2 = pts[(i + 1) % n]
        p3 = pts[(i + 2) % n]
        
        c1x = p1[0] + (p2[0] - p0[0]) / 6.0
        c1y = p1[1] + (p2[1] - p0[1]) / 6.0
        c2x = p2[0] - (p3[0] - p1[0]) / 6.0
        c2y = p2[1] - (p3[1] - p1[1]) / 6.0
        
        d.append(f"C {c1x:.2f} {c1y:.2f}, {c2x:.2f} {c2y:.2f}, {p2[0]:.2f} {p2[1]:.2f}")
    d.append("Z")
    return " ".join(d)

def extract_artwork_data(image_path, hl_area_thresh=100, hl_sat_thresh=185):
    img = cv2.imread(image_path)
    h_img, w_img, _ = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    mask_letters = (gray < 235).astype(np.uint8) * 255
    contours, hierarchy = cv2.findContours(mask_letters, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    
    letters = []
    if hierarchy is not None:
        hier = hierarchy[0]
        externals = []
        holes_by_parent = {}
        for i, h in enumerate(hier):
            area = cv2.contourArea(contours[i])
            if area > 1000:
                if h[3] == -1:
                    externals.append(i)
                else:
                    holes_by_parent.setdefault(h[3], []).append(i)
        
        for ext_idx in externals:
            ext_cnt = contours[ext_idx]
            ext_pts = smooth_contour(ext_cnt, s_factor=2.5, num_points=260)
            hole_paths = []
            if ext_idx in holes_by_parent:
                for hole_idx in holes_by_parent[ext_idx]:
                    h_cnt = contours[hole_idx]
                    if cv2.contourArea(h_cnt) > 200:
                        h_pts = smooth_contour(h_cnt, s_factor=1.8, num_points=120)
                        hole_paths.append(points_to_svg_path(h_pts))
            
            letters.append({
                "external_path": points_to_svg_path(ext_pts),
                "hole_paths": hole_paths,
                "bbox": cv2.boundingRect(ext_cnt)
            })
            
    # Sort left to right
    letters.sort(key=lambda item: item["bbox"][0])
    
    # Highlights
    s_chan = hsv[:, :, 1]
    v_chan = hsv[:, :, 2]
    hl_mask = (mask_letters > 0) & (s_chan < hl_sat_thresh) & (v_chan > 200)
    hl_u8 = hl_mask.astype(np.uint8) * 255
    hl_cnts, _ = cv2.findContours(hl_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    highlights = []
    for c in hl_cnts:
        if cv2.contourArea(c) > hl_area_thresh:
            h_pts = smooth_contour(c, s_factor=2.0, num_points=100)
            highlights.append({
                "path": points_to_svg_path(h_pts),
                "bbox": cv2.boundingRect(c)
            })
            
    # Compute overall bounding box
    all_x = [l["bbox"][0] for l in letters] + [l["bbox"][0] + l["bbox"][2] for l in letters]
    all_y = [l["bbox"][1] for l in letters] + [l["bbox"][1] + l["bbox"][3] for l in letters]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)
    
    return {
        "letters": letters,
        "highlights": highlights,
        "width": max_x - min_x,
        "height": max_y - min_y,
        "min_x": min_x,
        "min_y": min_y,
        "max_x": max_x,
        "max_y": max_y
    }

def generate_svg(data, title, mode="color", canvas_w=3600, canvas_h=1800, padding=250):
    src_w = data["width"]
    src_h = data["height"]
    min_x = data["min_x"]
    min_y = data["min_y"]
    
    avail_w = canvas_w - (padding * 2)
    avail_h = canvas_h - (padding * 2)
    scale = min(avail_w / src_w, avail_h / src_h)
    
    tx = (canvas_w - (src_w * scale)) / 2.0 - (min_x * scale)
    ty = (canvas_h - (src_h * scale)) / 2.0 - (min_y * scale)
    
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}">',
        f'  <title>{title}</title>',
        '  <defs>'
    ]
    
    if mode == "color":
        lines.extend([
            '    <linearGradient id="goldGrad" x1="0%" y1="0%" x2="0%" y2="100%">',
            f'      <stop offset="0%" stop-color="{PALETTE["marigold"]}" />',
            f'      <stop offset="25%" stop-color="{PALETTE["gold_vivid"]}" />',
            f'      <stop offset="55%" stop-color="{PALETTE["gold_vivid"]}" />',
            f'      <stop offset="85%" stop-color="{PALETTE["marigold"]}" />',
            f'      <stop offset="100%" stop-color="{PALETTE["bronze"]}" />',
            '    </linearGradient>',
            '    <linearGradient id="highlightGrad" x1="0%" y1="0%" x2="0%" y2="100%">',
            f'      <stop offset="0%" stop-color="{PALETTE["canary"]}" stop-opacity="0.9" />',
            f'      <stop offset="100%" stop-color="{PALETTE["champagne"]}" stop-opacity="0.55" />',
            '    </linearGradient>'
        ])
    lines.append('  </defs>')
    
    base_fill = "url(#goldGrad)" if mode == "color" else ("#000000" if mode == "black" else "#FFFFFF")
    
    lines.append(f'  <g id="letters" transform="translate({tx:.2f}, {ty:.2f}) scale({scale:.4f})">')
    for l in data["letters"]:
        all_d = l["external_path"]
        if l["hole_paths"]:
            all_d += " " + " ".join(l["hole_paths"])
        lines.append(f'    <path d="{all_d}" fill="{base_fill}" fill-rule="evenodd"/>')
    lines.append('  </g>')
    
    if mode == "color":
        lines.append(f'  <g id="highlights" transform="translate({tx:.2f}, {ty:.2f}) scale({scale:.4f})">')
        for h in data["highlights"]:
            lines.append(f'    <path d="{h["path"]}" fill="url(#highlightGrad)"/>')
        lines.append('  </g>')
        
    lines.append('</svg>')
    return "\n".join(lines)

def generate_lockup_svg(dies_data, num_data, mode="color", canvas_w=3600, canvas_h=3600):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}">',
        f'  <title>DIES NATALIS 44 - Lockup Kombinasi ({mode})</title>',
        '  <defs>'
    ]
    if mode in ["color", "dark"]:
        lines.extend([
            '    <linearGradient id="lockupGold" x1="0%" y1="0%" x2="0%" y2="100%">',
            f'      <stop offset="0%" stop-color="{PALETTE["marigold"]}" />',
            f'      <stop offset="25%" stop-color="{PALETTE["gold_vivid"]}" />',
            f'      <stop offset="55%" stop-color="{PALETTE["gold_vivid"]}" />',
            f'      <stop offset="85%" stop-color="{PALETTE["marigold"]}" />',
            f'      <stop offset="100%" stop-color="{PALETTE["bronze"]}" />',
            '    </linearGradient>',
            '    <linearGradient id="lockupHighlight" x1="0%" y1="0%" x2="0%" y2="100%">',
            f'      <stop offset="0%" stop-color="{PALETTE["canary"]}" stop-opacity="0.9" />',
            f'      <stop offset="100%" stop-color="{PALETTE["champagne"]}" stop-opacity="0.55" />',
            '    </linearGradient>'
        ])
    lines.append('  </defs>')
    
    if mode == "dark":
        lines.append(f'  <rect width="{canvas_w}" height="{canvas_h}" fill="#0A0D14" />')
        
    base_fill = "url(#lockupGold)" if mode in ["color", "dark"] else ("#000000" if mode == "black" else "#FFFFFF")
    
    # Scale DIES NATALIS to span top (width ~ 3000)
    target_dies_w = 3000.0
    scale_dies = target_dies_w / dies_data["width"]
    scaled_dies_h = dies_data["height"] * scale_dies
    
    tx_dies = (canvas_w - target_dies_w) / 2.0 - (dies_data["min_x"] * scale_dies)
    ty_dies = 500.0 - (dies_data["min_y"] * scale_dies)
    
    # Scale 44 to sit prominently below (height ~ 1300)
    target_44_h = 1350.0
    scale_44 = target_44_h / num_data["height"]
    target_44_w = num_data["width"] * scale_44
    
    tx_44 = (canvas_w - target_44_w) / 2.0 - (num_data["min_x"] * scale_44)
    ty_44 = (ty_dies + dies_data["min_y"] * scale_dies + scaled_dies_h + 160.0) - (num_data["min_y"] * scale_44)
    
    # DIES NATALIS group
    lines.append(f'  <g id="dies-natalis" transform="translate({tx_dies:.2f}, {ty_dies:.2f}) scale({scale_dies:.4f})">')
    for l in dies_data["letters"]:
        all_d = l["external_path"]
        if l["hole_paths"]:
            all_d += " " + " ".join(l["hole_paths"])
        lines.append(f'    <path d="{all_d}" fill="{base_fill}" fill-rule="evenodd"/>')
    if mode in ["color", "dark"]:
        for h in dies_data["highlights"]:
            lines.append(f'    <path d="{h["path"]}" fill="url(#lockupHighlight)"/>')
    lines.append('  </g>')
    
    # NUMERAL 44 group
    lines.append(f'  <g id="numeral-44" transform="translate({tx_44:.2f}, {ty_44:.2f}) scale({scale_44:.4f})">')
    for l in num_data["letters"]:
        all_d = l["external_path"]
        if l["hole_paths"]:
            all_d += " " + " ".join(l["hole_paths"])
        lines.append(f'    <path d="{all_d}" fill="{base_fill}" fill-rule="evenodd"/>')
    if mode in ["color", "dark"]:
        for h in num_data["highlights"]:
            lines.append(f'    <path d="{h["path"]}" fill="url(#lockupHighlight)"/>')
    lines.append('  </g>')
    
    # Subtitle Ribbon underneath
    cy_sub = ty_44 + num_data["min_y"] * scale_44 + target_44_h + 140.0
    line_col = PALETTE["gold_vivid"] if mode == "dark" else PALETTE["marigold"]
    text_main = "#FFFFFF" if mode == "dark" else PALETTE["marigold"]
    text_sub = PALETTE["champagne"] if mode == "dark" else PALETTE["bronze"]
    
    lines.append(f'  <line x1="{canvas_w//2 - 650}" y1="{cy_sub}" x2="{canvas_w//2 + 650}" y2="{cy_sub}" stroke="{line_col}" stroke-width="3" stroke-linecap="round"/>')
    lines.append(f'  <circle cx="{canvas_w//2}" cy="{cy_sub}" r="8" fill="{PALETTE["gold_vivid"]}"/>')
    lines.append(f'  <text x="{canvas_w//2}" y="{cy_sub + 110}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="800" font-size="78" fill="{text_main}" letter-spacing="14">SMA NEGERI 1 GEDEG</text>')
    lines.append(f'  <text x="{canvas_w//2}" y="{cy_sub + 195}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="600" font-size="44" fill="{text_sub}" letter-spacing="8">1982 – 2026 • KABUPATEN MOJOKERTO</text>')
    
    lines.append('</svg>')
    return "\n".join(lines)

def demat_white_background(img_rgba):
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

def render_and_export(svg_path, out_png, canvas_w=3600, canvas_h=1400):
    abs_svg = os.path.abspath(svg_path)
    abs_out = os.path.abspath(out_png)
    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    cmd = [
        chrome_bin,
        "--headless",
        "--disable-gpu",
        "--default-background-color=00000000",
        f"--window-size={canvas_w},{canvas_h}",
        f"--screenshot={abs_out}",
        f"file://{abs_svg}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    os.makedirs("assets/svg", exist_ok=True)
    os.makedirs("assets/png", exist_ok=True)
    
    print("=== TAHAP 1: EKSTRAKSI VEKTOR DIES NATALIS & 44 ===")
    dies_data = extract_artwork_data("assets/source/dies_natalis_handdraw.jpg", hl_area_thresh=100, hl_sat_thresh=185)
    print(f"DIES NATALIS: {len(dies_data['letters'])} letters, {len(dies_data['highlights'])} highlights. Dims: {dies_data['width']}x{dies_data['height']}")
    
    num_data = extract_artwork_data("assets/source/numeral_44_handdraw.jpg", hl_area_thresh=200, hl_sat_thresh=180)
    print(f"NUMERAL 44: {len(num_data['letters'])} digits, {len(num_data['highlights'])} highlights. Dims: {num_data['width']}x{num_data['height']}")
    
    print("\n=== TAHAP 2: EKSPOR SVG STANDALONE & LOCKUP ===")
    # 1. DIES NATALIS Standalone (Canvas 3600 x 1400)
    for mode in ["color", "black", "white"]:
        svg_str = generate_svg(dies_data, f"DIES NATALIS - Bubble Lettering ({mode})", mode=mode, canvas_w=3600, canvas_h=1400, padding=180)
        svg_file = f"assets/svg/dies-natalis-bubble-{mode}.svg"
        with open(svg_file, "w") as f:
            f.write(svg_str)
        png_file = f"assets/png/dies-natalis-bubble-{mode}.png"
        render_and_export(svg_file, png_file, canvas_w=3600, canvas_h=1400)
        print(f"✓ {svg_file} & {png_file}")

    # 2. NUMERAL 44 Standalone (Canvas 2400 x 2400)
    for mode in ["color", "black", "white"]:
        svg_str = generate_svg(num_data, f"NUMERAL 44 - Bubble Lettering ({mode})", mode=mode, canvas_w=2400, canvas_h=2400, padding=200)
        svg_file = f"assets/svg/numeral-44-bubble-{mode}.svg"
        with open(svg_file, "w") as f:
            f.write(svg_str)
        png_file = f"assets/png/numeral-44-bubble-{mode}.png"
        render_and_export(svg_file, png_file, canvas_w=2400, canvas_h=2400)
        print(f"✓ {svg_file} & {png_file}")

    # 3. COMBINED LOCKUP (DIES NATALIS + 44) (Canvas 3600 x 3600)
    for mode in ["color", "dark"]:
        svg_str = generate_lockup_svg(dies_data, num_data, mode=mode, canvas_w=3600, canvas_h=3600)
        suffix = f"-{mode}" if mode == "dark" else ""
        svg_file = f"assets/svg/dies-natalis-44-lockup{suffix}.svg"
        with open(svg_file, "w") as f:
            f.write(svg_str)
        png_file = f"assets/png/dies-natalis-44-lockup{suffix}.png"
        render_and_export(svg_file, png_file, canvas_w=3600, canvas_h=3600)
        print(f"✓ {svg_file} & {png_file}")

    print("\n=== TAHAP 3: AUDIT TRANSPARANSI & OUTLINE ===")
    for check_png in [
        "assets/png/dies-natalis-bubble-color.png",
        "assets/png/numeral-44-bubble-color.png",
        "assets/png/dies-natalis-44-lockup.png"
    ]:
        im = Image.open(check_png)
        arr = np.array(im)
        alpha = arr[:, :, 3]
        rgb = arr[alpha > 128, :3]
        pale_white = ((rgb[:, 0] > 245) & (rgb[:, 1] > 245) & (rgb[:, 2] > 245)).sum()
        black_cnt = ((rgb[:, 0] < 30) & (rgb[:, 1] < 30) & (rgb[:, 2] < 30)).sum()
        print(f"{check_png}: Visible={len(rgb)} | White Halo={pale_white} | Black Corruption={black_cnt}")

if __name__ == "__main__":
    main()
