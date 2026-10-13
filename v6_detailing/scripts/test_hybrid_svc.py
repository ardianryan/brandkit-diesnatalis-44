import cv2
import numpy as np
import subprocess
import xml.etree.ElementTree as ET
import os

# Load high-res crop of SVC
img = cv2.imread('scratch/svc_isolated_reference.png')
# Reference size: 725 x 395
h, w = img.shape[:2]

# Upscale 4x for super smooth bezier vectorization
scale = 4
hi = cv2.resize(img, (w * scale, h * scale), interpolation=cv2.INTER_LANCZOS4)

# Separate S, V, C regions in the high-res image
# In high-res coordinates (x * 4):
# S: x < 210 * scale
# C: x > 460 * scale
s_hi = hi[:, :int(220 * scale)]
c_hi = hi[:, int(460 * scale):]

def extract_facet_paths(crop, x_offset, name_prefix):
    # crop shape
    ch, cw = crop.shape[:2]
    b, g, r = cv2.split(crop)
    is_bg = (b > 35) & (r < 75) | ((r < 40) & (g < 40) & (b < 40))
    is_letter = ~is_bg & (r > 120) & (g > 70) & (b < 100) & (r > b + 45)
    
    # Facet masks
    m_light = is_letter & (r >= 225) & (g >= 175)
    m_shade = is_letter & (r >= 190) & (g >= 120) & ~m_light
    m_bevel = is_letter & (r >= 150) & (g >= 85) & ~m_light & ~m_shade
    m_depth = is_letter & ~m_light & ~m_shade & ~m_bevel
    
    facets = {}
    for fname, mask in [('depth', m_depth), ('bevel', m_bevel), ('shade', m_shade), ('light', m_light)]:
        bmp = f'scratch/h_{name_prefix}_{fname}.bmp'
        svg = f'scratch/h_{name_prefix}_{fname}.svg'
        m_u8 = (mask.astype(np.uint8)) * 255
        # 3px median blur removes raster pixelation while preserving sharp corners
        m_u8 = cv2.medianBlur(m_u8, 5)
        cv2.imwrite(bmp, m_u8)
        subprocess.run(['potrace', '-s', '--invert', '--alphamax', '1.0', '--opttolerance', '0.2', '-o', svg, bmp], check=True)
        
        # Parse path and adjust for coordinate offset
        tree = ET.parse(svg)
        root = tree.getroot()
        paths = []
        for g_elem in root.iter('{http://www.w3.org/2000/svg}g'):
            for p in g_elem.iter('{http://www.w3.org/2000/svg}path'):
                paths.append(p.attrib['d'])
        facets[fname] = ' '.join(paths)
        
    return facets

print("Tracing S facets...")
s_facets = extract_facet_paths(s_hi, 0, 's')
print("Tracing C facets...")
c_facets = extract_facet_paths(c_hi, 460 * scale, 'c')

# Potrace coordinate transformation:
# In high-res: potrace maps image height H = ch = 395 * 4 = 1580
# scale(0.1, -0.1) and translate(0, 1580)
# To place on 1000 x 1000 canvas with target letter size:
# The native letters are ~660 x 375 px.
# On 1000x1000 canvas, centered at (500, 500):
# Offset X = 170, Offset Y = 312
# Potrace output has scale 0.1 / 4 = 0.025 relative to canvas!

print("Done extracting facets!")
