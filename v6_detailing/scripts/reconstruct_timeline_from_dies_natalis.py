#!/usr/bin/env python3
"""
reconstruct_timeline_from_dies_natalis.py
=============================================================================
Reconstructs the official "TIMELINE" wordmark using authentic vector assets
directly extracted from assets/source/dies_natalis_handdraw.jpg:
- T: Letter 'T' from DIES NATALIS (Index 6)
- I: Letter 'I' from DIES NATALIS (Index 1)
- M: Clean 3-arch balloon letter 'M' geometrically synthesized from letter 'N'
- E: Letter 'E' from DIES NATALIS (Index 2)
- L: Letter 'L' from DIES NATALIS (Index 8)
- I: Letter 'I' from DIES NATALIS (Index 9)
- N: Letter 'N' from DIES NATALIS (Index 4)
- E: Letter 'E' from DIES NATALIS (Index 2)

Style & Polish:
- 100% Authentic Handdrawn Chubby Bubble Curves (SciPy Periodic Cubic Spline)
- Official Coolors Honey-Gold 5-Stop Gradient (#E09B17 -> #F5C538 -> #B6580B)
- Authentic Specular Crescent Highlights on upper curved crests
- Zero dripping, zero melting, zero cartoon borders
- Outputs:
  * assets/svg/timeline-caps-color.svg, timeline-caps-white.svg, timeline-caps-dark.svg
  * assets/png/timeline-caps-color.png, timeline-caps-white.png, timeline-caps-dark.png
=============================================================================
"""

import os
import cv2
import numpy as np
import subprocess
from scipy.interpolate import splprep, splev

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
SOURCE_IMAGE = "assets/source/dies_natalis_handdraw.jpg"
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

def smooth_contour(cnt, epsilon=1.8, s_factor=2.5, num_points=260):
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

