import cv2
import numpy as np
import subprocess

def test():
    svg = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 725 400" width="725" height="400">
  <defs>
    <!-- Metallic Gold Facet - Vertical Top-to-Bottom Flow -->
    <linearGradient id="goldSBody" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFAD0"/>
      <stop offset="30%" stop-color="#FAD758"/>
      <stop offset="65%" stop-color="#F2BF3E"/>
      <stop offset="100%" stop-color="#DC9126"/>
    </linearGradient>

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

  <!-- ==================== LETTER S ==================== -->
  <g id="letter-S">
    <!-- 3D Depth Block (Bottom-left & bottom under-curve) -->
    <polygon points="15,265 10,285 10,375 35,375 52,290 46,292" fill="url(#goldDepth)"/>
    <path d="M 10 375 C 35 392 70 398 115 398 L 115 385 C 70 385 35 380 10 375 Z" fill="url(#goldDepth)"/>

    <!-- Base Solid Letter S: Pure Smooth Bezier Curves -->
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
             C 130 122 140 135 140 165 Z" fill="url(#goldSBody)"/>

    <!-- Central Ridge Crease Line (Subtle embossed bevel edge) -->
    <path d="M 172 138
             C 162 105 145 88 115 88
             C 80 88 50 115 50 150
             C 50 185 80 205 115 220
             C 150 235 185 255 185 288
             C 185 325 150 355 115 355
             C 80 355 55 330 46 292" fill="none" stroke="#FFFAD0" stroke-width="2.5" opacity="0.6"/>

    <!-- Bevel Triangles -->
    <polygon points="140,165 202,165 172,138" fill="url(#goldBevelFacet)"/>
    <polygon points="15,265 78,265 46,292" fill="url(#goldBevelFacet)"/>
  </g>

  <!-- ==================== LETTER V ==================== -->
  <g id="letter-V">
    <polygon points="202,8 274,8 238,38" fill="url(#goldBevelFacet)"/>
    <polygon points="386,8 458,8 418,38" fill="url(#goldBevelFacet)"/>
    <polygon points="202,8 238,38 334,335 304,335" fill="url(#goldLightFacet)"/>
    <polygon points="274,8 238,38 334,335 330,248" fill="url(#goldLightFacet)"/>
    <polygon points="330,248 334,335 356,335 418,38 386,8" fill="url(#goldShadeFacet)"/>
    <polygon points="458,8 418,38 356,335 386,335" fill="url(#goldShadeFacet)"/>
    <polygon points="304,335 386,335 374,368 316,368" fill="url(#goldBevelFacet)"/>
  </g>

  <!-- ==================== LETTER C ==================== -->
  <g id="letter-C">
    <!-- C 3D Depth Underneath -->
    <path d="M 570 385 C 635 385 664 335 664 265 L 672 275 C 672 345 638 395 570 395 C 505 395 460 345 460 270 L 466 270 C 466 320 505 385 570 385 Z" fill="url(#goldDepth)"/>
    
    <!-- C Outer Light Facet -->
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
             
    <!-- C Inner Shade Facet -->
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
             
    <!-- C Bevel Triangles -->
    <polygon points="594,165 664,165 630,140" fill="url(#goldBevelFacet)"/>
    <polygon points="594,265 664,265 630,290" fill="url(#goldBevelFacet)"/>
  </g>
</svg>'''
    with open('scratch/test_authentic_s.svg', 'w') as f:
        f.write(svg)
    subprocess.run(['qlmanage', '-t', '-s', '1450', '-o', 'scratch', 'scratch/test_authentic_s.svg'], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

test()

ref = cv2.imread('scratch/svc_isolated_reference.png')
h, w = ref.shape[:2]
rendered = cv2.imread('scratch/test_authentic_s.svg.png')
actual = rendered[0:800, 0:1450]
res = cv2.resize(actual, (w, h), interpolation=cv2.INTER_LANCZOS4)

divider = np.full((h, 16, 3), [20, 30, 60], dtype=np.uint8)
comp = np.hstack([ref, divider, res])
cv2.imwrite('scratch/comp_authentic_s.png', comp)
print("Saved scratch/comp_authentic_s.png!")
