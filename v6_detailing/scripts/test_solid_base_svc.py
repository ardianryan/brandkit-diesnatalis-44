import subprocess
import cv2
import numpy as np

def generate_svg(mode="color"):
    is_color = (mode == "color")
    is_white = (mode == "white")
    
    if is_color:
        f_base = "url(#goldLightFacet)"
        f_shade = "url(#goldShadeFacet)"
        f_bevel = "url(#goldBevelFacet)"
        f_depth = "url(#goldDepth)"
        poly_stroke = ' stroke="none"'
    elif is_white:
        f_base = "#FFFFFF"
        f_shade = "#E2E8F0"
        f_bevel = "#CBD5E1"
        f_depth = "#94A3B8"
        poly_stroke = ' stroke="#000000" stroke-width="5" stroke-linejoin="round"'
    else: # dark
        f_base = "#E2E8F0"
        f_shade = "#94A3B8"
        f_bevel = "#64748B"
        f_depth = "#334155"
        poly_stroke = ' stroke="none"'

    bg = '<rect width="1000" height="1000" fill="#0A0E17"/>' if is_color else ('<rect width="1000" height="1000" fill="#020408"/>' if not is_white else '')

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <!-- Master Pure Metallic Gold Gradients -->
    <linearGradient id="goldLightFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFAD0"/>
      <stop offset="35%" stop-color="#FAD758"/>
      <stop offset="70%" stop-color="#F2BF3E"/>
      <stop offset="100%" stop-color="#EAA82C"/>
    </linearGradient>

    <linearGradient id="goldShadeFacet" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#EDA82C"/>
      <stop offset="50%" stop-color="#DC9026"/>
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

  <!-- Master SVC Letters Container (Centered: cx=500, cy=500) -->
  <g id="svc-letters" transform="translate(165, 310)">

    <!-- ========================================== -->
    <!-- 1. LETTER S                                -->
    <!-- ========================================== -->
    <g id="letter-S">
      <!-- S 3D Depth Drop Shadow -->
      <polygon points="18,260 10,275 10,375 35,375 53,290" fill="{f_depth}"{poly_stroke}/>
      <path d="M 18 360 C 50 395 85 398 118 398 C 165 398 215 385 225 340 L 215 310 C 205 355 165 370 118 370 C 85 370 45 365 20 345 Z" fill="{f_depth}"{poly_stroke}/>
      <path d="M 118 125 C 85 125 75 135 75 150 C 75 170 95 190 118 205 L 118 218 C 80 200 55 178 55 150 C 55 125 75 105 118 105 Z" fill="{f_depth}"{poly_stroke}/>

      <!-- S Solid Athletic Base Face (Light Gold) -->
      <!-- Smooth, plump, perfectly proportioned continuous stroke -->
      <path d="M 218 160
               C 218 105 180 55 118 55
               C 55 55 18 100 18 145
               C 18 195 52 220 88 240
               C 125 260 152 280 152 312
               C 152 342 135 358 118 358
               C 92 358 75 342 75 315
               L 18 260
               L 88 260
               C 88 290 100 305 118 305
               C 135 305 148 292 148 275
               C 148 252 128 235 90 215
               C 50 195 25 170 25 145
               C 25 115 52 100 88 100
               C 120 100 148 115 148 145
               L 148 160 Z
               M 18 260
               C 18 325 60 372 118 372
               C 178 372 218 335 218 280
               C 218 230 180 205 145 185
               C 110 168 88 152 88 125
               C 88 110 100 100 118 100
               C 148 100 178 115 183 145
               L 218 160 Z" fill="{f_base}" fill-rule="evenodd"{poly_stroke}/>

      <!-- Full Solid Face Contour -->
      <path d="M 218 160
               C 218 105 180 55 118 55
               C 55 55 18 100 18 145
               C 18 195 52 220 88 240
               C 125 260 152 280 152 312
               C 152 342 135 358 118 358
               C 92 358 75 342 75 315
               L 18 260
               C 18 325 60 372 118 372
               C 178 372 218 335 218 280
               C 218 230 180 205 145 185
               C 110 168 88 152 88 125
               C 88 110 100 100 118 100
               C 148 100 178 115 183 145
               L 218 160
               L 148 160
               C 148 135 135 125 118 125
               C 98 125 88 135 88 145
               C 88 165 110 185 148 205
               C 185 225 218 250 218 280
               C 218 335 178 372 118 372
               L 118 358
               C 135 358 148 342 148 312
               C 148 290 135 275 118 275
               C 98 275 88 285 88 260
               Z" fill="{f_base}"{poly_stroke}/>

      <!-- S Shaded Amber Facet (Upper crook & Lower inner facet along spine) -->
      <path d="M 183 130
               L 148 160
               C 148 135 135 125 118 125
               C 98 125 88 135 88 145
               C 88 165 110 185 148 205
               C 185 225 218 250 218 280
               C 218 335 178 372 118 372
               C 60 372 18 325 18 260
               L 53 290
               C 75 342 92 358 118 358
               C 135 358 152 342 152 312
               C 152 280 125 260 88 240
               C 52 220 18 195 18 145
               C 18 100 55 55 118 55
               C 180 55 218 105 218 160
               L 183 130 Z" fill="{f_shade}" opacity="0.95"{poly_stroke}/>

      <!-- S Terminal Bevel Triangles -->
      <polygon points="148,160 218,160 183,130" fill="{f_bevel}"{poly_stroke}/>
      <polygon points="18,260 88,260 53,290" fill="{f_bevel}"{poly_stroke}/>
    </g>

    <!-- ========================================== -->
    <!-- 2. LETTER V                                -->
    <!-- ========================================== -->
    <g id="letter-V">
      <!-- V Extrusion Depth -->
      <polygon points="455,10 468,18 400,345 385,335" fill="{f_depth}"{poly_stroke}/>
      <polygon points="385,335 400,345 388,375 375,365" fill="{f_depth}"{poly_stroke}/>

      <!-- Left Leg Top Bevel Triangle -->
      <polygon points="205,10 275,10 245,38" fill="{f_bevel}"{poly_stroke}/>

      <!-- Right Leg Top Bevel Triangle -->
      <polygon points="385,10 455,10 415,38" fill="{f_bevel}"{poly_stroke}/>

      <!-- Left Leg Outer Face (Light Gold direct light) -->
      <polygon points="205,10 245,38 335,335 305,335" fill="{f_base}"{poly_stroke}/>

      <!-- Left Leg Inner Face (Light Gold direct light) -->
      <polygon points="275,10 245,38 335,335 330,240" fill="{f_base}"{poly_stroke}/>

      <!-- Right Leg Face (Warm Amber Shade matching reference) -->
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
               C 580 125 605 130 632 130 Z" fill="{f_base}"{poly_stroke}/>

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

