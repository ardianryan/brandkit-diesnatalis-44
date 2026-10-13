#!/usr/bin/env python3
"""
build_pure_smooth_svc.py
========================
Builds 100% mathematically smooth, pristine vector SVG and high-res PNG assets
for the SVC standalone wordmark (Smansage Volleyball Competition), matching
'hand draw SVC.PNG' and AI-assisted athletic typography with perfect geometric precision.

Features:
- Pure parametric cubic Bezier curves and geometric polygons
- Zero potrace raster stepping, zero bumps ("tidak mblidut / bergelombang")
- Flawless, authentic athletic typography for S, V, and C
- Continuous central ridge lines dividing each letter into chiseled bevel facets:
    * Light Facet (goldLightFacet)
    * Shade Facet (goldShadeFacet)
    * Terminal Bevel Wedges (goldBevelFacet)
- Produces color, white (stencil outline), and dark monochrome variants
"""

import os
import subprocess
import cv2
import numpy as np
from scipy.interpolate import splprep, splev

# Curve fitting routines
def fit_cubic_bezier(points):
    p0 = points[0]
    p3 = points[-1]
    d = np.linalg.norm(np.diff(points, axis=0), axis=1)
    t = np.concatenate([[0], np.cumsum(d)])
    if t[-1] == 0:
        return p0, p0, p3, p3, 0.0, 0
    t /= t[-1]
    
    b1 = 3 * (1 - t)**2 * t
    b2 = 3 * (1 - t) * t**2
    A = np.column_stack([b1, b2])
    
    rhs_x = points[:, 0] - (1 - t)**3 * p0[0] - t**3 * p3[0]
    rhs_y = points[:, 1] - (1 - t)**3 * p0[1] - t**3 * p3[1]
    
    (p1_x, p2_x), _, _, _ = np.linalg.lstsq(A, rhs_x, rcond=None)
    (p1_y, p2_y), _, _, _ = np.linalg.lstsq(A, rhs_y, rcond=None)
    
    p1 = np.array([p1_x, p1_y])
    p2 = np.array([p2_x, p2_y])
    
    fitted = (1-t[:,None])**3 * p0 + 3*(1-t[:,None])**2 * t[:,None] * p1 + 3*(1-t[:,None]) * t[:,None]**2 * p2 + t[:,None]**3 * p3
    errors = np.linalg.norm(fitted - points, axis=1)
    max_idx = np.argmax(errors)
    return p0, p1, p2, p3, errors[max_idx], max_idx

def fit_curve_recursive(points, max_err=1.2):
    if len(points) <= 2:
        p0 = points[0]
        p3 = points[-1]
        return [(p0, p0, p3, p3)]
    
    p0, p1, p2, p3, err, split_idx = fit_cubic_bezier(points)
    if err <= max_err or len(points) < 8 or split_idx == 0 or split_idx == len(points) - 1:
        return [(p0, p1, p2, p3)]
    
    left = fit_curve_recursive(points[:split_idx+1], max_err)
    right = fit_curve_recursive(points[split_idx:], max_err)
    return left + right

def beziers_to_d(beziers, start_m=True):
    parts = []
    if start_m:
        parts.append(f"M {beziers[0][0][0]:.1f} {beziers[0][0][1]:.1f}")
    for b in beziers:
        parts.append(f"C {b[1][0]:.1f} {b[1][1]:.1f} {b[2][0]:.1f} {b[2][1]:.1f} {b[3][0]:.1f} {b[3][1]:.1f}")
    return " ".join(parts)

