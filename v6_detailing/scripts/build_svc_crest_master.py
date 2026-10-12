#!/usr/bin/env python3
"""
build_svc_crest_master.py
=============================================================================
Reconstructs and vectorizes the official SVC (Smansage Volleyball Competition)
emblem into high-precision, infinitely scalable SVG and ultra-HD PNG assets.

Key Architectural Updates (Precision V2.1):
1. 5-Sided Heraldic Shield (Pentagonal Crest):
   - Corrected from simple triangle to authentic 5-sided tournament crest
   - Steep upper diagonal slopes to mid-knuckles, gentle lower taper to base tip
   - 3D mitered platinum/silver outer bevel & metallic gold inner bevel
   - Split midnight navy field (Left #0F172A, Right #070A12)
2. Towering Panda Mascot (Header Crest):
   - Elevated upwards so full head, ears, and glare tower proudly above shield
   - Claws securely grasping the upper golden rim cradle
   - Multi-layer vector tracing (white face, gray shadow, slate arms, gold claws/eyes)
3. 100% Authentic Hand-Drawn "SVC" Typography:
   - S, V, C letters isolated without boundary artifacts or shield rim spikes
   - V letter with angled triangular bevel caps, spine ridge, and flat chamfered base
   - S and C letters with 3D chamfered terminal wedges and faceted body shading
4. Concentric Arched Ribbon Banner:
   - True mathematical concentric circular arc (equal top/bottom rim thickness)
   - Text "SMANSAGE VOLLEYBALL COMPETITION" centered along arc centerline
=============================================================================
"""

import os
import math
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

def trace_mask_potrace(mask_u8, name, alphamax=1.0):
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
    
    # Background flood fill
    flood = p_crop.copy()
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(flood, mask, (0, 0), (0, 255, 0), (5, 5, 5), (5, 5, 5))
    cv2.floodFill(flood, mask, (w - 1, 0), (0, 255, 0), (5, 5, 5), (5, 5, 5))
    panda_fg = ~((flood[:, :, 0] == 0) & (flood[:, :, 1] == 255) & (flood[:, :, 2] == 0))
    
    # Precision contour polygon clipping: eliminates legacy shield bar
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
    base_sil = (clean_fg.astype(np.uint8)) * 255
    white_mask = clean_fg & (rgb[:, :, 0] > 155) & (rgb[:, :, 1] > 155) & (rgb[:, :, 2] > 155)
    gray_mask = white_mask & (rgb[:, :, 0] < 225)
    slate_mask = clean_fg & (rgb[:, :, 2] > rgb[:, :, 0] + 5) & (rgb[:, :, 2] > 40) & (rgb[:, :, 2] < 125) & (rgb[:, :, 0] < 90)
    black_feat_mask = clean_fg & (rgb[:, :, 0] < 45) & (rgb[:, :, 1] < 45) & (rgb[:, :, 2] < 45)
    
    gold_fur_mask = clean_fg & (rgb[:, :, 0] > 140) & (rgb[:, :, 1] > 85) & (rgb[:, :, 2] < 95) & (rgb[:, :, 0] > rgb[:, :, 2] + 45)
    eyes_box = np.zeros((h, w), dtype=bool)
    eyes_box[200:255, 350:405] = True
    eyes_box[200:255, 520:575] = True
    eyes_mask = eyes_box & (rgb[:, :, 0] > 120) & (rgb[:, :, 1] > 90) & (rgb[:, :, 0] > rgb[:, :, 2] + 25)
    
    gold_total_mask = gold_fur_mask | eyes_mask
    gold_bright_mask = gold_total_mask & (rgb[:, :, 1] > 135)
    
    sil_d = trace_mask_potrace(base_sil, "p_sil")
    white_d = trace_mask_potrace(white_mask.astype(np.uint8) * 255, "p_white")
    gray_d = trace_mask_potrace(gray_mask.astype(np.uint8) * 255, "p_gray")
    slate_d = trace_mask_potrace(slate_mask.astype(np.uint8) * 255, "p_slate")
    black_d = trace_mask_potrace(black_feat_mask.astype(np.uint8) * 255, "p_black")
    gold_d = trace_mask_potrace(gold_total_mask.astype(np.uint8) * 255, "p_gold")
    gold_br_d = trace_mask_potrace(gold_bright_mask.astype(np.uint8) * 255, "p_gold_br")
    
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

