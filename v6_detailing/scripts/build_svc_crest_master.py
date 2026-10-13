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
    
    # Precision contour polygon clipping: hugs paws and claws without clipping inner paws
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
        [395, 510], # paw inner curve
        [380, 480], # paw top edge
        [350, 450], # outer arm tuck
        [350, 419], # meets chevron top
        [400, 449], # follows chevron top
        [460, 485], # chevron top center apex
        [520, 449], # follows chevron top
        [570, 419], # meets chevron top
        [570, 450], # right outer arm tuck
        [540, 480], # right paw top edge
        [525, 510], # right paw inner curve
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
        poly_stroke = ""
        show_highlights = True
    elif is_white:
        face_fill = "#FFFFFF"
        light_fill = "#FFFFFF"
        dark_fill = "#E2E8F0"
        depth_fill = "#CBD5E1"
        poly_stroke = ' stroke="#000000" stroke-width="3" stroke-linejoin="round"'
        show_highlights = False
    else:
        face_fill = "#94A3B8"
        light_fill = "#CBD5E1"
        dark_fill = "#475569"
        depth_fill = "#1E293B"
        poly_stroke = ""
        show_highlights = True
    
    lines = []
    
    # 1. LETTER S (Fully Beveled Prism matching hand draw SVC.PNG)
    lines.append('      <!-- 1. LETTER S (FULLY BEVELED PRISM) -->')
    lines.append('      <g id="letter-S">')
    # S 3D Depth Extrusion (Bottom belly drop shadow):
    lines.append(f'        <path d="M 80 325 L 64 345 C 50 395 90 438 175 438 C 235 438 272 405 272 355 L 272 350 C 272 415 238 420 175 420 C 112 420 80 385 80 325 Z" fill="{depth_fill}"{poly_stroke}/>')
    lines.append(f'        <polygon points="80,325 64,345 126,345 145,325" fill="{depth_fill}"{poly_stroke}/>')
    
    # Top terminal triangular bevel facet (cuts inward to central ridge):
    lines.append(f'        <polygon points="275,178 208,178 241,155" fill="{dark_fill}"{poly_stroke}/>')
    # Bottom terminal triangular bevel facet:
    lines.append(f'        <polygon points="80,325 145,325 112,350" fill="{dark_fill}"{poly_stroke}/>')
    
    # S Facet 1 (Outer / Upper Light Gold Facet):
    lines.append(f'''        <path d="M 241 155 
                 C 241 118 215 88 175 88 
                 C 115 88 72 108 72 165 
                 C 72 220 108 248 154 268 
                 C 190 282 212 298 212 330 
                 C 212 355 198 368 175 368 
                 C 155 368 145 355 145 325 
                 L 112 350 
                 C 112 370 135 394 175 394 
                 C 220 394 242 370 242 350 
                 C 242 315 225 279 168 252 
                 C 125 232 102 215 102 176 
                 C 102 135 125 113 175 113 
                 C 215 113 241 125 241 155 Z" fill="{light_fill}"{poly_stroke}/>''')
                 
    # S Facet 2 (Inner / Lower Shaded Amber Facet):
    lines.append(f'''        <path d="M 275 178 
                 L 241 155 
                 C 241 125 215 113 175 113 
                 C 125 113 102 135 102 176 
                 C 102 215 125 232 168 252 
                 C 225 279 242 315 242 350 
                 C 242 370 220 394 175 394 
                 C 135 394 112 370 112 350 
                 L 80 325 
                 C 80 385 112 420 175 420 
                 C 238 420 272 415 272 350 
                 C 272 288 238 260 188 240 
                 C 152 225 132 210 132 176 
                 C 132 152 148 138 175 138 
                 C 195 138 208 148 208 178 
                 L 275 178 Z" fill="{dark_fill}"{poly_stroke}/>''')
    lines.append('      </g>')
    
    # 2. LETTER C (Fully Beveled Prism matching hand draw SVC.PNG)
    lines.append('      <!-- 2. LETTER C (FULLY BEVELED PRISM) -->')
    lines.append('      <g id="letter-C">')
    # 3D Depth Extrusions:
    lines.append(f'        <polygon points="715,152 665,188 642,206 692,170" fill="{depth_fill}"{poly_stroke}/>')
    lines.append(f'        <polygon points="715,352 665,315 642,297 692,334" fill="{depth_fill}"{poly_stroke}/>')
    lines.append(f'        <path d="M 665 188 C 630 148 595 148 560 148 C 515 148 498 188 498 252 C 498 316 515 355 560 355 C 595 355 630 355 665 315 L 642 297 C 615 335 585 335 550 335 C 505 335 486 296 486 252 C 486 208 505 168 550 168 C 585 168 615 168 642 206 Z" fill="{depth_fill}"{poly_stroke}/>')

    # Terminal Triangular Bevel Facets:
    lines.append(f'        <polygon points="715,152 665,188 690,170" fill="{dark_fill}"{poly_stroke}/>')
    lines.append(f'        <polygon points="715,352 665,315 690,334" fill="{dark_fill}"{poly_stroke}/>')

    # C Facet 1 (Outer Light Gold Facet):
    lines.append(f'''        <path d="M 690 170 
                 L 715 152 
                 C 655 88 610 88 560 88 
                 C 475 88 440 158 440 252 
                 C 440 345 475 415 560 415 
                 C 610 415 655 415 715 352 
                 L 690 334 
                 C 645 385 605 385 560 385 
                 C 495 385 469 330 469 252 
                 C 469 174 495 118 560 118 
                 C 605 118 645 118 690 170 Z" fill="{light_fill}"{poly_stroke}/>''')

    # C Facet 2 (Inner Shaded Amber Facet):
    lines.append(f'''        <path d="M 690 170 
                 L 665 188 
                 C 630 148 595 148 560 148 
                 C 515 148 498 188 498 252 
                 C 498 316 515 355 560 355 
                 C 595 355 630 355 665 315 
                 L 690 334 
                 C 645 385 605 385 560 385 
                 C 495 385 469 330 469 252 
                 C 469 174 495 118 560 118 
                 C 605 118 645 118 690 170 Z" fill="{dark_fill}"{poly_stroke}/>''')
    lines.append('      </g>')

    # 3. LETTER V (Pure Faceted Prism - Flat Tops, Flat Bottom, Downward Facets)
    lines.append('      <!-- 3. LETTER V (PURE FACETED PRISM MATCHING HAND DRAW) -->')
    lines.append('      <g id="letter-V">')
    # Inner V Cavity (Seamless unified bright gold cavity)
    lines.append(f'        <polygon points="352,80 316,114 376,380 428,380 488,114 452,80 402,310" fill="{light_fill}"{poly_stroke}/>')
    # Left Leg Outer Face
    lines.append(f'        <polygon points="272,80 316,114 376,380 366,408" fill="{face_fill}"{poly_stroke}/>')
    # Left Leg Top Bevel Facet (Downward Triangle)
    lines.append(f'        <polygon points="272,80 352,80 316,114" fill="{dark_fill}"{poly_stroke}/>')
    # Right Leg Outer Extrusion Facet
    lines.append(f'        <polygon points="532,80 488,114 428,380 438,408" fill="{depth_fill}"{poly_stroke}/>')
    # Right Leg Top Bevel Facet (Downward Triangle)
    lines.append(f'        <polygon points="452,80 532,80 488,114" fill="{dark_fill}"{poly_stroke}/>')
    # Bottom Trapezoid Bevel Facet
    lines.append(f'        <polygon points="376,380 428,380 438,408 366,408" fill="{dark_fill}"{poly_stroke}/>')
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
    # Solid shield foundation (eliminates any holes or transparency under panda)
    shield_solid_base_d = "M 650 1050 L 3550 1050 L 3080 2850 L 2100 3780 L 1120 2850 Z"
    # Throat plate behind panda chin (extends well into chest/chin)
    shield_throat_left_d = "M 1200 800 L 2100 800 L 2100 1340 Z"
    shield_throat_right_d = "M 2100 800 L 3000 800 L 2100 1340 Z"
    
    # Outer Shield boundary:
    # Chevron enters under panda paws as a straight continuous diagonal line
    shield_outer_d = (
        "M 650 1050 L 1200 1050 L 1200 800 L 2100 1340 L 3000 800 L 3000 1050 L 3550 1050 "
        "L 3080 2850 L 2100 3780 L 1120 2850 Z"
    )
    
    # Silver Rim (Outer metallic platinum band):
    shield_silver_rim_d = (
        "M 650 1050 L 1200 1050 L 1200 800 L 2100 1340 L 3000 800 L 3000 1050 L 3550 1050 "
        "L 3080 2850 L 2100 3780 L 1120 2850 Z "
        "M 760 1150 L 1195 2815 L 2100 3650 L 3005 2815 L 3440 1150 L 3000 1150 "
        "L 3000 880 L 2100 1420 L 1200 880 L 1200 1150 Z"
    )
    
    # Gold Rim (Inner heavy gold metallic band):
    shield_gold_rim_d = (
        "M 760 1150 L 1200 1150 L 1200 880 L 2100 1420 L 3000 880 L 3000 1150 L 3440 1150 "
        "L 3005 2815 L 2100 3650 L 1195 2815 Z "
        "M 860 1240 L 1260 2780 L 2100 3530 L 2940 2780 L 3340 1240 L 3000 1240 "
        "L 3000 950 L 2100 1490 L 1200 950 L 1200 1240 Z"
    )
    
    # Midnight Navy Field:
    shield_navy_left_d = "M 860 1240 L 1200 1240 L 1200 950 L 2100 1490 L 2100 3530 L 1260 2780 Z"
    shield_navy_right_d = "M 2100 1490 L 3000 950 L 3000 1240 L 3340 1240 L 2940 2780 L 2100 3530 Z"
    
    # -------------------------------------------------------------
    # 2. Championship Tournament Ribbon Banner (Form from REFFERENCE.jpeg, Color from hand draw)
    # -------------------------------------------------------------
    # Center of arc: CX = 2100, CY = 6700
    # Main Arch:
    # R_top = 3980 (Peak Y = 6700 - 3980 = 2720, sits right below SVC tip at Y ~ 2680)
    # R_bot = 3680 (Peak Y = 6700 - 3680 = 3020) -> Thickness = 300 px
    # Span angle +/- 22 degrees (0.3839 rad)
    ribbon_body_d = "M 609 3010 A 3980 3980 0 0 1 3591 3010 L 3478 3288 A 3680 3680 0 0 0 722 3288 Z"
    ribbon_rim_top_d = "M 609 3010 A 3980 3980 0 0 1 3591 3010 L 3580 3045 A 3945 3945 0 0 0 620 3045 Z"
    ribbon_rim_bot_d = "M 711 3253 A 3715 3715 0 0 1 3489 3253 L 3478 3288 A 3680 3680 0 0 0 722 3288 Z"

    # Swallowtail Wings tucking deeply BEHIND main body (no visible seams or slits):
    ribbon_tail_left_d = "M 680 3040 L 360 3140 L 475 3260 L 350 3390 L 760 3270 Z"
    ribbon_tail_left_bevel_d = "M 680 3040 L 360 3140 L 475 3260 L 460 3240 L 375 3155 L 680 3060 Z"
    ribbon_fold_left_d = "M 625 3040 L 722 3288 L 635 3230 Z"

    ribbon_tail_right_d = "M 3520 3040 L 3840 3140 L 3725 3260 L 3850 3390 L 3440 3270 Z"
    ribbon_tail_right_bevel_d = "M 3520 3040 L 3840 3140 L 3725 3260 L 3740 3240 L 3825 3155 L 3520 3060 Z"
    ribbon_fold_right_d = "M 3575 3040 L 3478 3288 L 3565 3230 Z"

    # Text Arc: R = 3805 (perfect vertical center inside main arch body without overlapping folds)
    ribbon_text_path_d = "M 810 3125 A 3805 3805 0 0 1 3390 3125"
    
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
    # 5. Smooth Athletic 3D SVC Typography Placement (hand draw SVC.PNG)
    # -------------------------------------------------------------
    # Coordinates in 820 x 460 space scaled by 2.22
    svc_sc = 2.22
    # Exact optical midpoint: gap(S, left_rim) == gap(C, right_rim)
    svc_box_cx = 394.0
    svc_tx = CX - svc_box_cx * svc_sc
    svc_ty = 1760.0
    
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

    <!-- Concentric Arched Text Path for Tournament Ribbon -->
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
            lines.append(f'      <path d="{shield_solid_base_d}" fill="{PALETTE["obsidian"]}"/>')
            lines.append(f'      <path d="{shield_throat_left_d}" fill="url(#navyLeftGrad)"/>')
            lines.append(f'      <path d="{shield_throat_right_d}" fill="url(#navyRightGrad)"/>')
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
            lines.append(f'      <path d="{shield_navy_left_d} {shield_navy_right_d} {shield_throat_left_d} {shield_throat_right_d}" fill="#FFFFFF" stroke="#000000" stroke-width="16"/>')
        else:
            lines.append(f'      <path d="{shield_solid_base_d}" fill="{PALETTE["obsidian"]}"/>')
            lines.append(f'      <path d="{shield_throat_left_d} {shield_throat_right_d}" fill="#0A0E17"/>')
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
        banner_filter = ' filter="url(#masterDropGlow)"' if is_color else ''
        lines.append(f'    <g id="tournament-ribbon-banner"{banner_filter}>')
        if is_color:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="url(#goldRimGrad)" stroke="{PALETTE["black_ink"]}" stroke-width="26" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_tail_left_bevel_d} {ribbon_tail_right_bevel_d}" fill="url(#goldLightFacet)"/>')
            lines.append(f'      <path d="{ribbon_fold_left_d} {ribbon_fold_right_d}" fill="{PALETTE["mahogany"]}" stroke="{PALETTE["black_ink"]}" stroke-width="14" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="url(#goldRimGrad)" stroke="{PALETTE["black_ink"]}" stroke-width="32" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_rim_top_d}" fill="url(#goldLightFacet)"/>')
            lines.append(f'      <path d="{ribbon_rim_bot_d}" fill="url(#goldDarkFacet)"/>')
            text_fill = PALETTE["black_ink"]
            lines.append(f'      <text font-family="\'Plus Jakarta Sans\', Montserrat, \'Arial Black\', sans-serif" font-size="120" font-weight="900" letter-spacing="1.8" fill="{text_fill}" stroke="{text_fill}" stroke-width="4.5" stroke-linejoin="round">')
            lines.append('        <textPath href="#ribbonTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        elif is_white:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="#FFFFFF" stroke="#000000" stroke-width="26" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_fold_left_d} {ribbon_fold_right_d}" fill="#000000" stroke="#000000" stroke-width="14" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="#FFFFFF" stroke="#000000" stroke-width="32" stroke-linejoin="round"/>')
            lines.append('      <text font-family="\'Plus Jakarta Sans\', Montserrat, \'Arial Black\', sans-serif" font-size="120" font-weight="900" letter-spacing="1.8" fill="#000000" stroke="#000000" stroke-width="4.5" stroke-linejoin="round">')
            lines.append('        <textPath href="#ribbonTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        else:
            lines.append(f'      <path d="{ribbon_tail_left_d} {ribbon_tail_right_d}" fill="#1E293B" stroke="#020408" stroke-width="26" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_fold_left_d} {ribbon_fold_right_d}" fill="#0A0E17" stroke="#020408" stroke-width="14" stroke-linejoin="round"/>')
            lines.append(f'      <path d="{ribbon_body_d}" fill="#0A0E17" stroke="#334155" stroke-width="32" stroke-linejoin="round"/>')
            lines.append('      <text font-family="\'Plus Jakarta Sans\', Montserrat, \'Arial Black\', sans-serif" font-size="120" font-weight="900" letter-spacing="1.8" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="4.5" stroke-linejoin="round">')
            lines.append('        <textPath href="#ribbonTextArc" startOffset="50%" text-anchor="middle">SMANSAGE VOLLEYBALL COMPETITION</textPath>')
            lines.append('      </text>')
        lines.append('    </g>')

        # 4. SMOOTH ATHLETIC 3D "SVC" TYPOGRAPHY (EXACT HAND-DRAW SVC.PNG)
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
