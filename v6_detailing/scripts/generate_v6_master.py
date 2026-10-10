from scipy.interpolate import CubicSpline
import cv2
import numpy as np
import os
import re
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
    corners = [c for c in corners if not (1520 <= c[2][1] <= 1560 and 940 <= c[2][0] <= 980)]
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

print('=== DIES NATALIS 44 - V6 DETAILED MASTER GENERATOR ===')
print('Reading master raster digital hand draw.PNG...')
raster_path = 'digital-hand-draw.png' if os.path.exists('digital-hand-draw.png') else ('digital hand draw.PNG' if os.path.exists('digital hand draw.PNG') else 'IMG_2172.PNG')
img = cv2.imread(raster_path)
is_fg = np.any(img < 240, axis=2).astype(np.uint8) * 255

k_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fg_smooth = cv2.morphologyEx(is_fg, cv2.MORPH_CLOSE, k_close)
fg_smooth = cv2.morphologyEx(fg_smooth, cv2.MORPH_OPEN, k_close)

# 1. Base silhouette contours
cnts, _ = cv2.findContours(fg_smooth, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
major_cnts = sorted([c for c in cnts if cv2.contourArea(c) > 50000], key=cv2.contourArea, reverse=True)
c0 = major_cnts[0].reshape(-1, 2)
c1 = major_cnts[1].reshape(-1, 2)

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

# Initial clean masks
m_marigold = ((closest >= 1) & (fg_smooth > 0)).astype(np.uint8) * 255
m_marigold = cv2.morphologyEx(m_marigold, cv2.MORPH_OPEN, k3)
m_marigold = cv2.morphologyEx(m_marigold, cv2.MORPH_CLOSE, k3)

m_vivid = ((closest >= 2) & (fg_smooth > 0)).astype(np.uint8) * 255
m_vivid = cv2.morphologyEx(m_vivid, cv2.MORPH_OPEN, k3)
m_vivid = cv2.morphologyEx(m_vivid, cv2.MORPH_CLOSE, k3)

m_champagne = ((closest >= 3) & (fg_smooth > 0)).astype(np.uint8) * 255
m_champagne = cv2.morphologyEx(m_champagne, cv2.MORPH_OPEN, k3)
m_champagne = cv2.morphologyEx(m_champagne, cv2.MORPH_CLOSE, k3)

print('Applying V6 Medial Ribbon Ridge Line Rebalancing...')

# Natural symmetrical tail curvature preserved directly from v3 and digital hand draw

# 2. FLAME 1 VALLEY REBALANCING:
for y in range(480, 540):
    row_fg = np.where((fg_smooth[y, :] > 0) & (np.arange(2048) >= 1040) & (np.arange(2048) <= 1120))[0]
    if len(row_fg) > 15:
        x_l, x_r = row_fg[0], row_fg[-1]
        w = x_r - x_l + 1
        split_vivid = int(x_r - 0.40 * w)
        m_vivid[y, split_vivid:x_r+1] = 255

# 3. Specific fixes inherited from v5:
# Wing fold cut (Kotak 1 & 2) on Champagne
p_outer = (866, 1084)
p_inner = (842, 1072)
for y in range(1065, 1100):
    for x in range(835, 875):
        val = (p_inner[0] - p_outer[0]) * (y - p_outer[1]) - (p_inner[1] - p_outer[1]) * (x - p_outer[0])
        if val > 0 and y >= 1082:
            m_champagne[y, x] = 0

# Tail cusp (Kotak 3)
for y in range(1580, 1592):
    for x in range(1075, 1085):
        if x < 1080 and y >= 1585:
            m_vivid[y, x] = 0
            m_champagne[y, x] = 0

# Tail vivid boundary preserved cleanly without artificial blurring

def mask_to_svg_paths(m_clean, max_bezier_err=1.8):
    m_dil = cv2.dilate(m_clean, k3)
    m_expanded = m_clean | (m_dil & (fg_smooth == 0))
    cnts_m, _ = cv2.findContours(m_expanded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    major_m = [c.reshape(-1, 2) for c in cnts_m if cv2.contourArea(c) > 1500]
    paths = []
    for c in major_m:
        paths.append(contour_to_svg_path(c, max_bezier_err=max_bezier_err, is_silhouette=False))
    return ' '.join(paths)

print('Extracting V6 Marigold layer (#E09D17)...')
path_marigold = mask_to_svg_paths(m_marigold, max_bezier_err=1.8)

print('Extracting V6 Vivid Gold layer (#F5C538 with balanced 3D spines)...')
path_vivid = mask_to_svg_paths(m_vivid, max_bezier_err=1.8)

print('Extracting V6 Champagne Highlight layer (#F7D160)...')
path_champagne = mask_to_svg_paths(m_champagne, max_bezier_err=1.8)

# Preserve natural C1 continuous Bézier spines matching v3 and digital hand draw


# Harmonize tail outer curves with authentic V3 circular sweep
v3_sil_left = (
    'C 949.01 1580.65, 958.03 1626.60, 963.00 1668.00 '
    'C 967.17 1692.16, 981.61 1712.07, 996.00 1732.00 '
    'C 1006.32 1742.51, 1017.03 1752.07, 1028.00 1761.00 '
    'C 1033.18 1765.04, 1038.77 1768.08, 1044.00 1772.00 '
    'C 1049.16 1775.80, 1057.17 1774.11, 1060.89 1779.99'
)
v3_sil_right = (
    'C 1053.83 1749.08, 1042.46 1714.04, 1051.00 1680.00 '
    'C 1054.39 1645.73, 1065.49 1614.66, 1080.00 1585.00'
)
path_sil_0 = re.sub(r'C 964\.59 1534\.87.+?1060\.89 1779\.99', v3_sil_left, path_sil_0)
path_sil_0 = re.sub(r'C 1053\.34 1747\.36.+?1080\.00 1585\.00', v3_sil_right, path_sil_0)
path_silhouette = f'{path_sil_0} {path_sil_1}'

print('Harmonizing tail curves with authentic V3 circular sweep & 50:50 symmetrical spines...')
medial_spine_up = (
    'C 1052.15 1771.90, 1042.45 1763.58, 1036.18 1752.61 '
    'C 1025.27 1737.85, 1017.22 1721.22, 1012.37 1703.51 '
    'C 1003.76 1665.08, 1009.37 1624.57, 1018.00 1585.00 '
    'C 1018.00 1550.00, 1035.00 1495.00, 1055.00 1460.00'
)
highlight_spine_up = (
    'C 1049.25 1772.18, 1036.16 1764.51, 1027.09 1752.61 '
    'C 981.97 1710.33, 980.00 1643.97, 986.75 1585.00 '
    'C 986.75 1550.00, 1005.00 1495.00, 1026.00 1460.00'
)

path_vivid = re.sub(r'C 963\.84 1543\.44.+?1055\.00 1460\.00', v3_sil_left + ' ' + medial_spine_up, path_vivid)
path_champagne = re.sub(r'C 958\.40 1526\.79.+?1003\.67 1514\.00', v3_sil_left + ' ' + highlight_spine_up, path_champagne)
path_marigold = re.sub(r'C 960\.20 1536\.63.+?1016\.80 1530\.00', v3_sil_left + ' ' + medial_spine_up, path_marigold)

print('Generating 9 Master SVG Assets in v6_detailing/svg/...')
os.makedirs('v6_detailing/svg', exist_ok=True)
os.makedirs('v6_detailing/png', exist_ok=True)
os.makedirs('v6_detailing/comparison', exist_ok=True)

# 1. Master SVG
master_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Master Final Vector (v6 Detailing &amp; 3D Spine Harmony)</title>
  <defs>
    <linearGradient id="depthGrad" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <clipPath id="v6-silhouette-clip">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <style>
    .facet-base {{ fill: url(#depthGrad); }}
    .facet-marigold {{ fill: #E09D17; }}
    .facet-vivid {{ fill: #F5C538; }}
    .facet-champagne {{ fill: #F7D160; }}
  </style>
  <g id="v6-master-symbol">
    <path id="facet-base" class="facet-base" fill="url(#depthGrad)" d="{path_silhouette}" />
    <g id="v6-facets" clip-path="url(#v6-silhouette-clip)">
      <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
      <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
      <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
    </g>
  </g>
</svg>
'''
with open('v6_detailing/svg/logo-v6-master.svg', 'w') as f:
    f.write(master_svg)

# 2. Tight Bounding Box SVG (340 60 1370 1745)
tight_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="340 60 1370 1745" width="1370" height="1745">
  <title>Dies Natalis 44 - Tight Crop (v6 Detailing)</title>
  <defs>
    <linearGradient id="depthGradTight" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <clipPath id="v6-tight-clip">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <style>
    .facet-base {{ fill: url(#depthGradTight); }}
    .facet-marigold {{ fill: #E09D17; }}
    .facet-vivid {{ fill: #F5C538; }}
    .facet-champagne {{ fill: #F7D160; }}
  </style>
  <g id="v6-tight-symbol">
    <path id="facet-base" class="facet-base" fill="url(#depthGradTight)" d="{path_silhouette}" />
    <g id="v6-facets" clip-path="url(#v6-tight-clip)">
      <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
      <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
      <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
    </g>
  </g>
</svg>
'''
with open('v6_detailing/svg/logo-v6-tight.svg', 'w') as f:
    f.write(tight_svg)

# 3. With Circular Grid Overlay SVG
grid_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Master with Geometric Construction Grid (v6 Detailing)</title>
  <defs>
    <linearGradient id="depthGradGrid" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <clipPath id="v6-grid-clip">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <style>
    .grid-circle {{ fill: none; stroke: rgba(56, 189, 248, 0.45); stroke-width: 1.5; stroke-dasharray: 6 6; }}
    .grid-axis {{ fill: none; stroke: rgba(244, 63, 94, 0.4); stroke-width: 1.5; stroke-dasharray: 4 4; }}
    .grid-tangent {{ fill: none; stroke: rgba(52, 211, 153, 0.5); stroke-width: 1.5; }}
    .grid-node {{ fill: #38BDF8; stroke: #FFF; stroke-width: 1.5; }}
    .facet-base {{ fill: url(#depthGradGrid); opacity: 0.92; }}
    .facet-marigold {{ fill: #E09D17; opacity: 0.92; }}
    .facet-vivid {{ fill: #F5C538; opacity: 0.95; }}
    .facet-champagne {{ fill: #F7D160; }}
  </style>
  <g id="grid-underlay">
    <line x1="1024" y1="0" x2="1024" y2="2048" class="grid-axis" />
    <line x1="0" y1="1024" x2="2048" y2="1024" class="grid-axis" />
    <line x1="0" y1="0" x2="2048" y2="2048" class="grid-axis" />
    <circle cx="1024" cy="1024" r="850" class="grid-circle" />
    <circle cx="1024" cy="1024" r="600" class="grid-circle" />
    <circle cx="1024" cy="1024" r="400" class="grid-circle" />
    <circle cx="866" cy="1084" r="320" class="grid-circle" />
    <circle cx="1080" cy="1585" r="240" class="grid-circle" />
  </g>
  <g id="v6-symbol">
    <path id="facet-base" class="facet-base" fill="url(#depthGradGrid)" d="{path_silhouette}" />
    <g id="v6-facets" clip-path="url(#v6-grid-clip)">
      <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
      <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
      <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
    </g>
  </g>
  <g id="grid-nodes">
    <circle cx="1060.89" cy="1779.99" r="6" class="grid-node" />
    <circle cx="1080" cy="1585" r="6" class="grid-node" />
    <circle cx="866" cy="1084" r="6" class="grid-node" />
    <circle cx="1006.04" cy="378.35" r="6" class="grid-node" />
    <circle cx="1200.83" cy="558.60" r="6" class="grid-node" />
    <circle cx="1260.39" cy="701.00" r="6" class="grid-node" />
    <circle cx="1495.05" cy="954.68" r="6" class="grid-node" />
  </g>
</svg>
'''
with open('v6_detailing/svg/logo-v6-with-grid.svg', 'w') as f:
    f.write(grid_svg)

# 4. Linecut Precision Master SVG (Professional Black Wireframe Blueprint)
linecut_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Precision Line-Cut Vector (v6 Detailing &amp; Symmetrical Medial Spine)</title>
  <style>
    .linecut-outline {{ fill: none; stroke: #111827; stroke-width: 6; stroke-linejoin: round; stroke-linecap: round; }}
    .linecut-spine {{ fill: none; stroke: #111827; stroke-width: 4; stroke-linejoin: round; stroke-linecap: round; }}
  </style>
  <g id="v6-linecut">
    <path class="linecut-outline" d="{path_silhouette}" />
    <path class="linecut-spine" d="{path_vivid}" />
    <path class="linecut-spine" d="{path_champagne}" />
  </g>
</svg>
'''
with open('v6_detailing/svg/logo-v6-linecut.svg', 'w') as f:
    f.write(linecut_svg)

# 5. Monochrome Black SVG
mono_black_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Monochrome Solid Black (v6 Detailing)</title>
  <path fill="#05070D" d="{path_silhouette}" />
</svg>
'''
with open('v6_detailing/svg/logo-v6-monochrome-black.svg', 'w') as f:
    f.write(mono_black_svg)

# 6. Monochrome White (Inverted) SVG
mono_white_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2048" width="2048" height="2048">
  <title>Dies Natalis 44 - Monochrome Solid White (v6 Detailing)</title>
  <path fill="#FFFFFF" d="{path_silhouette}" />
</svg>
'''
with open('v6_detailing/svg/logo-v6-monochrome-white.svg', 'w') as f:
    f.write(mono_white_svg)

# 7. Horizontal Lockup Color SVG
h_color_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3200 1200" width="3200" height="1200">
  <title>Dies Natalis 44 - Horizontal Lockup Color (v6 Detailing)</title>
  <defs>
    <linearGradient id="depthGradHColor" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <clipPath id="v6-hcolor-clip">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <style>
    .facet-base {{ fill: url(#depthGradHColor); }}
    .facet-marigold {{ fill: #E09D17; }}
    .facet-vivid {{ fill: #F5C538; }}
    .facet-champagne {{ fill: #F7D160; }}
    .txt-title {{ font-family: 'Cinzel', 'Plus Jakarta Sans', serif; font-size: 130px; font-weight: 800; fill: #0F172A; letter-spacing: 4px; }}
    .txt-sub {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 58px; font-weight: 700; fill: #D48911; letter-spacing: 12px; }}
    .txt-univ {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 42px; font-weight: 600; fill: #64748B; letter-spacing: 6px; }}
  </style>
  <g transform="translate(150, 100) scale(0.5)">
    <path id="facet-base" class="facet-base" fill="url(#depthGradHColor)" d="{path_silhouette}" />
    <g id="v6-facets" clip-path="url(#v6-hcolor-clip)">
      <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
      <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
      <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
    </g>
  </g>
  <g transform="translate(1320, 430)">
    <text class="txt-sub" x="0" y="0">DIES NATALIS KE-44</text>
    <text class="txt-title" x="0" y="140">SMAN 1 GEDEG</text>
    <text class="txt-univ" x="0" y="220">SMA NEGERI 1 GEDEG • MOJOKERTO</text>
  </g>
</svg>
'''
with open('v6_detailing/svg/logo-v6-horizontal-color.svg', 'w') as f:
    f.write(h_color_svg)

# 8. Horizontal Lockup Dark SVG
h_dark_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 3200 1200" width="3200" height="1200">
  <title>Dies Natalis 44 - Horizontal Lockup Dark (v6 Detailing - SMA Negeri 1 Gedeg)</title>
  <defs>
    <linearGradient id="depthGradHDark" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <clipPath id="v6-hdark-clip">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <style>
    .bg-dark-lockup {{ fill: #05070D; }}
    .facet-base {{ fill: url(#depthGradHDark); }}
    .facet-marigold {{ fill: #E09D17; }}
    .facet-vivid {{ fill: #F5C538; }}
    .facet-champagne {{ fill: #F7D160; }}
    .txt-title-dark {{ font-family: 'Cinzel', 'Plus Jakarta Sans', serif; font-size: 130px; font-weight: 800; fill: #FFFFFF; letter-spacing: 4px; }}
    .txt-sub-dark {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 58px; font-weight: 700; fill: #F5C538; letter-spacing: 12px; }}
    .txt-univ-dark {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 42px; font-weight: 600; fill: #94A3B8; letter-spacing: 6px; }}
  </style>
  <rect width="3200" height="1200" class="bg-dark-lockup" />
  <g transform="translate(150, 100) scale(0.5)">
    <path id="facet-base" class="facet-base" fill="url(#depthGradHDark)" d="{path_silhouette}" />
    <g id="v6-facets" clip-path="url(#v6-hdark-clip)">
      <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
      <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
      <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
    </g>
  </g>
  <g transform="translate(1320, 430)">
    <text class="txt-sub-dark" x="0" y="0">DIES NATALIS KE-44</text>
    <text class="txt-title-dark" x="0" y="140">SMAN 1 GEDEG</text>
    <text class="txt-univ-dark" x="0" y="220">SMA NEGERI 1 GEDEG • MOJOKERTO</text>
  </g>
</svg>
'''
with open('v6_detailing/svg/logo-v6-horizontal-dark.svg', 'w') as f:
    f.write(h_dark_svg)

# 9. Vertical Lockup Color SVG
v_color_svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 2048 2700" width="2048" height="2700">
  <title>Dies Natalis 44 - Vertical Lockup Color (v6 Detailing - SMA Negeri 1 Gedeg)</title>
  <defs>
    <linearGradient id="depthGradVColor" x1="20%" y1="100%" x2="80%" y2="0%">
      <stop offset="0%" stop-color="#B6580B" />
      <stop offset="35%" stop-color="#D48911" />
      <stop offset="70%" stop-color="#E09D17" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <clipPath id="v6-vcolor-clip">
      <path d="{path_silhouette}" />
    </clipPath>
  </defs>
  <style>
    .facet-base {{ fill: url(#depthGradVColor); }}
    .facet-marigold {{ fill: #E09D17; }}
    .facet-vivid {{ fill: #F5C538; }}
    .facet-champagne {{ fill: #F7D160; }}
    .txt-title-v {{ font-family: 'Cinzel', 'Plus Jakarta Sans', serif; font-size: 130px; font-weight: 800; fill: #0F172A; letter-spacing: 6px; text-anchor: middle; }}
    .txt-sub-v {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 60px; font-weight: 700; fill: #D48911; letter-spacing: 14px; text-anchor: middle; }}
    .txt-univ-v {{ font-family: 'Plus Jakarta Sans', sans-serif; font-size: 42px; font-weight: 600; fill: #64748B; letter-spacing: 8px; text-anchor: middle; }}
  </style>
  <g transform="translate(274, 80) scale(0.73)">
    <path id="facet-base" class="facet-base" fill="url(#depthGradVColor)" d="{path_silhouette}" />
    <g id="v6-facets" clip-path="url(#v6-vcolor-clip)">
      <path id="facet-marigold" class="facet-marigold" fill="#E09D17" d="{path_marigold}" />
      <path id="facet-vivid" class="facet-vivid" fill="#F5C538" d="{path_vivid}" />
      <path id="facet-champagne" class="facet-champagne" fill="#F7D160" d="{path_champagne}" />
    </g>
  </g>
  <g transform="translate(1024, 2180)">
    <text class="txt-sub-v" x="0" y="0">DIES NATALIS KE-44</text>
    <text class="txt-title-v" x="0" y="160">SMAN 1 GEDEG</text>
    <text class="txt-univ-v" x="0" y="250">SMA NEGERI 1 GEDEG • MOJOKERTO</text>
  </g>
</svg>
'''
with open('v6_detailing/svg/logo-v6-vertical-color.svg', 'w') as f:
    f.write(v_color_svg)

print('All 9 Master SVG assets created successfully in v6_detailing/svg/!')
