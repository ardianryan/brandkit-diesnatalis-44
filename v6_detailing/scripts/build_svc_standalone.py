#!/usr/bin/env python3
"""
build_svc_standalone.py
=======================
Builds standalone, pristine SVG and PNG assets for the SVC wordmark
(Smansage Volleyball Competition) matching 'hand draw SVC.PNG' exactly.

Features:
- Pure chiseled 3D prismatic typography (Bevel)
- Matching horizontal terminal cuts with triangular bevel wedges
- Continuous central ridge lines connecting apex to apex
- Dual metallic gold facets (Light Gold highlight & Warm Amber shade)
- Grounded 3D drop depth extrusions on underside
- Generates 3 SVG variants: color, white (stencil outline), dark (monochrome)
- Renders high-resolution PNGs and side-by-side comparison with original reference
"""

import os
import subprocess
import cv2
import numpy as np

# Coordinates calibrated from scratch/svc_grid.png (native space 700 x 420 px)
# We use a clean 1000 x 600 canvas with letters centered.
CANVAS_W = 1000
CANVAS_H = 600

# Offset to center letters on canvas:
# Reference letters bounds: x=15..675 (w=660), y=10..385 (h=375)
# Target center: cx = 500, cy = 300
OX = 170.0
OY = 110.0

def build_svc_svg(mode="color"):
    is_color = (mode == "color")
    is_white = (mode == "white")
    
    if is_color:
        fill_light = "url(#goldLightFacet)"
        fill_shade = "url(#goldShadeFacet)"
        fill_bevel = "url(#goldBevelFacet)"
        fill_depth = "url(#goldDepth)"
        stroke_attr = ' stroke="none"'
        outline_bg = ""
    elif is_white:
        fill_light = "#FFFFFF"
        fill_shade = "#E2E8F0"
        fill_bevel = "#CBD5E1"
        fill_depth = "#94A3B8"
        stroke_attr = ' stroke="#000000" stroke-width="6" stroke-linejoin="round"'
        outline_bg = ""
    else: # dark
        fill_light = "#E2E8F0"
        fill_shade = "#94A3B8"
        fill_bevel = "#64748B"
        fill_depth = "#334155"
        stroke_attr = ' stroke="none"'
        outline_bg = ""

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CANVAS_W} {CANVAS_H}" width="{CANVAS_W}" height="{CANVAS_H}">')
    lines.append(f'  <title>SVC Wordmark - {mode.upper()}</title>')
    lines.append('  <defs>')
    
    if is_color:
        lines.append('''    <!-- Dual Metallic Gold Facet Gradients matching hand draw SVC.PNG -->
    <linearGradient id="goldLightFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF8C4"/>
      <stop offset="35%" stop-color="#F9D758"/>
      <stop offset="70%" stop-color="#F2BF3E"/>
      <stop offset="100%" stop-color="#EAA82C"/>
    </linearGradient>

    <linearGradient id="goldShadeFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EDA82C"/>
      <stop offset="50%" stop-color="#DC9126"/>
      <stop offset="100%" stop-color="#C6761A"/>
    </linearGradient>

    <linearGradient id="goldBevelFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#CB7B20"/>
      <stop offset="100%" stop-color="#A85B12"/>
    </linearGradient>

    <linearGradient id="goldDepth" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8C470E"/>
      <stop offset="50%" stop-color="#6A3208"/>
      <stop offset="100%" stop-color="#451D04"/>
    </linearGradient>''')

    lines.append('  </defs>')
    
    # Background for color & dark variant
    if is_color:
        lines.append(f'  <rect width="{CANVAS_W}" height="{CANVAS_H}" fill="#0A0E17"/>')
    elif not is_white:
        lines.append(f'  <rect width="{CANVAS_W}" height="{CANVAS_H}" fill="#020408"/>')

    lines.append(f'  <g id="svc-standalone" transform="translate({OX:.1f}, {OY:.1f})">')

    # =========================================================================
    # 1. LETTER S
    # =========================================================================
    lines.append('    <!-- ===== LETTER S ===== -->')
    lines.append('    <g id="letter-S">')
    
    # S 3D Depth Extrusions:
    # Drop shadow below bottom-left terminal & underside of top crook
    lines.append(f'''      <!-- S Extrusion Depth -->
      <path d="M 18 260 L 15 285 L 15 375 L 35 375 L 55 290 L 18 260 Z" fill="{fill_depth}"{stroke_attr}/>
      <path d="M 120 110 C 90 110 75 125 75 145 C 75 170 95 190 120 205 L 120 215 C 85 200 60 175 60 145 C 60 115 85 95 120 95 Z" fill="{fill_depth}"{stroke_attr}/>
      <path d="M 18 360 C 50 388 85 392 120 392 C 165 392 205 380 218 340 L 215 315 C 205 360 165 372 120 372 C 85 372 50 365 25 345 Z" fill="{fill_depth}"{stroke_attr}/>''')

    # S Top Terminal Triangular Bevel Wedge:
    # Horizontal flat cut from (150, 160) to (215, 160), apex at (175, 128)
    lines.append(f'''      <!-- S Top Bevel Triangle -->
      <polygon points="150,160 215,160 175,128" fill="{fill_bevel}"{stroke_attr}/>''')

    # S Bottom Terminal Triangular Bevel Wedge:
    # Horizontal flat cut from (18, 260) to (80, 260), apex at (52, 290)
    lines.append(f'''      <!-- S Bottom Bevel Triangle -->
      <polygon points="18,260 80,260 52,290" fill="{fill_bevel}"{stroke_attr}/>''')

    # S Facet 1: Outer / Light Gold Facet
    # Runs along the top outer arch, spine, and lower outer curve
    lines.append(f'''      <!-- S Light Gold Facet -->
      <path d="M 175 128
               C 175 90 155 58 118 58
               C 65 58 20 85 20 140
               C 20 195 55 220 95 240
               C 135 260 155 278 155 310
               C 155 338 140 355 118 355
               C 95 355 78 340 78 310
               L 52 290
               L 18 260
               C 18 320 60 372 118 372
               C 175 372 215 335 215 285
               C 215 225 175 200 135 180
               C 95 160 78 145 78 120
               C 78 95 95 78 118 78
               C 145 78 165 95 175 128 Z" fill="{fill_light}"{stroke_attr}/>''')

    # S Facet 2: Inner / Warm Amber Shade Facet
    # Runs along the inner top crook and inner lower loop, meeting at the central ridge
    lines.append(f'''      <!-- S Shade Amber Facet -->
      <path d="M 215 160
               L 175 128
               C 165 95 145 78 118 78
               C 95 78 78 95 78 120
               C 78 145 95 160 135 180
               C 175 200 215 225 215 285
               C 215 335 175 372 118 372
               C 60 372 18 320 18 260
               L 52 290
               C 78 340 95 355 118 355
               C 140 355 155 338 155 310
               C 155 278 135 260 95 240
               C 55 220 20 195 20 140
               C 20 85 65 58 118 58
               C 155 58 175 90 175 128
               L 150 160
               C 150 130 135 110 118 110
               C 98 110 88 122 88 140
               C 88 162 108 178 145 198
               C 185 218 202 245 202 285
               C 202 315 185 335 155 335
               L 150 160 Z" fill="{fill_shade}"{stroke_attr}/>''')
    lines.append('    </g>')

    # =========================================================================
    # 2. LETTER V
    # =========================================================================
    lines.append('    <!-- ===== LETTER V ===== -->')
    lines.append('    <g id="letter-V">')
    
    # V 3D Depth Extrusions:
    lines.append(f'''      <!-- V Extrusion Depth -->
      <polygon points="455,10 468,18 400,345 385,335" fill="{fill_depth}"{stroke_attr}/>
      <polygon points="385,335 400,345 388,375 375,365" fill="{fill_depth}"{stroke_attr}/>''')

    # Left Leg Top Bevel Triangle (points down):
    lines.append(f'''      <!-- V Left Top Bevel Triangle -->
      <polygon points="205,10 275,10 245,38" fill="{fill_bevel}"{stroke_attr}/>''')

    # Right Leg Top Bevel Triangle (points down):
    lines.append(f'''      <!-- V Right Top Bevel Triangle -->
      <polygon points="385,10 455,10 415,38" fill="{fill_bevel}"{stroke_attr}/>''')

    # Left Leg Outer Face (Light Gold):
    lines.append(f'''      <!-- V Left Leg Light Face -->
      <polygon points="205,10 245,38 335,335 305,335" fill="{fill_light}"{stroke_attr}/>''')

    # Central Valley & Right Leg Inner Face (Warm Amber Shade):
    lines.append(f'''      <!-- V Valley & Right Face -->
      <polygon points="275,10 245,38 335,335 355,335 415,38 385,10 330,240" fill="{fill_shade}"{stroke_attr}/>''')

    # Right Leg Outer Face (Light Gold Highlight):
    lines.append(f'''      <!-- V Right Outer Face -->
      <polygon points="455,10 415,38 355,335 385,335" fill="{fill_light}"{stroke_attr}/>''')

    # Bottom Trapezoid Bevel Wedge:
    lines.append(f'''      <!-- V Bottom Bevel Trapezoid -->
      <polygon points="305,335 385,335 375,365 315,365" fill="{fill_bevel}"{stroke_attr}/>''')
    lines.append('    </g>')

    # =========================================================================
    # 3. LETTER C
    # =========================================================================
    lines.append('    <!-- ===== LETTER C ===== -->')
    lines.append('    <g id="letter-C">')
    
    # C 3D Depth Extrusions:
    lines.append(f'''      <!-- C Extrusion Depth -->
      <path d="M 600 160 C 570 160 550 185 550 230 C 550 275 570 305 600 305 L 612 318 C 570 318 535 285 535 230 C 535 175 570 148 612 148 Z" fill="{fill_depth}"{stroke_attr}/>
      <path d="M 565 370 C 610 370 645 355 665 305 L 678 315 C 655 370 615 385 565 385 C 520 385 480 365 465 340 L 475 325 C 490 352 525 370 565 370 Z" fill="{fill_depth}"{stroke_attr}/>''')

    # Top Terminal Triangular Bevel Wedge:
    # Flat horizontal cut from (600, 160) to (665, 160), apex at (632, 130)
    lines.append(f'''      <!-- C Top Bevel Triangle -->
      <polygon points="600,160 665,160 632,130" fill="{fill_bevel}"{stroke_attr}/>''')

    # Bottom Terminal Triangular Bevel Wedge:
    # Flat horizontal cut from (600, 305) to (665, 305), apex at (632, 335)
    lines.append(f'''      <!-- C Bottom Bevel Triangle -->
      <polygon points="600,305 665,305 632,335" fill="{fill_bevel}"{stroke_attr}/>''')

    # C Facet 1: Outer Curved Light Gold Facet
    # From top apex (632, 130) along outer perimeter to bottom apex (632, 335)
    lines.append(f'''      <!-- C Outer Light Gold Facet -->
      <path d="M 632 130
               L 665 160
               L 665 140
               C 645 105 610 95 565 95
               C 490 95 445 150 445 230
               C 445 310 490 370 565 370
               C 610 370 645 355 665 305
               L 632 335
               C 605 352 580 352 565 352
               C 505 352 475 305 475 230
               C 475 155 505 112 565 112
               C 580 112 605 112 632 130 Z" fill="{fill_light}"{stroke_attr}/>''')

    # C Facet 2: Inner Curved Warm Amber Shade Facet
    # Between central ridge and inner cutout curve
    lines.append(f'''      <!-- C Inner Shade Amber Facet -->
      <path d="M 632 130
               L 600 160
               C 575 160 555 185 555 230
               C 555 275 575 305 600 305
               L 632 335
               C 605 352 580 352 565 352
               C 505 352 475 305 475 230
               C 475 155 505 112 565 112
               C 580 112 605 112 632 130 Z" fill="{fill_shade}"{stroke_attr}/>''')
    lines.append('    </g>')

    lines.append('  </g>')
    lines.append('</svg>')
    return "\n".join(lines)

