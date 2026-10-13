import cv2
import numpy as np

# Let's inspect the exact pixel coordinates of S, V, C key points in scratch/svc_isolated_reference.png
# Image shape: (395, 725, 3)

ref = cv2.imread('scratch/svc_isolated_reference.png')
h, w = ref.shape[:2]

# Let's write a helper to find points interactively or print specific feature locations
print(f"Reference dimensions: {w} x {h}")
