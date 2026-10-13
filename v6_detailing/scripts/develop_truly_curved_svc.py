import cv2
import numpy as np
import subprocess

def build_svg():
    # S, V, C native coordinate space (W=725, H=400)
    return '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 725 400" width="725" height="400">
  <defs>
    <!-- Master Pure Metallic Gold Facets calibrated from original hand draw SVC.PNG -->
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

    <linearGradient id="goldDepth" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#8C470E"/>
      <stop offset="50%" stop-color="#6A3208"/>
      <stop offset="100%" stop-color="#451D04"/>
    </linearGradient>
  </defs>

  <rect width="725" height="400" fill="#0A0E17"/>

  <!-- ========================================================================= -->
  <!-- 1. LETTER S (Full Dual-Facet Bevel System - Zero Seams)                    -->
  <!-- ========================================================================= -->
  <g id="letter-S">
    <!-- S 3D Depth Extrusion Block (Bottom-left terminal only, clean & flush) -->
    <polygon points="15,265 8,285 8,350 32,350 46,292" fill="url(#goldDepth)"/>

    <!-- S Base Silhouette (Prevents any rendering sub-pixel hairline gaps) -->
    <!-- Solid smooth S perimeter -->
    <path d="M 140 165
             L 202 165
             C 202 105 170 55 115 55
             C 60 55 18 100 18 150
             C 18 195 55 218 105 230
             C 175 245 218 260 218 290
             C 218 340 175 385 115 385
             C 60 385 15 335 15 265
             L 78 265
             C 78 305 95 325 115 325
             C 145 325 155 305 155 285
             C 155 265 140 248 115 238
             C 90 228 82 200 82 170
             C 82 135 95 122 115 122
             C 130 122 140 135 140 165 Z" fill="url(#goldLightFacet)"/>

    <!-- S Warm Amber Shade Facet:
         Covers the shaded side of S (Inner top crook, lower-left of waist, outer lower arch).
         Runs along the central chiseled ridge line from (172, 138) to (46, 292): -->
    <path d="M 172 138
             L 140 165
             C 140 135 130 122 115 122
             C 95 122 82 135 82 170
             C 82 200 90 228 115 238
             C 165 248 218 265 218 290
             C 218 340 175 385 115 385
             C 60 385 15 335 15 265
             L 46 292
             C 60 330 85 355 115 355
             C 150 355 185 325 185 288
             C 185 255 145 238 115 224
             C 80 208 50 185 50 150
             C 50 115 80 88 115 88
             C 145 88 162 105 172 138 Z" fill="url(#goldShadeFacet)"/>

    <!-- S Terminal Bevel Triangles -->
    <!-- Top Bevel Triangle: horizontal cut from (140, 165) to (202, 165), apex at (172, 138) -->
    <polygon points="140,165 202,165 172,138" fill="url(#goldBevelFacet)"/>
    <!-- Bottom Bevel Triangle: horizontal cut from (15, 265) to (78, 265), apex at (46, 292) -->
    <polygon points="15,265 78,265 46,292" fill="url(#goldBevelFacet)"/>
  </g>

  <!-- ========================================================================= -->
  <!-- 2. LETTER V (Pure Geometric Polygons - Pristine Chiseled Prism)           -->
  <!-- ========================================================================= -->
  <g id="letter-V">
    <!-- Left Top Bevel Triangle (points down) -->
    <polygon points="202,8 274,8 238,38" fill="url(#goldBevelFacet)"/>

    <!-- Right Top Bevel Triangle (points down, flush top edge) -->
    <polygon points="386,8 458,8 418,38" fill="url(#goldBevelFacet)"/>

    <!-- Left Leg Outer Face (Light Gold direct light) -->
    <polygon points="202,8 238,38 334,335 304,335" fill="url(#goldLightFacet)"/>

    <!-- Left Leg Inner Face (Light Gold direct light) -->
    <polygon points="274,8 238,38 334,335 330,248" fill="url(#goldLightFacet)"/>

    <!-- Right Leg Inner Face (Warm Amber Shade matching reference) -->
    <polygon points="330,248 334,335 356,335 418,38 386,8" fill="url(#goldShadeFacet)"/>

    <!-- Right Leg Outer Face (Warm Amber Shade matching reference) -->
    <polygon points="458,8 418,38 356,335 386,335" fill="url(#goldShadeFacet)"/>

    <!-- Bottom Trapezoid Bevel Wedge -->
    <polygon points="304,335 386,335 374,368 316,368" fill="url(#goldBevelFacet)"/>
  </g>

  <!-- ========================================================================= -->
  <!-- 3. LETTER C (Truly Rounded Parametric Curves - Flawless Degree Continuity)-->
  <!-- ========================================================================= -->
  <g id="letter-C">
    <!-- C 3D Depth Underneath Bottom Curve -->
    <path d="M 570 385
             C 625 385 658 340 664 265
             L 672 272
             C 666 350 630 395 570 395
             C 505 395 460 345 460 220
             L 466 220
             C 466 325 505 385 570 385 Z" fill="url(#goldDepth)"/>
    
    <!-- C Outer Light Facet:
         Continuous elliptical sweep with smooth curvature and round top/bottom arches -->
    <path d="M 630 140
             L 664 165
             C 664 95 628 55 570 55
             C 505 55 466 125 466 220
             C 466 315 505 385 570 385
             C 628 385 664 345 664 265
             L 630 290
             C 605 330 585 348 570 348
             C 525 348 502 290 502 220
             C 502 150 525 92 570 92
             C 585 92 605 110 630 140 Z" fill="url(#goldLightFacet)"/>
             
    <!-- C Inner Shade Facet:
         Continuous sweeping rounded arch inside C counter (no boxy corners) -->
    <path d="M 630 140
             C 605 110 585 92 570 92
             C 525 92 502 150 502 220
             C 502 290 525 348 570 348
             C 585 348 605 330 630 290
             L 594 265
             C 575 290 555 275 545 250
             C 538 238 538 228 538 220
             C 538 212 538 202 545 190
             C 555 165 575 150 594 165 Z" fill="url(#goldShadeFacet)"/>
             
    <!-- C Terminal Bevel Triangles -->
    <polygon points="594,165 664,165 630,140" fill="url(#goldBevelFacet)"/>
    <polygon points="594,265 664,265 630,290" fill="url(#goldBevelFacet)"/>
  </g>
</svg>'''

with open('scratch/test_truly_curved.svg', 'w') as f:
    f.write(build_svg())

subprocess.run(['qlmanage', '-t', '-s', '1450', '-o', 'scratch', 'scratch/test_truly_curved.svg'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

ref = cv2.imread('scratch/svc_isolated_reference.png')
h, w = ref.shape[:2]
rendered = cv2.imread('scratch/test_truly_curved.svg.png')
actual = rendered[0:800, 0:1450]
res = cv2.resize(actual, (w, h), interpolation=cv2.INTER_LANCZOS4)

divider = np.full((h, 16, 3), [20, 30, 60], dtype=np.uint8)
comp = np.hstack([ref, divider, res])
cv2.imwrite('scratch/comp_truly_curved.png', comp)
print("Saved scratch/comp_truly_curved.png!")
