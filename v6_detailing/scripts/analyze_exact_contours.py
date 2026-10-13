import cv2
import numpy as np

ref = cv2.imread('scratch/svc_isolated_reference.png')
H, W = ref.shape[:2] # 395 x 725

# Extract gold mask
b, g, r = cv2.split(ref)
mask = ((r > 120) & (g > 70) & (b < 100) & (r > b + 45)).astype(np.uint8) * 255

# Clean mask slightly to remove outer background noise
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
mask_clean = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Let's save a contour visualization on top of reference
overlay = ref.copy()

# Find contours
contours, hier = cv2.findContours(mask_clean, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
for i, cnt in enumerate(contours):
    area = cv2.contourArea(cnt)
    if area > 2000:
        cv2.drawContours(overlay, [cnt], -1, (0, 255, 0), 1)

cv2.imwrite('scratch/ref_contour_overlay.png', overlay)
print(f"Saved scratch/ref_contour_overlay.png with {len(contours)} contours")