def main():
    print("Generating standalone SVC wordmarks...")
    os.makedirs("assets/svg", exist_ok=True)
    os.makedirs("assets/png", exist_ok=True)

    for mode in ["color", "white", "dark"]:
        svg_content = build_svc_svg(mode)
        svg_path = f"assets/svg/svc-standalone-{mode}.svg"
        with open(svg_path, "w") as f:
            f.write(svg_content)
        print(f"Saved: {svg_path}")

        # Render PNG via qlmanage
        png_tmp_dir = "scratch/standalone_renders"
        os.makedirs(png_tmp_dir, exist_ok=True)
        subprocess.run(["qlmanage", "-t", "-s", "2000", "-o", png_tmp_dir, svg_path], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Copy to assets/png
        rendered_png = os.path.join(png_tmp_dir, f"svc-standalone-{mode}.svg.png")
        target_png = f"assets/png/svc-standalone-{mode}.png"
        if os.path.exists(rendered_png):
            im = cv2.imread(rendered_png)
            cv2.imwrite(target_png, im)
            print(f"Rendered: {target_png}")

    # Generate side-by-side comparison with hand draw reference
    print("\nGenerating side-by-side visual comparison...")
    ref = cv2.imread("scratch/svc_isolated_reference.png")
    test_im = cv2.imread("assets/png/svc-standalone-color.png")

    if ref is not None and test_im is not None:
        # Crop letter area from test_im
        # test_im is 2000x1200 or 2000x2000 depending on qlmanage
        h, w = test_im.shape[:2]
        # Crop central letter area
        gray = cv2.cvtColor(test_im, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
        pts = cv2.findNonZero(thresh)
        if pts is not None:
            rx, ry, rw, rh = cv2.boundingRect(pts)
            # Add small padding
            p = 20
            rx = max(0, rx - p)
            ry = max(0, ry - p)
            rw = min(w - rx, rw + 2*p)
            rh = min(h - ry, rh + 2*p)
            test_crop = test_im[ry:ry+rh, rx:rx+rw]
        else:
            test_crop = test_im

        # Resize test_crop to match reference height
        ref_h, ref_w = ref.shape[:2]
        target_h = 450
        scale_ref = target_h / ref_h
        ref_res = cv2.resize(ref, (int(ref_w * scale_ref), target_h), interpolation=cv2.INTER_LANCZOS4)
        
        scale_test = target_h / test_crop.shape[0]
        test_res = cv2.resize(test_crop, (int(test_crop.shape[1] * scale_test), target_h), interpolation=cv2.INTER_LANCZOS4)

        # Concatenate horizontally with label divider
        divider = np.full((target_h, 30, 3), [15, 23, 42], dtype=np.uint8)
        comparison = np.hstack([ref_res, divider, test_res])
        cv2.imwrite("scratch/svc_standalone_vs_reference.png", comparison)
        print("Comparison saved: scratch/svc_standalone_vs_reference.png")

if __name__ == "__main__":
    main()
