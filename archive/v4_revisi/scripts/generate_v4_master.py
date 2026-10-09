import cv2
import numpy as np
import os
import subprocess
from scipy.ndimage import gaussian_filter1d

def fit_cubic_bezier(pts):
    P0 = pts[0].astype(float)
    P3 = pts[-1].astype(float)
    N = len(pts)
    chord_len = np.linalg.norm(P3 - P0)
    if N <= 2 or chord_len < 1e-4:
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
    
    # Strict bounding box clamping to prevent numerical control-point explosion
    min_b = np.min(pts, axis=0) - 4.0
    max_b = np.max(pts, axis=0) + 4.0
    P1 = np.clip(P1, min_b, max_b)
    P2 = np.clip(P2, min_b, max_b)
    
    fitted = np.outer(b0, P0) + np.outer(b1, P1) + np.outer(b2, P2) + np.outer(b3, P3)
    err = np.max(np.linalg.norm(pts - fitted, axis=1))
    return P0, P1, P2, P3, err

def fit_curve_recursive(pts, max_err=2.0):
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

def contour_to_svg_path(contour_pts, max_bezier_err=2.0):
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
        
        # Gentle spline smoothing along curve segment to eliminate brush waviness while keeping endpoints fixed
        if len(seg_pts) >= 14:
            x_sm = gaussian_filter1d(seg_pts[:, 0], sigma=2.0, mode='nearest')
            y_sm = gaussian_filter1d(seg_pts[:, 1], sigma=2.0, mode='nearest')
            x_sm[0], x_sm[-1] = pt_start[0], pt_end[0]
            y_sm[0], y_sm[-1] = pt_start[1], pt_end[1]
            seg_pts = np.column_stack([x_sm, y_sm])
            
        beziers = fit_curve_recursive(seg_pts, max_err=max_bezier_err)
        if i == 0:
            path_d.append(f'M {beziers[0][0][0]:.2f} {beziers[0][0][1]:.2f}')
        for b in beziers:
            path_d.append(f'C {b[1][0]:.2f} {b[1][1]:.2f}, {b[2][0]:.2f} {b[2][1]:.2f}, {b[3][0]:.2f} {b[3][1]:.2f}')
    path_d.append('Z')
    return ' '.join(path_d)

print('=== DIES NATALIS 44 - V4 REVISION GENERATOR (PRO CURVES) ===')
print('Reading master raster IMG_2172.PNG...')
img = cv2.imread('IMG_2172.PNG')
is_fg = np.any(img < 240, axis=2).astype(np.uint8) * 255

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

print('Segmenting facet color layers with bilateral filter...')
filtered = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)
centers = np.array([
    [17, 137, 212],   # 0: #D48911 (Base deep shadow)
    [23, 157, 224],   # 1: #E09D17 (Marigold / amber shade)
    [56, 197, 245],   # 2: #F5C538 (Vivid warm gold body)
    [96, 209, 247]    # 3: #F7D160 (Champagne highlight)
], dtype=np.float32)

fg_pixels = filtered.astype(np.float32)
dists = np.zeros((img.shape[0], img.shape[1], 4), dtype=np.float32)
for i in range(4):
    dists[:, :, i] = np.sum((fg_pixels - centers[i])**2, axis=2)
closest = np.argmin(dists, axis=2)

