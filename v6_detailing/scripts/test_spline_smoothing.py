import cv2
import numpy as np
import scipy.interpolate as interp

ref = cv2.imread('scratch/svc_isolated_reference.png')
b, g, r = cv2.split(ref)
mask = ((r > 120) & (g > 70) & (b < 100) & (r > b + 45)).astype(np.uint8) * 255

s_mask = np.zeros_like(mask)
s_mask[:, :225] = mask[:, :225]

# Clean mask slightly to eliminate 1-pixel spurs
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
s_clean = cv2.morphologyEx(s_mask, cv2.MORPH_OPEN, kernel)
s_clean = cv2.morphologyEx(s_clean, cv2.MORPH_CLOSE, kernel)

contours, _ = cv2.findContours(s_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c = max(contours, key=cv2.contourArea).reshape(-1, 2)

# Subsample contour slightly (every 5 points) so spline can smooth out high-frequency noise
step = 6
pts = c[::step]
x = np.append(pts[:, 0], pts[0, 0])
y = np.append(pts[:, 1], pts[0, 1])

# Fit periodic cubic spline
tck, u = interp.splprep([x, y], s=2500, per=True, k=3)
u_new = np.linspace(0, 1, 400)
x_new, y_new = interp.splev(u_new, tck)

# Draw on image
canvas = ref.copy()
spline_pts = np.vstack([x_new, y_new]).T.astype(np.int32)
cv2.polylines(canvas, [spline_pts], isClosed=True, color=(0, 255, 0), thickness=2)

cv2.imwrite('scratch/s_spline_test.png', canvas)
print("Saved scratch/s_spline_test.png!")