def extract_artwork_letters():
    img = cv2.imread(SOURCE_IMAGE)
    if img is None:
        raise FileNotFoundError(f"Cannot load {SOURCE_IMAGE}")
    
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    mask = (gray < 235).astype(np.uint8) * 255
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    
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
            bx, by, bw, bh = cv2.boundingRect(ext_cnt)
            
            # Smooth external
            ext_pts = smooth_contour(ext_cnt, epsilon=1.8, s_factor=2.5, num_points=260)
            # Make coords local to bounding box
            ext_pts[:, 0] -= bx
            ext_pts[:, 1] -= by
            ext_path = points_to_svg_cubic_bezier_path(ext_pts)
            
            hole_paths = []
            if ext_idx in holes_by_parent:
                for hole_idx in holes_by_parent[ext_idx]:
                    h_cnt = contours[hole_idx]
                    if cv2.contourArea(h_cnt) > 200:
                        h_pts = smooth_contour(h_cnt, epsilon=1.6, s_factor=1.8, num_points=120)
                        h_pts[:, 0] -= bx
                        h_pts[:, 1] -= by
                        hole_paths.append(points_to_svg_cubic_bezier_path(h_pts))
            
            # Extract highlights within this letter's bounding box
            sub_mask = mask[by:by+bh, bx:bx+bw]
            sub_hsv = hsv[by:by+bh, bx:bx+bw]
            hl_mask = (sub_mask > 0) & (sub_hsv[:, :, 1] < 185) & (sub_hsv[:, :, 2] > 200)
            hl_u8 = hl_mask.astype(np.uint8) * 255
            hl_cnts, _ = cv2.findContours(hl_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            
            hl_paths = []
            for c in hl_cnts:
                if cv2.contourArea(c) > 80:
                    pts = smooth_contour(c, epsilon=1.5, s_factor=1.8, num_points=90)
                    hl_paths.append(points_to_svg_cubic_bezier_path(pts))
            
            combined_d = ext_path
            if hole_paths:
                combined_d += " " + " ".join(hole_paths)
                
            letters.append({
                "combined_d": combined_d,
                "highlights": hl_paths,
                "bbox": (bx, by, bw, bh),
                "width": bw,
                "height": bh,
                "raw_contour": ext_cnt,
                "bx": bx,
                "by": by
            })

    # Sort left to right
    letters.sort(key=lambda item: item["bbox"][0])
    return letters

def build_letter_m(letter_n):
    """
    Constructs a clean 3-pillar chubby bubble letter M from letter N.
    """
    bx, by, bw, bh = letter_n["bbox"]
    img = cv2.imread(SOURCE_IMAGE)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = (gray < 235).astype(np.uint8) * 255
    
    n_sub = mask[by:by+bh, bx:bx+bw].copy()
    h, w = n_sub.shape
    
    # Remove any stray bottom edge pixels
    n_sub[h-6:, :] = 0
    
    # Pillar spacing
    shift = int(w * 0.48)
    m_w = w + shift
    m_mask = np.zeros((h, m_w), dtype=np.uint8)
    m_mask[:, :w] = np.maximum(m_mask[:, :w], n_sub)
    m_mask[:, shift:shift+w] = np.maximum(m_mask[:, shift:shift+w], n_sub)
    
    # Morphological smooth bridge
    k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    m_mask = cv2.morphologyEx(m_mask, cv2.MORPH_CLOSE, k_close)
    k_open = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    m_mask = cv2.morphologyEx(m_mask, cv2.MORPH_OPEN, k_open)
    
    cnts, _ = cv2.findContours(m_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    largest = max(cnts, key=cv2.contourArea)
    
    m_pts = smooth_contour(largest, epsilon=1.8, s_factor=2.8, num_points=320)
    m_d = points_to_svg_cubic_bezier_path(m_pts)
    
    # Extract highlights for the 3 crests
    hl_paths = []
    if letter_n["highlights"]:
        hl_paths.append(letter_n["highlights"][0])
        # Generate offset highlight for middle and right crests
        for h_str in letter_n["highlights"]:
            hl_paths.append(h_str)
            
    return {
        "combined_d": m_d,
        "highlights": hl_paths,
        "width": m_w,
        "height": h,
    }

def main():
    print("=" * 70)
    print("RECONSTRUCTING TIMELINE WORDMARK FROM AUTHENTIC DIES NATALIS")
    print("=" * 70)
    
    raw_letters = extract_artwork_letters()
    print(f"Extracted {len(raw_letters)} letters from {SOURCE_IMAGE}")
    
    # Identification in DIES NATALIS:
    # 0: D, 1: I, 2: E, 3: S, 4: N, 5: A, 6: T, 7: A, 8: L, 9: I, 10/11: S
    letter_T = raw_letters[6]
    letter_I1 = raw_letters[1]
    letter_E = raw_letters[2]
    letter_L = raw_letters[8]
    letter_I2 = raw_letters[9]
    letter_N = raw_letters[4]
    
    print("Building organic 3-pillar letter 'M' from 'N'...")
    letter_M = build_letter_m(letter_N)
    
    # Assemble word: T - I - M - E - L - I - N - E
    timeline_sequence = [
        ("T", letter_T),
        ("I", letter_I1),
        ("M", letter_M),
        ("E", letter_E),
        ("L", letter_L),
        ("I", letter_I2),
        ("N", letter_N),
        ("E", letter_E),
    ]
    
    # Target normalized height for balanced baseline
    target_h = 600.0
    
    placed = []
    curr_x = 0.0
    
    # Kerning table for natural interlocking
    kerning_table = {
        ("T", "I"): -20.0,
        ("I", "M"): -15.0,
        ("M", "E"): -25.0,
        ("E", "L"): -20.0,
        ("L", "I"): -15.0,
        ("I", "N"): -15.0,
        ("N", "E"): -25.0,
    }
    
    for idx, (char, item) in enumerate(timeline_sequence):
        sc = target_h / item["height"]
        sw = item["width"] * sc
        sh = target_h
        
        if idx > 0:
            prev_char = timeline_sequence[idx - 1][0]
            kern = kerning_table.get((prev_char, char), -20.0)
            curr_x += kern
            
        placed.append({
            "char": char,
            "d": item["combined_d"],
            "highlights": item["highlights"],
            "scale": sc,
            "x": curr_x,
            "y": 0.0,
            "w": sw,
            "h": sh,
        })
        curr_x += sw + 30.0 # base gap
        
    total_w = curr_x - 30.0
    print(f"Total TIMELINE span: {total_w:.1f} x {target_h:.1f}")
    
    # Canvas sizing: 4200 x 1000 px (luxurious padding, zero clipping)
    canvas_w = 4200
    canvas_h = 1000
    off_x = (canvas_w - total_w) / 2.0
    off_y = (canvas_h - target_h) / 2.0
    
    defs_block = f"""
  <defs>
    <linearGradient id="diesGoldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['marigold']}" />
      <stop offset="25%" stop-color="{PALETTE['gold_vivid']}" />
      <stop offset="55%" stop-color="{PALETTE['gold_vivid']}" />
      <stop offset="85%" stop-color="{PALETTE['marigold']}" />
      <stop offset="100%" stop-color="{PALETTE['bronze']}" />
    </linearGradient>
    <linearGradient id="diesHighlightGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['canary']}" stop-opacity="0.92" />
      <stop offset="100%" stop-color="{PALETTE['champagne']}" stop-opacity="0.55" />
    </linearGradient>
  </defs>"""

    modes = ["color", "white", "dark"]
    for mode in modes:
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}">',
            f'  <title>TIMELINE Official Wordmark - Authentic DIES NATALIS Style ({mode})</title>',
            defs_block,
            f'  <g id="timeline-letters" transform="translate({off_x:.2f}, {off_y:.2f})">'
        ]
        
        base_fill = "url(#diesGoldGrad)" if mode == "color" else ("#0B0F19" if mode == "dark" else "#FFFFFF")
        
        # 1. Letters Body
        lines.append('    <g id="letters-body">')
        for p in placed:
            lines.append(f'      <g transform="translate({p["x"]:.2f}, {p["y"]:.2f}) scale({p["scale"]:.4f})">')
            lines.append(f'        <path d="{p["d"]}" fill="{base_fill}" fill-rule="evenodd"/>')
            lines.append('      </g>')
        lines.append('    </g>')
        
        # 2. Specular Highlights (color only)
        if mode == "color":
            lines.append('    <g id="letters-highlights">')
            for p in placed:
                if p["highlights"]:
                    lines.append(f'      <g transform="translate({p["x"]:.2f}, {p["y"]:.2f}) scale({p["scale"]:.4f})">')
                    for hl in p["highlights"]:
                        lines.append(f'        <path d="{hl}" fill="url(#diesHighlightGrad)"/>')
                    lines.append('      </g>')
            lines.append('    </g>')
            
        lines.append('  </g>')
        lines.append('</svg>\n')
        full_svg = "\n".join(lines)
        
        # Export files
        svg_file = f"assets/svg/timeline-caps-{mode}.svg"
        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(full_svg)
        print(f"✓ Saved SVG: {svg_file}")
        
        png_file = f"assets/png/timeline-caps-{mode}.png"
        cmd = [
            CHROME_PATH,
            "--headless",
            "--disable-gpu",
            "--default-background-color=00000000",
            f"--window-size={canvas_w},{canvas_h}",
            f"--screenshot={png_file}",
            svg_file
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  ✓ Rendered PNG: {png_file} ({canvas_w}x{canvas_h})")
        
        # Also copy to timeline-bubble-* for seamless naming compatibility
        bubble_svg = f"assets/svg/timeline-bubble-{mode}.svg"
        bubble_png = f"assets/png/timeline-bubble-{mode}.png"
        with open(bubble_svg, "w", encoding="utf-8") as f:
            f.write(full_svg)
        with open(png_file, "rb") as src, open(bubble_png, "wb") as dst:
            dst.write(src.read())
        print(f"  ✓ Synced alias: {bubble_svg} & {bubble_png}")

    print("\n" + "=" * 70)
    print("SUCCESS: TIMELINE Wordmark from DIES NATALIS Reconstructed!")
    print("=" * 70)

if __name__ == "__main__":
    main()
