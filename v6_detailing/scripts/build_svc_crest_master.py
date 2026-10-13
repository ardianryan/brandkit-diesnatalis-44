#!/usr/bin/env python3
"""
build_svc_crest_master.py
=============================================================================
Reconstructs and vectorizes the official SVC (Smansage Volleyball Competition)
emblem into high-precision, infinitely scalable SVG and ultra-HD PNG assets.

Key Architectural Updates (Precision V6 Master):
1. Continuous 5-Sided Heraldic Shield (Pentagonal Crest):
   - Fully continuous horizontal top rim passing solidly behind panda arms
   - Eliminates all step cutouts and exposed voids at top shoulders
   - 3D mitered platinum/silver outer bevel & metallic gold inner bevel
   - Split midnight navy field (Left #0F172A, Right #070A12)
2. Towering Panda Mascot (Header Crest):
   - Elevated upwards so full head, ears, and glare tower proudly above shield
   - Claws securely grasping the upper golden rim cradle
   - Multi-layer vector tracing (white face, gray shadow, slate arms, gold claws/eyes)
3. Chiseled 3D Athletic Display "SVC" Typography:
   - Approved pure smooth parametric vectors matching original hand draw & AI refinement
   - S with smooth dual-facet continuous spine ridge and terminal bevel wedges
   - V with mathematically symmetrical 4-facet chiseled prism, triangular apex bevels,
     and 36px bottom chamfer
   - C with restored natural curved geometry and terminal bevels
   - Seamless metallic gold gradients and deep drop shadow
4. Mathematically Centered AVERSA Wordmark:
   - Centered with sub-pixel precision at CX=2100.0 based on true path bounds
5. Impactful Arched Ribbon Banner:
   - Shared-vertex fold wedges welded to ribbon body endpoints (no gaps/slits)
   - Elegant horizontal tournament swallowtails extending outward
   - Concentric circular arc with bold, thick athletic championship typography
=============================================================================
"""

import os
import math
import cv2
import numpy as np
import subprocess
import xml.etree.ElementTree as ET

try:
    from ribbon_glyphs import FONT_SCALE, RIBBON_TEXT_GLYPHS
except ImportError:
    from v6_detailing.scripts.ribbon_glyphs import FONT_SCALE, RIBBON_TEXT_GLYPHS

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
HAND_DRAW_PATH = "hand draw SVC.PNG"
AVERSA_SVG_PATH = "assets/svg/aversa-standalone-color.svg"
SVG_OUT_DIR = "assets/svg"
PNG_OUT_DIR = "assets/png"

os.makedirs(SVG_OUT_DIR, exist_ok=True)
os.makedirs(PNG_OUT_DIR, exist_ok=True)

# Master Canvas 4200 x 4200 px
CANVAS_W = 4200
CANVAS_H = 4200
CX = 2100.0
CY = 2100.0

PALETTE = {
    # Gold & Bronze
    "canary": "#FDF39D",
    "champagne": "#F7D160",
    "vivid_gold": "#F5C538",
    "marigold": "#E09B17",
    "bronze": "#B6580B",
    "mahogany": "#7D1B05",
    "deep_crevice": "#420F03",
    # Platinum & Silver
    "pure_white": "#FFFFFF",
    "silver_highlight": "#F8FAFC",
    "silver_mid": "#E2E8F0",
    "silver_base": "#CBD5E1",
    "silver_shadow": "#64748B",
    "silver_dark": "#334155",
    # Midnight Navy & Obsidian
    "navy_light": "#1E293B",
    "navy_mid": "#0F172A",
    "navy_deep": "#070E1B",
    "obsidian": "#05080E",
    "black_ink": "#020408",
    # Authentic Panda Mascot Colors (Sampled directly from hand draw SVC.PNG)
    "panda_white": "#FEFEFE",
    "panda_gray": "#AEB0B3",
    "panda_slate": "#353B44",
    "panda_black": "#111212",
    "panda_gold_mid": "#B69348",
    "panda_gold_light": "#E1BE77",
}

