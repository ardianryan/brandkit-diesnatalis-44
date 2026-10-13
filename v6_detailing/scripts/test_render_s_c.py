import subprocess
import os

# Let's write out an SVG with the exact mathematical bezier curves for S, V, C
# on a 1000 x 1000 square canvas with letters centered.

svg_code = '''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
  <defs>
    <!-- Metallic Gold Facet Gradients matching hand draw SVC.PNG -->
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
    </linearGradient>
  </defs>

  <rect width="1000" height="1000" fill="#0A0E17"/>

  <!-- Centered Letters Group (cx=500, cy=500) -->
  <!-- Reference bounding box: x=15..665 (w=650), y=10..370 (h=360) -->
  <!-- Offset: tx = 500 - 340 = 160, ty = 500 - 190 = 310 -->
  <g id="svc-letters" transform="translate(160, 310)">
    
    <!-- ========================================== -->
    <!-- 1. LETTER S                                -->
    <!-- ========================================== -->
    <g id="letter-S">
      <!-- S 3D Depth Extrusions -->
      <path d="M 18 260 L 10 275 L 10 375 L 35 375 L 50 290 Z" fill="url(#goldDepth)"/>
      <path d="M 18 360 C 50 395 85 398 118 398 C 165 398 215 385 225 340 L 215 310 C 205 355 165 370 118 370 C 85 370 45 365 20 345 Z" fill="url(#goldDepth)"/>
      <path d="M 118 115 C 85 115 75 130 75 145 C 75 165 95 185 118 200 L 118 215 C 80 198 55 175 55 145 C 55 120 75 95 118 95 Z" fill="url(#goldDepth)"/>

      <!-- S Terminal Bevel Triangles -->
      <polygon points="150,160 215,160 182,130" fill="url(#goldBevelFacet)"/>
      <polygon points="18,260 80,260 50,290" fill="url(#goldBevelFacet)"/>

      <!-- S Outer Light Facet -->
      <!-- From top apex (182, 130) around outer perimeter to bottom apex (50, 290), then along spine ridge back to top apex -->
      <path d="M 182 130
               L 215 160
               C 215 115 180 55 118 55
               C 55 55 18 100 18 150
               C 18 200 50 225 85 242
               C 120 260 152 280 152 312
               C 152 342 135 358 118 358
               C 92 358 75 342 75 312
               L 50 290
               L 18 260
               C 18 325 60 372 118 372
               C 178 372 215 335 215 285
               C 215 230 180 205 145 188
               C 110 170 78 152 78 122
               C 78 95 95 78 118 78
               C 148 78 172 98 182 130 Z" fill="url(#goldLightFacet)"/>

      <!-- S Inner Shade Facet -->
      <!-- From top apex (182, 130) around inner crook to bottom apex (50, 290), then along spine ridge back to top apex -->
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
               C 135 358 152 342 152 312
               C 152 280 120 260 85 242
               C 50 225 18 200 18 150
               C 18 100 55 55 118 55
               C 180 55 215 115 215 160
               L 182 130 Z" fill="url(#goldShadeFacet)"/>
    </g>

    <!-- ========================================== -->
    <!-- 2. LETTER V                                -->
    <!-- ========================================== -->
    <g id="letter-V">
      <!-- V Extrusion Depth -->
      <polygon points="455,10 468,18 400,345 385,335" fill="url(#goldDepth)"/>
      <polygon points="385,335 400,345 388,375 375,365" fill="url(#goldDepth)"/>

      <!-- Left Leg Top Bevel Triangle (points down) -->
      <polygon points="205,10 275,10 245,38" fill="url(#goldBevelFacet)"/>

      <!-- Right Leg Top Bevel Triangle (points down) -->
      <polygon points="385,10 455,10 415,38" fill="url(#goldBevelFacet)"/>

      <!-- Left Leg Outer Face (Light Gold) -->
      <polygon points="205,10 245,38 335,335 305,335" fill="url(#goldLightFacet)"/>

      <!-- Central Valley & Right Leg Inner Face (Warm Amber Shade) -->
      <polygon points="275,10 245,38 335,335 355,335 415,38 385,10 330,240" fill="url(#goldShadeFacet)"/>

      <!-- Right Leg Outer Face (Light Gold Highlight) -->
      <polygon points="455,10 415,38 355,335 385,335" fill="url(#goldLightFacet)"/>

      <!-- Bottom Trapezoid Bevel Wedge -->
      <polygon points="305,335 385,335 375,365 315,365" fill="url(#goldBevelFacet)"/>
    </g>

    <!-- ========================================== -->
    <!-- 3. LETTER C                                -->
    <!-- ========================================== -->
    <g id="letter-C">
      <!-- C 3D Depth Extrusions -->
      <path d="M 600 160 C 570 160 550 185 550 232 C 550 280 570 305 600 305 L 612 318 C 570 318 535 285 535 232 C 535 178 570 148 612 148 Z" fill="url(#goldDepth)"/>
      <path d="M 565 370 C 610 370 645 355 665 305 L 678 315 C 655 370 615 385 565 385 C 520 385 480 365 465 340 L 475 325 C 490 352 525 370 565 370 Z" fill="url(#goldDepth)"/>

      <!-- C Terminal Bevel Triangles -->
      <polygon points="600,160 665,160 632,130" fill="url(#goldBevelFacet)"/>
      <polygon points="600,305 665,305 632,335" fill="url(#goldBevelFacet)"/>

      <!-- C Outer Light Facet -->
      <!-- From top apex (632, 130) along outer perimeter to bottom apex (632, 335), and along spine ridge back to top apex -->
      <path d="M 632 130
               L 665 160
               C 665 110 625 95 565 95
               C 490 95 445 150 445 232
               C 445 315 490 370 565 370
               C 625 370 665 355 665 305
               L 632 335
               C 605 352 580 352 565 352
               C 505 352 475 305 475 232
               C 475 160 505 115 565 115
               C 580 115 605 115 632 130 Z" fill="url(#goldLightFacet)"/>

      <!-- C Inner Shade Facet -->
      <!-- From top apex (632, 130) along inner cutout arc to bottom apex (632, 335), and along spine ridge back to top apex -->
      <path d="M 632 130
               L 600 160
               C 575 160 555 185 555 232
               C 555 280 575 305 600 305
               L 632 335
               C 605 352 580 352 565 352
               C 505 352 475 305 475 232
               C 475 160 505 115 565 115
               C 580 115 605 115 632 130 Z" fill="url(#goldShadeFacet)"/>
    </g>

  </g>
</svg>
'''

with open('scratch/test_svc_square.svg', 'w') as f:
    f.write(svg_code)

subprocess.run(['qlmanage', '-t', '-s', '1500', '-o', 'scratch', 'scratch/test_svc_square.svg'], check=True)
print('Rendered test_svc_square.svg!')