# =========================================================================
# 1. PROCESS LETTER S
# =========================================================================
print("Extracting and fitting Letter S...")
img_s = cv2.imread('scratch/isolated_clean_S.png')
gray_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2GRAY)
mask_s = (gray_s < 240).astype(np.uint8)
cnts_s, _ = cv2.findContours(mask_s, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnt_s = max(cnts_s, key=cv2.contourArea)[:, 0, :]

# Continuous central ridge spine from top apex (286, 150) to bottom apex (69, 412)
spine_pts_s = np.array([
    [286.0, 150.0],
    [245.0, 95.0],
    [175.0, 68.5],
    [110.0, 95.0],
    [85.0, 150.0],
    [88.0, 200.0],
    [115.0, 240.0],
    [165.0, 270.0], # Waist center
    [225.0, 300.0],
    [265.0, 340.0],
    [268.0, 390.0],
    [245.0, 450.0],
    [175.0, 490.5],
    [110.0, 470.0],
    [69.0, 412.0]
])
tck_s, _ = splprep([spine_pts_s[:, 0], spine_pts_s[:, 1]], s=0, k=3)
u_s = np.linspace(0, 1, 300)
x_spine_s, y_spine_s = splev(u_s, tck_s)
s_spine = np.column_stack([x_spine_s, y_spine_s])

# Side 1 (Light Gold boundary: 1926 -> 0 -> 713)
side1_pts_s = np.vstack([cnt_s[1926:], cnt_s[:714]])
side1_pts_s[0] = [345.0, 194.0]
side1_pts_s[-1] = [128.0, 368.0]

# Side 2 (Shade Gold boundary: 841 -> 1802)
side2_pts_s = cnt_s[841:1803]
side2_pts_s[0] = [10.0, 368.0]
side2_pts_s[-1] = [227.0, 194.0]

bez_s_side1 = fit_curve_recursive(side1_pts_s, max_err=1.2)
bez_s_side2 = fit_curve_recursive(side2_pts_s, max_err=1.2)
bez_s_spine_fwd = fit_curve_recursive(s_spine, max_err=1.2)
bez_s_spine_rev = fit_curve_recursive(s_spine[::-1], max_err=1.2)

s_facet_light_d = "M 286.0 150.0 " + \
                  "L 345.0 194.0 " + \
                  beziers_to_d(bez_s_side1, start_m=False) + \
                  " L 69.0 412.0 " + \
                  beziers_to_d(bez_s_spine_rev, start_m=False) + " Z"

s_facet_shade_d = "M 69.0 412.0 " + \
                  "L 10.0 368.0 " + \
                  beziers_to_d(bez_s_side2, start_m=False) + \
                  " L 286.0 150.0 " + \
                  beziers_to_d(bez_s_spine_fwd, start_m=False) + " Z"

# =========================================================================
# 2. PROCESS LETTER C (EXACT APPROVED V11 RESTORATION)
# =========================================================================
print("Extracting and fitting Letter C (Restoring approved v11 natural curvature)...")
img_c = cv2.imread('scratch/isolated_clean_C.png')
gray_c = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)
mask_c = (gray_c < 240).astype(np.uint8)
cnts_c, _ = cv2.findContours(mask_c, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnt_c = max(cnts_c, key=cv2.contourArea)[:, 0, :]

# Outer natural athletic curve
c_seg_out = np.vstack([cnt_c[1808:], cnt_c[:984]])
c_seg_out[0] = [354.0, 206.0]
c_seg_out[-1] = [354.0, 355.0]

# Inner counter curve
c_seg_in = cnt_c[1130:1671][::-1]
c_seg_in[0] = [226.0, 206.0]
c_seg_in[-1] = [226.0, 355.0]

# Compute exact v11 medial ridge line (0.5 * (outer + inner)) for natural dual-facet chiseled bevel
N = 100
t_eval = np.linspace(0, 1, N)
d_c_out = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(c_seg_out, axis=0), axis=1))])
d_c_out /= d_c_out[-1]
d_c_in = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(c_seg_in, axis=0), axis=1))])
d_c_in /= d_c_in[-1]

c_out_resamp = np.column_stack([np.interp(t_eval, d_c_out, c_seg_out[:, 0]), np.interp(t_eval, d_c_out, c_seg_out[:, 1])])
c_in_resamp = np.column_stack([np.interp(t_eval, d_c_in, c_seg_in[:, 0]), np.interp(t_eval, d_c_in, c_seg_in[:, 1])])

c_ridge = 0.5 * (c_out_resamp + c_in_resamp)
c_ridge[0] = [290.0, 168.0]
c_ridge[-1] = [290.0, 393.0]