# =========================================================================
# STANDALONE APPROVED SVC PARAMETRIC PATHS
# =========================================================================
s_facet_light_d = "M 286.0 150.0 L 345.0 194.0 C 346.7 194.0 348.3 194.0 350.0 194.0 C 349.3 178.1 351.3 161.2 349.0 146.0 C 349.2 126.3 343.4 109.0 337.0 92.0 C 290.4 1.1 158.8 -10.0 79.0 38.0 C 60.5 50.4 43.9 67.4 32.0 86.0 C 28.8 94.1 23.6 101.3 22.0 110.0 C 16.6 124.3 14.2 139.9 13.0 156.0 C 10.1 179.2 12.8 203.7 20.0 224.0 C 26.4 253.0 49.7 278.0 75.0 295.0 C 103.1 312.1 133.2 324.4 164.0 335.0 C 190.4 344.0 223.9 361.1 228.0 393.0 C 227.4 398.6 229.3 405.1 227.0 410.0 C 224.8 457.3 145.3 462.0 134.0 417.0 C 130.8 411.0 129.0 404.3 129.0 397.0 C 126.7 388.1 128.6 377.5 128.0 368.0 L 69.0 412.0 C 72.8 426.5 80.3 439.8 90.0 451.2 C 98.0 460.7 107.4 468.9 117.9 475.4 C 125.8 480.2 134.1 484.1 142.9 486.8 C 151.5 489.4 160.5 490.9 169.6 490.8 C 241.5 488.9 284.0 405.2 265.5 341.3 C 256.5 319.5 235.6 306.0 215.9 294.6 C 198.7 284.9 180.5 277.2 162.6 268.9 C 151.7 263.9 141.0 258.6 130.9 252.1 C 58.0 214.3 72.0 86.2 154.5 70.9 C 163.5 68.8 172.7 68.1 181.8 68.7 C 193.9 69.5 205.7 72.7 216.7 77.6 C 230.7 83.8 243.4 92.7 254.4 103.3 C 267.9 116.5 279.0 132.4 286.0 150.0 Z"
s_facet_shade_d = "M 69.0 412.0 L 10.0 368.0 C 10.7 383.9 8.7 400.8 11.0 416.0 C 11.4 429.1 13.8 441.4 18.0 453.0 C 20.7 466.4 27.8 478.0 34.0 490.0 C 81.4 557.6 175.9 559.5 250.0 542.0 C 262.7 537.6 274.9 532.0 287.0 526.0 C 328.5 501.4 350.1 457.4 352.0 411.0 C 354.5 389.4 353.0 365.8 348.0 346.0 C 343.0 314.9 326.4 287.3 300.0 266.0 C 274.3 248.4 246.8 235.0 218.0 225.0 C 191.8 212.0 153.6 205.7 143.0 173.0 C 143.6 167.8 141.8 161.5 144.0 157.0 C 148.4 114.0 222.7 118.6 224.0 161.0 C 226.0 166.1 226.1 172.0 226.0 178.0 C 228.2 182.5 226.4 188.8 227.0 194.0 L 286.0 150.0 C 279.0 132.4 267.9 116.5 254.4 103.3 C 243.4 92.7 230.7 83.8 216.7 77.6 C 205.7 72.7 193.9 69.5 181.8 68.7 C 172.7 68.1 163.5 68.8 154.5 70.9 C 72.0 86.2 58.0 214.3 130.9 252.1 C 141.0 258.6 151.7 263.9 162.6 268.9 C 180.5 277.2 198.7 284.9 215.9 294.6 C 235.6 306.0 256.5 319.5 265.5 341.3 C 284.0 405.2 241.5 488.9 169.6 490.8 C 160.5 490.9 151.5 489.4 142.9 486.8 C 134.1 484.1 125.8 480.2 117.9 475.4 C 107.4 468.9 98.0 460.7 90.0 451.2 C 80.3 439.8 72.8 426.5 69.0 412.0 Z"

c_outer_facet_d = "M 290.0 168.0 L 354.0 206.0 C 354.9 158.4 354.7 111.2 328.0 75.0 C 304.4 43.4 270.6 25.8 236.0 16.0 C 163.5 1.1 82.7 14.5 36.0 76.0 C 30.8 84.1 26.5 92.6 22.0 101.0 C 16.7 115.3 13.4 130.5 11.0 146.0 C 9.4 234.2 9.4 324.8 11.0 413.0 C 12.4 420.5 13.1 428.3 14.0 436.0 C 18.3 452.8 24.2 469.0 33.0 484.0 C 86.8 563.2 208.5 567.3 285.0 525.0 C 297.0 517.0 308.4 507.5 319.0 496.0 C 351.2 457.5 355.3 407.4 354.0 355.0 L 290.0 393.0 C 290.0 393.0 290.0 365.1 290.0 365.1 C 290.2 384.6 289.0 404.2 284.2 423.1 C 277.9 444.3 265.8 464.5 246.7 476.3 C 188.8 513.5 97.7 487.5 79.9 417.5 C 77.7 410.1 77.1 406.8 75.5 399.2 C 73.1 389.6 73.8 379.7 73.0 370.0 C 72.1 360.0 72.7 350.0 72.5 340.0 C 72.5 323.2 72.5 306.4 72.5 289.6 C 72.5 272.8 72.5 256.0 72.5 239.2 C 72.7 225.9 72.0 212.5 73.0 199.2 C 72.3 189.3 73.9 179.6 75.5 170.0 C 77.3 160.8 79.6 151.6 83.3 143.0 C 106.6 76.6 195.7 51.7 252.1 91.7 C 273.5 106.1 285.3 131.1 288.7 156.2 C 291.2 170.1 289.3 231.4 290.0 168.0 Z"
c_inner_facet_d = "M 290.0 168.0 L 226.0 206.0 C 226.2 187.4 226.8 168.7 220.0 153.0 C 213.3 141.3 201.5 134.0 189.0 132.0 C 171.2 130.8 155.2 134.1 144.0 149.0 C 139.8 155.0 138.2 162.2 136.0 169.0 C 133.7 238.9 135.6 310.5 135.0 381.0 C 136.6 388.4 136.7 396.4 138.0 404.0 C 139.9 410.3 142.5 416.3 146.0 422.0 C 164.1 442.7 204.0 441.3 218.0 417.0 C 226.9 398.9 226.3 376.9 226.0 355.0 L 290.0 393.0 C 290.0 393.0 290.0 365.1 290.0 365.1 C 290.2 384.6 289.0 404.2 284.2 423.1 C 277.9 444.3 265.8 464.5 246.7 476.3 C 188.8 513.5 97.7 487.5 79.9 417.5 C 77.7 410.1 77.1 406.8 75.5 399.2 C 73.1 389.6 73.8 379.7 73.0 370.0 C 72.1 360.0 72.7 350.0 72.5 340.0 C 72.5 323.2 72.5 306.4 72.5 289.6 C 72.5 272.8 72.5 256.0 72.5 239.2 C 72.7 225.9 72.0 212.5 73.0 199.2 C 72.3 189.3 73.9 179.6 75.5 170.0 C 77.3 160.8 79.6 151.6 83.3 143.0 C 106.6 76.6 195.7 51.7 252.1 91.7 C 273.5 106.1 285.3 131.1 288.7 156.2 C 291.2 170.1 289.3 231.4 290.0 168.0 Z"