def extract_svc_typography_layers():
    """
    Extracts authentic 3D faceted letterforms (S, V, C) directly from hand draw SVC.PNG.
    Components are cleanly segmented to remove shield rim artifacts on sides and bottom.
    """
    print("-> Extracting authentic 3D faceted SVC typography from hand draw SVC.PNG...")
    img = cv2.imread(HAND_DRAW_PATH)
    crop = img[750:1300, 800:1600]
    h, w = crop.shape[:2]
    rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
    
    is_gold = (rgb[:, :, 0] > 120) & (rgb[:, :, 1] > 70) & (rgb[:, :, 2] < 90)
    num, labels, stats, centroids = cv2.connectedComponentsWithStats(is_gold.astype(np.uint8))
    
    s_mask = (labels == 47)
    v_mask = (labels == 18)
    c_mask = (labels == 49)
    
    # 1. Clean S letter
    s_mask[425:, :] = False
    for y in range(260, 425):
        for x in range(125):
            s_mask[y, x] = False
            
    # 2. Clean C letter
    c_mask[430:, :] = False
    c_mask[140:220, 715:] = False
    c_mask[220:330, 710:] = False
    for y in range(320, 430):
        for x in range(745, w):
            c_mask[y, x] = False
            
    total_clean = s_mask | v_mask | c_mask
    
    # Multi-layer color masks
    sil_mask = total_clean.astype(np.uint8) * 255
    face_mask = (total_clean & (rgb[:, :, 0] > 195) & (rgb[:, :, 1] > 150)).astype(np.uint8) * 255
    mid_mask = (total_clean & (rgb[:, :, 0] > 165) & (rgb[:, :, 1] > 115) & (face_mask == 0)).astype(np.uint8) * 255
    facet_mask = (total_clean & (face_mask == 0) & (mid_mask == 0)).astype(np.uint8) * 255
    
    sil_d = trace_mask_potrace(sil_mask, "svc_sil", alphamax=1.0)
    face_d = trace_mask_potrace(face_mask, "svc_face", alphamax=1.0)
    mid_d = trace_mask_potrace(mid_mask, "svc_mid", alphamax=1.0)
    facet_d = trace_mask_potrace(facet_mask, "svc_facet", alphamax=1.0)
    
    return {
        "width": w,
        "height": h,
        "sil_d": sil_d,
        "face_d": face_d,
        "mid_d": mid_d,
        "facet_d": facet_d,
    }

