import cv2
import numpy as np
import scipy.interpolate as interp

ref = cv2.imread('scratch/svc_isolated_reference.png')
b, g, r = cv2.split(ref)
mask = ((r > 120) & (g > 70) & (b < 100) & (r > b + 45)).astype(np.uint8) * 255

s_mask = np.zeros_like(mask)
s_mask[:, :225] = mask[:, :225]

# Clean mask
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
s_clean = cv2.morphologyEx(s_mask, cv2.MORPH_OPEN, kernel)
s_clean = cv2.morphologyEx(s_clean, cv2.MORPH_CLOSE, kernel)

contours, _ = cv2.findContours(s_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c = max(contours, key=cv2.contourArea).reshape(-1, 2)

# Find the indices corresponding to the 4 corners:
# Corner 1 (top-outer): close to (202, 165)
# Corner 2 (top-inner): close to (140, 165)
# Corner 3 (bottom-inner): close to (78, 265)
# Corner 4 (bottom-outer): close to (15, 265)

def find_closest(pts, target):
    dists = np.sum((pts - target)**2, axis=1)
    return np.argmin(dists)

i_top_outer = find_closest(c, [202, 165])
i_top_inner = find_closest(c, [140, 165])
i_bot_inner = find_closest(c, [78, 265])
i_bot_outer = find_closest(c, [15, 265])

print(f"Indices: top_outer={i_top_outer}, top_inner={i_top_inner}, bot_inner={i_bot_inner}, bot_outer={i_bot_outer}")
print(f"Points: top_outer={c[i_top_outer]}, top_inner={c[i_top_inner]}, bot_inner={c[i_bot_inner]}, bot_outer={c[i_bot_outer]}")

# Reorder contour to start at top_outer
# Let's inspect the order of traversal (clockwise or CCW)
N = len(c)
print("Points around top_outer:", c[(i_top_outer - 5) % N], c[i_top_outer], c[(i_top_outer + 5) % N])