def build_chiseled_svc_svg(mode):
    """
    Constructs smooth athletic curved 3D typography for S, V, C
    matching hand draw SVC.PNG exactly.
    """
    is_color = (mode == "color")
    is_white = (mode == "white")
    
    if is_color:
        f_light = "url(#goldLightFacet)"
        f_shade = "url(#goldShadeFacet)"
        f_bevel = "url(#goldBevelFacet)"
        stroke_attr = ' stroke="none"'
    elif is_white:
        f_light = "#FFFFFF"
        f_shade = "#F1F5F9"
        f_bevel = "#E2E8F0"
        stroke_attr = ' stroke="#000000" stroke-width="8" stroke-linejoin="round"'
    else:  # dark
        f_light = "#E2E8F0"
        f_shade = "#94A3B8"
        f_bevel = "#64748B"
        stroke_attr = ' stroke="none"'
        
    s_scale = 0.6826
    v_scale = 0.6826
    c_scale = 0.6826
    
    s_tx_val, s_ty_val = 104.0, 315.0
    v_tx_val, v_ty_val = 357.0, 315.0
    c_tx_val, c_ty_val = 660.0, 315.0
    
    lines = []
    lines.append(f'''    <g id="crest-letter-S" transform="translate({s_tx_val:.1f}, {s_ty_val:.1f}) scale({s_scale:.4f})">
      <path d="{s_facet_light_d}" fill="{f_light}"{stroke_attr}/>
      <path d="{s_facet_shade_d}" fill="{f_shade}"{stroke_attr}/>
      <polygon points="227,194 345,194 286,150" fill="{f_bevel}"{stroke_attr}/>
      <polygon points="10,368 128,368 69,412" fill="{f_bevel}"{stroke_attr}/>
    </g>

    <g id="crest-letter-V" transform="translate({v_tx_val:.1f}, {v_ty_val:.1f}) scale({v_scale:.4f})">
      <polygon points="10,11 139,11 74,48" fill="{f_bevel}"{stroke_attr}/>
      <polygon points="298,11 427,11 362,48" fill="{f_bevel}"{stroke_attr}/>
      <polygon points="10,11 74,48 187.4,505 156.3,505" fill="{f_shade}"{stroke_attr}/>
      <polygon points="139,11 74,48 187.4,505 218.5,505 218.5,352" fill="{f_light}"{stroke_attr}/>
      <polygon points="218.5,352 218.5,505 249.6,505 362,48 298,11" fill="{f_light}"{stroke_attr}/>
      <polygon points="427,11 362,48 249.6,505 280.7,505" fill="{f_shade}"{stroke_attr}/>
      <polygon points="156.3,505 280.7,505 270,541 167,541" fill="{f_bevel}"{stroke_attr}/>
    </g>

    <g id="crest-letter-C" transform="translate({c_tx_val:.1f}, {c_ty_val:.1f}) scale({c_scale:.4f})">
      <path d="{c_outer_facet_d}" fill="{f_light}"{stroke_attr}/>
      <path d="{c_inner_facet_d}" fill="{f_shade}"{stroke_attr}/>
      <polygon points="226,206 354,206 290,168" fill="{f_bevel}"{stroke_attr}/>
      <polygon points="226,355 354,355 290,393" fill="{f_bevel}"{stroke_attr}/>
    </g>''')
    return "\n".join(lines)


def trace_mask_potrace(mask_u8, name, alphamax=1.0, blur=True):
    bmp = f"scratch/svc_clean_{name}.bmp"
    svg = f"scratch/svc_clean_{name}.svg"
    if blur:
        cleaned = cv2.medianBlur(mask_u8, 3)
    else:
        cleaned = mask_u8
    cv2.imwrite(bmp, cleaned)
    subprocess.run(["potrace", "-s", "--invert", "--alphamax", str(alphamax), "-o", svg, bmp], check=True)
    tree = ET.parse(svg)
    paths = [e.attrib["d"] for e in tree.getroot().iter() if e.tag.endswith("path") and "d" in e.attrib]
    return " ".join(paths)


