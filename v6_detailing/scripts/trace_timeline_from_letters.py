#!/usr/bin/env python3
"""
trace_timeline_from_letters.py
=============================================================================
Traces and vectorizes each individual AVERSA-style letter:
T, I, M, E, L, I, N, E
Using OpenCV + SciPy cubic spline / cubic Bezier smoothing.
Constructs the complete "TIMELINE" wordmark in 100% authentic AVERSA molten honey DNA:
- Letter E is extracted directly from the original aversa-handdraw.png
- Letters T, I, M, L, N are traced from individual AI-assisted reference tiles
- Assembles letters into an interlocking, fluid wordmark with authentic kerning
- Applies authentic Coolors Honey-Gold spectrum + specular crescent highlights
- Exports to:
  * assets/svg/timeline-aversa-color.svg, timeline-aversa-white.svg, timeline-aversa-dark.svg
  * assets/svg/timeline-caps-color.svg, timeline-caps-white.svg, timeline-caps-dark.svg
  * assets/png/timeline-aversa-color.png, timeline-aversa-white.png, timeline-aversa-dark.png
  * assets/png/timeline-caps-color.png, timeline-caps-white.png, timeline-caps-dark.png
=============================================================================
"""

import os
import cv2
import numpy as np
import subprocess
from scipy.interpolate import splprep, splev

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
ARTIFACTS_DIR = "/Users/ardianryan/.gemini/antigravity-ide/brain/1e5aebc6-88de-4318-a297-a371f05702be"
SVG_OUT_DIR = "assets/svg"
PNG_OUT_DIR = "assets/png"

os.makedirs(SVG_OUT_DIR, exist_ok=True)
os.makedirs(PNG_OUT_DIR, exist_ok=True)

PALETTE = {
    "marigold": "#E09B17",
    "gold_vivid": "#F5C538",
    "champagne": "#F7D160",
    "canary": "#FDF39D",
    "bronze": "#B6580B",
    "dark_slate": "#07090F",
}

def points_to_svg_cubic_bezier_path(pts):
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

def smooth_contour(cnt, epsilon=2.0, s_factor=3.0, num_points=260):
    approx = cv2.approxPolyDP(cnt, epsilon, True)
    pts = approx.reshape(-1, 2).astype(float)
    dx = np.diff(pts[:, 0])
    dy = np.diff(pts[:, 1])
    dist = np.hypot(dx, dy)
    keep = np.where(dist > 0.8)[0]
    pts = pts[np.append(keep, len(pts) - 1)]
    if len(pts) < 4:
        return pts
    try:
        tck, u = splprep([pts[:, 0], pts[:, 1]], s=len(pts) * s_factor, per=True)
        u_new = np.linspace(0, 1, num_points)
        xs, ys = splev(u_new, tck)
        return np.column_stack([xs, ys])
    except Exception:
        return pts

