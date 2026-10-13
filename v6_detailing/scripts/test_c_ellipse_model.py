import cv2
import numpy as np

ref = cv2.imread('scratch/svc_isolated_reference.png')
# C center and radii
cx = 570.0
cy = 222.5

rx_out = 104.0
ry_out = 167.5

rx_in = 33.0
ry_in = 97.5

rx_mid = 68.5
ry_mid = 132.5

# Let's draw the parametric arcs on top of ref
canvas = ref[:, 450:].copy()

# Sample angles from -60 deg to 240 deg (or 300 deg)
# C mouth opens on the right (from angle around -20 deg to +20 deg)
# Terminal cuts are at y=165 and y=265
# In ellipse coordinates: y = cy + ry * sin(theta)
# For y=165: sin(theta) = (165 - 222.5) / 167.5 = -57.5 / 167.5 = -0.343 -> theta ≈ -20 deg
# For y=265: sin(theta) = (265 - 222.5) / 167.5 = +42.5 / 167.5 = +0.254 -> theta ≈ +15 deg

thetas = np.linspace(-np.pi * 0.12, np.pi * 2 - np.pi * 0.10, 200)

pts_out = []
pts_in = []
pts_mid = []

for th in np.linspace(-np.pi * 0.12, np.pi * 1.10, 100):
    # theta goes counterclockwise from top right through left to bottom right
    # wait: let's parameterize from top cut theta_top to bottom cut theta_bot
    pass

# Let's plot with cv2.ellipse
cv2.ellipse(canvas, (int(cx - 450), int(cy)), (int(rx_out), int(ry_out)), 0, -20, 200, (0, 255, 0), 2)
cv2.ellipse(canvas, (int(cx - 450), int(cy)), (int(rx_in), int(ry_in)), 0, -35, 215, (0, 0, 255), 2)
cv2.ellipse(canvas, (int(cx - 450), int(cy)), (int(rx_mid), int(ry_mid)), 0, -25, 205, (255, 255, 0), 2)

cv2.imwrite('scratch/c_ellipse_overlay.png', canvas)
print("Saved scratch/c_ellipse_overlay.png!")
