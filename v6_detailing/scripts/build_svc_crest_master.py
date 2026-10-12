#!/usr/bin/env python3
"""
build_svc_crest_master.py
=============================================================================
Reconstructs and vectorizes the official SVC (Smansage Volleyball Competition)
emblem into high-precision, infinitely scalable SVG and ultra-HD PNG assets.

Components:
1. Panda Mascot (Header Crest):
   - Fierce esport facial expression, ears, black eye patches, nose, mouth
   - High-contrast 2-tone shading: white face, gray shadow, slate arms
   - Metallic gold claws grasping the upper rim of the shield
   - Glowing golden eyes & shoulder fur highlights
   - Clean polygon masking isolating mascot without legacy sketch artifacts
2. Beveled Triangular Shield (Crest):
   - Outer bevel frame: Metallic Platinum / Silver (#94A3B8 -> #E2E8F0 -> #475569)
   - Inner bevel frame: Metallic Gold (#B6580B -> #E09B17 -> #F5C538 -> #FDF39D)
   - Split-lighting Midnight Navy Field (Left #0F172A, Right #070A12)
   - Precision V-notch resting cradle for the mascot
3. Wordmark "AVERSA":
   - Authentic official AVERSA letterforms imported from assets/svg/aversa-standalone-color.svg
4. Akronim "SVC" (Centerpiece):
   - Bold athletic display typography (S, V, C) with Plus Jakarta Sans ExtraBold DNA
   - Multi-layered 3D bevels (deep shadow, gold outer bevel, gold face, inner highlight)
   - V letter slightly taller and extending lower, matching tournament crest aesthetic
5. Lower Arched Banner:
   - Golden curved ribbon with side folds
   - Text: "SMANSAGE VOLLEYBALL COMPETITION" (No "since", no year)
6. Deliverables:
   - assets/svg/svc-crest-color.svg, svc-crest-white.svg, svc-crest-dark.svg
   - assets/svg/svc-mascot-standalone.svg
   - assets/png/svc-crest-color.png, svc-crest-white.png, svc-crest-dark.png
   - assets/png/svc-mascot-standalone.png
=============================================================================
"""

import os
import cv2
import numpy as np
import subprocess
import xml.etree.ElementTree as ET

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
}

def trace_mask_potrace(mask_u8, name, alphamax=1.2):
    bmp = f"scratch/svc_clean_{name}.bmp"
    svg = f"scratch/svc_clean_{name}.svg"
    cleaned = cv2.medianBlur(mask_u8, 3)
    cv2.imwrite(bmp, cleaned)
    subprocess.run(["potrace", "-s", "--invert", "--alphamax", str(alphamax), "-o", svg, bmp], check=True)
    tree = ET.parse(svg)
    paths = [e.attrib["d"] for e in tree.getroot().iter() if e.tag.endswith("path") and "d" in e.attrib]
    return " ".join(paths)

