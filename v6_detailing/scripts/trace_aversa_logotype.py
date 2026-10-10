import os
import cv2
import numpy as np
import subprocess
from scipy.interpolate import splprep, splev
from PIL import Image

# ==============================================================================
# OFFICIAL DIES NATALIS 44 COOLORS PALETTE (AUTHENTIC HONEY GOLD SPECTRUM)
# ==============================================================================
PALETTE = {
    "marigold": "#E09B17",     # Dominant warm golden orange (top & mid-lower)
    "gold_vivid": "#F5C538",   # Brilliant honey gold (core body)
    "champagne": "#F7D160",    # Soft golden gleam
    "canary": "#FDF39D",       # Specular crest highlight
    "bronze": "#B6580B",       # Warm bottom shading & secondary text
    "rust": "#7D1B05",         # Deep accent
    "mahogany": "#310603",     # Deepest obsidian mahogany
    "dark_slate": "#07090F",   # Jet black
}

def points_to_svg_cubic_bezier_path(pts):
    """
    Converts smoothed polygon vertices into an exact C^1 cubic Bezier SVG path
    using Catmull-Rom to Cubic Bezier conversion.
    """
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

def smooth_contour(cnt, epsilon=2.2, s_factor=3.0, num_points=260):
    """
    Applies Douglas-Peucker polygon simplification followed by periodic
    cubic spline smoothing (SciPy splprep) to eliminate hand-drawing jitter.
    """
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