bez_c_out = fit_curve_recursive(c_seg_out, max_err=1.2)
bez_c_in = fit_curve_recursive(c_seg_in, max_err=1.2)
bez_c_ridge_rev = fit_curve_recursive(c_ridge[::-1], max_err=1.2)

# C Outer Facet: (290, 168) -> (354, 206) -> c_out -> (354, 355) -> (290, 393) -> c_ridge_rev -> (290, 168)
c_outer_facet_d = "M 290.0 168.0 " + \
                  "L 354.0 206.0 " + \
                  beziers_to_d(bez_c_out, start_m=False) + \
                  " L 290.0 393.0 " + \
                  beziers_to_d(bez_c_ridge_rev, start_m=False) + " Z"

# C Inner Facet: (290, 168) -> (226, 206) -> c_in -> (226, 355) -> (290, 393) -> c_ridge_rev -> (290, 168)
c_inner_facet_d = "M 290.0 168.0 " + \
                  "L 226.0 206.0 " + \
                  beziers_to_d(bez_c_in, start_m=False) + \
                  " L 290.0 393.0 " + \
                  beziers_to_d(bez_c_ridge_rev, start_m=False) + " Z"

# Master SVG Generator
def build_smooth_svc_svg(mode="color"):
    is_color = (mode == "color")
    is_white = (mode == "white")
    
    if is_color:
        f_light = "url(#goldLightFacet)"
        f_shade = "url(#goldShadeFacet)"
        f_bevel = "url(#goldBevelFacet)"
        stroke_attr = ' stroke="none"'
    elif is_white:
        f_light = "#FFFFFF"
        f_shade = "#E2E8F0"
        f_bevel = "#CBD5E1"
        stroke_attr = ' stroke="#000000" stroke-width="5" vector-effect="non-scaling-stroke" stroke-linejoin="round"'
    else: # dark
        f_light = "#E2E8F0"
        f_shade = "#94A3B8"
        f_bevel = "#64748B"
        stroke_attr = ' stroke="none"'

    bg = '<rect width="1000" height="1000" fill="#0A0E17"/>' if is_color else ('<rect width="1000" height="1000" fill="#020408"/>' if not is_white else '')

    s_scale = 0.6826
    v_scale = 0.6826
    c_scale = 0.6826
    
    s_tx, s_ty = 104.0, 315.0
    v_tx, v_ty = 357.0, 315.0
    c_tx, c_ty = 660.0, 315.0

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="1000" height="1000">
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
  </defs>

  {bg}

  <!-- Master SVC Letters Container (Centered at cx=500, cy=500) -->
  <g id="svc-letters">

    <!-- ========================================================================= -->
    <!-- 1. LETTER S (True Athletic Letterform - Ridge-aligned chiseled bevels)    -->
    <!-- ========================================================================= -->
    <g id="letter-S" transform="translate({s_tx:.1f}, {s_ty:.1f}) scale({s_scale:.4f})">
      <!-- Light Gold Facet (Facing Up/Top-Left) -->
      <path d="{s_facet_light_d}" fill="{f_light}"{stroke_attr}/>

      <!-- Shade Gold Facet (Facing Down/Bottom-Right) -->
      <path d="{s_facet_shade_d}" fill="{f_shade}"{stroke_attr}/>

      <!-- Top Terminal Bevel Wedge -->
      <polygon points="227,194 345,194 286,150" fill="{f_bevel}"{stroke_attr}/>

      <!-- Bottom Terminal Bevel Wedge -->
      <polygon points="10,368 128,368 69,412" fill="{f_bevel}"{stroke_attr}/>
    </g>

    <!-- ========================================================================= -->
    <!-- 2. LETTER V (Pure Geometric Chiseled Prism - Mathematically Symmetrical) -->
    <!-- ========================================================================= -->
    <g id="letter-V" transform="translate({v_tx:.1f}, {v_ty:.1f}) scale({v_scale:.4f})">
      <!-- Top Left Bevel Wedge (Points down to center ridge) -->
      <polygon points="10,11 139,11 74,48" fill="{f_bevel}"{stroke_attr}/>

      <!-- Top Right Bevel Wedge (Points down to center ridge) -->
      <polygon points="298,11 427,11 362,48" fill="{f_bevel}"{stroke_attr}/>

      <!-- Left Leg Outer Face (Warm Amber Shade - matching reference lighting) -->
      <polygon points="10,11 74,48 187.4,505 156.3,505" fill="{f_shade}"{stroke_attr}/>

      <!-- Left Leg Inner Face (Radiant Light Gold - illuminated inner face) -->
      <polygon points="139,11 74,48 187.4,505 218.5,505 218.5,352" fill="{f_light}"{stroke_attr}/>

      <!-- Right Leg Inner Face (Radiant Light Gold - illuminated inner face meeting at center) -->
      <polygon points="218.5,352 218.5,505 249.6,505 362,48 298,11" fill="{f_light}"{stroke_attr}/>

      <!-- Right Leg Outer Face (Warm Amber Shade - matching reference lighting) -->
      <polygon points="427,11 362,48 249.6,505 280.7,505" fill="{f_shade}"{stroke_attr}/>

      <!-- Bottom Bevel Wedge (Proportional, symmetrical athletic chamfer) -->
      <polygon points="156.3,505 280.7,505 270,541 167,541" fill="{f_bevel}"{stroke_attr}/>
    </g>

    <!-- ========================================================================= -->
    <!-- 3. LETTER C (True Athletic Collegiate C - Dual Chiseled Facets)           -->
    <!-- ========================================================================= -->
    <g id="letter-C" transform="translate({c_tx:.1f}, {c_ty:.1f}) scale({c_scale:.4f})">
      <!-- Outer Face (Light Gold) -->
      <path d="{c_outer_facet_d}" fill="{f_light}"{stroke_attr}/>

      <!-- Inner Face (Warm Amber Shade) -->
      <path d="{c_inner_facet_d}" fill="{f_shade}"{stroke_attr}/>

      <!-- Top Terminal Bevel Wedge -->
      <polygon points="226,206 354,206 290,168" fill="{f_bevel}"{stroke_attr}/>

      <!-- Bottom Terminal Bevel Wedge -->
      <polygon points="226,355 354,355 290,393" fill="{f_bevel}"{stroke_attr}/>
    </g>

  </g>
