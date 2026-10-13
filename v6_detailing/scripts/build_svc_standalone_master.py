import cv2
import numpy as np
import subprocess
import xml.etree.ElementTree as ET
import os

print("=" * 60)
print("BUILDING 100% AUTHENTIC STANDALONE SVC WORDMARK")
print("=" * 60)

# 1. Load native reference image
ref_img = cv2.imread('scratch/svc_isolated_reference.png')
ref_h, ref_w = ref_img.shape[:2] # 395 x 725

# Upscale 4x for sub-pixel anti-aliased vectorization
scale = 4
hi = cv2.resize(ref_img, (ref_w * scale, ref_h * scale), interpolation=cv2.INTER_LANCZOS4)
H, W = hi.shape[:2]

def trace_clean_layer(mask, name, blur_k=9, blur_sig=2.5, alphamax=1.0):
    m_u8 = (mask.astype(np.uint8)) * 255
    m_blur = cv2.GaussianBlur(m_u8, (blur_k, blur_k), blur_sig)
    _, m_thresh = cv2.threshold(m_blur, 128, 255, cv2.THRESH_BINARY)
    
    bmp = f'scratch/clean_{name}.bmp'
    svg = f'scratch/clean_{name}.svg'
    cv2.imwrite(bmp, m_thresh)
    subprocess.run(['potrace', '-s', '--invert', '--alphamax', str(alphamax), '--opttolerance', '0.2', '-o', svg, bmp], check=True)
    
    tree = ET.parse(svg)
    paths = []
    for g_elem in tree.getroot().iter('{http://www.w3.org/2000/svg}g'):
        for p in g_elem.iter('{http://www.w3.org/2000/svg}path'):
            paths.append(p.attrib['d'])
    return ' '.join(paths)

# 2. Extract S layers from high-res (x: 0..220*scale)
s_crop = hi[:, :int(220 * scale)]
sb, sg, sr = cv2.split(s_crop)
s_letter = (sr > 120) & (sg > 70) & (sb < 100) & (sr > sb + 45)

s_light = s_letter & (sr >= 225) & (sg >= 175)
s_shade = s_letter & (sr >= 190) & (sg >= 120) & ~s_light
s_bevel = s_letter & (sr >= 150) & (sg >= 85) & ~s_light & ~s_shade
s_depth = s_letter & ~s_light & ~s_shade & ~s_bevel

print("Tracing S...")
s_p_depth = trace_clean_layer(s_depth, 's_depth', blur_k=7, blur_sig=2.0)
s_p_bevel = trace_clean_layer(s_bevel, 's_bevel', blur_k=5, blur_sig=1.5, alphamax=0.6)
s_p_shade = trace_clean_layer(s_shade, 's_shade', blur_k=9, blur_sig=2.5)
s_p_light = trace_clean_layer(s_light, 's_light', blur_k=9, blur_sig=2.5)
s_p_base  = trace_clean_layer(s_letter, 's_base', blur_k=9, blur_sig=2.5)

# 3. Extract C layers from high-res (x: 460*scale..675*scale)
# Cut off right at 675*scale to avoid the shield rim
c_crop = hi[:, int(460 * scale):int(675 * scale)]
cb, cg, cr = cv2.split(c_crop)
c_letter = (cr > 120) & (cg > 70) & (cb < 100) & (cr > cb + 45)

c_light = c_letter & (cr >= 225) & (cg >= 175)
c_shade = c_letter & (cr >= 190) & (cg >= 120) & ~c_light
c_bevel = c_letter & (cr >= 150) & (cg >= 85) & ~c_light & ~c_shade
c_depth = c_letter & ~c_light & ~c_shade & ~c_bevel

print("Tracing C...")
c_p_depth = trace_clean_layer(c_depth, 'c_depth', blur_k=7, blur_sig=2.0)
c_p_bevel = trace_clean_layer(c_bevel, 'c_bevel', blur_k=5, blur_sig=1.5, alphamax=0.6)
c_p_shade = trace_clean_layer(c_shade, 'c_shade', blur_k=9, blur_sig=2.5)
c_p_light = trace_clean_layer(c_light, 'c_light', blur_k=9, blur_sig=2.5)
c_p_base  = trace_clean_layer(c_letter, 'c_base', blur_k=9, blur_sig=2.5)