def extract_aversa_vector_data(image_path="aversa handdraw.png"):
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"Cannot load image {image_path}")
        
    alpha = img[:, :, 3]
    bgr = img[:, :, :3]
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    
    # 1. Base Letter Contours with Hierarchy
    base_mask = (alpha > 40).astype(np.uint8) * 255
    contours, hierarchy = cv2.findContours(base_mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    
    externals = []
    children_map = {}
    for i, h in enumerate(hierarchy[0]):
        next_c, prev_c, first_child, parent = h
        if parent == -1 and cv2.contourArea(contours[i]) > 10000:
            externals.append(i)
            ch_list = []
            c_idx = first_child
            while c_idx != -1:
                if cv2.contourArea(contours[c_idx]) > 500:
                    ch_list.append(c_idx)
                c_idx = hierarchy[0][c_idx][0]
            children_map[i] = ch_list
            
    externals.sort(key=lambda idx: cv2.boundingRect(contours[idx])[0])
    
    all_letter_pts = np.vstack([contours[idx].reshape(-1, 2) for idx in externals])
    min_x, min_y = np.min(all_letter_pts, axis=0)
    max_x, max_y = np.max(all_letter_pts, axis=0)
    
    pad_x = 60.0
    pad_y = 60.0
    offset_x = min_x - pad_x
    offset_y = min_y - pad_y
    total_w = (max_x - min_x) + pad_x * 2
    total_h = (max_y - min_y) + pad_y * 2
    
    letters_data = []
    for letter_idx, c_idx in enumerate(externals):
        raw_cnt = contours[c_idx]
        sm_pts = smooth_contour(raw_cnt, epsilon=2.2, s_factor=3.0, num_points=260)
        sm_pts[:, 0] -= offset_x
        sm_pts[:, 1] -= offset_y
        outer_path = points_to_svg_cubic_bezier_path(sm_pts)
        
        holes_paths = []
        for h_idx in children_map.get(c_idx, []):
            h_cnt = contours[h_idx]
            h_pts = smooth_contour(h_cnt, epsilon=1.8, s_factor=2.0, num_points=120)
            h_pts[:, 0] -= offset_x
            h_pts[:, 1] -= offset_y
            holes_paths.append(points_to_svg_cubic_bezier_path(h_pts))
            
        combined_d = outer_path
        if holes_paths:
            combined_d += " " + " ".join(holes_paths)
            
        letters_data.append({
            "letter_num": letter_idx + 1,
            "outer_path": outer_path,
            "holes_paths": holes_paths,
            "combined_d": combined_d
        })
        
    # 2. Specular Highlights
    mask_letter = alpha > 40
    hl_mask = mask_letter & (hsv[:, :, 1] < 165) & (hsv[:, :, 2] > 210)
    hl_u8 = hl_mask.astype(np.uint8) * 255
    hl_cnts, _ = cv2.findContours(hl_u8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    highlights_data = []
    for c in hl_cnts:
        if cv2.contourArea(c) > 600:
            hl_pts = smooth_contour(c, epsilon=1.8, s_factor=2.5, num_points=140)
            hl_pts[:, 0] -= offset_x
            hl_pts[:, 1] -= offset_y
            hl_path = points_to_svg_cubic_bezier_path(hl_pts)
            highlights_data.append(hl_path)
            
    print(f"Extracted {len(letters_data)} letters, {len(highlights_data)} highlights.")
    print(f"Raw wordmark dimensions: {total_w:.1f} x {total_h:.1f}")
    
    return {
        "letters": letters_data,
        "highlights": highlights_data,
        "width": total_w,
        "height": total_h
    }

# ==============================================================================
# SVG DEFINITIONS: CLEAN ACCURATE HONEY-GOLD GRADIENT (NO DROP SHADOW, NO STROKE)
# ==============================================================================
SVG_DEFS = f"""
  <defs>
    <linearGradient id="aversaGoldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['marigold']}"/>
      <stop offset="25%" stop-color="{PALETTE['gold_vivid']}"/>
      <stop offset="55%" stop-color="{PALETTE['gold_vivid']}"/>
      <stop offset="85%" stop-color="{PALETTE['marigold']}"/>
      <stop offset="100%" stop-color="{PALETTE['bronze']}"/>
    </linearGradient>
    <linearGradient id="aversaHighlightGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['canary']}" stop-opacity="0.88"/>
      <stop offset="100%" stop-color="{PALETTE['champagne']}" stop-opacity="0.55"/>
    </linearGradient>
  </defs>"""

# ==============================================================================
# 1. STANDALONE WORDMARK (CANVAS 3600 x 3600 CENTERED)
# ==============================================================================
def create_standalone_wordmark_svg(data, mode="color"):
    CANVAS_SIZE = 3600
    cx = CANVAS_SIZE // 2
    cy = CANVAS_SIZE // 2
    
    wm_scale = 3100.0 / data["width"]
    scaled_w = data["width"] * wm_scale
    scaled_h = data["height"] * wm_scale
    wm_x = (CANVAS_SIZE - scaled_w) / 2.0
    wm_y = (CANVAS_SIZE - scaled_h) / 2.0
    
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_SIZE} {CANVAS_SIZE}" width="{CANVAS_SIZE}" height="{CANVAS_SIZE}">',
        SVG_DEFS,
        f'  <g transform="translate({wm_x:.1f}, {wm_y:.1f}) scale({wm_scale:.4f})">'
    ]
    
    if mode == "color":
        lines.append('    <g id="aversa-letters">')
        for l in data["letters"]:
            lines.append(f'      <path d="{l["combined_d"]}" fill="url(#aversaGoldGrad)" fill-rule="evenodd"/>')
        lines.append('    </g>')
        lines.append('    <g id="aversa-highlights">')
        for hl in data["highlights"]:
            lines.append(f'      <path d="{hl}" fill="url(#aversaHighlightGrad)"/>')
        lines.append('    </g>')
    elif mode == "black":
        lines.append('    <g id="aversa-letters-black">')
        for l in data["letters"]:
            lines.append(f'      <path d="{l["combined_d"]}" fill="#0B0F19" fill-rule="evenodd"/>')
        lines.append('    </g>')
    elif mode == "white":
        lines.append('    <g id="aversa-letters-white">')
        for l in data["letters"]:
            lines.append(f'      <path d="{l["combined_d"]}" fill="#FFFFFF" fill-rule="evenodd"/>')
        lines.append('    </g>')
        
    lines.append('  </g>')
    lines.append('</svg>')
    return "\n".join(lines)