def extract_facet_paths(min_level, max_bezier_err=2.0):
    m = ((closest >= min_level) & (is_fg > 0)).astype(np.uint8) * 255
    # MORPH_CLOSE preserves fine continuous tips like the tail apex
    m_clean = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    cnts_m, _ = cv2.findContours(m_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    major_m = [c.reshape(-1, 2) for c in cnts_m if cv2.contourArea(c) > 2000]
    paths = []
    for c in major_m:
        paths.append(contour_to_svg_path(c, max_bezier_err=max_bezier_err))
    return ' '.join(paths)

print('Fitting smooth harmonic Beziers to Marigold layer (#E09D17)...')
path_marigold = extract_facet_paths(min_level=1, max_bezier_err=2.0)

print('Fitting smooth harmonic Beziers to Vivid Gold layer (#F5C538)...')
path_vivid = extract_facet_paths(min_level=2, max_bezier_err=2.0)

print('Fitting smooth harmonic Beziers to Champagne Highlight layer (#F7D160)...')
path_champagne = extract_facet_paths(min_level=3, max_bezier_err=2.0)

print('Assembling Master SVG (v4) with Direct Presentation Attributes...')

# Master SVG
master_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Master Final Vector (v4 Professional Facets &amp; Unified Apexes)</title>
  <defs>
    <style>
      .facet-base {{ fill: #D48911; }}
      .facet-marigold {{ fill: #E09D17; }}
      .facet-vivid {{ fill: #F5C538; }}
      .facet-champagne {{ fill: #F7D160; }}
    </style>
  </defs>
  <g id="diesnat44-v4-symbol">
    <path id="facet-base" class="facet-base" fill="#D48911" d="{path_silhouette}" />
    <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
    <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
    <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
  </g>
</svg>'''

with open('v4_revisi/svg/logo-v4-master.svg', 'w') as f:
    f.write(master_svg)

# Grid Blueprint SVG
grid_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Master Vector with Geometric Construction Grid (v4)</title>
  <defs>
    <style>
      .facet-base {{ fill: #D48911; opacity: 0.88; }}
      .facet-marigold {{ fill: #E09D17; opacity: 0.92; }}
      .facet-vivid {{ fill: #F5C538; opacity: 0.95; }}
      .facet-champagne {{ fill: #F7D160; }}
      
      .grid-circle-major {{ fill: none; stroke: #38BDF8; stroke-width: 2.2; stroke-dasharray: 8,5; opacity: 0.9; }}
      .grid-circle-minor {{ fill: none; stroke: #F59E0B; stroke-width: 1.8; stroke-dasharray: 6,4; opacity: 0.8; }}
      .grid-axis {{ fill: none; stroke: rgba(255,255,255,0.35); stroke-width: 1.2; stroke-dasharray: 4,4; }}
      .grid-tangent {{ fill: none; stroke: #EC4899; stroke-width: 2.0; stroke-dasharray: 8,6; opacity: 0.85; }}
      .grid-center {{ fill: #38BDF8; }}
      .apex-marker {{ fill: #EF4444; stroke: #FFFFFF; stroke-width: 1.5; }}
    </style>
  </defs>
  <g id="diesnat44-v4-symbol">
    <path id="facet-base" class="facet-base" fill="#D48911" d="{path_silhouette}" />
    <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
    <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
    <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
  </g>
  <g id="construction-grid">
    <!-- Circle 1: Eagle Back Arc R=247px centered at (733, 793) -->
    <circle cx="733" cy="793" r="247" class="grid-circle-major" />
    <circle cx="733" cy="793" r="4.5" class="grid-center" />

    <!-- Circle 2: Outer Flame Arc R=163px centered at (1404, 1109) -->
    <circle cx="1404" cy="1109" r="163" class="grid-circle-major" />
    <circle cx="1404" cy="1109" r="4.5" class="grid-center" />

    <!-- Circle 3: Tail Spiral Arc R=133px centered at (1060, 1640) matching actual tail curve -->
    <circle cx="1060" cy="1640" r="133" class="grid-circle-major" />
    <circle cx="1060" cy="1640" r="4.5" class="grid-center" />

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
    
    <!-- Unified Convergent Apex Markers -->
    <circle cx="1060.89" cy="1779.99" r="6" class="apex-marker" />
    <circle cx="1522.69" cy="910.85" r="5" class="apex-marker" />
    <circle cx="1427.03" cy="783.56" r="5" class="apex-marker" />
    <circle cx="1200.83" cy="558.60" r="5" class="apex-marker" />
    <circle cx="1006.04" cy="378.35" r="5" class="apex-marker" />
    <circle cx="468.00" cy="1257.00" r="5" class="apex-marker" />
  </g>
</svg>'''

with open('v4_revisi/svg/logo-v4-with-grid.svg', 'w') as f:
    f.write(grid_svg)

# Tight Symbol SVG
tight_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="460 375 1080 1420" width="1080" height="1420">
  <title>Dies Natalis 44 - Tight Symbol Vector (v4)</title>
  <defs>
    <style>
      .facet-base {{ fill: #D48911; }}
      .facet-marigold {{ fill: #E09D17; }}
      .facet-vivid {{ fill: #F5C538; }}
      .facet-champagne {{ fill: #F7D160; }}
    </style>
  </defs>
  <g id="diesnat44-v4-symbol">
    <path id="facet-base" class="facet-base" fill="#D48911" d="{path_silhouette}" />
    <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
    <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
    <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
  </g>
</svg>'''

with open('v4_revisi/svg/logo-v4-tight.svg', 'w') as f:
    f.write(tight_svg)

# Monochrome Black SVG
mono_black_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Monochrome Black (v4)</title>
  <path fill="#0F172A" fill-rule="evenodd" d="{path_silhouette}" />
</svg>'''

with open('v4_revisi/svg/logo-v4-monochrome-black.svg', 'w') as f:
    f.write(mono_black_svg)

# Monochrome White SVG
mono_white_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Monochrome White (v4)</title>
  <path fill="#FFFFFF" fill-rule="evenodd" d="{path_silhouette}" />
</svg>'''

with open('v4_revisi/svg/logo-v4-monochrome-white.svg', 'w') as f:
    f.write(mono_white_svg)

# Line-Cut Technical SVG
linecut_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Line-Cut Technical Vector (v4)</title>
  <defs>
    <style>
      .cut-silhouette {{ fill: none; stroke: #0F172A; stroke-width: 6; stroke-linejoin: round; }}
      .cut-marigold {{ fill: none; stroke: #B6580B; stroke-width: 3.5; stroke-dasharray: 12,4; }}
      .cut-vivid {{ fill: none; stroke: #D48911; stroke-width: 3.5; }}
      .cut-champagne {{ fill: none; stroke: #E09D17; stroke-width: 3; stroke-dasharray: 6,4; }}
    </style>
  </defs>
  <g id="diesnat44-v4-linecut">
    <path class="cut-silhouette" fill="none" stroke="#0F172A" stroke-width="6" stroke-linejoin="round" d="{path_silhouette}" />
    <path class="cut-marigold" fill="none" stroke="#B6580B" stroke-width="3.5" stroke-dasharray: 12,4" d="{path_marigold}" />
    <path class="cut-vivid" fill="none" stroke="#D48911" stroke-width="3.5" d="{path_vivid}" />
    <path class="cut-champagne" fill="none" stroke="#E09D17" stroke-width="3" stroke-dasharray: 6,4" d="{path_champagne}" />
  </g>
</svg>'''

with open('v4_revisi/svg/logo-v4-linecut.svg', 'w') as f:
    f.write(linecut_svg)

# Lockup Horizontal Color SVG
horiz_color_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 900" width="2400" height="900">
  <title>Dies Natalis 44 - Horizontal Lockup Color (v4)</title>
  <defs>
    <style>
      .facet-base {{ fill: #D48911; }}
      .facet-marigold {{ fill: #E09D17; }}
      .facet-vivid {{ fill: #F5C538; }}
      .facet-champagne {{ fill: #F7D160; }}
      .text-title {{ font-family: Helvetica, Arial, sans-serif; font-size: 110px; font-weight: 900; fill: #0F172A; letter-spacing: -2px; }}
      .text-subtitle {{ font-family: Helvetica, Arial, sans-serif; font-size: 38px; font-weight: 700; fill: #D48911; letter-spacing: 12px; }}
      .text-tagline {{ font-family: Helvetica, Arial, sans-serif; font-size: 26px; font-weight: 500; fill: #64748B; letter-spacing: 2px; }}
      .text-year {{ font-family: Helvetica, Arial, sans-serif; font-size: 42px; font-weight: 800; fill: #0F172A; opacity: 0.25; }}
    </style>
  </defs>
  <g transform="translate(-140, -110) scale(0.62)">
    <path class="facet-base" fill="#D48911" d="{path_silhouette}" />
    <path class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
    <path class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
    <path class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
  </g>
  <g transform="translate(920, 290)">
    <text class="text-subtitle" x="0" y="0">44 TAHUN</text>
    <text class="text-title" x="0" y="115">DIES NATALIS</text>
    <text class="text-tagline" x="0" y="185">TRANSFORMASI BERKELANJUTAN MENUJU MASA DEPAN</text>
    <line x1="0" y1="230" x2="1350" y2="230" stroke="#E2E8F0" stroke-width="2.5" />
    <text class="text-year" x="0" y="295">1980 — 2024</text>
  </g>
</svg>'''

with open('v4_revisi/svg/logo-v4-horizontal-color.svg', 'w') as f:
    f.write(horiz_color_svg)

# Lockup Horizontal Dark SVG
horiz_dark_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 900" width="2400" height="900">
  <title>Dies Natalis 44 - Horizontal Lockup Dark (v4)</title>
  <defs>
    <style>
      .bg-dark {{ fill: #0B0F19; }}
      .facet-base {{ fill: #D48911; }}
      .facet-marigold {{ fill: #E09D17; }}
      .facet-vivid {{ fill: #F5C538; }}
      .facet-champagne {{ fill: #F7D160; }}
      .text-title-dark {{ font-family: Helvetica, Arial, sans-serif; font-size: 110px; font-weight: 900; fill: #F8FAFC; letter-spacing: -2px; }}
      .text-subtitle-dark {{ font-family: Helvetica, Arial, sans-serif; font-size: 38px; font-weight: 700; fill: #F5C538; letter-spacing: 12px; }}
      .text-tagline-dark {{ font-family: Helvetica, Arial, sans-serif; font-size: 26px; font-weight: 500; fill: #94A3B8; letter-spacing: 2px; }}
      .text-year-dark {{ font-family: Helvetica, Arial, sans-serif; font-size: 42px; font-weight: 800; fill: #FFFFFF; opacity: 0.3; }}
    </style>
  </defs>
  <rect class="bg-dark" width="2400" height="900" />
  <g transform="translate(-140, -110) scale(0.62)">
    <path class="facet-base" fill="#D48911" d="{path_silhouette}" />
    <path class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
    <path class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
    <path class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
  </g>
  <g transform="translate(920, 290)">
    <text class="text-subtitle-dark" x="0" y="0">44 TAHUN</text>
    <text class="text-title-dark" x="0" y="115">DIES NATALIS</text>
    <text class="text-tagline-dark" x="0" y="185">TRANSFORMASI BERKELANJUTAN MENUJU MASA DEPAN</text>
    <line x1="0" y1="230" x2="1350" y2="230" stroke="rgba(255,255,255,0.15)" stroke-width="2.5" />
    <text class="text-year-dark" x="0" y="295">1980 — 2024</text>
  </g>
</svg>'''

with open('v4_revisi/svg/logo-v4-horizontal-dark.svg', 'w') as f:
    f.write(horiz_dark_svg)

# Lockup Vertical Color SVG
vert_color_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 2200" width="1600" height="2200">
  <title>Dies Natalis 44 - Vertical Lockup Color (v4)</title>
  <defs>
    <style>
      .facet-base {{ fill: #D48911; }}
      .facet-marigold {{ fill: #E09D17; }}
      .facet-vivid {{ fill: #F5C538; }}
      .facet-champagne {{ fill: #F7D160; }}
      .v-title {{ font-family: Helvetica, Arial, sans-serif; font-size: 104px; font-weight: 900; fill: #0F172A; text-anchor: middle; letter-spacing: -2px; }}
      .v-subtitle {{ font-family: Helvetica, Arial, sans-serif; font-size: 34px; font-weight: 700; fill: #D48911; text-anchor: middle; letter-spacing: 14px; }}
      .v-tagline {{ font-family: Helvetica, Arial, sans-serif; font-size: 24px; font-weight: 500; fill: #64748B; text-anchor: middle; letter-spacing: 2px; }}
      .v-year {{ font-family: Helvetica, Arial, sans-serif; font-size: 38px; font-weight: 800; fill: #0F172A; text-anchor: middle; opacity: 0.25; }}
    </style>
  </defs>
  <g transform="translate(370, 80) scale(0.68)">
    <path class="facet-base" fill="#D48911" d="{path_silhouette}" />
    <path class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
    <path class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
    <path class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
  </g>
  <g transform="translate(800, 1640)">
    <text class="v-subtitle" x="0" y="0">44 TAHUN</text>
    <text class="v-title" x="0" y="115">DIES NATALIS</text>
    <text class="v-tagline" x="0" y="185">TRANSFORMASI BERKELANJUTAN MENUJU MASA DEPAN</text>
    <line x1="-450" y1="230" x2="450" y2="230" stroke="#E2E8F0" stroke-width="2.5" />
    <text class="v-year" x="0" y="295">1980 — 2024</text>
  </g>
</svg>'''

with open('v4_revisi/svg/logo-v4-vertical-color.svg', 'w') as f:
    f.write(vert_color_svg)

print('All 9 SVG variants generated successfully in v4_revisi/svg/!')

print('Rendering high-res 2048px PNGs with ImageMagick (transparent backgrounds)...')
svg_files = [
    'logo-v4-master',
    'logo-v4-with-grid',
    'logo-v4-tight',
    'logo-v4-monochrome-black',
    'logo-v4-monochrome-white',
    'logo-v4-horizontal-color',
    'logo-v4-horizontal-dark',
    'logo-v4-vertical-color'
]

for name in svg_files:
    svg_fp = f'v4_revisi/svg/{name}.svg'
    png_fp = f'v4_revisi/png/{name}.png'
    subprocess.run(['magick', '-background', 'none', '-font', '/System/Library/Fonts/Helvetica.ttc', svg_fp, png_fp])

# For linecut, render with WebKit QuickLook which supports strokes
subprocess.run(['qlmanage', '-t', '-s', '2048', '-o', 'v4_revisi/png', 'v4_revisi/svg/logo-v4-linecut.svg'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if os.path.exists('v4_revisi/png/logo-v4-linecut.svg.png'):
    os.rename('v4_revisi/png/logo-v4-linecut.svg.png', 'v4_revisi/png/logo-v4-linecut.png')

print('All PNGs successfully rendered!')
