import os
import subprocess
import cv2
import numpy as np

# Coordinates for 1000 x 1000 canvas, centered at (500, 500)
# Reference letters bounding box: w=660, h=370
# Center offset: tx = 165, ty = 310

def generate_svg(mode="color"):
    is_color = (mode == "color")
    is_white = (mode == "white")
    
    if is_color:
        f_light = "url(#goldLightFacet)"
        f_shade = "url(#goldShadeFacet)"
        f_bevel = "url(#goldBevelFacet)"
        f_depth = "url(#goldDepth)"
        poly_stroke = ' stroke="none"'
    elif is_white:
        f_light = "#FFFFFF"
        f_shade = "#E2E8F0"
        f_bevel = "#CBD5E1"
        f_depth = "#94A3B8"
        poly_stroke = ' stroke="#000000" stroke-width="6" stroke-linejoin="round"'
    else: # dark
        f_light = "#E2E8F0"
        f_shade = "#94A3B8"
        f_bevel = "#64748B"
        f_depth = "#334155"
        poly_stroke = ' stroke="none"'

    bg = '<rect width="1000" height="1000" fill="#0A0E17"/>' if is_color else ('<rect width="1000" height="1000" fill="#020408"/>' if not is_white else '')

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <!-- Accurate Metallic Gold Facets calibrated from original hand draw SVC.PNG -->
    <linearGradient id="goldLightFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFAD0"/>
      <stop offset="40%" stop-color="#FAD758"/>
      <stop offset="80%" stop-color="#F2BF3E"/>
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

    <linearGradient id="goldDepth" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8C470E"/>
      <stop offset="50%" stop-color="#6A3208"/>
      <stop offset="100%" stop-color="#451D04"/>
    </linearGradient>
  </defs>

  {bg}

  <g id="svc-letters" transform="translate(165, 310)">

    <!-- ========================================== -->
    <!-- 1. LETTER S                                -->
    <!-- ========================================== -->
    <g id="letter-S">
      <!-- S 3D Depth Extrusions -->
      <path d="M 18 260 L 10 275 L 10 375 L 35 375 L 50 290 Z" fill="{f_depth}"{poly_stroke}/>
      <path d="M 18 360 C 50 395 85 398 118 398 C 165 398 215 385 225 340 L 215 310 C 205 355 165 370 118 370 C 85 370 45 365 20 345 Z" fill="{f_depth}"{poly_stroke}/>
      <path d="M 118 115 C 85 115 75 130 75 145 C 75 165 95 185 118 200 L 118 215 C 80 198 55 175 55 145 C 55 120 75 95 118 95 Z" fill="{f_depth}"{poly_stroke}/>

      <!-- S Terminal Bevel Triangles -->
      <!-- Top Bevel Triangle: horizontal cut from (150, 160) to (215, 160), apex at (182, 130) -->
      <polygon points="150,160 215,160 182,130" fill="{f_bevel}"{poly_stroke}/>
      <!-- Bottom Bevel Triangle: horizontal cut from (18, 260) to (80, 260), apex at (50, 290) -->
      <polygon points="18,260 80,260 50,290" fill="{f_bevel}"{poly_stroke}/>

      <!-- S Outer Light Gold Facet -->
      <path d="M 182 130
               L 215 160
               C 215 105 180 55 118 55
               C 55 55 18 100 18 150
               C 18 200 52 225 90 245
               C 130 265 155 285 155 315
               C 155 342 138 358 118 358
               C 92 358 75 342 75 315
               L 50 290
               L 18 260
               C 18 325 60 372 118 372
               C 178 372 215 335 215 285
               C 215 230 180 205 145 185
               C 110 168 78 150 78 120
               C 78 95 95 78 118 78
               C 148 78 172 98 182 130 Z" fill="{f_light}"{poly_stroke}/>

      <!-- S Inner Warm Amber Shade Facet -->
      <path d="M 182 130
               L 150 160
               C 150 135 138 115 118 115
               C 95 115 82 130 82 150
               C 82 178 105 198 145 218
               C 185 238 215 260 215 285
               C 215 335 178 372 118 372
               C 60 372 18 325 18 260
               L 50 290
               C 75 342 92 358 118 358
               C 138 358 155 342 155 315
               C 155 285 130 265 90 245
               C 52 225 18 200 18 150
               C 18 100 55 55 118 55
               C 180 55 215 105 215 160
               L 182 130 Z" fill="{f_shade}"{poly_stroke}/>
    </g>

    <!-- ========================================== -->
    <!-- 2. LETTER V                                -->
    <!-- ========================================== -->
    <g id="letter-V">
      <!-- V Extrusion Depth -->
      <polygon points="455,10 468,18 400,345 385,335" fill="{f_depth}"{poly_stroke}/>
      <polygon points="385,335 400,345 388,375 375,365" fill="{f_depth}"{poly_stroke}/>

      <!-- Left Leg Top Bevel Triangle (points down) -->
      <polygon points="205,10 275,10 245,38" fill="{f_bevel}"{poly_stroke}/>

      <!-- Right Leg Top Bevel Triangle (points down) -->
      <polygon points="385,10 455,10 415,38" fill="{f_bevel}"{poly_stroke}/>

      <!-- Left Leg Outer Face (Light Gold direct light) -->
      <polygon points="205,10 245,38 335,335 305,335" fill="{f_light}"{poly_stroke}/>

      <!-- Left Leg Inner Face (Light Gold tone) -->
      <polygon points="275,10 245,38 335,335 330,240" fill="{f_light}"{poly_stroke}/>

      <!-- Right Leg Entire Face (Warm Amber Shade matching reference) -->
      <polygon points="330,240 335,335 355,335 415,38 385,10" fill="{f_shade}"{poly_stroke}/>
      <polygon points="455,10 415,38 355,335 385,335" fill="{f_shade}"{poly_stroke}/>

      <!-- Bottom Trapezoid Bevel Wedge -->
      <polygon points="305,335 385,335 375,365 315,365" fill="{f_bevel}"{poly_stroke}/>
    </g>

    <!-- ========================================== -->
    <!-- 3. LETTER C                                -->
    <!-- ========================================== -->
    <g id="letter-C">
      <!-- C 3D Depth Extrusions -->
      <path d="M 600 160 C 570 160 550 185 550 232 C 550 280 570 305 600 305 L 612 318 C 570 318 535 285 535 232 C 535 178 570 148 612 148 Z" fill="{f_depth}"{poly_stroke}/>
      <path d="M 565 370 C 610 370 645 355 665 305 L 678 315 C 655 370 615 385 565 385 C 520 385 480 365 465 340 L 475 325 C 490 352 525 370 565 370 Z" fill="{f_depth}"{poly_stroke}/>

      <!-- C Terminal Bevel Triangles -->
      <polygon points="600,160 665,160 632,130" fill="{f_bevel}"{poly_stroke}/>
      <polygon points="600,305 665,305 632,275" fill="{f_bevel}"{poly_stroke}/>

      <!-- C Outer Face: LIGHT GOLD (Direct top-left ambient light) -->
      <path d="M 632 130
               L 665 160
               C 665 110 625 95 565 95
               C 490 95 445 150 445 232
               C 445 315 490 370 565 370
               C 625 370 665 355 665 305
               L 632 275
               C 605 330 580 338 565 338
               C 505 338 480 295 480 232
               C 480 165 505 125 565 125
               C 580 125 605 130 632 130 Z" fill="{f_light}"{poly_stroke}/>

      <!-- C Inner Face: WARM AMBER SHADE (Inner cavity hollow) -->
      <path d="M 632 130
               L 600 160
               C 575 160 555 185 555 232
               C 555 280 575 305 600 305
               L 632 275
               C 605 330 580 338 565 338
               C 505 338 480 295 480 232
               C 480 165 505 125 565 125
               C 580 125 605 130 632 130 Z" fill="{f_shade}"{poly_stroke}/>
    </g>

  </g>