# ==============================================================================
# 2. LOGOTYPE VERTICAL (CANVAS 3600 x 3600)
# ==============================================================================
def create_logotype_vertical_svg(data, mode="color"):
    CANVAS_SIZE = 3600
    cx = CANVAS_SIZE // 2
    
    wm_scale = 2700.0 / data["width"]
    scaled_w = data["width"] * wm_scale
    scaled_h = data["height"] * wm_scale
    wm_x = (CANVAS_SIZE - scaled_w) / 2.0
    wm_y = 850.0
    
    text_color_main = PALETTE["marigold"] if mode == "color" else ("#0B0F19" if mode == "black" else "#FFFFFF")
    text_color_sub = PALETTE["bronze"] if mode == "color" else ("#1E293B" if mode == "black" else "#E2E8F0")
    line_col = PALETTE["marigold"] if mode == "color" else ("#64748B" if mode == "black" else "#94A3B8")
    
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_SIZE} {CANVAS_SIZE}" width="{CANVAS_SIZE}" height="{CANVAS_SIZE}">',
        SVG_DEFS,
        f'  <g transform="translate({wm_x:.1f}, {wm_y:.1f}) scale({wm_scale:.4f})">'
    ]
    
    if mode == "color":
        lines.append('    <g id="aversa-letters">')
        for l in data["letters"]:
            lines.append(f'      <path d="{l["combined_d"]}" fill="url(#aversaGoldGrad)" fill-rule="evenodd"/>')
        lines.append('    </g>')
        lines.append('    <g id="aversa-highlights">')
        for hl in data["highlights"]:
            lines.append(f'      <path d="{hl}" fill="url(#aversaHighlightGrad)"/>')
        lines.append('    </g>')
    elif mode == "black":
        lines.append('    <g id="aversa-letters-black">')
        for l in data["letters"]:
            lines.append(f'      <path d="{l["combined_d"]}" fill="#0B0F19" fill-rule="evenodd"/>')
        lines.append('    </g>')
    elif mode == "white":
        lines.append('    <g id="aversa-letters-white">')
        for l in data["letters"]:
            lines.append(f'      <path d="{l["combined_d"]}" fill="#FFFFFF" fill-rule="evenodd"/>')
        lines.append('    </g>')
        
    lines.append('  </g>')
    
    # Typography: DIES NATALIS 44 & SMA NEGERI 1 GEDEG
    line_y = wm_y + scaled_h + 70
    ty1 = line_y + 130
    ty2 = ty1 + 140
    ty3 = ty2 + 90
    
    lines.append(f'  <line x1="{cx - 750}" y1="{line_y}" x2="{cx + 750}" y2="{line_y}" stroke="{line_col}" stroke-width="3" stroke-linecap="round"/>')
    lines.append(f'  <circle cx="{cx}" cy="{line_y}" r="8" fill="{PALETTE["gold_vivid"]}"/>')
    lines.append(f'  <text x="{cx}" y="{ty1}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="900" font-size="124" fill="{text_color_main}" letter-spacing="18">DIES NATALIS 44</text>')
    lines.append(f'  <text x="{cx}" y="{ty2}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="84" fill="{text_color_sub}" letter-spacing="10">SMA NEGERI 1 GEDEG</text>')
    lines.append(f'  <text x="{cx}" y="{ty3}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="600" font-size="46" fill="{text_color_sub}" letter-spacing="8">1980 – 2024 • KABUPATEN MOJOKERTO</text>')
    
    lines.append('</svg>')
    return "\n".join(lines)

