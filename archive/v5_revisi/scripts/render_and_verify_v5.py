import os
import subprocess
import cv2
import numpy as np

print('=== RENDERING V5 SVGS TO 2048PX RASTERS WITH WEBKIT (FULL GRADIENT FIDELITY) ===')
os.makedirs('v5_revisi/png', exist_ok=True)
os.makedirs('v5_revisi/comparison', exist_ok=True)

svg_files = [
    'logo-v5-master',
    'logo-v5-tight',
    'logo-v5-with-grid',
    'logo-v5-monochrome-black',
    'logo-v5-monochrome-white',
    'logo-v5-horizontal-color',
    'logo-v5-horizontal-dark',
    'logo-v5-vertical-color',
    'logo-v5-linecut'
]

for name in svg_files:
    svg_fp = f'v5_revisi/svg/{name}.svg'
    png_fp = f'v5_revisi/png/{name}.png'
    tmp_png = f'v5_revisi/png/{name}.svg.png'
    print(f'Rendering {name}.svg -> {name}.png via WebKit...')
    subprocess.run(['qlmanage', '-t', '-s', '2048', '-o', 'v5_revisi/png', svg_fp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if os.path.exists(tmp_png):
        os.replace(tmp_png, png_fp)

print('\n=== GENERATING VERIFICATION COMPARISONS (V4 VS V5) ===')
v4_master = cv2.imread('v4_revisi/png/logo-v4-master.png')
v5_master = cv2.imread('v5_revisi/png/logo-v5-master.png')

# Generate zoom side-by-side comparison images for the 5 audited areas:
key_crops = [
    ('comparison-1-wing-ribbon-fold', (866, 1084), 160, 'Kotak 1 & 2: Wing Ribbon Fold Transition'),
    ('comparison-2-tail-cusp', (1080, 1585), 140, 'Kotak 3: Tail Inner Cusp & Spur Removal'),
    ('comparison-3-tail-tip', (1060, 1780), 140, 'Kotak 4: Tail Bottom Apex Needle Convergence'),
    ('comparison-4-flame1-outer-arc', (1050, 500), 160, 'Flame 1 Outer Arc: Zero Fringe & Harmonic Color'),
    ('comparison-5-flame-valley', (1090, 560), 160, 'Flame Valley 1-2: Smooth Inner Contour')
]

for fname, (cx, cy), sz, title in key_crops:
    x1 = max(0, cx - sz//2)
    y1 = max(0, cy - sz//2)
    x2 = min(2048, cx + sz//2)
    y2 = min(2048, cy + sz//2)
    
    crop_v4 = v4_master[y1:y2, x1:x2]
    crop_v5 = v5_master[y1:y2, x1:x2]
    
    scale = 3
    comp_v4_large = cv2.resize(crop_v4, (sz*scale, sz*scale), interpolation=cv2.INTER_NEAREST)
    comp_v5_large = cv2.resize(crop_v5, (sz*scale, sz*scale), interpolation=cv2.INTER_NEAREST)
    
    cv2.putText(comp_v4_large, 'V4 (Pucat/Flat)', (12, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(comp_v5_large, 'V5 (Harmonis/Emas)', (12, 32), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 128), 2, cv2.LINE_AA)
    
    divider = np.ones((sz*scale, 6, 3), dtype=np.uint8) * 128
    joined = np.hstack([comp_v4_large, divider, comp_v5_large])
    
    out_path = f'v5_revisi/comparison/{fname}.png'
    cv2.imwrite(out_path, joined)
    print(f'Generated comparison: {out_path}')

print('\nAll V5 renders and comparisons generated successfully!')
