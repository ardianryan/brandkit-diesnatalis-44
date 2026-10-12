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
    Constructs 100% geometric, razor-sharp 3D faceted athletic display typography
    for S, V, C matching the design anatomy of hand draw SVC.PNG.
    Canvas bounds: 1400 x 650 px.
    """
    is_color = (mode == "color")
    is_white = (mode == "white")
    
    # 3D Extrusion offsets
    edx, edy = 26, 32

    # Fills & Strokes
    if is_color:
        face_fill = "url(#goldFace)"
        light_fill = "url(#goldLightFacet)"
        dark_fill = "url(#goldDarkFacet)"
        depth_fill = "url(#goldDepth)"
        cap_fill = "url(#goldCap)"
        bp_fill = "#05080E"
        bp_stroke = "#05080E"
        front_stroke = "#78350F"
        spine_stroke = "#FFFFFF"
        show_highlights = True
    elif is_white:
        face_fill = "#FFFFFF"
        light_fill = "#FFFFFF"
        dark_fill = "#F1F5F9"
        depth_fill = "#E2E8F0"
        cap_fill = "#FFFFFF"
        bp_fill = "#FFFFFF"
        bp_stroke = "#000000"
        front_stroke = "#000000"
        spine_stroke = "#000000"
        show_highlights = False
    else:
        face_fill = "#94A3B8"
        light_fill = "#CBD5E1"
        dark_fill = "#475569"
        depth_fill = "#1E293B"
        cap_fill = "#64748B"
        bp_fill = "#020408"
        bp_stroke = "#020408"
        front_stroke = "#334155"
        spine_stroke = "#E2E8F0"
        show_highlights = True
    
    lines = []
    
    # 0. OBSIDIAN BACKPLATE / HEAVY SPORT CONTOUR (42px)
    lines.append('      <!-- 0. HEAVY SPORT OUTLINE BACKPLATE -->')
    lines.append(f'      <g id="svc-backplate" stroke="{bp_stroke}" stroke-width="42" stroke-linejoin="round" stroke-linecap="round" fill="{bp_fill}">')
    # S Outline (Shadow + Normal)
    lines.append(f'        <path d="M 235 110 L 390 110 L 440 155 L 440 230 L 395 265 L 340 265 L 340 215 L 255 215 L 255 240 L 390 300 L 440 345 L 440 470 L 390 520 L 210 520 L 155 470 L 155 390 L 245 390 L 245 435 L 335 435 L 350 415 L 350 375 L 225 320 L 155 270 L 155 160 Z" transform="translate({edx},{edy})"/>')
    lines.append('        <path d="M 235 110 L 390 110 L 440 155 L 440 230 L 395 265 L 340 265 L 340 215 L 255 215 L 255 240 L 390 300 L 440 345 L 440 470 L 390 520 L 210 520 L 155 470 L 155 390 L 245 390 L 245 435 L 335 435 L 350 415 L 350 375 L 225 320 L 155 270 L 155 160 Z"/>')
    # V Outline (Shadow + Normal)
    lines.append(f'        <path d="M 525 95 L 595 55 L 670 100 L 700 280 L 730 100 L 805 55 L 875 95 L 755 530 L 645 530 Z" transform="translate({edx},{edy})"/>')
    lines.append('        <path d="M 525 95 L 595 55 L 670 100 L 700 280 L 730 100 L 805 55 L 875 95 L 755 530 L 645 530 Z"/>')
    # C Outline (Shadow + Normal)
    lines.append(f'        <path d="M 1210 230 L 1210 160 L 1165 110 L 1010 110 L 960 160 L 960 470 L 1010 520 L 1175 520 L 1220 470 L 1220 395 L 1125 395 L 1125 435 L 1055 435 L 1045 415 L 1045 215 L 1055 195 L 1125 195 L 1125 230 Z" transform="translate({edx},{edy})"/>')
    lines.append('        <path d="M 1210 230 L 1210 160 L 1165 110 L 1010 110 L 960 160 L 960 470 L 1010 520 L 1175 520 L 1220 470 L 1220 395 L 1125 395 L 1125 435 L 1055 435 L 1045 415 L 1045 215 L 1055 195 L 1125 195 L 1125 230 Z"/>')
    lines.append('      </g>')

    # 1. 3D EXTRUSION DEPTH FACETS
    lines.append('      <!-- 1. 3D EXTRUSION DEPTH FACETS -->')
    lines.append(f'      <g id="svc-extrusion" fill="{depth_fill}" stroke="{front_stroke}" stroke-width="4">')
    # S Depth Walls
    lines.append('        <polygon points="390,110  416,142  466,187  440,155"/>')
    lines.append('        <polygon points="440,155  466,187  466,262  440,230"/>')
    lines.append('        <polygon points="440,230  466,262  421,297  395,265"/>')
    lines.append('        <polygon points="440,345  466,377  466,502  440,470"/>')
    lines.append('        <polygon points="440,470  466,502  416,552  390,520"/>')
    lines.append('        <polygon points="390,520  416,552  236,552  210,520"/>')
    lines.append('        <polygon points="210,520  236,552  181,502  155,470"/>')
    lines.append('        <polygon points="245,390  271,422  271,467  245,435"/>')
    lines.append('        <polygon points="335,435  361,467  376,447  350,415"/>')
    lines.append('        <polygon points="350,375  376,407  251,352  225,320"/>')
    # V Depth Walls
    lines.append('        <polygon points="875,95   901,127  781,562  755,530"/>')
    lines.append('        <polygon points="755,530  781,562  671,562  645,530"/>')
    lines.append('        <polygon points="645,530  671,562  655,545  645,530"/>')
    # C Depth Walls
    lines.append('        <polygon points="1210,160 1236,192 1236,262 1210,230"/>')
    lines.append('        <polygon points="1220,395 1246,427 1246,502 1220,470"/>')
    lines.append('        <polygon points="1220,470 1246,502 1201,552 1175,520"/>')
    lines.append('        <polygon points="1175,520 1201,552 1036,552 1010,520"/>')
    lines.append('        <polygon points="1010,520 1036,552  986,502  960,470"/>')
    lines.append('        <polygon points="1125,395 1151,427 1151,467 1125,435"/>')
    lines.append('        <polygon points="1125,195 1151,227 1151,262 1125,230"/>')
    lines.append('      </g>')

    # 2. FRONT FACES & CHISEL FACETS
    lines.append('      <!-- 2. FRONT FACES & CHISEL FACETS -->')
    # LETTER S FRONT
    lines.append('      <g id="letter-S-front">')
    lines.append(f'        <path d="M 235 110 L 390 110 L 440 155 L 440 230 L 395 265 L 340 265 L 340 215 L 255 215 L 255 240 L 390 300 L 440 345 L 440 470 L 390 520 L 210 520 L 155 470 L 155 390 L 245 390 L 245 435 L 335 435 L 350 415 L 350 375 L 225 320 L 155 270 L 155 160 Z" fill="{face_fill}" stroke="{front_stroke}" stroke-width="4"/>')
    lines.append(f'        <polygon points="235,110 390,110 365,140 235,140" fill="{light_fill}"/>')
    lines.append(f'        <polygon points="390,110 440,155 410,165 365,140" fill="{light_fill}"/>')
    lines.append(f'        <polygon points="210,520 390,520 365,490 235,490" fill="{dark_fill}"/>')
    lines.append(f'        <polygon points="155,470 210,520 235,490 185,450" fill="{dark_fill}"/>')
    lines.append(f'        <polygon points="155,160 235,110 235,140 180,180" fill="{light_fill}"/>')
    lines.append('      </g>')

    # LETTER V FRONT (HERO CHISELED PRISM)
    lines.append('      <g id="letter-V-front">')
    lines.append(f'        <polygon points="525,95 595,55 690,495 645,530" fill="{light_fill}"/>')
    lines.append(f'        <polygon points="595,55 670,100 700,280 690,495" fill="{dark_fill}"/>')
    lines.append(f'        <polygon points="700,280 730,100 805,55 710,495" fill="{light_fill}"/>')
    lines.append(f'        <polygon points="805,55 875,95 755,530 710,495" fill="{dark_fill}"/>')
    lines.append(f'        <polygon points="525,95 595,55 670,100" fill="{cap_fill}" stroke="{spine_stroke}" stroke-width="2.5"/>')
    lines.append(f'        <polygon points="730,100 805,55 875,95" fill="{cap_fill}" stroke="{spine_stroke}" stroke-width="2.5"/>')
    lines.append(f'        <polygon points="645,530 690,495 710,495 755,530" fill="{dark_fill}" stroke="{spine_stroke}" stroke-width="2.5"/>')
    lines.append(f'        <line x1="595" y1="55" x2="690" y2="495" stroke="{spine_stroke}" stroke-width="5" stroke-linecap="round"/>')
    lines.append(f'        <line x1="805" y1="55" x2="710" y2="495" stroke="{spine_stroke}" stroke-width="5" stroke-linecap="round"/>')
    lines.append('      </g>')

    # LETTER C FRONT
    lines.append('      <g id="letter-C-front">')
    lines.append(f'        <path d="M 1210 230 L 1210 160 L 1165 110 L 1010 110 L 960 160 L 960 470 L 1010 520 L 1175 520 L 1220 470 L 1220 395 L 1125 395 L 1125 435 L 1055 435 L 1045 415 L 1045 215 L 1055 195 L 1125 195 L 1125 230 Z" fill="{face_fill}" stroke="{front_stroke}" stroke-width="4"/>')
    lines.append(f'        <polygon points="1010,110 1165,110 1135,140 1030,140" fill="{light_fill}"/>')
    lines.append(f'        <polygon points="960,160 1010,110 1030,140 985,175" fill="{light_fill}"/>')
    lines.append(f'        <polygon points="1010,520 1175,520 1145,490 1035,490" fill="{dark_fill}"/>')
    lines.append(f'        <polygon points="960,470 1010,520 1035,490 985,455" fill="{dark_fill}"/>')
    lines.append(f'        <polygon points="1175,520 1220,470 1190,450 1145,490" fill="{dark_fill}"/>')
    lines.append('      </g>')

    # 3. WHITE SPECULAR LIGHT ACCENTS
    if show_highlights:
        lines.append('      <!-- 3. SPECULAR LIGHT ACCENTS -->')
        lines.append('      <g id="specular-highlights" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" opacity="0.9">')
        lines.append('        <line x1="240" y1="113" x2="385" y2="113"/>')
        lines.append('        <line x1="158" y1="165" x2="158" y2="265"/>')
        lines.append('        <line x1="250" y1="394" x2="250" y2="430"/>')
        lines.append('        <line x1="1015" y1="113" x2="1160" y2="113"/>')
        lines.append('        <line x1="964" y1="165" x2="964" y2="465"/>')
        lines.append('        <line x1="1049" y1="200" x2="1049" y2="420"/>')
        lines.append('      </g>')
    
    return "\n".join(lines)

def main():
    print("=" * 70)
    print("RECONSTRUCTING SVC EMBLEM (Smansage Volleyball Competition) - V4")
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
    # 2. Concentric Arched Ribbon Banner Geometry (Span +/- 21.5 deg, R_top=3890, R_bot=3630)
    # -------------------------------------------------------------
    ribbon_body_d = "M 674 3381 A 3890 3890 0 0 1 3526 3381 L 3431 3623 A 3630 3630 0 0 0 769 3623 Z"
    ribbon_rim_top_d = "M 674 3381 A 3890 3890 0 0 1 3526 3381 L 3515 3418 A 3855 3855 0 0 0 685 3418 Z"
    ribbon_rim_bot_d = "M 758 3585 A 3665 3665 0 0 1 3442 3585 L 3431 3623 A 3630 3630 0 0 0 769 3623 Z"
    
    # Side fold ribbon tails:
    ribbon_tail_left_d = "M 674 3381 L 390 3445 L 490 3575 L 390 3705 L 769 3623 Z"
    ribbon_fold_left_d = "M 674 3381 L 769 3623 L 655 3525 Z"
    ribbon_tail_right_d = "M 3526 3381 L 3810 3445 L 3710 3575 L 3810 3705 L 3431 3623 Z"
    ribbon_fold_right_d = "M 3526 3381 L 3431 3623 L 3545 3525 Z"
    
    # Baseline text arc: R=3760 (perfect vertical midpoint between 3890 & 3630)
    ribbon_text_path_d = "M 572 3563 A 3760 3760 0 0 1 3628 3563"
    
    # -------------------------------------------------------------
    # 3. Towering Panda Mascot Placement
    # -------------------------------------------------------------
    p_sc = 2200.0 / panda["width"]
    p_tx = CX - (panda["width"] * p_sc) / 2.0
    p_ty = 180.0
    
    # -------------------------------------------------------------
    # 4. Optically Centered AVERSA Wordmark Placement
    # -------------------------------------------------------------
    # In aversa-standalone-color.svg, bounds: X=57.37..3117.24 (mid=1587.30)
    # Optical center adjustment: shifting +18 px aligns 3 letters AVE and 3 letters RSA exactly at CX=2100.
    av_sc = 0.39
    av_center_x = 1587.30 - 18.0
    av_tx = CX - av_center_x * av_sc
    av_ty = 1485.0  # Clear space above SVC!
    
    # -------------------------------------------------------------
    # 5. Chiseled 3D Faceted SVC Placement
    # -------------------------------------------------------------
    # Using the perfect 1400 x 650 athletic geometry
    svc_sc = 1.72
    svc_box_cx = 700.0
    svc_tx = CX - svc_box_cx * svc_sc
    svc_ty = 1940.0
    
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
      <stop offset="0%" stop-color="#FFF8B0"/>
      <stop offset="20%" stop-color="#FED049"/>
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
      <stop offset="0%" stop-color="#92400E"/>
      <stop offset="50%" stop-color="#78350F"/>
      <stop offset="100%" stop-color="#451A03"/>
    </linearGradient>

    <linearGradient id="goldCap" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FEF08A"/>
      <stop offset="50%" stop-color="#FDE047"/>
      <stop offset="100%" stop-color="#F59E0B"/>
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
      <feDropShadow dx="0" dy="24" stdDeviation="20" flood-color="#020408" flood-opacity="0.95"/>
    </filter>

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

        # 3. CHISELED 3D FACETED "SVC" TYPOGRAPHY
        lines.append('    <!-- 3. CHISELED 3D FACETED "SVC" TYPOGRAPHY -->')
        filter_attr = ' filter="url(#masterDropGlow)"' if is_color else ''
        lines.append(f'    <g id="svc-letters" transform="translate({svc_tx:.2f}, {svc_ty:.2f}) scale({svc_sc:.4f})"{filter_attr}>')
        lines.append(build_chiseled_svc_svg(mode))
        lines.append('    </g>')

        # 4. CONCENTRIC ARCHED RIBBON BANNER (EXTRA BOLD & IMPACTFUL)
        lines.append('    <!-- 4. CONCENTRIC ARCHED RIBBON BANNER -->')
        lines.append('    <g id="ribbon-banner">')
        if is_color:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="{PALETTE["bronze"]}" stroke="{PALETTE["obsidian"]}" stroke-width="18"/>')
            lines.append(f'      <path d="{ribbon_fold_left_d} {ribbon_fold_right_d}" fill="{PALETTE["mahogany"]}"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="url(#goldRimGrad)" stroke="{PALETTE["obsidian"]}" stroke-width="28" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_rim_top_d}" fill="url(#goldLightFacet)"/>')
            lines.append(f'      <path d="{ribbon_rim_bot_d}" fill="url(#goldDarkFacet)"/>')
            text_fill = PALETTE["black_ink"]
            lines.append(f'      <text font-family="Plus Jakarta Sans, Montserrat, Arial, sans-serif" font-size="116" font-weight="900" letter-spacing="2.6" fill="{text_fill}" stroke="{text_fill}" stroke-width="4">')
            lines.append('        <textPath href="#ribbonTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        elif is_white:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="#FFFFFF" stroke="#000000" stroke-width="20"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="#FFFFFF" stroke="#000000" stroke-width="28"/>')
            lines.append(f'      <text font-family="Plus Jakarta Sans, Montserrat, Arial, sans-serif" font-size="116" font-weight="900" letter-spacing="2.6" fill="#000000" stroke="#000000" stroke-width="4">')
            lines.append('        <textPath href="#ribbonTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        else:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="#1E293B" stroke="#020408" stroke-width="20"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="#0A0E17" stroke="#334155" stroke-width="28"/>')
            lines.append(f'      <text font-family="Plus Jakarta Sans, Montserrat, Arial, sans-serif" font-size="116" font-weight="900" letter-spacing="2.6" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="4">')
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
    print("SUCCESS: ALL PRECISION V3 SVC ASSETS GENERATED & RENDERED!")
    print("=" * 70)

if __name__ == "__main__":
    main()