</svg>'''

# Save color, white, dark
for mode in ["color", "white", "dark"]:
    svg_code = generate_svg(mode)
    svg_file = f"assets/svg/svc-standalone-{mode}.svg"
    with open(svg_file, "w") as f:
        f.write(svg_code)
    png_file = f"assets/png/svc-standalone-{mode}.png"
    subprocess.run(["qlmanage", "-t", "-s", "2000", "-o", "scratch", svg_file], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rendered = f"scratch/svc-standalone-{mode}.svg.png"
    if os.path.exists(rendered):
        im = cv2.imread(rendered)
        cv2.imwrite(png_file, im)

print("Generated updated standalone assets!")

# Rebuild side-by-side comparison
ref = cv2.imread('scratch/svc_isolated_reference.png')
test = cv2.imread('assets/png/svc-standalone-color.png')

crop_test = test[550:1450, 250:1750]
h = 450
ref_scaled = cv2.resize(ref, (int(ref.shape[1] * h / ref.shape[0]), h), interpolation=cv2.INTER_LANCZOS4)
test_scaled = cv2.resize(crop_test, (int(crop_test.shape[1] * h / crop_test.shape[0]), h), interpolation=cv2.INTER_LANCZOS4)

divider = np.full((h, 24, 3), [20, 30, 60], dtype=np.uint8)
comp = np.hstack([ref_scaled, divider, test_scaled])
cv2.imwrite('scratch/svc_standalone_vs_reference_tuned.png', comp)
print('Saved scratch/svc_standalone_vs_reference_tuned.png!')
