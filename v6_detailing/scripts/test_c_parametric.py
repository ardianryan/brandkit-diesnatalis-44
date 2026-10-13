import cv2
import numpy as np

ref = cv2.imread('scratch/svc_isolated_reference.png')
H, W = ref.shape[:2]

# Let's write an SVG with just C using pure cubic beziers and test its fit!
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
  </defs>

  <!-- Transparent or dark background -->
  <rect width="725" height="400" fill="#0A0E17"/>

  <!-- ==================== LETTER C ==================== -->
  <g id="letter-C">
    <!-- C Outer Light Facet:
         From top apex (630, 140) to outer top cut (664, 165),
         around outer curve to bottom outer cut (664, 265),
         to bottom apex (630, 290),
         and back along central ridge to top apex (630, 140). -->
    <path d="M 630 140
             L 664 165
             C 664 105 628 55 570 55
             C 505 55 466 115 466 220
             C 466 325 505 385 570 385
             C 628 385 664 335 664 265
             L 630 290
             C 610 330 585 348 570 348
             C 520 348 502 295 502 220
             C 502 145 520 92 570 92
             C 585 92 610 110 630 140 Z" fill="url(#goldLightFacet)"/>

    <!-- C Inner Shade Facet:
         Between central ridge and inner cutout curve -->
    <path d="M 630 140
             C 610 110 585 92 570 92
             C 520 92 502 145 502 220
             C 502 295 520 348 570 348
             C 585 348 610 330 630 290
             L 594 265
             C 575 285 560 285 550 270
             C 538 255 538 235 538 220
             C 538 205 538 185 550 170
             C 560 155 575 155 594 165 Z" fill="url(#goldShadeFacet)"/>

    <!-- Bevel Wedges -->
    <polygon points="594,165 664,165 630,140" fill="url(#goldBevelFacet)"/>
    <polygon points="594,265 664,265 630,290" fill="url(#goldBevelFacet)"/>
  </g>
</svg>
'''

with open('scratch/test_c_parametric.svg', 'w') as f:
    f.write(svg)

import subprocess
subprocess.run(['qlmanage', '-t', '-s', '1450', '-o', 'scratch', 'scratch/test_c_parametric.svg'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

rendered = cv2.imread('scratch/test_c_parametric.svg.png')
# Resize to 725 x 400
h, w = ref.shape[:2]
rendered_res = cv2.resize(rendered, (w, h), interpolation=cv2.INTER_LANCZOS4)

# Overlay with ref
comp = np.hstack([ref[:, 450:], rendered_res[:, 450:]])
cv2.imwrite('scratch/comp_c_only.png', comp)
print("Saved scratch/comp_c_only.png!")
