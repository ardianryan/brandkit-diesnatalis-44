import subprocess
import xml.etree.ElementTree as ET
import cv2
import numpy as np

# Load S facets and C facets from previous step
def get_path_d(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()
    paths = []
    for g in root.iter('{http://www.w3.org/2000/svg}g'):
        for p in g.iter('{http://www.w3.org/2000/svg}path'):
            paths.append(p.attrib['d'])
    return ' '.join(paths)

s_depth = get_path_d('scratch/h_s_depth.svg')
s_bevel = get_path_d('scratch/h_s_bevel.svg')
s_shade = get_path_d('scratch/h_s_shade.svg')
s_light = get_path_d('scratch/h_s_light.svg')

c_depth = get_path_d('scratch/h_c_depth.svg')
c_bevel = get_path_d('scratch/h_c_bevel.svg')
c_shade = get_path_d('scratch/h_c_shade.svg')
c_light = get_path_d('scratch/h_c_light.svg')

# Scale and translation:
# Native crop height = 395 * 4 = 1580
# Potrace output is: translate(0, 1580) scale(0.1, -0.1)
# That produces native image coordinates (0..725, 0..395).
# On 1000 x 1000 canvas, centered at (500, 500):
# Letters bounds: x=15..665 (w=650), y=10..370 (h=360)
# Offset: tx = 175, ty = 320

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
        poly_stroke = ' stroke="#000000" stroke-width="4" stroke-linejoin="round"'
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
    <!-- Metallic Gold Facets calibrated from original hand draw SVC.PNG -->
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

  <!-- Master SVC Letters Container -->
  <g id="svc-letters" transform="translate(170, 315)">
    
    <!-- 1. LETTER S (Authentic Facets) -->
    <g id="letter-S" transform="translate(0, 395) scale(0.025, -0.025)">
      <path d="{s_depth}" fill="{f_depth}"{poly_stroke}/>
      <path d="{s_bevel}" fill="{f_bevel}"{poly_stroke}/>
      <path d="{s_shade}" fill="{f_shade}"{poly_stroke}/>
      <path d="{s_light}" fill="{f_light}"{poly_stroke}/>
    </g>

    <!-- 2. LETTER V (Pure Geometric Prism) -->
    <g id="letter-V">
      <!-- V Extrusion Depth -->
      <polygon points="455,10 468,18 400,345 385,335" fill="{f_depth}"{poly_stroke}/>
      <polygon points="385,335 400,345 388,375 375,365" fill="{f_depth}"{poly_stroke}/>

      <!-- Left Leg Top Bevel Triangle -->
      <polygon points="205,10 275,10 245,38" fill="{f_bevel}"{poly_stroke}/>

      <!-- Right Leg Top Bevel Triangle -->
      <polygon points="385,10 455,10 415,38" fill="{f_bevel}"{poly_stroke}/>

      <!-- Left Leg Outer Face (Light Gold direct light) -->
      <polygon points="205,10 245,38 335,335 305,335" fill="{f_light}"{poly_stroke}/>

      <!-- Left Leg Inner Face (Light Gold tone) -->
      <polygon points="275,10 245,38 335,335 330,240" fill="{f_light}"{poly_stroke}/>

      <!-- Right Leg Face (Warm Amber Shade matching reference) -->
      <polygon points="330,240 335,335 355,335 415,38 385,10" fill="{f_shade}"{poly_stroke}/>
      <polygon points="455,10 415,38 355,335 385,335" fill="{f_shade}"{poly_stroke}/>

      <!-- Bottom Trapezoid Bevel Wedge -->
      <polygon points="305,335 385,335 375,365 315,365" fill="{f_bevel}"{poly_stroke}/>
    </g>

    <!-- 3. LETTER C (Authentic Facets) -->
    <g id="letter-C" transform="translate(460, 395) scale(0.025, -0.025)">
      <path d="{c_depth}" fill="{f_depth}"{poly_stroke}/>
      <path d="{c_bevel}" fill="{f_bevel}"{poly_stroke}/>
      <path d="{c_shade}" fill="{f_shade}"{poly_stroke}/>
      <path d="{c_light}" fill="{f_light}"{poly_stroke}/>
    </g>

  </g>
</svg>'''

for mode in ["color", "white", "dark"]:
    svg_data = generate_svg(mode)
    svg_file = f"assets/svg/svc-standalone-{mode}.svg"
    with open(svg_file, "w") as f:
        f.write(svg_data)
    png_file = f"assets/png/svc-standalone-{mode}.png"
    subprocess.run(["qlmanage", "-t", "-s", "2000", "-o", "scratch", svg_file], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rendered = f"scratch/svc-standalone-{mode}.svg.png"
    im = cv2.imread(rendered)
    if im is not None:
        cv2.imwrite(png_file, im)

print("Saved standalone SVG and PNG assets!")

# Side-by-side comparison
ref = cv2.imread('scratch/svc_isolated_reference.png')
test = cv2.imread('assets/png/svc-standalone-color.png')

crop_test = test[600:1400, 300:1700]
h = 450
ref_scaled = cv2.resize(ref, (int(ref.shape[1] * h / ref.shape[0]), h), interpolation=cv2.INTER_LANCZOS4)
test_scaled = cv2.resize(crop_test, (int(crop_test.shape[1] * h / crop_test.shape[0]), h), interpolation=cv2.INTER_LANCZOS4)

divider = np.full((h, 24, 3), [20, 30, 60], dtype=np.uint8)
comp = np.hstack([ref_scaled, divider, test_scaled])
cv2.imwrite('scratch/svc_standalone_final_comparison.png', comp)
print('Saved scratch/svc_standalone_final_comparison.png!')