# ==============================================================================
# 3. LOGOTYPE HORIZONTAL (CANVAS 4000 x 4000)
# ==============================================================================
def create_logotype_horizontal_svg(data, mode="color"):
    CANVAS_SIZE = 4000
    cx = CANVAS_SIZE // 2
    cy = CANVAS_SIZE // 2
    
    wm_scale = 1950.0 / data["width"]
    scaled_w = data["width"] * wm_scale
    scaled_h = data["height"] * wm_scale
    wm_x = 220.0
    wm_y = cy - scaled_h / 2.0
    
    text_color_main = PALETTE["marigold"] if mode == "color" else ("#0B0F19" if mode == "black" else "#FFFFFF")
    text_color_sub = PALETTE["bronze"] if mode == "color" else ("#1E293B" if mode == "black" else "#E2E8F0")
    line_col = PALETTE["marigold"] if mode == "color" else ("#64748B" if mode == "black" else "#94A3B8")
    
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_SIZE} {CANVAS_SIZE}" width="{CANVAS_SIZE}" height="{CANVAS_SIZE}">',
        SVG_DEFS,
        f'  <g transform="translate({wm_x:.1f}, {wm_y:.1f}) scale({wm_scale:.4f})">'
    ]
    
    if mode == "color":
        lines.append('    <g id="aversa-letters">')
        for l in data["letters"]:
            lines.append(f'      <path d="{l["combined_d"]}" fill="url(#aversaGoldGrad)" fill-rule="evenodd"/>')
        lines.append('    </g>')
        lines.append('    <g id="aversa-highlights">')
        for hl in data["highlights"]:
            lines.append(f'      <path d="{hl}" fill="url(#aversaHighlightGrad)"/>')
        lines.append('    </g>')
    elif mode == "black":
        lines.append('    <g id="aversa-letters-black">')
        for l in data["letters"]:
            lines.append(f'      <path d="{l["combined_d"]}" fill="#0B0F19" fill-rule="evenodd"/>')
        lines.append('    </g>')
    elif mode == "white":
        lines.append('    <g id="aversa-letters-white">')
        for l in data["letters"]:
            lines.append(f'      <path d="{l["combined_d"]}" fill="#FFFFFF" fill-rule="evenodd"/>')
        lines.append('    </g>')
        
    lines.append('  </g>')
    
    # Divider Vertical
    div_x = wm_x + scaled_w + 120
    lines.append(f'  <line x1="{div_x}" y1="{cy - 500}" x2="{div_x}" y2="{cy + 500}" stroke="{line_col}" stroke-width="4" stroke-linecap="round"/>')
    lines.append(f'  <circle cx="{div_x}" cy="{cy}" r="10" fill="{PALETTE["gold_vivid"]}"/>')
    
    # Typography Right
    tx_start = div_x + 130
    lines.append(f'  <text x="{tx_start}" y="{cy - 120}" font-family="Arial, Helvetica, sans-serif" font-weight="900" font-size="124" fill="{text_color_main}" letter-spacing="14">DIES NATALIS 44</text>')
    lines.append(f'  <text x="{tx_start}" y="{cy + 60}" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="82" fill="{text_color_sub}" letter-spacing="8">SMA NEGERI 1 GEDEG</text>')
    lines.append(f'  <text x="{tx_start}" y="{cy + 190}" font-family="Arial, Helvetica, sans-serif" font-weight="600" font-size="48" fill="{text_color_sub}" letter-spacing="6">KABUPATEN MOJOKERTO • EST. 1980</text>')
    
    lines.append('</svg>')
    return "\n".join(lines)