# 4. Define master SVG builder
# Transform:
# In high-res: potrace maps H = 395 * 4 = 1580
# scale(0.025, -0.025) and translate(0, 395) restores native coordinates (0..725, 0..395)
# In 1000 x 1000 canvas, centered at (500, 500):
# Offset X = 170, Offset Y = 310

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
        poly_stroke = ' stroke="#000000" stroke-width="5" vector-effect="non-scaling-stroke" stroke-linejoin="round"'
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

  {bg}

  <!-- Master SVC Letters Container (Centered: cx=500, cy=500) -->
  <g id="svc-letters" transform="translate(170, 310)">

    <!-- ========================================== -->
    <!-- 1. LETTER S (Authentic Beveled Prism)      -->
    <!-- ========================================== -->
    <g id="letter-S" transform="translate(0, 395) scale(0.025, -0.025)">
      <!-- S 3D Depth Drop Shadow -->
      <path d="{s_p_depth}" fill="{f_depth}"{poly_stroke}/>
      <!-- S Base Solid Letterform (Prevents any gaps) -->
      <path d="{s_p_base}" fill="{f_light}"{poly_stroke}/>
      <!-- S Shaded Inner/Waist Facet -->
      <path d="{s_p_shade}" fill="{f_shade}"{poly_stroke}/>
      <!-- S Terminal Bevel Triangles -->
      <path d="{s_p_bevel}" fill="{f_bevel}"{poly_stroke}/>
    </g>

    <!-- ========================================== -->
    <!-- 2. LETTER V (Pure Geometric Chiseled Prism)-->
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

      <!-- Left Leg Inner Face (Light Gold direct light) -->
      <polygon points="275,10 245,38 335,335 330,240" fill="{f_light}"{poly_stroke}/>

      <!-- Right Leg Face (Warm Amber Shade matching reference) -->
      <polygon points="330,240 335,335 355,335 415,38 385,10" fill="{f_shade}"{poly_stroke}/>
      <polygon points="455,10 415,38 355,335 385,335" fill="{f_shade}"{poly_stroke}/>

      <!-- Bottom Trapezoid Bevel Wedge -->
      <polygon points="305,335 385,335 375,365 315,365" fill="{f_bevel}"{poly_stroke}/>
    </g>

    <!-- ========================================== -->
    <!-- 3. LETTER C (Authentic Beveled Prism)      -->
    <!-- ========================================== -->
    <g id="letter-C" transform="translate(460, 395) scale(0.025, -0.025)">
      <!-- C 3D Depth Drop Shadow -->
      <path d="{c_p_depth}" fill="{f_depth}"{poly_stroke}/>
      <!-- C Base Solid Letterform (Prevents any gaps) -->
      <path d="{c_p_base}" fill="{f_light}"{poly_stroke}/>
      <!-- C Inner Shaded Facet -->
      <path d="{c_p_shade}" fill="{f_shade}"{poly_stroke}/>
      <!-- C Terminal Bevel Triangles -->
      <path d="{c_p_bevel}" fill="{f_bevel}"{poly_stroke}/>
    </g>

  </g>
</svg>'''

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

print("Generated master standalone SVG and PNG assets!")

# Rebuild side-by-side comparison
ref = cv2.imread('scratch/svc_isolated_reference.png')
test = cv2.imread('assets/png/svc-standalone-color.png')

crop_test = test[550:1450, 250:1750]
h = 450
ref_scaled = cv2.resize(ref, (int(ref.shape[1] * h / ref.shape[0]), h), interpolation=cv2.INTER_LANCZOS4)
test_scaled = cv2.resize(crop_test, (int(crop_test.shape[1] * h / crop_test.shape[0]), h), interpolation=cv2.INTER_LANCZOS4)

divider = np.full((h, 24, 3), [20, 30, 60], dtype=np.uint8)
comp = np.hstack([ref_scaled, divider, test_scaled])
cv2.imwrite('scratch/svc_standalone_master_comparison.png', comp)
print('Saved scratch/svc_standalone_master_comparison.png!')
