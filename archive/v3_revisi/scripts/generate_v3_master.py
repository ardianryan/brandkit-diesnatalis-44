import cv2
import numpy as np
import os
import subprocess

def fit_cubic_bezier(pts):
    P0 = pts[0].astype(float)
    P3 = pts[-1].astype(float)
    N = len(pts)
    if N <= 2:
        return P0, (P0*2 + P3)/3, (P0 + P3*2)/3, P3, 0.0
    dists = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    total_len = np.sum(dists)
    if total_len < 1e-4:
        return P0, P0, P3, P3, 0.0
    u = np.concatenate([[0], np.cumsum(dists)]) / total_len
    b0 = (1 - u)**3
    b1 = 3 * (1 - u)**2 * u
    b2 = 3 * (1 - u) * u**2
    b3 = u**3
    target = pts - np.outer(b0, P0) - np.outer(b3, P3)
    A = np.column_stack([b1, b2])
    res_x, _, _, _ = np.linalg.lstsq(A, target[:, 0], rcond=None)
    res_y, _, _, _ = np.linalg.lstsq(A, target[:, 1], rcond=None)
    P1 = np.array([res_x[0], res_y[0]])
    P2 = np.array([res_x[1], res_y[1]])
    fitted = np.outer(b0, P0) + np.outer(b1, P1) + np.outer(b2, P2) + np.outer(b3, P3)
    err = np.max(np.linalg.norm(pts - fitted, axis=1))
    return P0, P1, P2, P3, err

def fit_curve_recursive(pts, max_err=1.8):
    if len(pts) <= 4:
        p0, p1, p2, p3, err = fit_cubic_bezier(pts)
        return [(p0, p1, p2, p3)]
    p0, p1, p2, p3, err = fit_cubic_bezier(pts)
    if err <= max_err:
        return [(p0, p1, p2, p3)]
    mid = len(pts) // 2
    return fit_curve_recursive(pts[:mid+1], max_err) + fit_curve_recursive(pts[mid:], max_err)

def detect_corners(contour_pts, window=16, max_interior_angle=140.0):
    N = len(contour_pts)
    if N < 20:
        return []
    interior_angles = []
    w = min(window, N // 4)
    for i in range(N):
        p_prev = contour_pts[(i - w) % N]
        p_curr = contour_pts[i]
        p_next = contour_pts[(i + w) % N]
        v1 = p_prev - p_curr
        v2 = p_next - p_curr
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)
        if norm1 < 1e-5 or norm2 < 1e-5:
            interior_angles.append(180.0)
            continue
        cos_ang = np.dot(v1, v2) / (norm1 * norm2)
        ang = np.degrees(np.arccos(np.clip(cos_ang, -1.0, 1.0)))
        interior_angles.append(ang)
    interior_angles = np.array(interior_angles)
    corners = []
    suppress_r = w
    for i in range(N):
        ang_i = interior_angles[i]
        if ang_i <= max_interior_angle:
            is_min = True
            for offset in range(-suppress_r, suppress_r + 1):
                if offset == 0: continue
                if interior_angles[(i + offset) % N] < ang_i:
                    is_min = False
                    break
            if is_min:
                corners.append((i, ang_i, contour_pts[i]))
    return corners