def extract_panda_vector_layers():
    print("-> Extracting full Panda Mascot with uncut arms and radiant golden eyes...")
    img = cv2.imread(HAND_DRAW_PATH)
    if img is None:
        raise FileNotFoundError(f"Cannot load {HAND_DRAW_PATH}")
    
    p_crop = img[80:660, 740:1660]
    h, w = p_crop.shape[:2]
    rgb = cv2.cvtColor(p_crop, cv2.COLOR_BGR2RGB)
    
    flood = p_crop.copy()
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood, mask, (0, 0), (0, 255, 0), (15, 15, 15), (15, 15, 15))
    cv2.floodFill(flood, mask, (w - 1, 0), (0, 255, 0), (15, 15, 15), (15, 15, 15))
    is_bg_white = (flood[:, :, 0] == 0) & (flood[:, :, 1] == 255) & (flood[:, :, 2] == 0)
    
    r, g, b = rgb[:, :, 0].astype(int), rgb[:, :, 1].astype(int), rgb[:, :, 2].astype(int)
    lum = (r * 299 + g * 587 + b * 114) // 1000
    
    # Precise Navy Shield Field Segmentation (preserves exact natural claws and knuckles)
    is_navy = (b > r + 8) & (b > g + 4) & (r < 40) & (g < 45) & (b < 75)
    navy_u8 = (is_navy * 255).astype(np.uint8)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(navy_u8)
    navy_bottom = np.zeros((h, w), dtype=bool)
    for i in range(1, num_labels):
        comp_mask = (labels == i)
        if np.any(comp_mask[h - 1, :]):
            navy_bottom |= comp_mask
    
    # Outer arm boundaries: preserve full muscular forearms and smooth under-arm rim
    arm_mask = np.ones((h, w), dtype=bool)
    arm_mask[:, :86] = False
    arm_mask[:, 834:] = False
    
    # Left under-arm cutoff (connects cleanly at x=275, y=516 to leftmost claw)
    left_arm_pts = [[0, 0], [86, 0], [86, 430], [90, 460], [110, 485], [150, 505], [210, 518], [275, 516], [275, h], [0, h]]
    cv2.fillPoly(arm_mask.view(np.uint8), [np.array(left_arm_pts, dtype=np.int32)], 0)
    
    # Right under-arm cutoff (connects cleanly at x=672, y=510 to rightmost claw)
    right_arm_pts = [[672, 510], [710, 518], [770, 505], [810, 485], [830, 460], [834, 430], [834, 0], [w, 0], [w, h], [672, h]]
    cv2.fillPoly(arm_mask.view(np.uint8), [np.array(right_arm_pts, dtype=np.int32)], 0)
    
    # Complete Foreground: 100% natural claws, knuckles, chest V-triangle, and arms!
    fg_bool = arm_mask & (~is_bg_white) & (~navy_bottom)
    

    
    # 1. Radiant Glowing Golden Eyes
    eye_mask = np.zeros((h, w), dtype=bool)
    eye_mask[215:265, 350:420] = (r[215:265, 350:420] > 110) & (g[215:265, 350:420] > 80) & (b[215:265, 350:420] < 120) & (r[215:265, 350:420] - b[215:265, 350:420] > 20)
    eye_mask[215:265, 510:575] = (r[215:265, 510:575] > 110) & (g[215:265, 510:575] > 80) & (b[215:265, 510:575] < 120) & (r[215:265, 510:575] - b[215:265, 510:575] > 20)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    eye_closed = cv2.morphologyEx(eye_mask.astype(np.uint8) * 255, cv2.MORPH_CLOSE, kernel)
    num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(eye_closed)
    clean_eyes = np.zeros((h, w), dtype=bool)
    if num_labels > 1:
        sorted_indices = np.argsort(stats[1:, cv2.CC_STAT_AREA])[::-1] + 1
        for idx in sorted_indices[:2]:
            clean_eyes[labels == idx] = True


    # 2. Authentic Gold fur & claws (R > G > B, excluding eyes)
    is_gold = fg_bool & (r > 120) & (g > 85) & (r - b > 25) & (g - b > 10) & (~clean_eyes)
    is_gold_light = is_gold & (r > 200) & (g > 165)
    is_gold_mid = is_gold & ~is_gold_light

    # 3. Authentic White Face & Gray Face Shadows
    is_white = fg_bool & (r > 225) & (g > 225) & (b > 225)
    is_gray = fg_bool & ~is_white & ~is_gold & ~clean_eyes & (lum > 140) & (lum <= 225) & (np.abs(r - b) < 20)

    # 4. Authentic Slate / Charcoal Arm Body
    is_slate = fg_bool & ~is_gold & ~is_white & ~is_gray & ~clean_eyes & (lum > 30) & (lum <= 130) & (b >= r - 5)

    # 5. Deep Black Ink Lines, Shadows & Eye Patches
    is_black = fg_bool & ~is_gold & ~is_white & ~is_gray & ~is_slate & ~clean_eyes
    
    sil_d = trace_mask_potrace((fg_bool * 255).astype(np.uint8), "panda_sil", 1.0, blur=True)
    black_d = trace_mask_potrace((is_black * 255).astype(np.uint8), "panda_black", 0.9, blur=True)
    slate_d = trace_mask_potrace((is_slate * 255).astype(np.uint8), "panda_slate", 1.0, blur=True)
    gray_d = trace_mask_potrace((is_gray * 255).astype(np.uint8), "panda_gray", 0.9, blur=True)
    white_d = trace_mask_potrace((is_white * 255).astype(np.uint8), "panda_white", 0.9, blur=True)
    gold_d = trace_mask_potrace((is_gold_mid * 255).astype(np.uint8), "panda_gold", 0.8, blur=True)
    gold_br_d = trace_mask_potrace((is_gold_light * 255).astype(np.uint8), "panda_gold_br", 0.8, blur=True)
    eyes_d = trace_mask_potrace((clean_eyes * 255).astype(np.uint8), "panda_eyes", 1.0, blur=False)
    
    return {
        "width": w,
        "height": h,
        "sil_d": sil_d,
        "black_d": black_d,
        "slate_d": slate_d,
        "gray_d": gray_d,
        "white_d": white_d,
        "gold_d": gold_d,
        "gold_br_d": gold_br_d,
        "eyes_d": eyes_d,
    }


