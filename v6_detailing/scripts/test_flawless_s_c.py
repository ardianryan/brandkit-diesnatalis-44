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
  <!-- 1. LETTER S (Seamless Solid Waist - Pristine Bevel Wedges & Facets)       -->
  <!-- ========================================================================= -->
  <g id="letter-S">
    <!-- Base Solid Letter S Body: Pure Smooth Parametric Cubic Bezier Curves (Light Gold) -->
    <path d="M 142 165
             L 202 165
             C 202 105 170 55 115 55
             C 60 55 18 100 18 150
             C 18 195 55 218 105 230
             C 175 245 218 260 218 290
             C 218 340 175 385 115 385
             C 60 385 16 335 16 265
             L 81 265
             C 81 305 95 325 115 325
             C 145 325 155 305 155 285
             C 155 265 140 248 115 238
             C 90 228 82 200 82 170
             C 82 135 95 122 115 122
             C 130 122 142 135 142 165 Z" fill="url(#goldLightFacet)"/>

    <!-- Shaded Inner Top Crook Facet (Confined to upper bowl, zero waist cuts) -->
    <path d="M 174 136
             L 142 165
             C 142 135 130 122 115 122
             C 95 122 82 135 82 170
             C 82 185 75 185 68 175
             C 55 155 55 125 75 105
             C 90 92 115 88 135 88
             C 155 88 168 110 174 136 Z" fill="url(#goldShadeFacet)"/>

    <!-- Shaded Lower Outer Arch Facet (Confined to lower bowl, zero waist cuts) -->
    <path d="M 16 265
             C 16 335 60 385 115 385
             C 175 385 218 340 218 290
             C 218 275 200 270 185 285
             C 165 305 145 350 115 350
             C 80 350 58 320 53 288
             L 16 265 Z" fill="url(#goldShadeFacet)"/>

    <!-- Top Terminal Bevel Triangle -->
    <polygon points="142,165 202,165 174,136" fill="url(#goldBevelFacet)"/>

    <!-- Bottom Terminal Bevel Triangle -->
    <polygon points="16,265 81,265 53,288" fill="url(#goldBevelFacet)"/>
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
  <!-- 3. LETTER C (Truly Rounded Parametric Curves - Flawless Circular Sweeps)  -->
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
         Continuous elliptical sweep, NO straight vertical edges -->
    <path d="M 630 140
             L 664 165
             C 664 90 625 55 570 55
             C 500 55 466 120 466 220
             C 466 320 500 385 570 385
             C 625 385 664 345 664 265
             L 630 290
             C 605 330 585 348 570 348
             C 525 348 502 290 502 220
             C 502 150 525 92 570 92
             C 585 92 605 110 630 140 Z" fill="url(#goldLightFacet)"/>
             
    <!-- C Inner Shade Facet:
         Continuous sweeping rounded arch inside C counter (smooth round top and bottom) -->
    <path d="M 630 140
             C 605 110 585 92 570 92
             C 525 92 502 150 502 220
             C 502 290 525 348 570 348
             C 585 348 605 330 630 290
             L 594 265
             C 575 295 555 280 545 250
             C 538 238 538 228 538 220
             C 538 212 538 202 545 190
             C 555 160 575 145 594 165 Z" fill="url(#goldShadeFacet)"/>
             
    <!-- C Terminal Bevel Triangles -->
    <!-- Top Bevel Triangle: horizontal cut from (594, 165) to (664, 165), apex at (630, 140) -->
    <polygon points="594,165 664,165 630,140" fill="url(#goldBevelFacet)"/>
    <!-- Bottom Bevel Triangle: horizontal cut from (594, 265) to (664, 265), apex at (630, 290) -->
    <polygon points="594,265 664,265 630,290" fill="url(#goldBevelFacet)"/>
  </g>

</svg>'''

with open('scratch/test_flawless.svg', 'w') as f:
    f.write(build_svg())

subprocess.run(['qlmanage', '-t', '-s', '1450', '-o', 'scratch', 'scratch/test_flawless.svg'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

ref = cv2.imread('scratch/svc_isolated_reference.png')
h, w = ref.shape[:2]
rendered = cv2.imread('scratch/test_flawless.svg.png')
actual = rendered[0:800, 0:1450]
res = cv2.resize(actual, (w, h), interpolation=cv2.INTER_LANCZOS4)

divider = np.full((h, 16, 3), [20, 30, 60], dtype=np.uint8)
comp = np.hstack([ref, divider, res])
cv2.imwrite('scratch/comp_flawless.png', comp)
print("Saved scratch/comp_flawless.png!")
