import cv2
import numpy as np

img = cv2.imread('scratch/svc_ai_reference.jpg')
h, w = img.shape[:2]

# Detect non-white background
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mask = gray < 240

# Clean mask
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
mask = cv2.morphologyEx(mask.astype(np.uint8)*255, cv2.MORPH_CLOSE, kernel)

# Find contours of the three letters
contours, hier = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
letters = []
for c in contours:
    area = cv2.contourArea(c)
    if area > 10000:
        x, y, bw, bh = cv2.boundingRect(c)
        letters.append((x, y, bw, bh, c))

letters = sorted(letters, key=lambda item: item[0])
print(f"Found {len(letters)} letters:")
names = ['S', 'V', 'C']
for i, (x, y, bw, bh, c) in enumerate(letters):
    name = names[i] if i < 3 else f'L_{i}'
    print(f"Letter {name}: bbox=({x}, {y}, {bw}, {bh}), area={cv2.contourArea(c)}")
    crop = img[y-10:y+bh+10, x-10:x+bw+10]
    cv2.imwrite(f'scratch/ai_letter_{name}.png', crop)

print("Saved scratch/ai_letter_S.png, V.png, C.png!")