</svg>'''

os.makedirs("assets/svg", exist_ok=True)
os.makedirs("assets/png", exist_ok=True)

for mode in ["color", "white", "dark"]:
    svg_data = build_smooth_svc_svg(mode)
    svg_file = f"assets/svg/svc-standalone-{mode}.svg"
    with open(svg_file, "w") as f:
        f.write(svg_data)
    
    png_file = f"assets/png/svc-standalone-{mode}.png"
    subprocess.run(["qlmanage", "-t", "-s", "2000", "-o", "scratch", svg_file], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    rendered = f"scratch/svc-standalone-{mode}.svg.png"
    if os.path.exists(rendered):
        im = cv2.imread(rendered)
        cv2.imwrite(png_file, im)

print("Saved assets/svg/svc-standalone-*.svg and assets/png/svc-standalone-*.png!")

# Rebuild 3-way comparison
ref_orig = cv2.imread('scratch/svc_native_crop.png')
ref_ai = cv2.imread('scratch/svc_ai_reference.jpg')
test = cv2.imread('assets/png/svc-standalone-color.png')

crop_test = test[550:1450, 180:1820]
h = 400

orig_scaled = cv2.resize(ref_orig, (int(ref_orig.shape[1] * h / ref_orig.shape[0]), h), interpolation=cv2.INTER_LANCZOS4)
ai_scaled = cv2.resize(ref_ai, (int(ref_ai.shape[1] * h / ref_ai.shape[0]), h), interpolation=cv2.INTER_LANCZOS4)
test_scaled = cv2.resize(crop_test, (int(crop_test.shape[1] * h / crop_test.shape[0]), h), interpolation=cv2.INTER_LANCZOS4)

divider = np.full((h, 15, 3), [20, 30, 60], dtype=np.uint8)
comp = np.hstack([orig_scaled, divider, ai_scaled, divider, test_scaled])
cv2.imwrite('scratch/svc_3way_perfect_final.png', comp)
print('Saved scratch/svc_3way_perfect_final.png!')