def extract_single_letter(img_path, is_white_bg=True, min_area=8000):
    """
    Extracts the main letter contour, holes, and highlights from a single-letter tile.
    """
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Cannot load image {img_path}")
        
    if img.shape[2] == 4 and not is_white_bg:
        alpha = img[:, :, 3]
        mask = (alpha > 40).astype(np.uint8) * 255
        bgr = img[:, :, :3]
    else:
        bgr = img[:, :, :3]
        gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        # White background threshold
        mask = (gray < 240).astype(np.uint8) * 255

    # Clean morphology
    kernel = np.ones((5, 5), np.uint8)
    mask_clean = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(mask_clean, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    if hierarchy is None:
        return None

    # Find the largest external contour (the letter)
    best_idx = -1
    best_area = 0
    for i, h in enumerate(hierarchy[0]):
        if h[3] == -1:
            area = cv2.contourArea(contours[i])
            if area > best_area:
                best_area = area
                best_idx = i

    if best_idx == -1:
        return None

    ext_cnt = contours[best_idx]
    bx, by, bw, bh = cv2.boundingRect(ext_cnt)
    ext_pts = smooth_contour(ext_cnt, epsilon=2.0, s_factor=3.0, num_points=260)
    # Translate relative to bounding box top-left
    ext_pts[:, 0] -= bx
    ext_pts[:, 1] -= by
    ext_path = points_to_svg_cubic_bezier_path(ext_pts)

    # Holes
    hole_paths = []
    child = hierarchy[0][best_idx][2]
    while child != -1:
        if cv2.contourArea(contours[child]) > 300:
            h_pts = smooth_contour(contours[child], epsilon=1.8, s_factor=2.2, num_points=140)
            h_pts[:, 0] -= bx
            h_pts[:, 1] -= by
            hole_paths.append(points_to_svg_cubic_bezier_path(h_pts))
        child = hierarchy[0][child][0]

    # Specular highlights (high value, low-mid saturation, upper half)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    v_chan = hsv[:, :, 2]
    s_chan = hsv[:, :, 1]
    hl_mask = (mask > 0) & (v_chan > 200) & (s_chan < 180)
    hl_u8 = hl_mask.astype(np.uint8) * 255
    hl_cnts, _ = cv2.findContours(hl_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    hl_paths = []
    for c in hl_cnts:
        if cv2.contourArea(c) > 350:
            pts = smooth_contour(c, epsilon=1.8, s_factor=2.0, num_points=100)
            pts[:, 0] -= bx
            pts[:, 1] -= by
            hl_paths.append(points_to_svg_cubic_bezier_path(pts))

    combined_d = ext_path
    if hole_paths:
        combined_d += " " + " ".join(hole_paths)

    return {
        "combined_d": combined_d,
        "highlights": hl_paths,
        "width": bw,
        "height": bh,
    }

def extract_letter_e_from_aversa():
    """
    Extracts the authentic 'E' directly from aversa-handdraw.png (the 3rd letter in AVERSA).
    """
    img_path = "aversa-handdraw.png"
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    alpha = img[:, :, 3]
    bgr = img[:, :, :3]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    mask = (alpha > 40).astype(np.uint8) * 255
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)

    # Find external letters sorted by X
    ext_list = []
    for i, h in enumerate(hierarchy[0]):
        if h[3] == -1 and cv2.contourArea(contours[i]) > 10000:
            bx, by, bw, bh = cv2.boundingRect(contours[i])
            ext_list.append((bx, i, bx, by, bw, bh))

    ext_list.sort(key=lambda x: x[0])
    # Letter E is the 3rd letter in A-V-E-R-S-A (index 2)
    e_item = ext_list[2]
    e_idx = e_item[1]
    bx, by, bw, bh = e_item[2], e_item[3], e_item[4], e_item[5]

    ext_pts = smooth_contour(contours[e_idx], epsilon=2.0, s_factor=3.0, num_points=260)
    ext_pts[:, 0] -= bx
    ext_pts[:, 1] -= by
    ext_path = points_to_svg_cubic_bezier_path(ext_pts)

    # Holes for E (if any)
    hole_paths = []
    child = hierarchy[0][e_idx][2]
    while child != -1:
        if cv2.contourArea(contours[child]) > 300:
            h_pts = smooth_contour(contours[child], epsilon=1.8, s_factor=2.2, num_points=140)
            h_pts[:, 0] -= bx
            h_pts[:, 1] -= by
            hole_paths.append(points_to_svg_cubic_bezier_path(h_pts))
        child = hierarchy[0][child][0]

    # Highlights in E bounding box
    sub_mask = mask[by:by+bh, bx:bx+bw]
    sub_hsv = hsv[by:by+bh, bx:bx+bw]
    hl_mask = (sub_mask > 0) & (sub_hsv[:, :, 2] > 200) & (sub_hsv[:, :, 1] < 185)
    hl_u8 = hl_mask.astype(np.uint8) * 255
    hl_cnts, _ = cv2.findContours(hl_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    hl_paths = []
    for c in hl_cnts:
        if cv2.contourArea(c) > 300:
            pts = smooth_contour(c, epsilon=1.8, s_factor=2.0, num_points=100)
            hl_paths.append(points_to_svg_cubic_bezier_path(pts))

    combined_d = ext_path
    if hole_paths:
        combined_d += " " + " ".join(hole_paths)

    return {
        "combined_d": combined_d,
        "highlights": hl_paths,
        "width": bw,
        "height": bh,
    }

def main():
    print("=" * 70)
    print("TRACING TIMELINE LETTERS USING INDIVIDUAL AVERSA TILES")
    print("=" * 70)

    # Paths to generated letter images
    letter_files = {
        "T": f"{ARTIFACTS_DIR}/letter_t_aversa_style_1791711365198.jpg",
        "I": f"{ARTIFACTS_DIR}/letter_i_aversa_style_1791711383377.jpg",
        "M": f"{ARTIFACTS_DIR}/letter_m_aversa_style_1791711404967.jpg",
        "L": f"{ARTIFACTS_DIR}/letter_l_aversa_style_1791711423412.jpg",
        "N": f"{ARTIFACTS_DIR}/letter_n_aversa_style_1791711448048.jpg",
    }

    letters_data = {}
    for char, fpath in letter_files.items():
        print(f"Extracting letter '{char}' from {os.path.basename(fpath)}...")
        letters_data[char] = extract_single_letter(fpath, is_white_bg=True)
        print(f"  ✓ '{char}': {letters_data[char]['width']}x{letters_data[char]['height']}, {len(letters_data[char]['highlights'])} highlights")

    # Extract original E from AVERSA
    print("Extracting authentic letter 'E' from aversa-handdraw.png...")
    letters_data["E"] = extract_letter_e_from_aversa()
    print(f"  ✓ 'E': {letters_data['E']['width']}x{letters_data['E']['height']}, {len(letters_data['E']['highlights'])} highlights")

    # Word sequence: T - I - M - E - L - I - N - E
    word_sequence = ["T", "I", "M", "E", "L", "I", "N", "E"]

    # Target normalized height for consistent baseline and ample canvas margins
    target_letter_h = 580.0

    # Layout computation with organic spacing
    placed_letters = []
    current_x = 0.0

    # Custom kerning adjustments between pairs
    kerning_map = {
        ("T", "I"): -20.0,
        ("I", "M"): -15.0,
        ("M", "E"): -30.0,
        ("E", "L"): -25.0,
        ("L", "I"): -20.0,
        ("I", "N"): -15.0,
        ("N", "E"): -30.0,
    }

    for idx, char in enumerate(word_sequence):
        ldata = letters_data[char]
        scale = target_letter_h / ldata["height"]
        scaled_w = ldata["width"] * scale
        scaled_h = target_letter_h

        # Apply kerning
        if idx > 0:
            prev_char = word_sequence[idx - 1]
            kern = kerning_map.get((prev_char, char), -20.0)
            current_x += kern

        placed_letters.append({
            "char": char,
            "data": ldata,
            "scale": scale,
            "x": current_x,
            "y": 0.0, # baseline
            "width": scaled_w,
            "height": scaled_h
        })
        current_x += scaled_w + 25.0 # base letter gap

    total_word_w = current_x - 25.0
    print(f"\nTotal wordmark span: {total_word_w:.1f} x {target_letter_h:.1f}")

    # Canvas dimensions: 4200 x 1000 (ample margins, zero clipping)
    canvas_w = 4200
    canvas_h = 1000
    offset_x = (canvas_w - total_word_w) / 2.0
    offset_y = (canvas_h - target_letter_h) / 2.0

    # Build SVG for each mode
    modes = ["color", "white", "dark"]

    defs_block = f"""
  <defs>
    <linearGradient id="aversaGoldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['marigold']}"/>
      <stop offset="25%" stop-color="{PALETTE['gold_vivid']}"/>
      <stop offset="55%" stop-color="{PALETTE['gold_vivid']}"/>
      <stop offset="85%" stop-color="{PALETTE['marigold']}"/>
      <stop offset="100%" stop-color="{PALETTE['bronze']}"/>
    </linearGradient>
    <linearGradient id="aversaHighlightGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['canary']}" stop-opacity="0.90"/>
      <stop offset="100%" stop-color="{PALETTE['champagne']}" stop-opacity="0.55"/>
    </linearGradient>
  </defs>"""

    for mode in modes:
        svg_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}">',
            f'  <title>TIMELINE Official Wordmark - Authentic AVERSA Molten Honey Style ({mode})</title>',
            defs_block,
            f'  <g id="timeline-letters" transform="translate({offset_x:.2f}, {offset_y:.2f})">'
        ]

        if mode == "color":
            # 1. Letters Body
            svg_lines.append('    <g id="body-group">')
            for item in placed_letters:
                d = item["data"]["combined_d"]
                sc = item["scale"]
                ix = item["x"]
                iy = item["y"]
                svg_lines.append(f'      <g transform="translate({ix:.2f}, {iy:.2f}) scale({sc:.4f})">')
                svg_lines.append(f'        <path d="{d}" fill="url(#aversaGoldGrad)" fill-rule="evenodd"/>')
                svg_lines.append('      </g>')
            svg_lines.append('    </g>')

            # 2. Highlights
            svg_lines.append('    <g id="highlights-group">')
            for item in placed_letters:
                hls = item["data"]["highlights"]
                sc = item["scale"]
                ix = item["x"]
                iy = item["y"]
                if hls:
                    svg_lines.append(f'      <g transform="translate({ix:.2f}, {iy:.2f}) scale({sc:.4f})">')
                    for hl in hls:
                        svg_lines.append(f'        <path d="{hl}" fill="url(#aversaHighlightGrad)"/>')
                    svg_lines.append('      </g>')
            svg_lines.append('    </g>')

        elif mode == "white":
            svg_lines.append('    <g id="body-white">')
            for item in placed_letters:
                d = item["data"]["combined_d"]
                sc = item["scale"]
                ix = item["x"]
                iy = item["y"]
                svg_lines.append(f'      <g transform="translate({ix:.2f}, {iy:.2f}) scale({sc:.4f})">')
                svg_lines.append(f'        <path d="{d}" fill="#FFFFFF" fill-rule="evenodd"/>')
                svg_lines.append('      </g>')
            svg_lines.append('    </g>')

        elif mode == "dark":
            svg_lines.append('    <g id="body-dark">')
            for item in placed_letters:
                d = item["data"]["combined_d"]
                sc = item["scale"]
                ix = item["x"]
                iy = item["y"]
                svg_lines.append(f'      <g transform="translate({ix:.2f}, {iy:.2f}) scale({sc:.4f})">')
                svg_lines.append(f'        <path d="{d}" fill="#0B0F19" fill-rule="evenodd"/>')
                svg_lines.append('      </g>')
            svg_lines.append('    </g>')

        svg_lines.append('  </g>')
        svg_lines.append('</svg>\n')
        full_svg = "\n".join(svg_lines)

        # Write to timeline-aversa-*.svg and overwrite timeline-caps-*.svg & timeline-bubble-*.svg
        target_svgs = [
            f"assets/svg/timeline-aversa-{mode}.svg",
            f"assets/svg/timeline-caps-{mode}.svg",
            f"assets/svg/timeline-bubble-{mode}.svg",
        ]

        for s_path in target_svgs:
            with open(s_path, "w", encoding="utf-8") as f:
                f.write(full_svg)
            print(f"✓ Saved SVG: {s_path}")

        # Render PNG for each
        target_pngs = [
            f"assets/png/timeline-aversa-{mode}.png",
            f"assets/png/timeline-caps-{mode}.png",
            f"assets/png/timeline-bubble-{mode}.png",
        ]

        master_png = target_pngs[0]
        cmd = [
            CHROME_PATH,
            "--headless",
            "--disable-gpu",
            "--default-background-color=00000000",
            f"--window-size={canvas_w},{canvas_h}",
            f"--screenshot={master_png}",
            target_svgs[0]
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  ✓ Rendered master PNG: {master_png}")

        # Copy to other PNG targets
        with open(master_png, "rb") as src:
            png_bytes = src.read()
        for p_path in target_pngs[1:]:
            with open(p_path, "wb") as dst:
                dst.write(png_bytes)
            print(f"  ✓ Synced PNG: {p_path}")

    print("\n" + "=" * 70)
    print("ALL AVERSA TIMELINE VECTOR ASSETS CREATED SUCCESSFULLY!")
    print("=" * 70)

if __name__ == "__main__":
    main()
