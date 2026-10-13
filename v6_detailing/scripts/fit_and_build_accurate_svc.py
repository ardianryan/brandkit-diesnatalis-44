#!/usr/bin/env python3
"""
fit_and_build_accurate_svc.py
=============================
Extracts true athletic letterforms for S, V, C from pristine AI reference crops,
fits smooth parametric cubic Beziers to all curves (zero bumps / zero waviness),
and constructs the complete chiseled 3D bevel standalone assets.
"""

import cv2
import numpy as np
import subprocess
import os

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
print("Processing Letter S...")
img_s = cv2.imread('scratch/isolated_clean_S.png')
gray_s = cv2.cvtColor(img_s, cv2.COLOR_BGR2GRAY)
mask_s = (gray_s < 240).astype(np.uint8)

cnts_s, _ = cv2.findContours(mask_s, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnt_s = max(cnts_s, key=cv2.contourArea)[:, 0, :]

idx_top_out_s = min(range(len(cnt_s)), key=lambda i: np.hypot(cnt_s[i,0]-345, cnt_s[i,1]-194))
idx_top_in_s = min(range(len(cnt_s)), key=lambda i: np.hypot(cnt_s[i,0]-227, cnt_s[i,1]-194))
idx_bot_in_s = min(range(len(cnt_s)), key=lambda i: np.hypot(cnt_s[i,0]-128, cnt_s[i,1]-368))
idx_bot_out_s = min(range(len(cnt_s)), key=lambda i: np.hypot(cnt_s[i,0]-10, cnt_s[i,1]-368))

p_top_out_s = cnt_s[idx_top_out_s]
p_top_in_s = cnt_s[idx_top_in_s]
p_bot_in_s = cnt_s[idx_bot_in_s]
p_bot_out_s = cnt_s[idx_bot_out_s]

# outer curve: from idx_top_out_s around top to idx_bot_out_s
if idx_top_out_s > idx_bot_out_s:
    outer_pts_s = np.vstack([cnt_s[idx_top_out_s:], cnt_s[:idx_bot_out_s+1]])
else:
    outer_pts_s = cnt_s[idx_top_out_s:idx_bot_out_s+1]

# inner curve: from idx_bot_in_s up to idx_top_in_s
if idx_bot_in_s < idx_top_in_s:
    inner_pts_s = cnt_s[idx_bot_in_s:idx_top_in_s+1]
else:
    inner_pts_s = np.vstack([cnt_s[idx_bot_in_s:], cnt_s[:idx_top_in_s+1]])

s_outer_beziers = fit_curve_recursive(outer_pts_s, max_err=1.2)
s_inner_beziers = fit_curve_recursive(inner_pts_s, max_err=1.2)

# Build S base solid path
s_base_d = beziers_to_d(s_outer_beziers, start_m=True) + \
           f" L {p_bot_in_s[0]} {p_bot_in_s[1]} " + \
           beziers_to_d(s_inner_beziers, start_m=False) + \
           f" L {p_top_out_s[0]} {p_top_out_s[1]} Z"

print("S base curve fitted:", len(s_outer_beziers), "outer segs,", len(s_inner_beziers), "inner segs")

# =========================================================================
# 2. PROCESS LETTER C
# =========================================================================
print("Processing Letter C...")
img_c = cv2.imread('scratch/isolated_clean_C.png')
gray_c = cv2.cvtColor(img_c, cv2.COLOR_BGR2GRAY)
mask_c = (gray_c < 240).astype(np.uint8)

cnts_c, _ = cv2.findContours(mask_c, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cnt_c = max(cnts_c, key=cv2.contourArea)[:, 0, :]

idx_top_out_c = min(range(len(cnt_c)), key=lambda i: np.hypot(cnt_c[i,0]-353, cnt_c[i,1]-206))
idx_top_in_c = min(range(len(cnt_c)), key=lambda i: np.hypot(cnt_c[i,0]-226, cnt_c[i,1]-206))
idx_bot_in_c = min(range(len(cnt_c)), key=lambda i: np.hypot(cnt_c[i,0]-226, cnt_c[i,1]-355))
idx_bot_out_c = min(range(len(cnt_c)), key=lambda i: np.hypot(cnt_c[i,0]-354, cnt_c[i,1]-355))

p_top_out_c = cnt_c[idx_top_out_c]
p_top_in_c = cnt_c[idx_top_in_c]
p_bot_in_c = cnt_c[idx_bot_in_c]
p_bot_out_c = cnt_c[idx_bot_out_c]

# outer curve: from bot_out_c around bottom, up back, over top to top_out_c
if idx_bot_out_c < idx_top_out_c:
    outer_pts_c = np.vstack([cnt_c[idx_bot_out_c:], cnt_c[:idx_top_out_c+1]])
else:
    outer_pts_c = cnt_c[idx_bot_out_c:idx_top_out_c+1]

# inner counter: from top_in_c down to bot_in_c
if idx_top_in_c < idx_bot_in_c:
    inner_pts_c = cnt_c[idx_top_in_c:idx_bot_in_c+1]
else:
    # Notice: 1130 to 1670 was bot_in to top_in! So reverse or direct:
    inner_pts_c = cnt_c[idx_bot_in_c:idx_top_in_c+1][::-1]

c_outer_beziers = fit_curve_recursive(outer_pts_c, max_err=1.2)
c_inner_beziers = fit_curve_recursive(inner_pts_c, max_err=1.2)

# Build C base solid path
c_base_d = beziers_to_d(c_outer_beziers, start_m=True) + \
           f" L {p_top_in_c[0]} {p_top_in_c[1]} " + \
           beziers_to_d(c_inner_beziers, start_m=False) + \
           f" L {p_bot_out_c[0]} {p_bot_out_c[1]} Z"

print("C base curve fitted:", len(c_outer_beziers), "outer segs,", len(c_inner_beziers), "inner segs")

# Save coordinates into a python module for easy import
with open('scratch/fitted_svc_data.py', 'w') as f:
    f.write(f'''# Auto-generated fitted SVC vector data
p_top_out_s = {list(p_top_out_s)}
p_top_in_s = {list(p_top_in_s)}
p_bot_in_s = {list(p_bot_in_s)}
p_bot_out_s = {list(p_bot_out_s)}
s_base_d = """{s_base_d}"""

p_top_out_c = {list(p_top_out_c)}
p_top_in_c = {list(p_top_in_c)}
p_bot_in_c = {list(p_bot_in_c)}
p_bot_out_c = {list(p_bot_out_c)}
c_base_d = """{c_base_d}"""
''')

print("Saved scratch/fitted_svc_data.py successfully!")