# ==============================================================================
# 4. FULL BRAND COMBINATION (V6 EAGLE + AVERSA + SCHOOL ID) (CANVAS 4000 x 4000)
# ==============================================================================
def create_brand_combination_svg(data):
    CANVAS_SIZE = 4000
    cx = CANVAS_SIZE // 2
    
    v6_svg_path = "assets/svg/logo-symbol-color.svg"
    v6_inner = ""
    if os.path.exists(v6_svg_path):
        with open(v6_svg_path, "r") as f:
            v6_content = f.read()
            start_tag = v6_content.find("<svg")
            close_tag = v6_content.find(">", start_tag)
            end_svg = v6_content.rfind("</svg>")
            v6_inner = v6_content[close_tag+1:end_svg]
            
    symbol_size = 1350
    sym_x = cx - symbol_size // 2
    sym_y = 280
    
    wm_scale = 2600.0 / data["width"]
    scaled_w = data["width"] * wm_scale
    scaled_h = data["height"] * wm_scale
    wm_x = (CANVAS_SIZE - scaled_w) / 2.0
    wm_y = sym_y + symbol_size + 160
    
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_SIZE} {CANVAS_SIZE}" width="{CANVAS_SIZE}" height="{CANVAS_SIZE}">',
        SVG_DEFS,
        f'  <!-- OFFICIAL V6 EAGLE MASTER EMBLEM -->',
        f'  <g transform="translate({sym_x}, {sym_y}) scale({symbol_size/2048.0:.4f})">',
        v6_inner,
        f'  </g>',
        f'  <!-- TRACED AVERSA FLUID WORDMARK (CLEAN, NO STROKE) -->',
        f'  <g transform="translate({wm_x:.1f}, {wm_y:.1f}) scale({wm_scale:.4f})">',
        f'    <g id="aversa-letters">'
    ]
    for l in data["letters"]:
        lines.append(f'      <path d="{l["combined_d"]}" fill="url(#aversaGoldGrad)" fill-rule="evenodd"/>')
    lines.append('    </g>')
    lines.append('    <g id="aversa-highlights">')
    for hl in data["highlights"]:
        lines.append(f'      <path d="{hl}" fill="url(#aversaHighlightGrad)"/>')
    lines.append('    </g>')
    lines.append('  </g>')
    
    # Typography bottom
    line_y = wm_y + scaled_h + 70
    ty1 = line_y + 130
    ty2 = ty1 + 140
    ty3 = ty2 + 90
    lines.append(f'  <line x1="{cx - 750}" y1="{line_y}" x2="{cx + 750}" y2="{line_y}" stroke="{PALETTE["marigold"]}" stroke-width="3" stroke-linecap="round"/>')
    lines.append(f'  <circle cx="{cx}" cy="{line_y}" r="8" fill="{PALETTE["gold_vivid"]}"/>')
    lines.append(f'  <text x="{cx}" y="{ty1}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="900" font-size="116" fill="{PALETTE["marigold"]}" letter-spacing="18">DIES NATALIS 44</text>')
    lines.append(f'  <text x="{cx}" y="{ty2}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="80" fill="{PALETTE["bronze"]}" letter-spacing="10">SMA NEGERI 1 GEDEG</text>')
    lines.append(f'  <text x="{cx}" y="{ty3}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="600" font-size="46" fill="{PALETTE["bronze"]}" letter-spacing="8">1980 – 2024 • MOJOKERTO</text>')
    
    lines.append('</svg>')
    return "\n".join(lines)

# ==============================================================================
# TRANSPARENT DEMATTING FUNCTION (ELIMINATES ANY WHITE OUTLINE)
# ==============================================================================
def demat_white_background(rgba_array):
    """
    Extracts pure alpha transparency from a raster image rendered against white,
    un-premultiplying the background so no white fringe or halo remains.
    """
    arr = rgba_array.astype(float)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    
    # Distance from pure white
    dist_from_white = np.maximum(255.0 - r, np.maximum(255.0 - g, 255.0 - b))
    
    # Alpha transition curve
    alpha = np.clip((dist_from_white - 8.0) / 32.0, 0.0, 1.0)
    alpha[dist_from_white > 40.0] = 1.0
    
    # Un-premultiply RGB against white
    safe_alpha = np.maximum(alpha, 0.001)[:, :, np.newaxis]
    rgb = (arr[:, :, :3] - 255.0 * (1.0 - safe_alpha)) / safe_alpha
    rgb = np.clip(rgb, 0.0, 255.0)
    
    out = np.dstack([rgb, alpha * 255.0]).astype(np.uint8)
    return out

