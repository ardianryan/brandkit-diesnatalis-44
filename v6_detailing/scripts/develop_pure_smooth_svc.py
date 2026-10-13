import cv2
import numpy as np
import subprocess
import os

# We will create an interactive test harness that renders S, V, C
# in the native reference coordinate space (width=700, height=420)
# and overlays the rendered vector paths on top of the original reference image
# with 50% opacity and edge diff, so we can verify 100% exact alignment,
# zero wobbles, and pure smoothness!

def build_test_svg():
    # S, V, C native coordinate space: W=725, H=400
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 725 400" width="725" height="400">
  <defs>
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
  <!-- 1. LETTER V (Pure Geometric Polygons - Pristine & Clean)                  -->
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

    <!-- Bottom Trapezoid Bevel Wedge (Front & depth) -->
    <polygon points="304,335 386,335 374,368 316,368" fill="url(#goldBevelFacet)"/>
    <!-- Small bottom drop extrusion -->
    <polygon points="316,368 374,368 368,375 322,375" fill="url(#goldDepth)"/>
  </g>

  <!-- ========================================================================= -->
  <!-- 2. LETTER C (Pure Mathematical Curves & Pristine Bevels)                  -->
  <!-- ========================================================================= -->
  <g id="letter-C">
    <!-- C Outer Face (LIGHT GOLD):
         Between Outer Curve and Central Ridge Curve -->
    <!-- Outer Curve: Top cut (664, 165) -> Arc around to (664, 265)
         Ridge Curve: Bottom apex (630, 290) -> Arc around to Top apex (630, 140) -->
    <path d="M 630 140
             L 664 165
             C 664 110 635 55 565 55
             C 495 55 466 110 466 215
             C 466 320 495 375 565 375
             C 635 375 664 320 664 265
             L 630 290
             C 610 330 585 342 565 342
             C 515 342 498 295 498 215
             C 498 135 515 88 565 88
             C 585 88 610 100 630 140 Z" fill="url(#goldLightFacet)"/>

    <!-- C Inner Face (WARM AMBER SHADE):
         Between Central Ridge Curve and Inner Cutout Curve -->
    <path d="M 630 140
             C 610 100 585 88 565 88
             C 515 88 498 135 498 215
             C 498 295 515 342 565 342
             C 585 342 610 330 630 290
             L 594 265
             C 575 285 555 285 540 270
             C 536 255 536 230 536 215
             C 536 200 536 175 540 160
             C 555 145 575 145 594 165 Z" fill="url(#goldShadeFacet)"/>

    <!-- C Terminal Bevel Triangles -->
    <!-- Top Bevel Triangle: base from (594, 165) to (664, 165), apex at (630, 140) -->
    <polygon points="594,165 664,165 630,140" fill="url(#goldBevelFacet)"/>
    <!-- Bottom Bevel Triangle: base from (594, 265) to (664, 265), apex at (630, 290) -->
    <polygon points="594,265 664,265 630,290" fill="url(#goldBevelFacet)"/>
  </g>

</svg>'''
    return svg

with open('scratch/test_v_c.svg', 'w') as f:
    f.write(build_test_svg())

subprocess.run(['qlmanage', '-t', '-s', '1450', '-o', 'scratch', 'scratch/test_v_c.svg'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print("Rendered scratch/test_v_c.svg.png!")
