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

# Master canonical apex coordinates for 100% unified vertex snapping across all layers
CANONICAL_APEXES = {
    'tail_tip': np.array([1060.89, 1779.99]),
    'tail_cusp': np.array([1080.00, 1585.00]),
    'wing_fold_corner': np.array([866.00, 1084.00]),
    'crossbar_right': np.array([816.00, 1235.00]),
    'crossbar_left': np.array([468.00, 1257.00]),
    'flame_1': np.array([1006.04, 378.35]),
    'flame_2': np.array([1200.83, 558.60]),
    'flame_3': np.array([1260.39, 701.00]),
    'beak_tip': np.array([1495.05, 954.68]),
    'beak_gape': np.array([1427.03, 783.56]),
    'head_crest': np.array([1254.17, 838.00])
}

def snap_to_canonical_apex(pt, threshold=14.0):
    for name, c_pt in CANONICAL_APEXES.items():
        if np.linalg.norm(pt - c_pt) <= threshold:
            return c_pt.copy()
    return pt

def contour_to_svg_path(contour_pts, max_bezier_err=1.8, is_silhouette=False):
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
            corner_points.append(snap_to_canonical_apex(sharp_pt))
        else:
            corner_points.append(snap_to_canonical_apex(contour_pts[c_idx].astype(float)))
            
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
        
        # Smooth interior of segment to eliminate micro-waviness while preserving exact snapped endpoints
        if len(seg_pts) >= 14:
            x_sm = gaussian_filter1d(seg_pts[:, 0], sigma=2.2, mode='nearest')
            y_sm = gaussian_filter1d(seg_pts[:, 1], sigma=2.2, mode='nearest')
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

print('=== DIES NATALIS 44 - V5 PROFESSIONAL MASTER GENERATOR ===')
print('Reading master raster digital hand draw.PNG...')
img = cv2.imread('digital hand draw.PNG')
is_fg = np.any(img < 240, axis=2).astype(np.uint8) * 255

k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fg_smooth = cv2.morphologyEx(is_fg, cv2.MORPH_CLOSE, k_close)
fg_smooth = cv2.morphologyEx(fg_smooth, cv2.MORPH_OPEN, k_close)

