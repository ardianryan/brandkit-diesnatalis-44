#!/usr/bin/env python3
"""
build_svc_crest_master.py
=============================================================================
Reconstructs and vectorizes the official SVC (Smansage Volleyball Competition)
emblem into high-precision, infinitely scalable SVG and ultra-HD PNG assets.

Key Architectural Updates (Precision V3):
1. 5-Sided Heraldic Shield (Pentagonal Crest):
   - Authentic 5-sided tournament crest with mid-knuckles and pointed base
   - 3D mitered platinum/silver outer bevel & metallic gold inner bevel
   - Split midnight navy field (Left #0F172A, Right #070A12)
2. Towering Panda Mascot (Header Crest):
   - Elevated upwards so full head, ears, and glare tower proudly above shield
   - Claws securely grasping the upper golden rim cradle
   - Multi-layer vector tracing (white face, gray shadow, slate arms, gold claws/eyes)
3. Chiseled 3D Athletic Display "SVC" Typography:
   - Pure geometric vector paths (eliminating all wobbly raster-tracing artifacts)
   - V letter with angled triangular bevel caps, central spine crease, and flat chamfered base
   - S and C letters with 3D chamfered terminal wedges, extruded shadows, and inner highlights
   - Seamless metallic gold gradients and deep drop shadow
4. Mathematically Centered AVERSA Wordmark:
   - Centered with sub-pixel precision at CX=2100.0 based on true path bounds
5. Impactful Arched Ribbon Banner:
   - Concentric circular arc with bold, thick athletic championship typography
   - Text "SMANSAGE VOLLEYBALL COMPETITION" enlarged to font-size 116 with heavy stroke
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

def build_chiseled_svc_svg(mode):
    """
    Constructs smooth athletic curved 3D typography for S, V, C
    matching hand draw SVC.PNG exactly.
    Coordinate space: 820 x 460 px.
    """
    is_color = (mode == "color")
    is_white = (mode == "white")
    
    if is_color:
        face_fill = "url(#goldFace)"
        light_fill = "url(#goldLightFacet)"
        dark_fill = "url(#goldDarkFacet)"
        depth_fill = "url(#goldDepth)"
        bp_fill = "#05080E"
        bp_stroke = "#05080E"
        front_stroke = "#78350F"
        spine_light = "#FFFDF0"
        spine_gold = "#FEF08A"
        show_highlights = True
    elif is_white:
        face_fill = "#FFFFFF"
        light_fill = "#FFFFFF"
        dark_fill = "#E2E8F0"
        depth_fill = "#CBD5E1"
        bp_fill = "#FFFFFF"
        bp_stroke = "#000000"
        front_stroke = "#000000"
        spine_light = "#000000"
        spine_gold = "#000000"
        show_highlights = False
    else:
        face_fill = "#94A3B8"
        light_fill = "#CBD5E1"
        dark_fill = "#475569"
        depth_fill = "#1E293B"
        bp_fill = "#020408"
        bp_stroke = "#020408"
        front_stroke = "#334155"
        spine_light = "#F8FAFC"
        spine_gold = "#94A3B8"
        show_highlights = True
    
    lines = []
    
    # 0. OBSIDIAN BACKPLATE / SPORT CONTOUR
    lines.append('      <!-- 0. OBSIDIAN BACKPLATE SILHOUETTE -->')
    lines.append(f'      <g id="svc-backplate" stroke="{bp_stroke}" stroke-width="26" stroke-linejoin="round" stroke-linecap="round" fill="{bp_fill}">')
    lines.append('        <path d="M 175 88 C 242 88 275 120 275 178 L 208 178 C 208 148 195 138 175 138 C 148 138 132 152 132 176 C 132 210 152 225 188 240 C 238 260 272 288 272 350 C 272 415 238 420 175 420 C 112 420 80 385 80 325 L 142 325 C 142 355 155 368 175 368 C 198 368 212 355 212 330 C 212 298 190 282 154 268 C 108 248 72 220 72 165 C 72 108 115 88 175 88 Z"/>')
    lines.append('        <path d="M 80 325 L 62 335 C 62 400 105 442 175 442 C 245 442 284 395 284 340 L 272 335 C 272 385 238 420 175 420 C 112 420 80 380 80 325 Z"/>')
    lines.append('        <polygon points="270,95 330,58 375,95 402,368 436,398 402,414 368,398"/>')
    lines.append('        <polygon points="430,95 475,58 535,95 436,398 402,368 368,398"/>')
    lines.append('        <path d="M 725 148 L 668 188 C 650 160 635 142 602 142 C 560 142 542 188 542 252 C 542 316 560 362 602 362 C 635 362 650 344 668 315 L 725 355 C 698 400 660 415 602 415 C 520 415 480 345 480 252 C 480 158 520 88 602 88 C 660 88 698 105 725 148 Z"/>')
    lines.append('        <path d="M 605 155 C 575 185 565 220 565 252 C 565 285 575 320 605 350 L 590 365 C 550 330 538 290 538 252 C 538 212 550 170 590 140 Z"/>')
    lines.append('      </g>')
    
    # 1. 3D EXTRUSION DEPTH
    lines.append('      <!-- 1. 3D EXTRUSION DEPTH -->')
    lines.append('      <g id="svc-extrusion">')
    lines.append(f'        <path d="M 80 325 L 62 335 C 62 400 105 442 175 442 C 245 442 284 395 284 340 L 272 335 C 272 385 238 420 175 420 C 112 420 80 380 80 325 Z" fill="{depth_fill}"/>')
    lines.append(f'        <polygon points="80,325 80,380 62,390 62,335" fill="{dark_fill}"/>')
    lines.append(f'        <polygon points="275,178 208,178 245,148" fill="{dark_fill}"/>')
    lines.append(f'        <path d="M 605 155 C 575 185 565 220 565 252 C 565 285 575 320 605 350 L 590 365 C 550 330 538 290 538 252 C 538 212 550 170 590 140 Z" fill="{depth_fill}"/>')
    lines.append(f'        <polygon points="725,148 668,188 702,198" fill="{dark_fill}"/>')
    lines.append(f'        <polygon points="725,355 668,315 702,305" fill="{dark_fill}"/>')
    lines.append('      </g>')
    
    # 2. FRONT FACES (Smooth athletic curves & faceted prism)
    lines.append('      <!-- 2. FRONT FACES (Smooth athletic curves & faceted prism) -->')
    lines.append('      <!-- LETTER S FRONT -->')
    lines.append('      <g id="letter-S-front">')
    lines.append(f'        <path d="M 175 88 C 242 88 275 120 275 178 L 208 178 C 208 148 195 138 175 138 C 148 138 132 152 132 176 C 132 210 152 225 188 240 C 238 260 272 288 272 350 C 272 415 238 420 175 420 C 112 420 80 385 80 325 L 142 325 C 142 355 155 368 175 368 C 198 368 212 355 212 330 C 212 298 190 282 154 268 C 108 248 72 220 72 165 C 72 108 115 88 175 88 Z" fill="{face_fill}" stroke="{front_stroke}" stroke-width="2"/>')
    lines.append('      </g>')
    
    lines.append('      <!-- LETTER V FRONT -->')
    lines.append('      <g id="letter-V-front">')
    lines.append(f'        <polygon points="270,95 330,58 402,368 368,398" fill="{light_fill}"/>')
    lines.append(f'        <polygon points="475,58 535,95 436,398 402,368" fill="{dark_fill}"/>')
    lines.append(f'        <polygon points="270,95 330,58 350,95" fill="{light_fill}" stroke="{spine_gold}" stroke-width="1.5"/>')
    lines.append(f'        <polygon points="350,95 330,58 375,95" fill="{dark_fill}" stroke="{spine_gold}" stroke-width="1.5"/>')
    lines.append(f'        <polygon points="430,95 475,58 455,95" fill="{light_fill}" stroke="{spine_gold}" stroke-width="1.5"/>')
    lines.append(f'        <polygon points="455,95 475,58 535,95" fill="{dark_fill}" stroke="{spine_gold}" stroke-width="1.5"/>')
    lines.append(f'        <polygon points="368,398 402,368 436,398 402,414" fill="{dark_fill}" stroke="{spine_gold}" stroke-width="1.5"/>')
    lines.append(f'        <line x1="330" y1="58" x2="402" y2="368" stroke="{spine_light}" stroke-width="4" stroke-linecap="round"/>')
    lines.append(f'        <line x1="475" y1="58" x2="402" y2="368" stroke="{spine_gold}" stroke-width="2.5" stroke-linecap="round"/>')
    lines.append('      </g>')
    
    lines.append('      <!-- LETTER C FRONT -->')
    lines.append('      <g id="letter-C-front">')
    lines.append(f'        <path d="M 725 148 L 668 188 C 650 160 635 142 602 142 C 560 142 542 188 542 252 C 542 316 560 362 602 362 C 635 362 650 344 668 315 L 725 355 C 698 400 660 415 602 415 C 520 415 480 345 480 252 C 480 158 520 88 602 88 C 660 88 698 105 725 148 Z" fill="{face_fill}" stroke="{front_stroke}" stroke-width="2"/>')
    lines.append('      </g>')
    
    if show_highlights:
        lines.append('      <!-- 3. SPECULAR HIGHLIGHTS -->')
        lines.append('      <g id="specular-highlights" stroke="#FFFFFF" stroke-width="2.5" stroke-linecap="round" fill="none" opacity="0.85">')
        lines.append('        <path d="M 175 90 C 235 90 268 120 268 160"/>')
        lines.append('        <path d="M 602 90 C 655 90 690 105 715 145"/>')
        lines.append('      </g>')
    
    return "\n".join(lines)

def main():
    print("=" * 70)
    print("RECONSTRUCTING SVC EMBLEM (Smansage Volleyball Competition) - V5 PRECISION")
    print("=" * 70)
    
    # 1. Panda Mascot Vectors
    panda = extract_panda_vector_layers()
    
    # 2. Master AVERSA Vectors
    aversa_letters, aversa_highlights = get_aversa_vector()
    
    # =============================================================
    # Geometry Layout Calculations (Canvas 4200 x 4200 px)
    # =============================================================
    
    # -------------------------------------------------------------
    # 1. 5-Sided Heraldic Pentagonal Shield Geometry
    # -------------------------------------------------------------
    shield_outer_d = "M 650 1050 L 1550 1050 L 2100 1340 L 2650 1050 L 3550 1050 L 3080 2850 L 2100 3780 L 1120 2850 Z"
    shield_silver_rim_d = (
        "M 650 1050 L 1550 1050 L 2100 1340 L 2650 1050 L 3550 1050 L 3080 2850 L 2100 3780 L 1120 2850 Z "
        "M 760 1150 L 1195 2815 L 2100 3650 L 3005 2815 L 3440 1150 L 2620 1150 L 2100 1420 L 1580 1150 Z"
    )
    shield_gold_rim_d = (
        "M 760 1150 L 1580 1150 L 2100 1420 L 2620 1150 L 3440 1150 L 3005 2815 L 2100 3650 L 1195 2815 Z "
        "M 860 1240 L 1260 2780 L 2100 3530 L 2940 2780 L 3340 1240 L 2590 1240 L 2100 1490 L 1610 1240 Z"
    )
    shield_navy_left_d = "M 860 1240 L 1610 1240 L 2100 1490 L 2100 3530 L 1260 2780 Z"
    shield_navy_right_d = "M 2100 1490 L 2590 1240 L 3340 1240 L 2940 2780 L 2100 3530 Z"
    
    # -------------------------------------------------------------
    # 2. Concentric Arched Emblem Banner (No Tails - Exact Hand Draw Matching)
    # -------------------------------------------------------------
    # Concentric circular arc with bold, thick athletic championship typography
    # Center of arc: CX = 2100, CY = 6500
    emblem_body_d = "M 621 3328 A 3500 3500 0 0 1 3579 3328 L 3461 3582 A 3220 3220 0 0 0 739 3582 Z"
    emblem_rim_top_d = "M 621 3328 A 3500 3500 0 0 1 3579 3328 L 3568 3362 A 3464 3464 0 0 0 632 3362 Z"
    emblem_rim_bot_d = "M 728 3548 A 3256 3256 0 0 1 3472 3548 L 3461 3582 A 3220 3220 0 0 0 739 3582 Z"
    
    # Baseline text arc: R = 3340 (centered vertically between 3500 and 3220)
    # Text covers the arched emblem completely from end to end
    emblem_text_path_d = "M 540 3510 A 3340 3340 0 0 1 3660 3510"
    
    # -------------------------------------------------------------
    # 3. Towering Panda Mascot Placement
    # -------------------------------------------------------------
    p_sc = 2200.0 / panda["width"]
    p_tx = CX - (panda["width"] * p_sc) / 2.0
    p_ty = 180.0
    
    # -------------------------------------------------------------
    # 4. Optically Centered AVERSA Wordmark Placement
    # -------------------------------------------------------------
    av_sc = 0.38
    av_center_x = 1587.30 - 18.0
    av_tx = CX - av_center_x * av_sc
    av_ty = 1460.0
    
    # -------------------------------------------------------------
    # 5. Smooth Athletic 3D SVC Typography Placement
    # -------------------------------------------------------------
    # Coordinates in 820 x 460 space scaled by 2.22
    svc_sc = 2.22
    svc_box_cx = 410.0
    svc_tx = CX - svc_box_cx * svc_sc
    svc_ty = 1800.0
    
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

    <linearGradient id="goldFace" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFAD2"/>
      <stop offset="20%" stop-color="#FED75B"/>
      <stop offset="55%" stop-color="#F59E0B"/>
      <stop offset="100%" stop-color="#D97706"/>
    </linearGradient>

    <linearGradient id="goldLightFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFDF0"/>
      <stop offset="40%" stop-color="#FEF08A"/>
      <stop offset="100%" stop-color="#FBBF24"/>
    </linearGradient>

    <linearGradient id="goldDarkFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#D97706"/>
      <stop offset="50%" stop-color="#B45309"/>
      <stop offset="100%" stop-color="#78350F"/>
    </linearGradient>

    <linearGradient id="goldDepth" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#B45309"/>
      <stop offset="60%" stop-color="#78350F"/>
      <stop offset="100%" stop-color="#3B1502"/>
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

    <filter id="masterDropGlow" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="28" stdDeviation="24" flood-color="#020408" flood-opacity="0.95"/>
    </filter>

    <!-- Concentric Arched Text Path for Emblem Banner -->
    <path id="emblemTextArc" d="{emblem_text_path_d}"/>
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

        # 3. ARCHED EMBLEM BANNER (COVERED FULLY BY TEXT)
        lines.append('    <!-- 3. ARCHED EMBLEM BANNER (COVERED FULLY BY TEXT) -->')
        banner_filter = ' filter="url(#masterDropGlow)"' if is_color else ''
        lines.append(f'    <g id="arched-emblem-banner"{banner_filter}>')
        if is_color:
            lines.append(f'      <path d="{emblem_body_d}" fill="url(#goldRimGrad)" stroke="{PALETTE["black_ink"]}" stroke-width="32" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{emblem_rim_top_d}" fill="url(#goldLightFacet)"/>')
            lines.append(f'      <path d="{emblem_rim_bot_d}" fill="url(#goldDarkFacet)"/>')
            text_fill = PALETTE["black_ink"]
            lines.append(f'      <text font-family="\'Plus Jakarta Sans\', Montserrat, \'Arial Black\', sans-serif" font-size="134" font-weight="900" letter-spacing="2.2" fill="{text_fill}" stroke="{text_fill}" stroke-width="5" stroke-linejoin="round">')
            lines.append('        <textPath href="#emblemTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        elif is_white:
            lines.append(f'      <path d="{emblem_body_d}" fill="#FFFFFF" stroke="#000000" stroke-width="32" stroke-linejoin="round"/>')
            lines.append('      <text font-family="\'Plus Jakarta Sans\', Montserrat, \'Arial Black\', sans-serif" font-size="134" font-weight="900" letter-spacing="2.2" fill="#000000" stroke="#000000" stroke-width="5" stroke-linejoin="round">')
            lines.append('        <textPath href="#emblemTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        else:
            lines.append(f'      <path d="{emblem_body_d}" fill="#0A0E17" stroke="#334155" stroke-width="32" stroke-linejoin="round"/>')
            lines.append('      <text font-family="\'Plus Jakarta Sans\', Montserrat, \'Arial Black\', sans-serif" font-size="134" font-weight="900" letter-spacing="2.2" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round">')
            lines.append('        <textPath href="#emblemTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        lines.append('    </g>')

        # 4. SMOOTH ATHLETIC 3D "SVC" TYPOGRAPHY
        lines.append('    <!-- 4. SMOOTH ATHLETIC 3D "SVC" TYPOGRAPHY -->')
        filter_attr = ' filter="url(#masterDropGlow)"' if is_color else ''
        lines.append(f'    <g id="svc-letters" transform="translate({svc_tx:.2f}, {svc_ty:.2f}) scale({svc_sc:.4f})"{filter_attr}>')
        lines.append(build_chiseled_svc_svg(mode))
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
    print("SUCCESS: ALL PRECISION V3 SVC ASSETS GENERATED & RENDERED!")
    print("=" * 70)

if __name__ == "__main__":
    main()