def extract_panda_vector_layers():
    print("-> Extracting and tracing Panda Mascot layers from hand draw SVC.PNG...")
    img = cv2.imread(HAND_DRAW_PATH)
    if img is None:
        raise FileNotFoundError(f"Cannot load {HAND_DRAW_PATH}")
    
    # Panda bounding box in hand draw SVC: x=740..1660, y=90..670 (width=920, height=580)
    p_crop = img[90:670, 740:1660]
    h, w = p_crop.shape[:2]
    rgb = cv2.cvtColor(p_crop, cv2.COLOR_BGR2RGB)
    
    # 1. Background flood fill
    flood = p_crop.copy()
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood, mask, (0, 0), (0, 255, 0), (5, 5, 5), (5, 5, 5))
    cv2.floodFill(flood, mask, (w - 1, 0), (0, 255, 0), (5, 5, 5), (5, 5, 5))
    panda_fg = ~((flood[:, :, 0] == 0) & (flood[:, :, 1] == 255) & (flood[:, :, 2] == 0))
    
    # 2. Precision contour clipping: isolates arms, paws, claws, and chin while excluding legacy sketch shield bar
    pts = [
        [0, 0],
        [0, 300],
        [120, 340],
        [170, 410],
        [220, 470],
        [240, 510],
        [285, 565], # left claw 1 tip
        [295, 525], # notch
        [320, 560], # left claw 2 tip
        [335, 515], # notch
        [358, 545], # left claw 3 tip
        [375, 460], # left inner wrist
        [400, 420], # chin left
        [450, 435], # chin center
        [500, 420], # chin right
        [525, 460], # right inner wrist
        [542, 545], # right claw 1 tip
        [565, 515], # notch
        [580, 560], # right claw 2 tip
        [605, 525], # notch
        [615, 565], # right claw 3 tip
        [660, 510],
        [680, 470],
        [730, 410],
        [780, 340],
        [w - 1, 300],
        [w - 1, 0],
    ]
    poly = np.array(pts, dtype=np.int32)
    mask_poly = np.zeros((h, w), dtype=np.uint8)
    cv2.fillPoly(mask_poly, [poly], 255)
    clean_fg = panda_fg & (mask_poly > 0)
    
    # Layers:
    # 1. Outer Silhouette (Base Black)
    base_sil = (clean_fg.astype(np.uint8)) * 255
    
    # 2. White Face Fur (rgb > 155 in face)
    white_mask = clean_fg & (rgb[:, :, 0] > 155) & (rgb[:, :, 1] > 155) & (rgb[:, :, 2] > 155)
    
    # 3. Soft Gray Face Shadows
    gray_mask = white_mask & (rgb[:, :, 0] < 225)
    
    # 4. Slate Navy Fur Shading (Arms & Chest)
    slate_mask = clean_fg & (rgb[:, :, 2] > rgb[:, :, 0] + 5) & (rgb[:, :, 2] > 40) & (rgb[:, :, 2] < 125) & (rgb[:, :, 0] < 90)
    
    # 5. Black Facial Features (Ears, Eye patches, Nose, Mouth, Arm creases)
    black_feat_mask = clean_fg & (rgb[:, :, 0] < 45) & (rgb[:, :, 1] < 45) & (rgb[:, :, 2] < 45)
    
    # 6. Gold Claws, Shoulder Fur, and Eyes
    gold_fur_mask = clean_fg & (rgb[:, :, 0] > 140) & (rgb[:, :, 1] > 85) & (rgb[:, :, 2] < 95) & (rgb[:, :, 0] > rgb[:, :, 2] + 45)
    eyes_box = np.zeros((h, w), dtype=bool)
    eyes_box[200:255, 350:405] = True
    eyes_box[200:255, 520:575] = True
    eyes_mask = eyes_box & (rgb[:, :, 0] > 120) & (rgb[:, :, 1] > 90) & (rgb[:, :, 0] > rgb[:, :, 2] + 25)
    
    gold_total_mask = gold_fur_mask | eyes_mask
    gold_bright_mask = gold_total_mask & (rgb[:, :, 1] > 135)
    
    sil_d = trace_mask_potrace(base_sil, "sil")
    white_d = trace_mask_potrace(white_mask.astype(np.uint8) * 255, "white")
    gray_d = trace_mask_potrace(gray_mask.astype(np.uint8) * 255, "gray")
    slate_d = trace_mask_potrace(slate_mask.astype(np.uint8) * 255, "slate")
    black_d = trace_mask_potrace(black_feat_mask.astype(np.uint8) * 255, "black")
    gold_d = trace_mask_potrace(gold_total_mask.astype(np.uint8) * 255, "gold")
    gold_br_d = trace_mask_potrace(gold_bright_mask.astype(np.uint8) * 255, "gold_br")
    
    return {
        "width": w,
        "height": h,
        "sil_d": sil_d,
        "white_d": white_d,
        "gray_d": gray_d,
        "slate_d": slate_d,
        "black_d": black_d,
        "gold_d": gold_d,
        "gold_br_d": gold_br_d,
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

def get_beveled_svc_paths():
    """
    Returns high-impact athletic display typography for S, V, C.
    Derived from Plus Jakarta Sans ExtraBold with esport crest beveling.
    """
    s_path = "M 234.81 504.81 Q 206.81 504.81 182.19 494.62 Q 157.62 484.38 139.81 465.62 Q 122.00 446.81 113.19 421.19 L 164.00 398.38 Q 175.19 422.81 195.00 436.81 Q 214.81 450.81 238.81 450.81 Q 257.62 450.81 269.00 442.25 Q 280.38 433.62 280.38 419.19 Q 280.38 398.38 254.00 389.62 L 195.62 370.38 Q 124.00 346.81 124.00 286.00 Q 124.00 259.62 137.00 239.62 Q 150.00 219.62 173.38 208.44 Q 196.81 197.19 227.19 197.19 Q 267.62 197.19 298.19 217.44 Q 328.81 237.62 341.19 272.81 L 290.81 295.62 Q 282.38 274.81 265.56 263.00 Q 248.81 251.19 227.19 251.19 Q 208.38 251.19 196.75 260.19 Q 185.19 269.19 185.19 283.62 Q 185.19 304.81 212.38 314.00 L 269.62 332.38 Q 341.19 355.62 341.19 415.62 Q 341.19 441.62 327.56 461.81 Q 314.00 482.00 290.19 493.44 Q 266.38 504.81 234.81 504.81 Z"
    v_path = "M 534.35 515.00 L 424.70 194.65 L 497.80 194.65 L 573.05 429.00 L 648.30 194.65 L 721.40 194.65 L 611.75 515.00 L 534.35 515.00 Z"
    c_path = "M 958.00 504.81 Q 926.00 504.81 898.56 493.25 Q 871.19 481.62 850.75 460.81 Q 830.38 440.00 819.00 412.00 Q 807.62 384.00 807.62 350.81 Q 807.62 317.62 818.81 289.44 Q 830.00 261.19 850.38 240.62 Q 870.81 220.00 898.19 208.62 Q 925.62 197.19 958.00 197.19 Q 990.38 197.19 1016.19 208.00 Q 1042.00 218.81 1060.00 236.81 Q 1078.00 254.81 1085.62 276.81 L 1030.81 303.19 Q 1023.19 281.62 1004.19 267.44 Q 985.19 253.19 958.00 253.19 Q 931.62 253.19 911.62 265.62 Q 891.62 278.00 880.62 299.81 Q 869.62 321.62 869.62 350.81 Q 869.62 380.00 880.62 402.00 Q 891.62 424.00 911.62 436.44 Q 931.62 448.81 958.00 448.81 Q 985.19 448.81 1004.19 434.62 Q 1023.19 420.38 1030.81 398.81 L 1085.62 425.19 Q 1078.00 447.19 1060.00 465.19 Q 1042.00 483.19 1016.19 494.00 Q 990.38 504.81 958.00 504.81 Z"
    return f"{s_path} {v_path} {c_path}"

def main():
    print("=" * 70)
    print("RECONSTRUCTING SVC EMBLEM (Smansage Volleyball Competition)")
    print("=" * 70)
    
    # 1. Panda Mascot Vectors
    panda = extract_panda_vector_layers()
    
    # 2. Master AVERSA Vectors
    aversa_letters, aversa_highlights = get_aversa_vector()
    
    # 3. Athletic 3D Beveled SVC Paths
    svc_combined_d = get_beveled_svc_paths()
    
    # Geometry Layout Calculations (Canvas 4200 x 4200 px)
    # -------------------------------------------------------------
    # Triangular Shield Geometry:
    # Outer Silhouette Path:
    shield_outer_d = "M 550 1180 L 1380 1180 L 2100 1550 L 2820 1180 L 3650 1180 L 2100 3780 Z"
    
    # Shield Outer Platinum / Silver Rim (Inset):
    shield_silver_rim_d = "M 550 1180 L 1380 1180 L 2100 1550 L 2820 1180 L 3650 1180 L 2100 3780 Z M 670 1280 L 2100 3620 L 3530 1280 L 2780 1280 L 2100 1630 L 1420 1280 Z"
    
    # Shield Inner Gold Rim (Inset):
    shield_gold_rim_d = "M 670 1280 L 1420 1280 L 2100 1630 L 2780 1280 L 3530 1280 L 2100 3620 Z M 780 1370 L 2100 3470 L 3420 1370 L 2740 1370 L 2100 1700 L 1460 1370 Z"
    
    # Shield Midnight Navy Field (Split-Lit):
    shield_navy_left_d = "M 780 1370 L 1460 1370 L 2100 1700 L 2100 3470 Z"
    shield_navy_right_d = "M 2100 1700 L 2740 1370 L 3420 1370 L 2100 3470 Z"
    
    # -------------------------------------------------------------
    # Lower Ribbon / Banner Geometry:
    ribbon_body_d = "M 880 3270 Q 2100 2930 3320 3270 L 3320 3510 Q 2100 3170 880 3510 Z"
    ribbon_rim_top_d = "M 880 3270 Q 2100 2930 3320 3270 L 3320 3310 Q 2100 2970 880 3310 Z"
    ribbon_rim_bot_d = "M 880 3470 Q 2100 3130 3320 3470 L 3320 3510 Q 2100 3170 880 3510 Z"
    
    ribbon_tail_left_d = "M 880 3270 L 640 3340 L 730 3460 L 640 3580 L 880 3510 Z"
    ribbon_fold_left_d = "M 880 3270 L 880 3510 L 790 3420 Z"
    
    ribbon_tail_right_d = "M 3320 3270 L 3560 3340 L 3470 3460 L 3560 3580 L 3320 3510 Z"
    ribbon_fold_right_d = "M 3320 3270 L 3320 3510 L 3410 3420 Z"
    
    ribbon_text_path_d = "M 960 3455 Q 2100 3115 3240 3455"
    
    # -------------------------------------------------------------
    # Panda Mascot Scaling & Placement:
    # Mascot sits perched on the shield rim, paws grasping the cradle
    p_sc = 2200.0 / panda["width"]
    p_tx = CX - (panda["width"] * p_sc) / 2.0
    p_ty = 490.0
    
    # -------------------------------------------------------------
    # AVERSA Wordmark Placement:
    # Placed below the panda chin & claws, above SVC acronym
    av_sc = 0.44
    av_tx = CX - (2700 * av_sc) / 2.0
    av_ty = 1760.0
    
    # -------------------------------------------------------------
    # SVC Wordmark Placement:
    # Centered at CX=2100, Y=2620, width ~ 2260 px
    svc_box_w = 973.0
    svc_box_h = 321.0
    svc_target_w = 2260.0
    svc_scale = svc_target_w / svc_box_w
    svc_center_x = 600.0
    svc_center_y = 354.5
    svc_target_cx = CX
    svc_target_cy = 2520.0
    svc_tx = svc_target_cx - svc_center_x * svc_scale
    svc_ty = svc_target_cy - svc_center_y * svc_scale
    
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
      <stop offset="20%" stop-color="{PALETTE['vivid_gold']}"/>
      <stop offset="50%" stop-color="{PALETTE['marigold']}"/>
      <stop offset="80%" stop-color="{PALETTE['bronze']}"/>
      <stop offset="100%" stop-color="{PALETTE['mahogany']}"/>
    </linearGradient>

    <linearGradient id="svcGoldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['canary']}"/>
      <stop offset="22%" stop-color="{PALETTE['vivid_gold']}"/>
      <stop offset="68%" stop-color="{PALETTE['marigold']}"/>
      <stop offset="100%" stop-color="{PALETTE['bronze']}"/>
    </linearGradient>

    <linearGradient id="goldFacetLight" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['canary']}"/>
      <stop offset="100%" stop-color="{PALETTE['vivid_gold']}"/>
    </linearGradient>

    <linearGradient id="goldFacetDark" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['bronze']}"/>
      <stop offset="100%" stop-color="{PALETTE['deep_crevice']}"/>
    </linearGradient>

    <!-- Midnight Navy Shield Field Gradients -->
    <linearGradient id="navyLeftGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['navy_light']}"/>
      <stop offset="60%" stop-color="{PALETTE['navy_mid']}"/>
      <stop offset="100%" stop-color="{PALETTE['navy_deep']}"/>
    </linearGradient>

    <linearGradient id="navyRightGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['navy_mid']}"/>
      <stop offset="70%" stop-color="{PALETTE['navy_deep']}"/>
      <stop offset="100%" stop-color="{PALETTE['obsidian']}"/>
    </linearGradient>

    <!-- Text Path Curve for Ribbon -->
    <path id="ribbonTextArc" d="{ribbon_text_path_d}"/>
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
        
        # 1. TRIANGULAR SHIELD FOUNDATION
        lines.append('    <!-- 1. TRIANGULAR SHIELD FOUNDATION -->')
        lines.append('    <g id="shield-base">')
        if is_color:
            lines.append(f'      <path d="{shield_outer_d}" fill="{PALETTE["obsidian"]}" stroke="{PALETTE["black_ink"]}" stroke-width="48" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{shield_silver_rim_d}" fill="url(#silverRimGrad)" fill-rule="evenodd"/>')
            lines.append(f'      <path d="{shield_gold_rim_d}" fill="url(#goldRimGrad)" fill-rule="evenodd"/>')
            lines.append(f'      <path d="{shield_navy_left_d}" fill="url(#navyLeftGrad)"/>')
            lines.append(f'      <path d="{shield_navy_right_d}" fill="url(#navyRightGrad)"/>')
        elif is_white:
            lines.append(f'      <path d="{shield_outer_d}" fill="#FFFFFF" stroke="#000000" stroke-width="48" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{shield_silver_rim_d}" fill="#000000" fill-rule="evenodd" opacity="0.15"/>')
            lines.append(f'      <path d="{shield_gold_rim_d}" fill="#000000" fill-rule="evenodd" opacity="0.08"/>')
            lines.append(f'      <path d="{shield_navy_left_d} {shield_navy_right_d}" fill="#FFFFFF" stroke="#000000" stroke-width="16"/>')
        else:
            lines.append(f'      <path d="{shield_outer_d}" fill="{PALETTE["obsidian"]}" stroke="{PALETTE["black_ink"]}" stroke-width="36"/>')
            lines.append(f'      <path d="{shield_silver_rim_d}" fill="#334155" fill-rule="evenodd"/>')
            lines.append(f'      <path d="{shield_gold_rim_d}" fill="#1E293B" fill-rule="evenodd"/>')
            lines.append(f'      <path d="{shield_navy_left_d} {shield_navy_right_d}" fill="#0A0E17"/>')
        lines.append('    </g>')

        # 2. AVERSA WORDMARK
        lines.append('    <!-- 2. AVERSA WORDMARK (Official Master Letterforms) -->')
        av_fill = "url(#goldRimGrad)" if is_color else ("#FFFFFF" if is_white else "#CBD5E1")
        av_hl_fill = "url(#goldFacetLight)" if is_color else ("#FFFFFF" if is_white else "#94A3B8")
        lines.append(f'    <g id="aversa-wordmark" transform="translate({av_tx:.2f}, {av_ty:.2f}) scale({av_sc:.4f})">')
        # Drop shadow for AVERSA
        if is_color:
            lines.append('      <g transform="translate(0, 14)" opacity="0.9">')
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

        # 3. ATHLETIC 3D BEVELED "SVC"
        lines.append('    <!-- 3. ATHLETIC 3D BEVELED "SVC" TYPOGRAPHY -->')
        lines.append(f'    <g id="svc-letters" transform="translate({svc_tx:.2f}, {svc_ty:.2f}) scale({svc_scale:.4f})">')
        if is_color:
            # Layer 1: Heavy black drop shadow
            lines.append(f'      <g transform="translate(0, 16)" fill="none" stroke="{PALETTE["obsidian"]}" stroke-width="48" stroke-linejoin="round">')
            lines.append(f'        <path d="{svc_combined_d}"/>')
            lines.append('      </g>')
            # Layer 2: Beveled Gold Outer Stroke
            lines.append(f'      <g fill="none" stroke="url(#goldRimGrad)" stroke-width="32" stroke-linejoin="round">')
            lines.append(f'        <path d="{svc_combined_d}"/>')
            lines.append('      </g>')
            # Layer 3: Solid Face Gold
            lines.append(f'      <g fill="url(#svcGoldGrad)">')
            lines.append(f'        <path d="{svc_combined_d}"/>')
            lines.append('      </g>')
            # Layer 4: Inner Bevel Inset Highlight Stroke
            lines.append(f'      <g fill="none" stroke="{PALETTE["canary"]}" stroke-width="6" opacity="0.8" stroke-linejoin="round">')
            lines.append(f'        <path d="{svc_combined_d}"/>')
            lines.append('      </g>')
        elif is_white:
            lines.append(f'      <g fill="none" stroke="#000000" stroke-width="36" stroke-linejoin="round">')
            lines.append(f'        <path d="{svc_combined_d}"/>')
            lines.append('      </g>')
            lines.append(f'      <g fill="#FFFFFF">')
            lines.append(f'        <path d="{svc_combined_d}"/>')
            lines.append('      </g>')
            lines.append(f'      <g fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.6" stroke-linejoin="round">')
            lines.append(f'        <path d="{svc_combined_d}"/>')
            lines.append('      </g>')
        else:
            lines.append(f'      <g fill="none" stroke="{PALETTE["black_ink"]}" stroke-width="40" stroke-linejoin="round">')
            lines.append(f'        <path d="{svc_combined_d}"/>')
            lines.append('      </g>')
            lines.append(f'      <g fill="#1E293B" stroke="#64748B" stroke-width="14">')
            lines.append(f'        <path d="{svc_combined_d}"/>')
            lines.append('      </g>')
        lines.append('    </g>')

        # 4. LOWER ARCHED RIBBON BANNER
        lines.append('    <!-- 4. LOWER ARCHED BANNER (SMANSAGE VOLLEYBALL COMPETITION) -->')
        lines.append('    <g id="ribbon-banner">')
        if is_color:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="{PALETTE["bronze"]}" stroke="{PALETTE["obsidian"]}" stroke-width="16"/>')
            lines.append(f'      <path d="{ribbon_fold_left_d} {ribbon_fold_right_d}" fill="{PALETTE["mahogany"]}"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="url(#goldRimGrad)" stroke="{PALETTE["obsidian"]}" stroke-width="20"/>')
            lines.append(f'      <path d="{ribbon_rim_top_d}" fill="url(#goldFacetLight)"/>')
            lines.append(f'      <path d="{ribbon_rim_bot_d}" fill="url(#goldFacetDark)"/>')
            text_fill = PALETTE["black_ink"]
            lines.append(f'      <text font-family="Plus Jakarta Sans, Montserrat, Arial, sans-serif" font-size="94" font-weight="900" letter-spacing="9" fill="{text_fill}">')
            lines.append('        <textPath href="#ribbonTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        elif is_white:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="none" stroke="#FFFFFF" stroke-width="20"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="#FFFFFF" stroke="#000000" stroke-width="16"/>')
            lines.append(f'      <text font-family="Plus Jakarta Sans, Montserrat, Arial, sans-serif" font-size="94" font-weight="900" letter-spacing="9" fill="#000000">')
            lines.append('        <textPath href="#ribbonTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        else:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="#1E293B" stroke="#020408" stroke-width="20"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="#0A0E17" stroke="#334155" stroke-width="20"/>')
            lines.append(f'      <text font-family="Plus Jakarta Sans, Montserrat, Arial, sans-serif" font-size="94" font-weight="900" letter-spacing="9" fill="#FFFFFF">')
            lines.append('        <textPath href="#ribbonTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        lines.append('    </g>')

        # 5. PANDA MASCOT (HEADER CREST - TOPMOST LAYER)
        lines.append('    <!-- 5. PANDA MASCOT (HEADER CREST) -->')
        lines.append(f'    <g id="panda-mascot-crest" transform="translate({p_tx:.2f}, {p_ty:.2f}) scale({p_sc:.4f})">')
        lines.append(f'      <g transform="translate(0, {panda["height"]}) scale(0.1, -0.1)">')
        if is_color:
            lines.append(f'        <path id="panda-base-sil" d="{panda["sil_d"]}" fill="{PALETTE["obsidian"]}"/>')
            lines.append(f'        <path id="panda-slate-arms" d="{panda["slate_d"]}" fill="{PALETTE["navy_light"]}"/>')
            lines.append(f'        <path id="panda-white-face" d="{panda["white_d"]}" fill="{PALETTE["pure_white"]}"/>')
            lines.append(f'        <path id="panda-gray-shadow" d="{panda["gray_d"]}" fill="{PALETTE["silver_base"]}"/>')
            lines.append(f'        <path id="panda-black-features" d="{panda["black_d"]}" fill="{PALETTE["black_ink"]}"/>')
            lines.append(f'        <path id="panda-gold-accents" d="{panda["gold_d"]}" fill="{PALETTE["marigold"]}"/>')
            lines.append(f'        <path id="panda-gold-bright" d="{panda["gold_br_d"]}" fill="{PALETTE["vivid_gold"]}"/>')
        elif is_white:
            lines.append(f'        <path id="panda-base-sil" d="{panda["sil_d"]}" fill="#FFFFFF"/>')
            lines.append(f'        <path id="panda-black-features" d="{panda["black_d"]}" fill="#000000"/>')
        else:
            lines.append(f'        <path id="panda-base-sil" d="{panda["sil_d"]}" fill="#080C14"/>')
            lines.append(f'        <path id="panda-white-face" d="{panda["white_d"]}" fill="#475569"/>')
            lines.append(f'        <path id="panda-black-features" d="{panda["black_d"]}" fill="#020408"/>')
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
  <g id="svc-panda-standalone" transform="translate({m_tx:.2f}, {m_ty:.2f}) scale({m_sc:.4f})">
    <g transform="translate(0, {panda['height']}) scale(0.1, -0.1)">
      <path id="panda-base-sil" d="{panda['sil_d']}" fill="{PALETTE['obsidian']}"/>
      <path id="panda-slate-arms" d="{panda['slate_d']}" fill="{PALETTE['navy_light']}"/>
      <path id="panda-white-face" d="{panda['white_d']}" fill="{PALETTE['pure_white']}"/>
      <path id="panda-gray-shadow" d="{panda['gray_d']}" fill="{PALETTE['silver_base']}"/>
      <path id="panda-black-features" d="{panda['black_d']}" fill="{PALETTE['black_ink']}"/>
      <path id="panda-gold-accents" d="{panda['gold_d']}" fill="{PALETTE['marigold']}"/>
      <path id="panda-gold-bright" d="{panda['gold_br_d']}" fill="{PALETTE['vivid_gold']}"/>
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
    print("SUCCESS: ALL SVC EMBLEM ASSETS GENERATED & RENDERED!")
    print("=" * 70)

if __name__ == "__main__":
    main()