def sharpen_apex(contour_pts, corner_idx, window=22):
    N = len(contour_pts)
    w = min(window, N // 6)
    if w < 6:
        return contour_pts[corner_idx].astype(float)
    p_in = np.array([contour_pts[(corner_idx - w + j) % N] for j in range(w - 3)])
    p_out = np.array([contour_pts[(corner_idx + 3 + j) % N] for j in range(w - 3)])
    vx1, vy1, x0_1, y0_1 = cv2.fitLine(p_in, cv2.DIST_L2, 0, 0.01, 0.01)
    vx2, vy2, x0_2, y0_2 = cv2.fitLine(p_out, cv2.DIST_L2, 0, 0.01, 0.01)
    A = np.array([[vx1[0], -vx2[0]], [vy1[0], -vy2[0]]])
    B = np.array([x0_2[0] - x0_1[0], y0_2[0] - y0_1[0]])
    det = A[0,0]*A[1,1] - A[0,1]*A[1,0]
    if abs(det) < 1e-4:
        return contour_pts[corner_idx].astype(float)
    t = np.linalg.solve(A, B)
    intersect = np.array([x0_1[0] + t[0] * vx1[0], y0_1[0] + t[0] * vy1[0]])
    if np.linalg.norm(intersect - contour_pts[corner_idx]) > 20.0:
        return contour_pts[corner_idx].astype(float)
    return intersect

def contour_to_svg_path(contour_pts, max_bezier_err=1.8):
    N = len(contour_pts)
    if N < 8:
        return ''
    corners = detect_corners(contour_pts, window=16, max_interior_angle=140.0)
    corners = sorted(corners, key=lambda x: x[0])
    if len(corners) < 3:
        corner_indices = [0, N//3, 2*N//3]
    else:
        corner_indices = [c[0] for c in corners]
    num_c = len(corner_indices)
    corner_points = []
    for c_idx in corner_indices:
        ang = next((c[1] for c in corners if c[0] == c_idx), 180.0)
        if ang < 85.0:
            sharp_pt = sharpen_apex(contour_pts, c_idx, window=22)
            corner_points.append(sharp_pt)
        else:
            corner_points.append(contour_pts[c_idx].astype(float))
            
    path_d = []
    for i in range(num_c):
        idx_start = corner_indices[i]
        idx_end = corner_indices[(i + 1) % num_c]
        pt_start = corner_points[i]
        pt_end = corner_points[(i + 1) % num_c]
        if idx_end > idx_start:
            seg_pts = contour_pts[idx_start : idx_end + 1].astype(float).copy()
        else:
            seg_pts = np.vstack([contour_pts[idx_start:], contour_pts[:idx_end + 1]]).astype(float)
        seg_pts[0] = pt_start
        seg_pts[-1] = pt_end
        beziers = fit_curve_recursive(seg_pts, max_err=max_bezier_err)
        if i == 0:
            path_d.append(f'M {beziers[0][0][0]:.2f} {beziers[0][0][1]:.2f}')
        for b in beziers:
            path_d.append(f'C {b[1][0]:.2f} {b[1][1]:.2f}, {b[2][0]:.2f} {b[2][1]:.2f}, {b[3][0]:.2f} {b[3][1]:.2f}')
    path_d.append('Z')
    return ' '.join(path_d)

print('Reading master raster IMG_2172.PNG...')
img = cv2.imread('IMG_2172.PNG')
is_fg = np.any(img < 240, axis=2).astype(np.uint8) * 255

# Morphological smoothing to remove raster pixel-staircases while preserving sharp corners
kernel_3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fg_smooth = cv2.morphologyEx(is_fg, cv2.MORPH_CLOSE, kernel_3)
fg_smooth = cv2.morphologyEx(fg_smooth, cv2.MORPH_OPEN, kernel_3)

# 1. Base silhouette contours
cnts, _ = cv2.findContours(fg_smooth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
major_cnts = sorted([c for c in cnts if cv2.contourArea(c) > 50000], key=cv2.contourArea, reverse=True)
c0 = major_cnts[0].reshape(-1, 2)  # Right 4
c1 = major_cnts[1].reshape(-1, 2)  # Left 4

print('Reconstructing silhouette curves with cubic Beziers & sharp corners...')
path_sil_0 = contour_to_svg_path(c0, max_bezier_err=1.8)
path_sil_1 = contour_to_svg_path(c1, max_bezier_err=1.8)
path_silhouette = f'{path_sil_0} {path_sil_1}'

# 2. Extract facet layers using bilateral filter for clean tone borders
print('Segmenting facet color layers...')
filtered = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
centers = np.array([
    [17, 137, 212],   # 0: #D48911
    [23, 157, 224],   # 1: #E09D17
    [56, 197, 245],   # 2: #F5C538
    [96, 209, 247]    # 3: #F7D160
], dtype=np.float32)

fg_pixels = filtered.astype(np.float32)
dists = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.float32)
for i in range(4):
    dists[:, :, i] = np.sum((fg_pixels - centers[i])**2, axis=2)
closest = np.argmin(dists, axis=2)

def extract_layer_paths(min_level):
    m = ((closest >= min_level) & (is_fg > 0)).astype(np.uint8) * 255
    m_clean = cv2.morphologyEx(m, cv2.MORPH_OPEN, kernel_3)
    m_clean = cv2.morphologyEx(m_clean, cv2.MORPH_CLOSE, kernel_3)
    cnts_m, _ = cv2.findContours(m_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    major_m = [c.reshape(-1, 2) for c in cnts_m if cv2.contourArea(c) > 2000]
    paths = []
    for c in major_m:
        paths.append(contour_to_svg_path(c, max_bezier_err=2.0))
    return ' '.join(paths)

print('Fitting cubic Beziers to Marigold layer (#E09D17)...')
path_marigold = extract_layer_paths(min_level=1)

print('Fitting cubic Beziers to Vivid Gold layer (#F5C538)...')
path_vivid = extract_layer_paths(min_level=2)

print('Fitting cubic Beziers to Champagne layer (#F7D160)...')
path_champagne = extract_layer_paths(min_level=3)

print('Assembling Master Final SVG (v3)...')

# Master SVG
master_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Master Final Vector (v3 Precise Arcs)</title>
  <defs>
    <linearGradient id="depthGrad" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <style>
      .facet-base {{ fill: url(#depthGrad); }}
      .facet-marigold {{ fill: #E09D17; }}
      .facet-vivid {{ fill: #F5C538; }}
      .facet-champagne {{ fill: #F7D160; }}
      .facet-highlight {{ fill: #FDF39D; opacity: 0.8; }}
    </style>
  </defs>
  <g id="diesnat44-v3-symbol">
    <path id="facet-base" class="facet-base" d="{path_silhouette}" />
    <path id="facet-marigold" class="facet-marigold" d="{path_marigold}" />
    <path id="facet-vivid" class="facet-vivid" d="{path_vivid}" />
    <path id="facet-champagne" class="facet-champagne" d="{path_champagne}" />
  </g>
</svg>'''

with open('v3_revisi/svg/logo-v3-master.svg', 'w') as f:
    f.write(master_svg)

# Grid Blueprint SVG
grid_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Master Vector with Geometric Construction Grid (v3)</title>
  <defs>
    <linearGradient id="depthGradGrid" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <style>
      .facet-base {{ fill: url(#depthGradGrid); }}
      .facet-marigold {{ fill: #E09D17; }}
      .facet-vivid {{ fill: #F5C538; }}
      .facet-champagne {{ fill: #F7D160; }}
      
      .grid-circle-major {{ fill: none; stroke: #38BDF8; stroke-width: 2; stroke-dasharray: 8,5; opacity: 0.85; }}
      .grid-circle-minor {{ fill: none; stroke: #F59E0B; stroke-width: 1.5; stroke-dasharray: 6,4; opacity: 0.75; }}
      .grid-axis {{ fill: none; stroke: rgba(255,255,255,0.3); stroke-width: 1.2; stroke-dasharray: 4,4; }}
      .grid-tangent {{ fill: none; stroke: #EC4899; stroke-width: 1.8; stroke-dasharray: 8,6; opacity: 0.8; }}
      .grid-center {{ fill: #38BDF8; }}
    </style>
  </defs>
  <g id="diesnat44-v3-symbol">
    <path id="facet-base" class="facet-base" d="{path_silhouette}" />
    <path id="facet-marigold" class="facet-marigold" d="{path_marigold}" />
    <path id="facet-vivid" class="facet-vivid" d="{path_vivid}" />
    <path id="facet-champagne" class="facet-champagne" d="{path_champagne}" />
  </g>
  <g id="construction-grid">
    <!-- Circle 1: Eagle Back Arc R=247px centered at (733, 793) -->
    <circle cx="733" cy="793" r="247" class="grid-circle-major" />
    <circle cx="733" cy="793" r="4" class="grid-center" />

    <!-- Circle 2: Outer Flame Arc R=163px centered at (1404, 1109) -->
    <circle cx="1404" cy="1109" r="163" class="grid-circle-major" />
    <circle cx="1404" cy="1109" r="4" class="grid-center" />

    <!-- Circle 3: Tail Spiral Arc R=133px centered at (1060, 1640) matching actual tail curve -->
    <circle cx="1060" cy="1640" r="133" class="grid-circle-major" />
    <circle cx="1060" cy="1640" r="4" class="grid-center" />

    <!-- Circle 4: Flame 1 Arc R=310px centered at (1050, 680) -->
    <circle cx="1050" cy="680" r="310" class="grid-circle-minor" />

    <!-- Circle 5: Flame 2 Arc R=220px centered at (1220, 950) -->
    <circle cx="1220" cy="950" r="220" class="grid-circle-minor" />

    <!-- Circle 6: Beak Arc R=90px centered at (540, 1200) -->
    <circle cx="540" cy="1200" r="90" class="grid-circle-minor" />

    <!-- Axes & Tangents -->
    <line x1="200" y1="1024" x2="1848" y2="1024" class="grid-axis" />
    <line x1="1024" y1="200" x2="1024" y2="1848" class="grid-axis" />
    <line x1="464" y1="1776" x2="1534" y2="382" class="grid-tangent" />
  </g>
</svg>'''

with open('v3_revisi/svg/logo-v3-with-grid.svg', 'w') as f:
    f.write(grid_svg)

# Tight Bounding Box SVG
# Bounding box is approximately x: 464..1534, y: 382..1785
tight_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="460 375 1080 1420" width="1080" height="1420">
  <title>Dies Natalis 44 - Tight Symbol Vector (v3)</title>
  <defs>
    <linearGradient id="depthGradTight" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <style>
      .facet-base {{ fill: url(#depthGradTight); }}
      .facet-marigold {{ fill: #E09D17; }}
      .facet-vivid {{ fill: #F5C538; }}
      .facet-champagne {{ fill: #F7D160; }}
    </style>
  </defs>
  <g id="diesnat44-v3-tight">
    <path id="facet-base" class="facet-base" d="{path_silhouette}" />
    <path id="facet-marigold" class="facet-marigold" d="{path_marigold}" />
    <path id="facet-vivid" class="facet-vivid" d="{path_vivid}" />
    <path id="facet-champagne" class="facet-champagne" d="{path_champagne}" />
  </g>
</svg>'''

with open('v3_revisi/svg/logo-v3-tight.svg', 'w') as f:
    f.write(tight_svg)

# Line-cut SVG
linecut_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Line-Cut Outline Vector (v3)</title>
  <style>
    .linecut-path {{ fill: none; stroke: #111827; stroke-width: 6; stroke-linejoin: round; stroke-linecap: round; }}
  </style>
  <g id="diesnat44-v3-linecut">
    <path class="linecut-path" d="{path_silhouette}" />
    <path class="linecut-path" stroke-width="4" d="{path_marigold}" />
    <path class="linecut-path" stroke-width="4" d="{path_vivid}" />
    <path class="linecut-path" stroke-width="4" d="{path_champagne}" />
  </g>
</svg>'''

with open('v3_revisi/svg/logo-v3-linecut.svg', 'w') as f:
    f.write(linecut_svg)

# Monochrome Black SVG
mono_black_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Monochrome Black (v3)</title>
  <path fill="#111827" d="{path_silhouette}" />
</svg>'''

with open('v3_revisi/svg/logo-v3-monochrome-black.svg', 'w') as f:
    f.write(mono_black_svg)

# Monochrome White SVG
mono_white_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Monochrome White (v3)</title>
  <path fill="#FFFFFF" d="{path_silhouette}" />
</svg>'''

with open('v3_revisi/svg/logo-v3-monochrome-white.svg', 'w') as f:
    f.write(mono_white_svg)

# Typography outlines for Horizontal & Vertical lockups
# We can embed the symbol directly into horizontal and vertical SVGs
horiz_color_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2800 1200" width="2800" height="1200">
  <title>Dies Natalis 44 - Horizontal Lockup Color (v3)</title>
  <defs>
    <linearGradient id="depthGradH" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <style>
      .facet-base {{ fill: url(#depthGradH); }}
      .facet-marigold {{ fill: #E09D17; }}
      .facet-vivid {{ fill: #F5C538; }}
      .facet-champagne {{ fill: #F7D160; }}
      .text-title {{ font-family: 'Plus Jakarta Sans', Arial, sans-serif; font-size: 130px; font-weight: 900; fill: #0F172A; letter-spacing: -2px; }}
      .text-sub {{ font-family: 'Plus Jakarta Sans', Arial, sans-serif; font-size: 52px; font-weight: 700; fill: #D48911; letter-spacing: 8px; }}
      .divider {{ stroke: #E2E8F0; stroke-width: 4; }}
    </style>
  </defs>
  <g transform="translate(100, 100) scale(0.68)">
    <path class="facet-base" d="{path_silhouette}" />
    <path class="facet-marigold" d="{path_marigold}" />
    <path class="facet-vivid" d="{path_vivid}" />
    <path class="facet-champagne" d="{path_champagne}" />
  </g>
  <line x1="1240" y1="280" x2="1240" y2="920" class="divider" />
  <g transform="translate(1340, 560)">
    <text class="text-title" x="0" y="0">DIES NATALIS 44</text>
    <text class="text-sub" x="0" y="90">PEDOMAN IDENTITAS RESMI</text>
  </g>
</svg>'''

with open('v3_revisi/svg/logo-v3-horizontal-color.svg', 'w') as f:
    f.write(horiz_color_svg)

horiz_dark_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2800 1200" width="2800" height="1200">
  <title>Dies Natalis 44 - Horizontal Lockup Dark Canvas (v3)</title>
  <defs>
    <linearGradient id="depthGradHD" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <style>
      .facet-base {{ fill: url(#depthGradHD); }}
      .facet-marigold {{ fill: #E09D17; }}
      .facet-vivid {{ fill: #F5C538; }}
      .facet-champagne {{ fill: #F7D160; }}
      .text-title-d {{ font-family: 'Plus Jakarta Sans', Arial, sans-serif; font-size: 130px; font-weight: 900; fill: #FFFFFF; letter-spacing: -2px; }}
      .text-sub-d {{ font-family: 'Plus Jakarta Sans', Arial, sans-serif; font-size: 52px; font-weight: 700; fill: #F7D160; letter-spacing: 8px; }}
      .divider-d {{ stroke: rgba(255,255,255,0.15); stroke-width: 4; }}
    </style>
  </defs>
  <g transform="translate(100, 100) scale(0.68)">
    <path class="facet-base" d="{path_silhouette}" />
    <path class="facet-marigold" d="{path_marigold}" />
    <path class="facet-vivid" d="{path_vivid}" />
    <path class="facet-champagne" d="{path_champagne}" />
  </g>
  <line x1="1240" y1="280" x2="1240" y2="920" class="divider-d" />
  <g transform="translate(1340, 560)">
    <text class="text-title-d" x="0" y="0">DIES NATALIS 44</text>
    <text class="text-sub-d" x="0" y="90">PEDOMAN IDENTITAS RESMI</text>
  </g>
</svg>'''

with open('v3_revisi/svg/logo-v3-horizontal-dark.svg', 'w') as f:
    f.write(horiz_dark_svg)

vert_color_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 2200" width="1600" height="2200">
  <title>Dies Natalis 44 - Vertical Stacked Lockup (v3)</title>
  <defs>
    <linearGradient id="depthGradV" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <style>
      .facet-base {{ fill: url(#depthGradV); }}
      .facet-marigold {{ fill: #E09D17; }}
      .facet-vivid {{ fill: #F5C538; }}
      .facet-champagne {{ fill: #F7D160; }}
      .text-title-v {{ font-family: 'Plus Jakarta Sans', Arial, sans-serif; font-size: 110px; font-weight: 900; fill: #0F172A; text-anchor: middle; letter-spacing: -1px; }}
      .text-sub-v {{ font-family: 'Plus Jakarta Sans', Arial, sans-serif; font-size: 42px; font-weight: 700; fill: #D48911; text-anchor: middle; letter-spacing: 6px; }}
    </style>
  </defs>
  <g transform="translate(180, 80) scale(0.61)">
    <path class="facet-base" d="{path_silhouette}" />
    <path class="facet-marigold" d="{path_marigold}" />
    <path class="facet-vivid" d="{path_vivid}" />
    <path class="facet-champagne" d="{path_champagne}" />
  </g>
  <text class="text-title-v" x="800" y="1520">DIES NATALIS 44</text>
  <text class="text-sub-v" x="800" y="1610">PEDOMAN IDENTITAS RESMI</text>
</svg>'''

with open('v3_revisi/svg/logo-v3-vertical-color.svg', 'w') as f:
    f.write(vert_color_svg)

print('All 9 v3 SVG assets written successfully!')