def get_aversa_vector():
    print("-> Reading master AVERSA wordmark from assets/svg/aversa-standalone-color.svg...")
    tree = ET.parse(AVERSA_SVG_PATH)
    root = tree.getroot()
    letters_elem = root.find(".//*[@id='aversa-letters']")
    highlights_elem = root.find(".//*[@id='aversa-highlights']")
    
    letters_paths = []
    if letters_elem is not None:
        for c in letters_elem:
            if "d" in c.attrib:
                letters_paths.append(c.attrib["d"])
                
    hl_paths = []
    if highlights_elem is not None:
        for c in highlights_elem:
            if "d" in c.attrib:
                hl_paths.append(c.attrib["d"])
                
    return letters_paths, hl_paths


def main():
    print("=" * 70)
    print("RECONSTRUCTING SVC EMBLEM (Smansage Volleyball Competition) - V6 MASTER")
    print("=" * 70)
    
    # 1. Panda Mascot Vectors
    panda = extract_panda_vector_layers()
    
    # 2. Master AVERSA Vectors
    aversa_letters, aversa_highlights = get_aversa_vector()
    
    # =============================================================
    # Geometry Layout Calculations (Canvas 4200 x 4200 px)
    # =============================================================
    
    # -------------------------------------------------------------
    # 1. 5-Sided Heraldic Pentagonal Shield Geometry (Continuous Rim)
    # -------------------------------------------------------------
    shield_solid_base_d = "M 650 1050 L 3550 1050 L 3080 2850 L 2100 3780 L 1120 2850 Z"
    shield_outer_d = "M 650 1050 L 3550 1050 L 3080 2850 L 2100 3780 L 1120 2850 Z"
    
    # Continuous silver rim passing smoothly behind panda arms
    shield_silver_rim_d = (
        "M 650 1050 L 3550 1050 L 3080 2850 L 2100 3780 L 1120 2850 Z "
        "M 760 1150 L 1195 2815 L 2100 3650 L 3005 2815 L 3440 1150 Z"
    )
    
    # Continuous inner gold rim
    shield_gold_rim_d = (
        "M 760 1150 L 3440 1150 L 3005 2815 L 2100 3650 L 1195 2815 Z "
        "M 860 1240 L 3340 1240 L 2940 2780 L 2100 3530 L 1260 2780 Z"
    )
    
    # Midnight Navy Field (Split 50/50 down the center spine)
    shield_navy_left_d = "M 860 1240 L 2100 1240 L 2100 3530 L 1260 2780 Z"
    shield_navy_right_d = "M 2100 1240 L 3340 1240 L 2940 2780 L 2100 3530 Z"
    
    # -------------------------------------------------------------
    # 2. Championship Tournament Ribbon Banner
    # -------------------------------------------------------------
    ribbon_body_d = "M 609 3010 A 3980 3980 0 0 1 3591 3010 L 3479 3288 A 3680 3680 0 0 0 721 3288 Z"
    ribbon_rim_top_d = "M 609 3010 A 3980 3980 0 0 1 3591 3010 L 3580 3045 A 3945 3945 0 0 0 620 3045 Z"
    ribbon_rim_bot_d = "M 711 3253 A 3715 3715 0 0 1 3489 3253 L 3479 3288 A 3680 3680 0 0 0 721 3288 Z"

    # Shared vertices fold triangles (welded to ribbon body endpoints)
    ribbon_fold_left_d = "M 609 3010 L 721 3288 L 770 3180 Z"
    ribbon_fold_right_d = "M 3591 3010 L 3479 3288 L 3430 3180 Z"

    # Elegant horizontal swallowtails extending outward
    ribbon_tail_left_d = "M 680 3040 L 300 3100 L 420 3210 L 280 3320 L 760 3270 Z"
    ribbon_tail_right_d = "M 3520 3040 L 3900 3100 L 3780 3210 L 3920 3320 L 3440 3270 Z"

    ribbon_tail_left_bevel_d = "M 680 3040 L 300 3100 L 420 3210 L 405 3190 L 315 3115 L 680 3060 Z"
    ribbon_tail_right_bevel_d = "M 3520 3040 L 3900 3100 L 3780 3210 L 3795 3190 L 3885 3115 L 3520 3060 Z"

    # Concentric Text Arc
    ribbon_text_path_d = "M 820 3125 A 3805 3805 0 0 1 3380 3125"
    
    # -------------------------------------------------------------
    # 3. Towering Panda Mascot Placement
    # -------------------------------------------------------------
    p_sc = 2200.0 / panda["width"]
    p_tx = CX - (panda["width"] * p_sc) / 2.0
    p_ty = 50.0
    
    # -------------------------------------------------------------
    # 4. Optically Centered AVERSA Wordmark Placement
    # -------------------------------------------------------------
    av_sc = 0.38
    av_center_x = 1587.30 - 18.0
    av_tx = CX - av_center_x * av_sc
    av_ty = 1460.0
    
    # -------------------------------------------------------------
    # 5. Approved Standalone SVC Placement
    # -------------------------------------------------------------
    svc_sc = 2.45
    svc_tx = 859.8
    svc_ty = 1058.5
    
    defs_block = f"""
  <defs>
    <!-- Platinum / Silver Metallic Gradients -->
    <linearGradient id="silverRimGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['silver_highlight']}"/>
      <stop offset="25%" stop-color="{PALETTE['silver_mid']}"/>
      <stop offset="60%" stop-color="{PALETTE['silver_base']}"/>
      <stop offset="85%" stop-color="{PALETTE['silver_shadow']}"/>
      <stop offset="100%" stop-color="{PALETTE['silver_dark']}"/>
    </linearGradient>

    <!-- Master Gold Gradients -->
    <linearGradient id="goldRimGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['canary']}"/>
      <stop offset="30%" stop-color="{PALETTE['champagne']}"/>
      <stop offset="60%" stop-color="{PALETTE['vivid_gold']}"/>
      <stop offset="85%" stop-color="{PALETTE['bronze']}"/>
      <stop offset="100%" stop-color="{PALETTE['mahogany']}"/>
    </linearGradient>

    <!-- Authentic Panda Eye Radial Gradient (from hand draw SVC.PNG) -->
    <radialGradient id="pandaEyeGrad" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#F2DC9E"/>
      <stop offset="50%" stop-color="{PALETTE['panda_gold_mid']}"/>
      <stop offset="100%" stop-color="#8C6826"/>
    </radialGradient>

    <!-- Calibrated Metallic Gold Facets for Standalone SVC Wordmark -->
    <linearGradient id="goldLightFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFAD0"/>
      <stop offset="35%" stop-color="#FAD758"/>
      <stop offset="70%" stop-color="#F2BF3E"/>
      <stop offset="100%" stop-color="#EAA82C"/>
    </linearGradient>

    <linearGradient id="goldShadeFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EDA82C"/>
      <stop offset="50%" stop-color="#DB8E26"/>
      <stop offset="100%" stop-color="#C57418"/>
    </linearGradient>

    <linearGradient id="goldBevelFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#CB7B20"/>
      <stop offset="100%" stop-color="#A85B12"/>
    </linearGradient>

    <linearGradient id="goldDarkFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#D97706"/>
      <stop offset="50%" stop-color="#B45309"/>
      <stop offset="100%" stop-color="#78350F"/>
    </linearGradient>

    <!-- Midnight Navy Shield Field Gradients -->
    <linearGradient id="navyLeftGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['navy_mid']}"/>
      <stop offset="100%" stop-color="{PALETTE['navy_deep']}"/>
    </linearGradient>

    <linearGradient id="navyRightGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['navy_deep']}"/>
      <stop offset="100%" stop-color="{PALETTE['obsidian']}"/>
    </linearGradient>

  </defs>"""

    # Generate 3 Master Crest Variants: color, white, dark
    modes = [("color", True, False), ("white", False, True), ("dark", False, False)]
    
    for mode, is_color, is_white in modes:
        print(f"\n-> Generating Master SVG variant: svc-crest-{mode}.svg...")
        lines = []
        lines.append('<?xml version="1.0" encoding="UTF-8"?>')
        lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" width="{CANVAS_W}" height="{CANVAS_H}">')
        lines.append(f'  <title>SVC Emblem - {mode.upper()}</title>')
        lines.append(defs_block)
        lines.append('  <g id="master-crest">')
        
        # 1. 5-SIDED HERALDIC SHIELD FOUNDATION
        lines.append('    <!-- 1. 5-SIDED HERALDIC SHIELD FOUNDATION -->')
        lines.append('    <g id="shield-base">')
        if is_color:
            lines.append(f'      <path d="{shield_solid_base_d}" fill="{PALETTE["obsidian"]}"/>')
            lines.append(f'      <path d="{shield_outer_d}" fill="{PALETTE["obsidian"]}" stroke="{PALETTE["black_ink"]}" stroke-width="48" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{shield_silver_rim_d}" fill="url(#silverRimGrad)" fill-rule="evenodd"/>')
            lines.append(f'      <path d="{shield_gold_rim_d}" fill="url(#goldRimGrad)" fill-rule="evenodd"/>')
            lines.append(f'      <path d="{shield_navy_left_d}" fill="url(#navyLeftGrad)"/>')
            lines.append(f'      <path d="{shield_navy_right_d}" fill="url(#navyRightGrad)"/>')
        elif is_white:
            lines.append(f'      <path d="{shield_solid_base_d}" fill="#FFFFFF"/>')
            lines.append(f'      <path d="{shield_outer_d}" fill="#FFFFFF" stroke="#000000" stroke-width="48" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{shield_silver_rim_d}" fill="#000000" fill-rule="evenodd" opacity="0.15"/>')
            lines.append(f'      <path d="{shield_gold_rim_d}" fill="#000000" fill-rule="evenodd" opacity="0.08"/>')
            lines.append(f'      <path d="{shield_navy_left_d} {shield_navy_right_d}" fill="#FFFFFF" stroke="#000000" stroke-width="16"/>')
        else:
            lines.append(f'      <path d="{shield_solid_base_d}" fill="{PALETTE["obsidian"]}"/>')
            lines.append(f'      <path d="{shield_outer_d}" fill="{PALETTE["obsidian"]}" stroke="{PALETTE["black_ink"]}" stroke-width="36"/>')
            lines.append(f'      <path d="{shield_silver_rim_d}" fill="#334155" fill-rule="evenodd"/>')
            lines.append(f'      <path d="{shield_gold_rim_d}" fill="#1E293B" fill-rule="evenodd"/>')
            lines.append(f'      <path d="{shield_navy_left_d} {shield_navy_right_d}" fill="#0A0E17"/>')
        lines.append('    </g>')

        # 2. AVERSA WORDMARK (OPTICALLY CENTERED)
        lines.append('    <!-- 2. AVERSA WORDMARK (OPTICALLY CENTERED) -->')
        av_fill = "url(#goldRimGrad)" if is_color else ("#FFFFFF" if is_white else "#CBD5E1")
        av_hl_fill = "url(#goldLightFacet)" if is_color else ("#FFFFFF" if is_white else "#94A3B8")
        lines.append(f'    <g id="aversa-wordmark" transform="translate({av_tx:.2f}, {av_ty:.2f}) scale({av_sc:.4f})">')
        if is_color:
            lines.append('      <g transform="translate(0, 16)" opacity="0.95">')
            for d_str in aversa_letters:
                lines.append(f'        <path d="{d_str}" fill="{PALETTE["black_ink"]}"/>')
            lines.append('      </g>')
        for d_str in aversa_letters:
            av_stroke_attr = ' stroke="#000000" stroke-width="14" stroke-linejoin="round"' if is_white else ''
            lines.append(f'      <path d="{d_str}" fill="{av_fill}"{av_stroke_attr}/>')
        if is_color:
            for d_hl in aversa_highlights:
                lines.append(f'      <path d="{d_hl}" fill="{av_hl_fill}"/>')
        lines.append('    </g>')

        # 3. CHAMPIONSHIP TOURNAMENT RIBBON BANNER (REFERENCE FORM + HAND-DRAW COLOR)
        lines.append('    <!-- 3. CHAMPIONSHIP TOURNAMENT RIBBON BANNER -->')
        lines.append('    <g id="tournament-ribbon-banner" transform="translate(0, 45)">')
        if is_color:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="url(#goldRimGrad)" stroke="{PALETTE["black_ink"]}" stroke-width="26" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_tail_left_bevel_d} {ribbon_tail_right_bevel_d}" fill="url(#goldLightFacet)"/>')
            lines.append(f'      <path d="{ribbon_fold_left_d} {ribbon_fold_right_d}" fill="{PALETTE["mahogany"]}" stroke="{PALETTE["black_ink"]}" stroke-width="14" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="url(#goldRimGrad)" stroke="{PALETTE["black_ink"]}" stroke-width="32" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_rim_top_d}" fill="url(#goldLightFacet)"/>')
            lines.append(f'      <path d="{ribbon_rim_bot_d}" fill="url(#goldDarkFacet)"/>')
        elif is_white:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="#FFFFFF" stroke="#000000" stroke-width="26" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_fold_left_d} {ribbon_fold_right_d}" fill="#000000" stroke="#000000" stroke-width="14" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="#FFFFFF" stroke="#000000" stroke-width="32" stroke-linejoin="round"/>')
        else:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="#1E293B" stroke="#020408" stroke-width="26" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_fold_left_d} {ribbon_fold_right_d}" fill="#0A0E17" stroke="#020408" stroke-width="14" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="#0A0E17" stroke="#334155" stroke-width="32" stroke-linejoin="round"/>')
        
        # Pure Vector Ribbon Arched Lettering (100% Canva-Compatible, no <textPath>)
        text_fill = PALETTE["black_ink"] if is_color else ("#000000" if is_white else "#FFFFFF")
        lines.append('      <!-- Pure Vector Ribbon Arched Lettering (Canva Compatible) -->')
        lines.append(f'      <g id="ribbon-text-vector" fill="{text_fill}" stroke="{text_fill}" stroke-width="4" stroke-linejoin="round">')
        for ch, x, y, rot, d in RIBBON_TEXT_GLYPHS:
            lines.append(f'        <g transform="translate({x}, {y}) rotate({rot}) scale({FONT_SCALE}, {-FONT_SCALE})">')
            lines.append(f'          <path d="{d}"/>')
            lines.append('        </g>')
        lines.append('      </g>')
        lines.append('    </g>')

        # 4. APPROVED STANDALONE "SVC" TYPOGRAPHY
        lines.append('    <!-- 4. APPROVED STANDALONE "SVC" TYPOGRAPHY -->')
        lines.append(f'    <g id="svc-letters" transform="translate({svc_tx:.2f}, {svc_ty:.2f}) scale({svc_sc:.4f})">')
        lines.append(build_chiseled_svc_svg(mode))
        lines.append('    </g>')

        # 5. TOWERING PANDA MASCOT (HEADER CREST - TOPMOST LAYER)
        lines.append('    <!-- 5. TOWERING PANDA MASCOT (HEADER CREST) -->')
        lines.append(f'    <g id="panda-mascot-crest" transform="translate({p_tx:.2f}, {p_ty:.2f}) scale({p_sc:.4f})">')
        lines.append(f'      <g transform="translate(0, {panda["height"]}) scale(0.1, -0.1)">')
        if is_color:
            lines.append(f'        <path id="panda-base-sil" d="{panda["sil_d"]}" fill="{PALETTE["panda_black"]}"/>')
            lines.append(f'        <path id="panda-slate-arms" d="{panda["slate_d"]}" fill="{PALETTE["panda_slate"]}"/>')
            lines.append(f'        <path id="panda-white-face" d="{panda["white_d"]}" fill="{PALETTE["panda_white"]}"/>')
            lines.append(f'        <path id="panda-gray-shadow" d="{panda["gray_d"]}" fill="{PALETTE["panda_gray"]}"/>')
            lines.append(f'        <path id="panda-black-features" d="{panda["black_d"]}" fill="{PALETTE["panda_black"]}"/>')
            lines.append(f'        <path id="panda-gold-accents" d="{panda["gold_d"]}" fill="{PALETTE["panda_gold_mid"]}"/>')
            lines.append(f'        <path id="panda-gold-bright" d="{panda["gold_br_d"]}" fill="{PALETTE["panda_gold_light"]}"/>')
            lines.append(f'        <path id="panda-glowing-eyes" d="{panda["eyes_d"]}" fill="url(#pandaEyeGrad)"/>')
        elif is_white:
            lines.append(f'        <path id="panda-base-sil" d="{panda["sil_d"]}" fill="#FFFFFF"/>')
            lines.append(f'        <path id="panda-black-features" d="{panda["black_d"]}" fill="#000000"/>')
            lines.append(f'        <path id="panda-glowing-eyes" d="{panda["eyes_d"]}" fill="#FFFFFF" stroke="#000000" stroke-width="8"/>')
        else:
            lines.append(f'        <path id="panda-base-sil" d="{panda["sil_d"]}" fill="#080C14"/>')
            lines.append(f'        <path id="panda-slate-arms" d="{panda["slate_d"]}" fill="#1E293B"/>')
            lines.append(f'        <path id="panda-white-face" d="{panda["white_d"]}" fill="#475569"/>')
            lines.append(f'        <path id="panda-gray-shadow" d="{panda["gray_d"]}" fill="#334155"/>')
            lines.append(f'        <path id="panda-black-features" d="{panda["black_d"]}" fill="#020408"/>')
            lines.append(f'        <path id="panda-gold-accents" d="{panda["gold_d"]}" fill="{PALETTE["panda_gold_mid"]}"/>')
            lines.append(f'        <path id="panda-gold-bright" d="{panda["gold_br_d"]}" fill="{PALETTE["panda_gold_light"]}"/>')
            lines.append(f'        <path id="panda-glowing-eyes" d="{panda["eyes_d"]}" fill="{PALETTE["panda_gold_light"]}"/>')
        lines.append('      </g>')
        lines.append('    </g>')

        lines.append('  </g>')
        lines.append('</svg>\n')
        
        full_svg = "\n".join(lines)
        svg_file = os.path.join(SVG_OUT_DIR, f"svc-crest-{mode}.svg")
        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(full_svg)
        print(f"✓ Saved Master SVG: {svg_file}")
        
        # Render Ultra-HD Transparent PNG (4200 x 4200 px)
        png_file = os.path.join(PNG_OUT_DIR, f"svc-crest-{mode}.png")
        cmd = [
            CHROME_PATH,
            "--headless",
            "--disable-gpu",
            "--default-background-color=00000000",
            f"--window-size={CANVAS_W},{CANVAS_H}",
            f"--screenshot={png_file}",
            svg_file
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"  ✓ Rendered PNG: {png_file} ({CANVAS_W}x{CANVAS_H})")

    # 6. Standalone Mascot Export
    print("\n-> Exporting Standalone Mascot (svc-mascot-standalone.svg & png)...")
    mascot_canvas_w = 2400
    mascot_canvas_h = 1600
    m_sc = 2200.0 / panda["width"]
    m_tx = (mascot_canvas_w - panda["width"] * m_sc) / 2.0
    m_ty = (mascot_canvas_h - panda["height"] * m_sc) / 2.0
    
    mascot_svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {mascot_canvas_w} {mascot_canvas_h}" width="{mascot_canvas_w}" height="{mascot_canvas_h}">
  <title>SVC Mascot Panda - Standalone</title>
  <defs>
    <radialGradient id="pandaEyeGrad" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#F2DC9E"/>
      <stop offset="50%" stop-color="{PALETTE['panda_gold_mid']}"/>
      <stop offset="100%" stop-color="#8C6826"/>
    </radialGradient>
  </defs>
  <g id="svc-panda-standalone" transform="translate({m_tx:.2f}, {m_ty:.2f}) scale({m_sc:.4f})">
    <g transform="translate(0, {panda['height']}) scale(0.1, -0.1)">
      <path id="panda-base-sil" d="{panda['sil_d']}" fill="{PALETTE['panda_black']}"/>
      <path id="panda-slate-arms" d="{panda['slate_d']}" fill="{PALETTE['panda_slate']}"/>
      <path id="panda-white-face" d="{panda['white_d']}" fill="{PALETTE['panda_white']}"/>
      <path id="panda-gray-shadow" d="{panda['gray_d']}" fill="{PALETTE['panda_gray']}"/>
      <path id="panda-black-features" d="{panda['black_d']}" fill="{PALETTE['panda_black']}"/>
      <path id="panda-gold-accents" d="{panda['gold_d']}" fill="{PALETTE['panda_gold_mid']}"/>
      <path id="panda-gold-bright" d="{panda['gold_br_d']}" fill="{PALETTE['panda_gold_light']}"/>
      <path id="panda-glowing-eyes" d="{panda['eyes_d']}" fill="url(#pandaEyeGrad)"/>
    </g>
  </g>
</svg>"""

    mascot_svg_file = os.path.join(SVG_OUT_DIR, "svc-mascot-standalone.svg")
    with open(mascot_svg_file, "w", encoding="utf-8") as f:
        f.write(mascot_svg)
    print(f"✓ Saved Standalone Mascot SVG: {mascot_svg_file}")
    
    mascot_png_file = os.path.join(PNG_OUT_DIR, "svc-mascot-standalone.png")
    cmd_m = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--default-background-color=00000000",
        f"--window-size={mascot_canvas_w},{mascot_canvas_h}",
        f"--screenshot={mascot_png_file}",
        mascot_svg_file
    ]
    subprocess.run(cmd_m, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  ✓ Rendered Standalone Mascot PNG: {mascot_png_file} ({mascot_canvas_w}x{mascot_canvas_h})")

    print("\n" + "=" * 70)
    print("SUCCESS: ALL PRECISION V6 SVC ASSETS GENERATED & RENDERED!")
    print("=" * 70)


if __name__ == "__main__":
    main()