def main():
    print("=" * 70)
    print("RECONSTRUCTING SVC EMBLEM (Smansage Volleyball Competition) - V2.1")
    print("=" * 70)
    
    # 1. Panda Mascot Vectors
    panda = extract_panda_vector_layers()
    
    # 2. Master AVERSA Vectors
    aversa_letters, aversa_highlights = get_aversa_vector()
    
    # 3. Authentic 3D Faceted SVC Typography
    svc_data = extract_svc_typography_layers()
    
    # =============================================================
    # Geometry Layout Calculations (Canvas 4200 x 4200 px)
    # =============================================================
    
    # -------------------------------------------------------------
    # 1. 5-Sided Heraldic Pentagonal Shield Geometry
    # -------------------------------------------------------------
    # Outer Shield Silhouette (Mitered 5-sided crest with top V-cradle):
    shield_outer_d = "M 650 1050 L 1550 1050 L 2100 1340 L 2650 1050 L 3550 1050 L 3080 2850 L 2100 3780 L 1120 2850 Z"
    
    # Outer Platinum / Silver Rim (Inset):
    shield_silver_rim_d = (
        "M 650 1050 L 1550 1050 L 2100 1340 L 2650 1050 L 3550 1050 L 3080 2850 L 2100 3780 L 1120 2850 Z "
        "M 760 1150 L 1195 2815 L 2100 3650 L 3005 2815 L 3440 1150 L 2620 1150 L 2100 1420 L 1580 1150 Z"
    )
    
    # Inner Gold Rim (Inset):
    shield_gold_rim_d = (
        "M 760 1150 L 1580 1150 L 2100 1420 L 2620 1150 L 3440 1150 L 3005 2815 L 2100 3650 L 1195 2815 Z "
        "M 860 1240 L 1260 2780 L 2100 3530 L 2940 2780 L 3340 1240 L 2590 1240 L 2100 1490 L 1610 1240 Z"
    )
    
    # Split Midnight Navy Field:
    shield_navy_left_d = "M 860 1240 L 1610 1240 L 2100 1490 L 2100 3530 L 1260 2780 Z"
    shield_navy_right_d = "M 2100 1490 L 2590 1240 L 3340 1240 L 2940 2780 L 2100 3530 Z"
    
    # -------------------------------------------------------------
    # 2. Concentric Arched Ribbon Banner Geometry
    # -------------------------------------------------------------
    # Mathematical concentric circular arcs centered at (X0=2100, Y0=7000)
    # Radii: R_top=3900, R_mid=3770 (text centerline), R_bot=3640 (thickness=260 px)
    ribbon_body_d = "M 895 3291 A 3900 3900 0 0 1 3305 3291 L 3225 3538 A 3640 3640 0 0 0 975 3538 Z"
    ribbon_rim_top_d = "M 895 3291 A 3900 3900 0 0 1 3305 3291 L 3290 3330 A 3860 3860 0 0 0 910 3330 Z"
    ribbon_rim_bot_d = "M 960 3500 A 3680 3680 0 0 1 3240 3500 L 3225 3538 A 3640 3640 0 0 0 975 3538 Z"
    
    # Side fold ribbon tails:
    ribbon_tail_left_d = "M 895 3291 L 630 3360 L 730 3485 L 630 3610 L 975 3538 Z"
    ribbon_fold_left_d = "M 895 3291 L 975 3538 L 870 3440 Z"
    ribbon_tail_right_d = "M 3305 3291 L 3570 3360 L 3470 3485 L 3570 3610 L 3225 3538 Z"
    ribbon_fold_right_d = "M 3305 3291 L 3225 3538 L 3330 3440 Z"
    
    ribbon_text_path_d = "M 935 3415 A 3770 3770 0 0 1 3265 3415"
    
    # -------------------------------------------------------------
    # 3. Towering Panda Mascot Placement
    # -------------------------------------------------------------
    # Elevated so entire head & glare tower proudly above the shield crest
    p_sc = 2200.0 / panda["width"]
    p_tx = CX - (panda["width"] * p_sc) / 2.0
    p_ty = 180.0
    
    # -------------------------------------------------------------
    # 4. AVERSA Wordmark Placement
    # -------------------------------------------------------------
    # Placed in the spacious upper navy field below chin and above SVC
    av_sc = 0.44
    av_tx = CX - (2700 * av_sc) / 2.0
    av_ty = 1600.0
    
    # -------------------------------------------------------------
    # 5. Authentic 3D Faceted SVC Placement
    # -------------------------------------------------------------
    # Centered at CX=2100, Y=2400 with width ~ 2300 px
    svc_w = svc_data["width"]
    svc_h = svc_data["height"]
    svc_target_w = 2300.0
    svc_sc = svc_target_w / svc_w
    svc_tx = CX - (svc_w * svc_sc) / 2.0
    svc_ty = 1960.0
    
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

    <linearGradient id="svcGoldFaceGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['canary']}"/>
      <stop offset="25%" stop-color="{PALETTE['champagne']}"/>
      <stop offset="70%" stop-color="{PALETTE['vivid_gold']}"/>
      <stop offset="100%" stop-color="{PALETTE['marigold']}"/>
    </linearGradient>

    <linearGradient id="svcGoldFacetGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['marigold']}"/>
      <stop offset="40%" stop-color="{PALETTE['bronze']}"/>
      <stop offset="80%" stop-color="{PALETTE['mahogany']}"/>
      <stop offset="100%" stop-color="{PALETTE['deep_crevice']}"/>
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

    <!-- Concentric Arched Text Path for Ribbon -->
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
        
        # 1. 5-SIDED HERALDIC SHIELD FOUNDATION
        lines.append('    <!-- 1. 5-SIDED HERALDIC SHIELD FOUNDATION -->')
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

        # 3. 100% AUTHENTIC 3D FACETED "SVC" TYPOGRAPHY
        lines.append('    <!-- 3. AUTHENTIC 3D FACETED "SVC" TYPOGRAPHY -->')
        lines.append(f'    <g id="svc-letters" transform="translate({svc_tx:.2f}, {svc_ty:.2f}) scale({svc_sc:.4f})">')
        lines.append(f'      <g transform="translate(0, {svc_h}) scale(0.1, -0.1)">')
        if is_color:
            # Layer 1: Heavy black drop shadow
            lines.append(f'        <g transform="translate(0, -18)">')
            lines.append(f'          <path d="{svc_data["sil_d"]}" fill="{PALETTE["obsidian"]}" stroke="{PALETTE["black_ink"]}" stroke-width="32" stroke-linejoin="round"/>')
            lines.append('        </g>')
            # Layer 2: Beveled Gold Outer Base
            lines.append(f'        <path d="{svc_data["sil_d"]}" fill="{PALETTE["bronze"]}" stroke="{PALETTE["mahogany"]}" stroke-width="20" stroke-linejoin="round"/>')
            # Layer 3: 3D Shadow Facets (Bevels & Central Spine)
            lines.append(f'        <path d="{svc_data["facet_d"]}" fill="url(#svcGoldFacetGrad)"/>')
            # Layer 4: Rich Mid Gold Body
            lines.append(f'        <path d="{svc_data["mid_d"]}" fill="url(#goldRimGrad)"/>')
            # Layer 5: Brilliant Canary Face
            lines.append(f'        <path d="{svc_data["face_d"]}" fill="url(#svcGoldFaceGrad)"/>')
            # Layer 6: Inset Highlights
            lines.append(f'        <path d="{svc_data["face_d"]}" fill="none" stroke="{PALETTE["canary"]}" stroke-width="4" opacity="0.6"/>')
        elif is_white:
            lines.append(f'        <path d="{svc_data["sil_d"]}" fill="#000000" stroke="#000000" stroke-width="24" stroke-linejoin="round"/>')
            lines.append(f'        <path d="{svc_data["sil_d"]}" fill="#FFFFFF"/>')
            lines.append(f'        <path d="{svc_data["facet_d"]}" fill="#E2E8F0"/>')
            lines.append(f'        <path d="{svc_data["face_d"]}" fill="#FFFFFF"/>')
        else:
            lines.append(f'        <path d="{svc_data["sil_d"]}" fill="{PALETTE["black_ink"]}" stroke="{PALETTE["black_ink"]}" stroke-width="24" stroke-linejoin="round"/>')
            lines.append(f'        <path d="{svc_data["sil_d"]}" fill="#1E293B"/>')
            lines.append(f'        <path d="{svc_data["facet_d"]}" fill="#070E1B"/>')
            lines.append(f'        <path d="{svc_data["face_d"]}" fill="#334155"/>')
        lines.append('      </g>')
        lines.append('    </g>')

        # 4. CONCENTRIC ARCHED RIBBON BANNER
        lines.append('    <!-- 4. CONCENTRIC ARCHED RIBBON BANNER -->')
        lines.append('    <g id="ribbon-banner">')
        if is_color:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="{PALETTE["bronze"]}" stroke="{PALETTE["obsidian"]}" stroke-width="16"/>')
            lines.append(f'      <path d="{ribbon_fold_left_d} {ribbon_fold_right_d}" fill="{PALETTE["mahogany"]}"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="url(#goldRimGrad)" stroke="{PALETTE["obsidian"]}" stroke-width="24" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_rim_top_d}" fill="url(#goldFacetLight)"/>')
            lines.append(f'      <path d="{ribbon_rim_bot_d}" fill="url(#goldFacetDark)"/>')
            text_fill = PALETTE["black_ink"]
            lines.append(f'      <text font-family="Plus Jakarta Sans, Montserrat, Arial, sans-serif" font-size="84" font-weight="900" letter-spacing="8" fill="{text_fill}">')
            lines.append('        <textPath href="#ribbonTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        elif is_white:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="#FFFFFF" stroke="#000000" stroke-width="20"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="#FFFFFF" stroke="#000000" stroke-width="24"/>')
            lines.append(f'      <text font-family="Plus Jakarta Sans, Montserrat, Arial, sans-serif" font-size="84" font-weight="900" letter-spacing="8" fill="#000000">')
            lines.append('        <textPath href="#ribbonTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        else:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="#1E293B" stroke="#020408" stroke-width="20"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="#0A0E17" stroke="#334155" stroke-width="24"/>')
            lines.append(f'      <text font-family="Plus Jakarta Sans, Montserrat, Arial, sans-serif" font-size="84" font-weight="900" letter-spacing="8" fill="#FFFFFF">')
            lines.append('        <textPath href="#ribbonTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        lines.append('    </g>')

        # 5. TOWERING PANDA MASCOT (HEADER CREST - TOPMOST LAYER)
        lines.append('    <!-- 5. TOWERING PANDA MASCOT (HEADER CREST) -->')
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
    print("SUCCESS: ALL PRECISION V2.1 SVC ASSETS GENERATED & RENDERED!")
    print("=" * 70)

if __name__ == "__main__":
    main()
