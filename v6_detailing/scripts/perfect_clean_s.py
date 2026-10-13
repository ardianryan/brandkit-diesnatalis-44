import cv2
import numpy as np
import subprocess

def build_svg():
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
  <!-- 1. LETTER S (Pure Mathematical Curves - Smooth & Chiseled)                -->
  <!-- ========================================================================= -->
  <g id="letter-S">
    <!-- S 3D Depth Extrusion Block (Bottom-left & bottom under-curve) -->
    <polygon points="15,265 10,285 10,375 35,375 52,290 46,292" fill="url(#goldDepth)"/>
    <path d="M 10 375 C 35 392 70 398 115 398 L 115 385 C 70 385 35 380 10 375 Z" fill="url(#goldDepth)"/>

    <!-- S Base Solid Letterform: LIGHT GOLD FACET -->
    <!-- Defines the complete pristine smooth silhouette of S -->
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

    <!-- S Shaded Facet: Single continuous non-self-intersecting polygon!
         Runs from top bevel apex (172, 138) down inner top crook (140, 165),
         along inner crook to waist (115, 238),
         around outer bottom arch (218, 290 -> 115, 385 -> 15, 265),
         to bottom bevel apex (46, 292),
         and returns along the central chiseled ridge line back to top apex (172, 138)! -->
    <path d="M 172 138
             L 140 165
             C 140 135 130 122 115 122
             C 95 122 82 135 82 170
             C 82 200 90 228 115 238
             C 150 248 185 260 218 290
             C 218 340 175 385 115 385
             C 60 385 15 335 15 265
             L 46 292
             C 55 330 80 355 115 355
             C 150 355 185 325 185 288
             C 185 255 150 235 115 220
             C 80 205 50 185 50 150
             C 50 115 80 88 115 88
             C 145 88 162 105 172 138 Z" fill="url(#goldShadeFacet)"/>

    <!-- S Terminal Bevel Triangles -->
    <polygon points="140,165 202,165 172,138" fill="url(#goldBevelFacet)"/>
    <polygon points="15,265 78,265 46,292" fill="url(#goldBevelFacet)"/>
  </g>

  <!-- ========================================================================= -->
  <!-- 2. LETTER V (Pure Geometric Polygons - Pristine & Clean)                  -->
  <!-- ========================================================================= -->
  <g id="letter-V">
    <!-- Left Top Bevel Triangle (points down) -->
    <polygon points="202,8 274,8 238,38" fill="url(#goldBevelFacet)"/>

    <!-- Right Top Bevel Triangle (points down) -->
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
  <!-- 3. LETTER C (Pure Mathematical Curves & Athletic Proportions)             -->
  <!-- ========================================================================= -->
  <g id="letter-C">
    <!-- C 3D Depth Drop Shadow (Under bottom curve) -->
    <path d="M 570 385 C 635 385 664 335 664 265 L 672 275 C 672 345 638 395 570 395 C 505 395 460 345 460 270 L 466 270 C 466 320 505 385 570 385 Z" fill="url(#goldDepth)"/>

    <!-- C Outer Face (LIGHT GOLD):
         Between Outer Curve and Central Ridge Curve -->
    <path d="M 630 140
             L 664 165
             C 664 105 635 55 570 55
             C 505 55 466 110 466 160
             L 466 270
             C 466 320 505 385 570 385
             C 635 385 664 335 664 265
             L 630 290
             C 610 330 585 348 570 348
             C 525 348 502 305 502 260
             L 502 170
             C 502 125 525 90 570 90
             C 585 90 610 105 630 140 Z" fill="url(#goldLightFacet)"/>

    <!-- C Inner Face (WARM AMBER SHADE):
         Between Central Ridge Curve and Inner Cutout Curve -->
    <path d="M 630 140
             C 610 105 585 90 570 90
             C 525 90 502 125 502 170
             L 502 260
             C 502 305 525 348 570 348
             C 585 348 610 330 630 290
             L 594 265
             C 580 280 565 285 552 285
             C 538 285 538 275 538 260
             L 538 170
             C 538 155 538 145 552 145
             C 565 145 580 150 594 165 Z" fill="url(#goldShadeFacet)"/>

    <!-- C Terminal Bevel Triangles -->
    <!-- Top Bevel Triangle: base from (594, 165) to (664, 165), apex at (630, 140) -->
    <polygon points="594,165 664,165 630,140" fill="url(#goldBevelFacet)"/>
    <!-- Bottom Bevel Triangle: base from (594, 265) to (664, 265), apex at (630, 290) -->
    <polygon points="594,265 664,265 630,290" fill="url(#goldBevelFacet)"/>
  </g>

</svg>'''

with open('scratch/test_perfect_clean.svg', 'w') as f:
    f.write(build_svg())

subprocess.run(['qlmanage', '-t', '-s', '1450', '-o', 'scratch', 'scratch/test_perfect_clean.svg'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

ref = cv2.imread('scratch/svc_isolated_reference.png')
h, w = ref.shape[:2] # 395, 725

rendered = cv2.imread('scratch/test_perfect_clean.svg.png')
actual = rendered[0:800, 0:1450]
res = cv2.resize(actual, (w, h), interpolation=cv2.INTER_LANCZOS4)

# Side-by-side comparison
divider = np.full((h, 16, 3), [20, 30, 60], dtype=np.uint8)
comp = np.hstack([ref, divider, res])
cv2.imwrite('scratch/comp_perfect_clean.png', comp)

print("Saved scratch/comp_perfect_clean.png!")
