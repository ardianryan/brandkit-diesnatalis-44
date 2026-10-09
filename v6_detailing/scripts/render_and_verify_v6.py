import os
import subprocess
import glob
import cv2
import numpy as np

print('=== RENDERING V6 SVGS TO 2048px PNG VIA WEBKIT (qlmanage) ===')
svg_files = sorted(glob.glob('v6_detailing/svg/*.svg'))
out_dir = 'v6_detailing/png'
os.makedirs(out_dir, exist_ok=True)
tmp_dir = 'v6_detailing/png/tmp_ql'
os.makedirs(tmp_dir, exist_ok=True)

for svg_path in svg_files:
    base = os.path.splitext(os.path.basename(svg_path))[0]
    out_png = os.path.join(out_dir, f'{base}.png')
    print(f'Rendering {base}.svg -> {out_png}...')
    cmd = ['qlmanage', '-t', '-s', '2048', '-o', tmp_dir, svg_path]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    generated = os.path.join(tmp_dir, f'{os.path.basename(svg_path)}.png')
    if os.path.exists(generated):
        os.replace(generated, out_png)
    else:
        print(f'Warning: {generated} not found!')

if os.path.exists(tmp_dir):
    os.rmdir(tmp_dir)

print('All 9 V6 PNGs rendered successfully.')

print('\n=== CHROMATIC METRICS VERIFICATION ===')
v6_master_png = 'v6_detailing/png/logo-v6-master.png'
v5_master_png = 'v5_revisi/png/logo-v5-master.png'
orig_png = 'digital hand draw.PNG' if os.path.exists('digital hand draw.PNG') else 'IMG_2172.PNG'

orig = cv2.imread(orig_png)
v5 = cv2.imread(v5_master_png)
v6 = cv2.imread(v6_master_png)

# Compute mean non-white BGR
def get_mean_color(img):
    mask = ~((img[:,:,0] > 240) & (img[:,:,1] > 240) & (img[:,:,2] > 240))
    px = img[mask]
    return np.mean(px, axis=0)

orig_mean = get_mean_color(orig)
v5_mean = get_mean_color(v5)
v6_mean = get_mean_color(v6)

print(f'Original  Mean BGR: B={orig_mean[0]:.2f}, G={orig_mean[1]:.2f}, R={orig_mean[2]:.2f}')
print(f'V5 Master Mean BGR: B={v5_mean[0]:.2f}, G={v5_mean[1]:.2f}, R={v5_mean[2]:.2f}')
print(f'V6 Master Mean BGR: B={v6_mean[0]:.2f}, G={v6_mean[1]:.2f}, R={v6_mean[2]:.2f}')

print('\n=== GENERATING VISUAL VERIFICATION CROPS ===')
cmp_dir = 'v6_detailing/comparison'
os.makedirs(cmp_dir, exist_ok=True)

# 1. Image 1: Wing Diagonal Ribbon (y=650..1150, x=650..1050)
cv2.imwrite(f'{cmp_dir}/crop_image1_wing_v5.png', v5[650:1150, 650:1050])
cv2.imwrite(f'{cmp_dir}/crop_image1_wing_v6.png', v6[650:1150, 650:1050])

# 2. Image 2: Tail Swoop & Lower Cusp (y=1300..1880, x=900..1450)
cv2.imwrite(f'{cmp_dir}/crop_image2_tail_v5.png', v5[1300:1880, 900:1450])
cv2.imwrite(f'{cmp_dir}/crop_image2_tail_v6.png', v6[1300:1880, 900:1450])

# 3. Flame 1 Valley (y=300..650, x=980..1250)
cv2.imwrite(f'{cmp_dir}/crop_flame1_v5.png', v5[300:650, 980:1250])
cv2.imwrite(f'{cmp_dir}/crop_flame1_v6.png', v6[300:650, 980:1250])

# Create Side-by-Side Comparison Boards
def make_side_by_side(img_left, img_right, title_left='v5 Revisi', title_right='v6 Detailing'):
    h, w, c = img_left.shape
    board = np.zeros((h + 60, w * 2 + 20, c), dtype=np.uint8)
    board[:] = [15, 20, 25]  # Dark background
    board[50:50+h, 0:w] = img_left
    board[50:50+h, w+20:w*2+20] = img_right
    cv2.putText(board, title_left, (20, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (180, 180, 180), 2, cv2.LINE_AA)
    cv2.putText(board, title_right, (w + 40, 36), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (56, 189, 248), 2, cv2.LINE_AA)
    return board

# Side-by-side boards:
sb_tail = make_side_by_side(v5[1300:1880, 900:1450], v6[1300:1880, 900:1450], 'v5 Tail (Starved Sliver 8%)', 'v6 Tail (Balanced Spine 42%)')
cv2.imwrite(f'{cmp_dir}/comparison_image2_tail.png', sb_tail)

sb_wing = make_side_by_side(v5[650:1150, 650:1050], v6[650:1150, 650:1050], 'v5 Wing (Reference)', 'v6 Wing (Preserved)')
cv2.imwrite(f'{cmp_dir}/comparison_image1_wing.png', sb_wing)

print('Side-by-side comparison boards saved to v6_detailing/comparison/!')