import os
os.makedirs("assets/svg", exist_ok=True)
os.makedirs("assets/png", exist_ok=True)

for mode in ["color", "white", "dark"]:
    svg_data = generate_svg(mode)
    svg_file = f"assets/svg/svc-standalone-{mode}.svg"
    with open(svg_file, "w") as f:
        f.write(svg_data)
    png_file = f"assets/png/svc-standalone-{mode}.png"
    subprocess.run(["qlmanage", "-t", "-s", "2000", "-o", "scratch", svg_file], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rendered = f"scratch/svc-standalone-{mode}.svg.png"
    if os.path.exists(rendered):
        im = cv2.imread(rendered)
        cv2.imwrite(png_file, im)

print("Generated solid base standalone assets!")

# Comparison
ref = cv2.imread('scratch/svc_isolated_reference.png')
test = cv2.imread('assets/png/svc-standalone-color.png')

crop_test = test[550:1450, 250:1750]
h = 450
ref_scaled = cv2.resize(ref, (int(ref.shape[1] * h / ref.shape[0]), h), interpolation=cv2.INTER_LANCZOS4)
test_scaled = cv2.resize(crop_test, (int(crop_test.shape[1] * h / crop_test.shape[0]), h), interpolation=cv2.INTER_LANCZOS4)

divider = np.full((h, 24, 3), [20, 30, 60], dtype=np.uint8)
comp = np.hstack([ref_scaled, divider, test_scaled])
cv2.imwrite('scratch/svc_standalone_solid_comparison.png', comp)
print('Saved scratch/svc_standalone_solid_comparison.png!')