# ==============================================================================
# MAIN EXECUTION & RENDERING PIPELINE
# ==============================================================================
def main():
    print("=== TAHAP 1: EKSTRAKSI & VEKTORISASI AVERSA HANDDRAW ===")
    vector_data = extract_aversa_vector_data("aversa handdraw.png")
    
    svg_dir = "assets/svg"
    png_dir = "assets/png"
    os.makedirs(svg_dir, exist_ok=True)
    os.makedirs(png_dir, exist_ok=True)
    
    svg_outputs = {
        "aversa-standalone-color.svg": create_standalone_wordmark_svg(vector_data, "color"),
        "aversa-standalone-black.svg": create_standalone_wordmark_svg(vector_data, "black"),
        "aversa-standalone-white.svg": create_standalone_wordmark_svg(vector_data, "white"),
        "aversa-logotype-vertical.svg": create_logotype_vertical_svg(vector_data, "color"),
        "aversa-logotype-vertical-dark.svg": create_logotype_vertical_svg(vector_data, "black"),
        "aversa-logotype-horizontal.svg": create_logotype_horizontal_svg(vector_data, "color"),
        "aversa-logotype-horizontal-dark.svg": create_logotype_horizontal_svg(vector_data, "black"),
        "aversa-brand-combination.svg": create_brand_combination_svg(vector_data),
    }
    
    print("\n=== TAHAP 2: EKSPOR BERKAS VEKTOR SVG ===")
    for filename, content in svg_outputs.items():
        filepath = os.path.join(svg_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved SVG: {filepath} ({len(content)} bytes)")
        
    print("\n=== TAHAP 3: PERENDERAN RASTER PNG TRANSPARAN (DE-MATTING ALPHA) ===")
    tmp_dir = "tmp_ql_render"
    os.makedirs(tmp_dir, exist_ok=True)
    
    for filename in svg_outputs.keys():
        base = filename[:-4]
        svg_file = os.path.join(svg_dir, filename)
        png_file = os.path.join(png_dir, f"{base}.png")
        
        if "white" in filename:
            print(f"Rendering {filename} -> {png_file} via ImageMagick transparent...")
            cmd = ["magick", "-background", "none", "-density", "300", svg_file, "-resize", "2048x2048", f"png32:{png_file}"]
            subprocess.run(cmd, check=True)
        else:
            print(f"Rendering {filename} -> {png_file} via WebKit + Alpha De-matting...")
            subprocess.run(["qlmanage", "-t", "-s", "2048", "-o", tmp_dir, svg_file], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            gen_path = os.path.join(tmp_dir, f"{filename}.png")
            if os.path.exists(gen_path):
                im = Image.open(gen_path).convert("RGBA")
                dematted = demat_white_background(np.array(im))
                clean_im = Image.fromarray(dematted)
                clean_im.save(png_file)
                os.remove(gen_path)
                
    if os.path.exists(tmp_dir):
        os.rmdir(tmp_dir)
            
    print("\n=== TAHAP 4: VERIFIKASI TRANSPARANSI & DETEKSI OUTLINE PUTIH ===")
    for filename in svg_outputs.keys():
        base = filename[:-4]
        png_file = os.path.join(png_dir, f"{base}.png")
        if os.path.exists(png_file):
            im = Image.open(png_file)
            arr = np.array(im)
            if im.mode == "RGBA":
                alpha = arr[:, :, 3]
                trans_px = (alpha == 0).sum()
                solid_px = (alpha > 0).sum()
                # Check for pale white fringe
                pale = (alpha == 255) & (arr[:, :, 0] > 215) & (arr[:, :, 1] > 215) & (arr[:, :, 2] > 215)
                # Check mean color in solid area
                vis_rgb = arr[alpha > 120, :3]
                mean_col = vis_rgb.mean(axis=0) if len(vis_rgb) else [0, 0, 0]
                print(f"Verified {base}.png: transparent={trans_px}, visible={solid_px}, pale_white={pale.sum()}, mean_RGB=[{mean_col[0]:.1f}, {mean_col[1]:.1f}, {mean_col[2]:.1f}]")
            else:
                print(f"Verified {base}.png: mode={im.mode}")
                
    print("\n=== SELESAI: SEMUA ASET LOGOTYPE AVERSA BERHASIL DIPERBARUI! ===")

if __name__ == "__main__":
    main()
