import cv2
import numpy as np
import subprocess
import xml.etree.ElementTree as ET

ref_img = cv2.imread('scratch/svc_isolated_reference.png')
ref_h, ref_w = ref_img.shape[:2]

scale = 4
hi = cv2.resize(ref_img, (ref_w * scale, ref_h * scale), interpolation=cv2.INTER_LANCZOS4)

# 1. Clean C mask:
# C is strictly within x: 460..664 in native coords (460*scale .. 664*scale)
c_crop = hi[:, int(460 * scale):int(664 * scale)].copy()
cb, cg, cr = cv2.split(c_crop)
c_letter = (cr > 120) & (cg > 70) & (cb < 100) & (cr > cb + 45)

# Remove any stray shield fragments at the far right
c_letter[:, int((664-460)*scale - 10):] = False

# Now let's test tracing C with different blur and opttolerance
for blur_k, sig, opt in [(15, 4.0, 0.8), (21, 6.0, 1.2), (25, 7.5, 1.5)]:
    m_u8 = (c_letter.astype(np.uint8)) * 255
    m_blur = cv2.GaussianBlur(m_u8, (blur_k, blur_k), sig)
    _, m_thresh = cv2.threshold(m_blur, 128, 255, cv2.THRESH_BINARY)
    
    bmp = f'scratch/test_c_blur_{blur_k}.bmp'
    svg = f'scratch/test_c_blur_{blur_k}.svg'
    cv2.imwrite(bmp, m_thresh)
    subprocess.run(['potrace', '-s', '--invert', '--alphamax', '1.0', '--opttolerance', str(opt), '-o', svg, bmp], check=True)
    subprocess.run(['qlmanage', '-t', '-s', '1000', '-o', 'scratch', svg], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Rendered blur_k={blur_k}, opt={opt}")