# 1. Base silhouette contours
cnts, _ = cv2.findContours(fg_smooth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
major_cnts = sorted([c for c in cnts if cv2.contourArea(c) > 50000], key=cv2.contourArea, reverse=True)
c0 = major_cnts[0].reshape(-1, 2)  # Right 4
c1 = major_cnts[1].reshape(-1, 2)  # Left 4

print('Reconstructing master silhouette curves with canonical apex snapping...')
path_sil_0 = contour_to_svg_path(c0, max_bezier_err=1.8, is_silhouette=True)
path_sil_1 = contour_to_svg_path(c1, max_bezier_err=1.8, is_silhouette=True)
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

k3 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

def extract_v5_facet_paths(min_level, max_bezier_err=1.8):
    m = ((closest >= min_level) & (fg_smooth > 0)).astype(np.uint8) * 255
    # Morphological OPEN then CLOSE preserves precise proportional facet ribbons without runaway expansion
    m_clean = cv2.morphologyEx(m, cv2.MORPH_OPEN, k3)
    m_clean = cv2.morphologyEx(m_clean, cv2.MORPH_CLOSE, k3)
    
    # Specific fix for Kotak 1 & 2 (wing ribbon fold) on level 3 (Champagne):
    if min_level == 3:
        p_outer = (866, 1084)
        p_inner = (842, 1072)
        for y in range(1065, 1100):
            for x in range(835, 875):
                val = (p_inner[0] - p_outer[0]) * (y - p_outer[1]) - (p_inner[1] - p_outer[1]) * (x - p_outer[0])
                if val > 0 and y >= 1082:
                    m_clean[y, x] = 0
                    
    # Specific fix for Kotak 3 (tail cusp):
    for y in range(1580, 1592):
        for x in range(1075, 1085):
            if x < 1080 and y >= 1585:
                m_clean[y, x] = 0

    # Expand outward into background by subtle 2px to guarantee 0.00px edge gap under clipPath
    # without bridging separate flame ribbons into giant blobs
    m_dil = cv2.dilate(m_clean, k3)
    m_expanded = m_clean | (m_dil & (fg_smooth == 0))
    
    cnts_m, _ = cv2.findContours(m_expanded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    major_m = [c.reshape(-1, 2) for c in cnts_m if cv2.contourArea(c) > 1500]
    paths = []
    for c in major_m:
        paths.append(contour_to_svg_path(c, max_bezier_err=max_bezier_err, is_silhouette=False))
    return ' '.join(paths)

print('Extracting V5 Marigold layer (#E09D17)...')
path_marigold = extract_v5_facet_paths(min_level=1, max_bezier_err=1.8)

print('Extracting V5 Vivid Gold layer (#F5C538)...')
path_vivid = extract_v5_facet_paths(min_level=2, max_bezier_err=1.8)

print('Extracting V5 Champagne Highlight layer (#F7D160)...')
path_champagne = extract_v5_facet_paths(min_level=3, max_bezier_err=1.8)

print('Writing Master SVG assets to v5_revisi/svg/...')

# 1. Master SVG
master_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Master Final Vector (v5 Flawless Precision &amp; Harmonic Color Balance)</title>
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
    </style>
    <clipPath id="v5-silhouette-clip">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <g id="diesnat44-v5-symbol">
    <!-- Base silhouette foundation with authentic v3 depth luster -->
    <path id="facet-base" class="facet-base" fill="url(#depthGrad)" d="{path_silhouette}" />
    <!-- Color facets clipped with master silhouette to guarantee 0.00px edge bleed -->
    <g id="v5-facets" clip-path="url(#v5-silhouette-clip)">
      <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
      <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
      <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
    </g>
  </g>
</svg>'''

with open('v5_revisi/svg/logo-v5-master.svg', 'w') as f:
    f.write(master_svg)

# 2. Tight Symbol SVG
tight_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="460 375 1080 1420" width="1080" height="1420">
  <title>Dies Natalis 44 - Tight Symbol Vector (v5)</title>
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
    <clipPath id="v5-silhouette-clip-tight">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <g id="diesnat44-v5-symbol">
    <path id="facet-base" class="facet-base" fill="url(#depthGradTight)" d="{path_silhouette}" />
    <g clip-path="url(#v5-silhouette-clip-tight)">
      <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
      <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
      <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
    </g>
  </g>
</svg>'''

with open('v5_revisi/svg/logo-v5-tight.svg', 'w') as f:
    f.write(tight_svg)

# 3. Geometric Blueprint Grid SVG
grid_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Geometric Construction Blueprint (v5)</title>
  <defs>
    <linearGradient id="depthGradGrid" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <style>
      .facet-base {{ fill: url(#depthGradGrid); opacity: 0.92; }}
      .facet-marigold {{ fill: #E09D17; opacity: 0.92; }}
      .facet-vivid {{ fill: #F5C538; opacity: 0.95; }}
      .facet-champagne {{ fill: #F7D160; }}
      
      .grid-circle-major {{ fill: none; stroke: #38BDF8; stroke-width: 2.2; stroke-dasharray: 8,5; opacity: 0.9; }}
      .grid-circle-minor {{ fill: none; stroke: #F59E0B; stroke-width: 1.8; stroke-dasharray: 6,4; opacity: 0.8; }}
      .grid-axis {{ fill: none; stroke: rgba(255,255,255,0.35); stroke-width: 1.2; stroke-dasharray: 4,4; }}
      .grid-tangent {{ fill: none; stroke: #EC4899; stroke-width: 2.0; stroke-dasharray: 8,6; opacity: 0.85; }}
      .grid-center {{ fill: #38BDF8; }}
      .apex-marker {{ fill: #10B981; stroke: #FFFFFF; stroke-width: 2.0; }}
    </style>
    <clipPath id="v5-grid-clip">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <g id="diesnat44-v5-symbol">
    <path id="facet-base" class="facet-base" fill="url(#depthGradGrid)" d="{path_silhouette}" />
    <g clip-path="url(#v5-grid-clip)">
      <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
      <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
      <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
    </g>
  </g>
  <g id="construction-grid">
    <!-- Circles -->
    <circle cx="733" cy="793" r="247" class="grid-circle-major" />
    <circle cx="733" cy="793" r="4.5" class="grid-center" />
    <circle cx="1404" cy="1109" r="163" class="grid-circle-major" />
    <circle cx="1404" cy="1109" r="4.5" class="grid-center" />
    <circle cx="1060" cy="1640" r="133" class="grid-circle-major" />
    <circle cx="1060" cy="1640" r="4.5" class="grid-center" />
    <circle cx="1050" cy="680" r="310" class="grid-circle-minor" />
    <circle cx="1220" cy="950" r="220" class="grid-circle-minor" />
    <circle cx="540" cy="1200" r="90" class="grid-circle-minor" />

    <!-- Axes -->
    <line x1="200" y1="1024" x2="1848" y2="1024" class="grid-axis" />
    <line x1="1024" y1="200" x2="1024" y2="1848" class="grid-axis" />
    <line x1="464" y1="1776" x2="1534" y2="382" class="grid-tangent" />
    
    <!-- Unified Convergent Apex Markers (Single Vertex Confirmed) -->
    <circle cx="1060.89" cy="1779.99" r="6" class="apex-marker" />
    <circle cx="1080.00" cy="1585.00" r="5" class="apex-marker" />
    <circle cx="866.00" cy="1084.00" r="5" class="apex-marker" />
    <circle cx="1522.69" cy="910.85" r="5" class="apex-marker" />
    <circle cx="1495.05" cy="954.68" r="5" class="apex-marker" />
    <circle cx="1427.03" cy="783.56" r="5" class="apex-marker" />
    <circle cx="1260.39" cy="701.00" r="5" class="apex-marker" />
    <circle cx="1200.83" cy="558.60" r="5" class="apex-marker" />
    <circle cx="1006.04" cy="378.35" r="5" class="apex-marker" />
    <circle cx="468.00" cy="1257.00" r="5" class="apex-marker" />
  </g>
</svg>'''

with open('v5_revisi/svg/logo-v5-with-grid.svg', 'w') as f:
    f.write(grid_svg)

# 4. Monochrome Black SVG
mono_black_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Monochrome Black (v5)</title>
  <path fill="#0F172A" fill-rule="evenodd" d="{path_silhouette}" />
</svg>'''

with open('v5_revisi/svg/logo-v5-monochrome-black.svg', 'w') as f:
    f.write(mono_black_svg)

# 5. Monochrome White SVG
mono_white_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Monochrome White (v5)</title>
  <path fill="#FFFFFF" fill-rule="evenodd" d="{path_silhouette}" />
</svg>'''

with open('v5_revisi/svg/logo-v5-monochrome-white.svg', 'w') as f:
    f.write(mono_white_svg)

# 6. Line-Cut Technical SVG
linecut_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Line-Cut Technical Blueprint (v5)</title>
  <defs>
    <style>
      .cut-silhouette {{ fill: none; stroke: #0F172A; stroke-width: 6; stroke-linejoin: round; }}
      .cut-marigold {{ fill: none; stroke: #B6580B; stroke-width: 3.5; stroke-dasharray: 12,4; }}
      .cut-vivid {{ fill: none; stroke: #D48911; stroke-width: 3.5; }}
      .cut-champagne {{ fill: none; stroke: #E09D17; stroke-width: 3; stroke-dasharray: 6,4; }}
    </style>
    <clipPath id="v5-linecut-clip">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <g id="diesnat44-v5-linecut">
    <path class="cut-silhouette" fill="none" stroke="#0F172A" stroke-width="6" stroke-linejoin="round" d="{path_silhouette}" />
    <g clip-path="url(#v5-linecut-clip)">
      <path class="cut-marigold" fill="none" stroke="#B6580B" stroke-width="3.5" stroke-dasharray="12,4" d="{path_marigold}" />
      <path class="cut-vivid" fill="none" stroke="#D48911" stroke-width="3.5" d="{path_vivid}" />
      <path class="cut-champagne" fill="none" stroke="#E09D17" stroke-width="3" stroke-dasharray="6,4" d="{path_champagne}" />
    </g>
  </g>
</svg>'''

with open('v5_revisi/svg/logo-v5-linecut.svg', 'w') as f:
    f.write(linecut_svg)

# 7. Horizontal Lockup Color SVG
horiz_color_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4000 1600" width="4000" height="1600">
  <title>Dies Natalis 44 - Horizontal Lockup Color (v5)</title>
  <defs>
    <linearGradient id="depthGradHColor" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <style>
      .title-main {{ font-family: 'Cinzel', 'Times New Roman', serif; font-size: 132px; font-weight: 900; fill: #0F172A; letter-spacing: 4px; }}
      .title-sub {{ font-family: 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif; font-size: 64px; font-weight: 800; fill: #B6580B; letter-spacing: 12px; }}
      .title-years {{ font-family: 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif; font-size: 42px; font-weight: 600; fill: #64748B; letter-spacing: 18px; }}
      .accent-line {{ stroke: #E09D17; stroke-width: 6; stroke-linecap: round; }}
    </style>
    <clipPath id="v5-hcolor-clip">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <g id="brand-symbol" transform="translate(180, 100) scale(0.85)">
    <path id="facet-base" class="facet-base" fill="url(#depthGradHColor)" d="{path_silhouette}" />
    <g clip-path="url(#v5-hcolor-clip)">
      <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
      <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
      <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
    </g>
  </g>
  <g id="brand-typography" transform="translate(1950, 620)">
    <text x="0" y="0" class="title-sub">DIES NATALIS 44</text>
    <line x1="0" y1="40" x2="1650" y2="40" class="accent-line" />
    <text x="0" y="210" class="title-main">SMA NEGERI 1 GEDEG</text>
    <text x="0" y="320" class="title-years">1981 — 2025 • MOJOKERTO</text>
  </g>
</svg>'''

with open('v5_revisi/svg/logo-v5-horizontal-color.svg', 'w') as f:
    f.write(horiz_color_svg)

# 8. Horizontal Dark SVG
horiz_dark_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 4000 1600" width="4000" height="1600">
  <title>Dies Natalis 44 - Horizontal Lockup Dark (v5)</title>
  <defs>
    <linearGradient id="depthGradHDark" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <style>
      .title-main-dark {{ font-family: 'Cinzel', 'Times New Roman', serif; font-size: 132px; font-weight: 900; fill: #FFFFFF; letter-spacing: 4px; }}
      .title-sub-dark {{ font-family: 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif; font-size: 64px; font-weight: 800; fill: #F5C538; letter-spacing: 12px; }}
      .title-years-dark {{ font-family: 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif; font-size: 42px; font-weight: 600; fill: #94A3B8; letter-spacing: 18px; }}
      .accent-line-dark {{ stroke: #F7D160; stroke-width: 6; stroke-linecap: round; }}
    </style>
    <clipPath id="v5-hdark-clip">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <rect width="4000" height="1600" fill="#0B0F19" />
  <g id="brand-symbol" transform="translate(180, 100) scale(0.85)">
    <path id="facet-base" class="facet-base" fill="url(#depthGradHDark)" d="{path_silhouette}" />
    <g clip-path="url(#v5-hdark-clip)">
      <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
      <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
      <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
    </g>
  </g>
  <g id="brand-typography" transform="translate(1950, 620)">
    <text x="0" y="0" class="title-sub-dark">DIES NATALIS 44</text>
    <line x1="0" y1="40" x2="1650" y2="40" class="accent-line-dark" />
    <text x="0" y="210" class="title-main-dark">SMA NEGERI 1 GEDEG</text>
    <text x="0" y="320" class="title-years-dark">1981 — 2025 • MOJOKERTO</text>
  </g>
</svg>'''

with open('v5_revisi/svg/logo-v5-horizontal-dark.svg', 'w') as f:
    f.write(horiz_dark_svg)

# 9. Vertical Lockup Color SVG
vert_color_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2400 3200" width="2400" height="3200">
  <title>Dies Natalis 44 - Vertical Stacked Lockup (v5)</title>
  <defs>
    <linearGradient id="depthGradVColor" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <style>
      .v-title-main {{ font-family: 'Cinzel', 'Times New Roman', serif; font-size: 110px; font-weight: 900; fill: #0F172A; letter-spacing: 4px; text-anchor: middle; }}
      .v-title-sub {{ font-family: 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif; font-size: 68px; font-weight: 800; fill: #B6580B; letter-spacing: 14px; text-anchor: middle; }}
      .v-title-years {{ font-family: 'Plus Jakarta Sans', 'Helvetica Neue', Arial, sans-serif; font-size: 40px; font-weight: 600; fill: #64748B; letter-spacing: 16px; text-anchor: middle; }}
      .v-accent-line {{ stroke: #E09D17; stroke-width: 5; stroke-linecap: round; }}
    </style>
    <clipPath id="v5-vcolor-clip">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <g id="brand-symbol" transform="translate(250, 150) scale(0.92)">
    <path id="facet-base" class="facet-base" fill="url(#depthGradVColor)" d="{path_silhouette}" />
    <g clip-path="url(#v5-vcolor-clip)">
      <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
      <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
      <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
    </g>
  </g>
  <g id="brand-typography" transform="translate(1200, 2300)">
    <text x="0" y="0" class="v-title-sub">DIES NATALIS 44</text>
    <line x1="-500" y1="45" x2="500" y2="45" class="v-accent-line" />
    <text x="0" y="190" class="v-title-main">SMA NEGERI 1 GEDEG</text>
    <text x="0" y="310" class="v-title-years">1981 — 2025 • MOJOKERTO</text>
  </g>
</svg>'''

with open('v5_revisi/svg/logo-v5-vertical-color.svg', 'w') as f:
    f.write(vert_color_svg)

print('All 9 Master V5 SVGs written successfully!')
