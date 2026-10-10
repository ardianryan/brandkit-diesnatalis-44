"""
Skrip Generator Aset Penyerta Brand Kit Resmi (Expanded Edition)
Kategori: Supporting Brand Assets (Aset Ornamen & Kanvas Pendukung)
Proyek: Dies Natalis ke-44 SMA Negeri 1 Gedeg (1982 – 2026)
Palet Warna:
- Warna Utama: Coolors Resmi (Midnight Plum, Obsidian Mahogany, Crimson Fire, Bronze, Marigold, Vivid Gold, Champagne, Canary)
- Aksen Moodboard Fantasi: Tirai Beludru Magenta (#9D1B68), Rose Pink (#D4428D), Cotton Candy (#F5A8D0), Hypnotic Lilac (#9333EA), Mint (#5EEAD4)

Menghasilkan:
1. Magic Burst Rays (Pancaran Kerucut Cahaya Teater/Panggung)
2. Floating Magic Ribbons & Waves (Pita-pita Meliuk Melayang)
3. Confectionery Swirl Rosette (Pusaran Karamel & Roset Penomoran)
4. Magic Sparkles & Stardust Clusters (Bintang Kilau 4-Sudut)
5. Geometric Watermark Arcs (Garis Pandu Busur Piagam/Sertifikat)
6. Theater Curtain Drape Overlay (Tirai Beludru Teater Atas - PNG Transparan)
7. Cotton Candy Clouds Overlay (Awan Permen Kapas Pink - PNG Transparan)
8. Hypnotic Swirl Disc (Cakram Pusaran Hipnotis Ungu/Lilac - PNG Transparan)
9. Preset Backgrounds:
   - Deep Plum Stage (Feed 1:1 & Story 9:16)
   - Amber Caramel Sunset (Feed 1:1 & Story 9:16)
   - Golden Ticket Gala (Feed 1:1 & Story 9:16)
   - Hypnotic Purple Swirl (Feed 1:1 & Story 9:16 - Ungu & Lilac Spiral)
   - Fantasy Curtain Confectionery Stage (Feed 1:1 & Story 9:16 - Tirai Magenta & Spiral Pelangi Pastel)
   - Confectionery Icon Wallpaper Pattern (Feed 1:1 & Story 9:16 - Pola Motif Ikon Magis)
"""

import os
import math
import subprocess
import numpy as np
from PIL import Image

PALETTE = {
    "mahogany": "#310603",
    "crimson": "#7D1B05",
    "bronze": "#B6580B",
    "marigold": "#E09B17",
    "gold_vivid": "#F5C538",
    "champagne": "#F7D160",
    "canary": "#FDF39D",
    "plum": "#360538",
    # Fantasy Confectionery Accents
    "magenta": "#9D1B68",
    "rose_pink": "#D4428D",
    "candy_pink": "#F5A8D0",
    "lilac_purple": "#9333EA",
    "violet_deep": "#4A0E4E",
    "mint": "#5EEAD4",
    "cream": "#FFF8E7"
}

def render_svg_to_png(svg_path, out_png, width, height):
    abs_svg = os.path.abspath(svg_path)
    abs_out = os.path.abspath(out_png)
    chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    
    cmd = [
        chrome_bin,
        "--headless",
        "--disable-gpu",
        "--default-background-color=00000000",
        f"--window-size={width},{height}",
        f"--screenshot={abs_out}",
        f"file://{abs_svg}"
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# ==========================================
# 1. MAGIC BURST RAYS (KERUCUT SINAR PANGGUNG)
# ==========================================
def generate_magic_burst_svg(canvas_w=2400, canvas_h=2400):
    cx = canvas_w / 2.0
    cy = canvas_h * 0.92
    
    num_rays = 28
    spread_angle = math.radians(88)
    start_angle = -math.pi/2 - spread_angle/2
    angle_step = spread_angle / num_rays
    
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}">',
        '  <defs>',
        '    <linearGradient id="rayGradWarm" x1="0%" y1="100%" x2="0%" y2="0%">',
        f'      <stop offset="0%" stop-color="{PALETTE["canary"]}" stop-opacity="0.95" />',
        f'      <stop offset="35%" stop-color="{PALETTE["gold_vivid"]}" stop-opacity="0.85" />',
        f'      <stop offset="70%" stop-color="{PALETTE["marigold"]}" stop-opacity="0.5" />',
        f'      <stop offset="90%" stop-color="{PALETTE["crimson"]}" stop-opacity="0.2" />',
        f'      <stop offset="100%" stop-color="{PALETTE["plum"]}" stop-opacity="0.0" />',
        '    </linearGradient>',
        '    <linearGradient id="coreGlow" x1="0%" y1="100%" x2="0%" y2="0%">',
        f'      <stop offset="0%" stop-color="{PALETTE["canary"]}" stop-opacity="0.8" />',
        f'      <stop offset="40%" stop-color="{PALETTE["gold_vivid"]}" stop-opacity="0.45" />',
        f'      <stop offset="100%" stop-color="{PALETTE["marigold"]}" stop-opacity="0.0" />',
        '    </linearGradient>',
        '  </defs>',
        '  <g id="magic-cone-rays">'
    ]
    
    cone_p1 = f"{cx} {cy}"
    cone_p2 = f"{cx - math.sin(spread_angle/2)*2600:.1f} {cy - math.cos(spread_angle/2)*2600:.1f}"
    cone_p3 = f"{cx + math.sin(spread_angle/2)*2600:.1f} {cy - math.cos(spread_angle/2)*2600:.1f}"
    lines.append(f'    <polygon points="{cone_p1} {cone_p2} {cone_p3}" fill="url(#coreGlow)" opacity="0.6"/>')
    
    for i in range(num_rays):
        a1 = start_angle + i * angle_step
        a2 = a1 + (angle_step * 0.55 if i % 2 == 0 else angle_step * 0.35)
        
        r_far = 2800.0 if i % 2 == 0 else 2400.0
        x1, y1 = cx, cy
        x2 = cx + math.cos(a1) * r_far
        y2 = cy + math.sin(a1) * r_far
        x3 = cx + math.cos(a2) * r_far
        y3 = cy + math.sin(a2) * r_far
        
        poly = f"{x1:.1f},{y1:.1f} {x2:.1f},{y2:.1f} {x3:.1f},{y3:.1f}"
        op = 0.85 if i % 2 == 0 else 0.5
        lines.append(f'    <polygon points="{poly}" fill="url(#rayGradWarm)" opacity="{op:.2f}"/>')
        
    np.random.seed(44)
    for _ in range(65):
        ang = start_angle + np.random.uniform(0.05, 0.95) * spread_angle
        rad = np.random.uniform(200, 2000)
        px = cx + math.cos(ang) * rad
        py = cy + math.sin(ang) * rad
        sz = np.random.uniform(3, 14)
        alpha = np.random.uniform(0.4, 0.95)
        col = PALETTE["canary"] if np.random.rand() > 0.4 else PALETTE["champagne"]
        lines.append(f'    <circle cx="{px:.1f}" cy="{py:.1f}" r="{sz:.1f}" fill="{col}" opacity="{alpha:.2f}"/>')
        
    lines.append('  </g>')
    lines.append('</svg>')
    return "\n".join(lines)

# ==========================================
# 2. FLOATING MAGIC RIBBONS & WAVES
# ==========================================
def generate_magic_ribbon_svg(canvas_w=2400, canvas_h=1200):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}">',
        '  <defs>',
        '    <linearGradient id="ribbonGrad1" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'      <stop offset="0%" stop-color="{PALETTE["plum"]}" />',
        f'      <stop offset="30%" stop-color="{PALETTE["crimson"]}" />',
        f'      <stop offset="60%" stop-color="{PALETTE["bronze"]}" />',
        f'      <stop offset="85%" stop-color="{PALETTE["marigold"]}" />',
        f'      <stop offset="100%" stop-color="{PALETTE["gold_vivid"]}" />',
        '    </linearGradient>',
        '    <linearGradient id="ribbonGrad2" x1="0%" y1="0%" x2="100%" y2="0%">',
        f'      <stop offset="0%" stop-color="{PALETTE["canary"]}" stop-opacity="0.9" />',
        f'      <stop offset="50%" stop-color="{PALETTE["gold_vivid"]}" stop-opacity="0.8" />',
        f'      <stop offset="100%" stop-color="{PALETTE["bronze"]}" stop-opacity="0.4" />',
        '    </linearGradient>',
        '  </defs>',
        '  <g id="magic-ribbons">'
    ]
    
    p1 = "M 100 850 C 500 150, 950 1150, 1450 450 C 1800 -50, 2150 750, 2350 350 " \
         "L 2300 420 C 2100 820, 1750 20, 1400 520 C 900 1220, 450 220, 100 920 Z"
    lines.append(f'    <path d="{p1}" fill="url(#ribbonGrad1)" opacity="0.95" />')
    
    p2 = "M 120 780 C 520 80, 970 1080, 1470 380 C 1820 -120, 2170 680, 2370 280 " \
         "L 2350 310 C 2150 710, 1800 -90, 1450 410 C 950 1110, 500 110, 120 810 Z"
    lines.append(f'    <path d="{p2}" fill="url(#ribbonGrad2)" opacity="0.85" />')
    
    p3 = "M 200 300 C 600 700, 1200 200, 1700 850 C 1950 1150, 2200 900, 2320 750 " \
         "L 2300 780 C 2180 930, 1930 1180, 1680 880 C 1180 230, 580 730, 200 330 Z"
    lines.append(f'    <path d="{p3}" fill="{PALETTE["marigold"]}" opacity="0.65" />')
    
    for (sx, sy, sz) in [
        (480, 150, 18), (950, 1100, 14), (1420, 420, 22), 
        (1800, 80, 20), (2150, 720, 16), (1180, 240, 15)
    ]:
        lines.append(f'    <g transform="translate({sx}, {sy}) scale({sz/20.0})">')
        lines.append(f'      <path d="M 0 -20 Q 0 0 20 0 Q 0 0 0 20 Q 0 0 -20 0 Q 0 0 0 -20 Z" fill="{PALETTE["canary"]}"/>')
        lines.append(f'      <circle cx="0" cy="0" r="4" fill="#FFFFFF"/>')
        lines.append('    </g>')
        
    lines.append('  </g>')
    lines.append('</svg>')
    return "\n".join(lines)

# ==========================================
# 3. CONFECTIONERY SWIRL ROSETTE
# ==========================================
def generate_swirl_svg(canvas_dim=2000):
    cx = canvas_dim / 2.0
    cy = canvas_dim / 2.0
    r_outer = 850.0
    num_blades = 16
    
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_dim} {canvas_dim}" width="{canvas_dim}" height="{canvas_dim}">',
        '  <defs>',
        '    <linearGradient id="swirlPlum" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'      <stop offset="0%" stop-color="{PALETTE["plum"]}" />',
        f'      <stop offset="60%" stop-color="{PALETTE["crimson"]}" />',
        f'      <stop offset="100%" stop-color="{PALETTE["mahogany"]}" />',
        '    </linearGradient>',
        '    <linearGradient id="swirlGold" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'      <stop offset="0%" stop-color="{PALETTE["canary"]}" />',
        f'      <stop offset="40%" stop-color="{PALETTE["gold_vivid"]}" />',
        f'      <stop offset="85%" stop-color="{PALETTE["marigold"]}" />',
        f'      <stop offset="100%" stop-color="{PALETTE["bronze"]}" />',
        '    </linearGradient>',
        '  </defs>',
        '  <g id="confectionery-swirl">'
    ]
    
    lines.append(f'    <circle cx="{cx}" cy="{cy}" r="{r_outer + 35}" fill="url(#swirlGold)" stroke="{PALETTE["mahogany"]}" stroke-width="8"/>')
    lines.append(f'    <circle cx="{cx}" cy="{cy}" r="{r_outer + 15}" fill="{PALETTE["plum"]}"/>')
    
    for i in range(num_blades):
        a_start = (i / num_blades) * 2 * math.pi
        a_end = ((i + 1) / num_blades) * 2 * math.pi
        
        x0, y0 = cx, cy
        x1 = cx + math.cos(a_start) * r_outer
        y1 = cy + math.sin(a_start) * r_outer
        
        cp_ang = a_start + 0.42
        cpx = cx + math.cos(cp_ang) * (r_outer * 0.6)
        cpy = cy + math.sin(cp_ang) * (r_outer * 0.6)
        
        x2 = cx + math.cos(a_end) * r_outer
        y2 = cy + math.sin(a_end) * r_outer
        
        d = f"M {x0} {y0} Q {cpx} {cpy} {x1} {y1} A {r_outer} {r_outer} 0 0 1 {x2} {y2} Q {cpx} {cpy} {x0} {y0} Z"
        fill_col = "url(#swirlGold)" if (i % 2 == 0) else "url(#swirlPlum)"
        lines.append(f'    <path d="{d}" fill="{fill_col}"/>')
        
    lines.append(f'    <circle cx="{cx}" cy="{cy}" r="170" fill="url(#swirlGold)" stroke="{PALETTE["plum"]}" stroke-width="12"/>')
    lines.append(f'    <circle cx="{cx}" cy="{cy}" r="120" fill="{PALETTE["crimson"]}"/>')
    lines.append(f'    <circle cx="{cx}" cy="{cy}" r="65" fill="{PALETTE["canary"]}"/>')
    
    lines.append('  </g>')
    lines.append('</svg>')
    return "\n".join(lines)

# ==========================================
# 4. MAGIC SPARKLES & STARDUST CLUSTERS
# ==========================================
def generate_sparkles_cluster_svg(canvas_dim=2000):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_dim} {canvas_dim}" width="{canvas_dim}" height="{canvas_dim}">',
        '  <defs>',
        '    <linearGradient id="sparkleGrad" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'      <stop offset="0%" stop-color="{PALETTE["canary"]}" />',
        f'      <stop offset="60%" stop-color="{PALETTE["gold_vivid"]}" />',
        f'      <stop offset="100%" stop-color="{PALETTE["marigold"]}" />',
        '    </linearGradient>',
        '  </defs>',
        '  <g id="sparkle-clusters">'
    ]
    
    stars = [
        (1000, 1000, 240, 1.0),
        (650, 680, 140, 0.9),
        (1420, 620, 160, 0.95),
        (1380, 1380, 130, 0.85),
        (620, 1320, 110, 0.8),
        (1000, 480, 95, 0.85),
        (1000, 1550, 90, 0.75),
        (420, 980, 85, 0.8),
        (1600, 1020, 100, 0.85),
        (350, 450, 60, 0.7),
        (1650, 400, 75, 0.75),
        (1700, 1600, 70, 0.7),
        (320, 1620, 65, 0.7)
    ]
    
    for (sx, sy, sz, op) in stars:
        r_inner = sz * 0.16
        lines.append(f'  <g transform="translate({sx}, {sy})" opacity="{op}">')
        pure_star = f"M 0 {-sz} Q {r_inner} {-r_inner} {sz} 0 Q {r_inner} {r_inner} 0 {sz} Q {-r_inner} {r_inner} {-sz} 0 Q {-r_inner} {-r_inner} 0 {-sz} Z"
        lines.append(f'    <path d="{pure_star}" fill="url(#sparkleGrad)" />')
        lines.append(f'    <circle cx="0" cy="0" r="{sz*0.14:.1f}" fill="#FFFFFF" />')
        lines.append('  </g>')
        
    np.random.seed(99)
    for _ in range(80):
        px = np.random.uniform(150, 1850)
        py = np.random.uniform(150, 1850)
        pr = np.random.uniform(3, 10)
        pop = np.random.uniform(0.35, 0.9)
        pcol = PALETTE["canary"] if np.random.rand() > 0.3 else PALETTE["champagne"]
        lines.append(f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="{pr:.1f}" fill="{pcol}" opacity="{pop:.2f}"/>')
        
    lines.append('  </g>')
    lines.append('</svg>')
    return "\n".join(lines)

# ==========================================
# 5. GEOMETRIC BLUEPRINT WATERMARK ARCS
# ==========================================
def generate_watermark_arcs_svg(canvas_w=2800, canvas_h=2000, color_mode="gold"):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}">',
        '  <g id="geometric-arcs">'
    ]
    
    stroke_col = PALETTE["gold_vivid"] if color_mode == "gold" else PALETTE["plum"]
    
    c1x, c1y = 400.0, 1000.0
    c2x, c2y = 2400.0, 1000.0
    
    radii = [250, 420, 600, 800, 1020, 1260, 1520, 1800, 2100]
    for r in radii:
        op = max(0.12, 0.45 - (r / 5000.0))
        lines.append(f'    <circle cx="{c1x}" cy="{c1y}" r="{r}" fill="none" stroke="{stroke_col}" stroke-width="2.5" opacity="{op:.2f}" stroke-dasharray="12,12"/>')
        lines.append(f'    <circle cx="{c2x}" cy="{c2y}" r="{r}" fill="none" stroke="{stroke_col}" stroke-width="2.5" opacity="{op:.2f}" stroke-dasharray="12,12"/>')
        
    lines.append(f'    <line x1="{canvas_w/2}" y1="100" x2="{canvas_w/2}" y2="{canvas_h-100}" stroke="{stroke_col}" stroke-width="3" opacity="0.4" stroke-dasharray="8,8"/>')
    lines.append(f'    <line x1="200" y1="{canvas_h/2}" x2="{canvas_w-200}" y2="{canvas_h/2}" stroke="{stroke_col}" stroke-width="3" opacity="0.4" stroke-dasharray="8,8"/>')
    lines.append(f'    <line x1="200" y1="200" x2="{canvas_w-200}" y2="{canvas_h-200}" stroke="{stroke_col}" stroke-width="2" opacity="0.25"/>')
    lines.append(f'    <line x1="{canvas_w-200}" y1="200" x2="200" y2="{canvas_h-200}" stroke="{stroke_col}" stroke-width="2" opacity="0.25"/>')
    
    for rx in [600, 1000, 1400]:
        lines.append(f'    <polygon points="{canvas_w/2},{canvas_h/2 - rx} {canvas_w/2 + rx},{canvas_h/2} {canvas_w/2},{canvas_h/2 + rx} {canvas_w/2 - rx},{canvas_h/2}" fill="none" stroke="{stroke_col}" stroke-width="2" opacity="0.2"/>')
        
    lines.append('  </g>')
    lines.append('</svg>')
    return "\n".join(lines)

# ==========================================
# 6. THEATER CURTAIN DRAPE OVERLAY (ATAS)
# ==========================================
def generate_curtain_drape_svg(canvas_w=2400, canvas_h=800):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}">',
        '  <defs>',
        '    <linearGradient id="curtainGrad" x1="0%" y1="0%" x2="0%" y2="100%">',
        f'      <stop offset="0%" stop-color="{PALETTE["mahogany"]}" />',
        f'      <stop offset="30%" stop-color="{PALETTE["crimson"]}" />',
        f'      <stop offset="70%" stop-color="{PALETTE["magenta"]}" />',
        f'      <stop offset="95%" stop-color="{PALETTE["rose_pink"]}" />',
        f'      <stop offset="100%" stop-color="{PALETTE["plum"]}" />',
        '    </linearGradient>',
        '    <linearGradient id="curtainGoldTrim" x1="0%" y1="0%" x2="100%" y2="0%">',
        f'      <stop offset="0%" stop-color="{PALETTE["bronze"]}" />',
        f'      <stop offset="50%" stop-color="{PALETTE["gold_vivid"]}" />',
        f'      <stop offset="100%" stop-color="{PALETTE["canary"]}" />',
        '    </linearGradient>',
        '  </defs>',
        '  <g id="theater-curtain-drape">'
    ]
    
    # 5 Big luxurious scallop loops across width
    num_scallops = 6
    w_sc = canvas_w / num_scallops
    
    for i in range(num_scallops):
        x_left = i * w_sc
        x_right = (i + 1) * w_sc
        x_mid = (x_left + x_right) / 2.0
        depth = 380.0 if (i == 0 or i == num_scallops-1) else 460.0
        
        # Scallop body
        d_scallop = f"M {x_left} 0 L {x_right} 0 L {x_right} 80 Q {x_mid} {depth} {x_left} 80 Z"
        lines.append(f'    <path d="{d_scallop}" fill="url(#curtainGrad)" opacity="0.95"/>')
        
        # Pleat folds (shading shadow lines)
        for fold_offset in [-w_sc*0.25, 0, w_sc*0.25]:
            fx = x_mid + fold_offset
            lines.append(f'    <path d="M {fx} 20 Q {fx} {depth*0.8} {x_mid} {depth-15}" stroke="{PALETTE["mahogany"]}" stroke-width="6" opacity="0.4" fill="none"/>')
            lines.append(f'    <path d="M {fx+5} 20 Q {fx+5} {depth*0.8} {x_mid+5} {depth-15}" stroke="{PALETTE["rose_pink"]}" stroke-width="2.5" opacity="0.6" fill="none"/>')
            
        # Golden fringe trim on scallop hem
        d_fringe = f"M {x_left} 80 Q {x_mid} {depth} {x_right} 80"
        lines.append(f'    <path d="{d_fringe}" fill="none" stroke="url(#curtainGoldTrim)" stroke-width="10"/>')
        lines.append(f'    <path d="{d_fringe}" fill="none" stroke="{PALETTE["canary"]}" stroke-width="3" stroke-dasharray="6,6"/>')
        
    # Top valance banner bar
    lines.append(f'  <rect x="0" y="0" width="{canvas_w}" height="45" fill="{PALETTE["mahogany"]}"/>')
    lines.append(f'  <rect x="0" y="45" width="{canvas_w}" height="8" fill="url(#curtainGoldTrim)"/>')
    
    lines.append('  </g>')
    lines.append('</svg>')
    return "\n".join(lines)

# ==========================================
# 7. COTTON CANDY CLOUDS OVERLAY
# ==========================================
def generate_cotton_candy_clouds_svg(canvas_w=2400, canvas_h=1000):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w} {canvas_h}" width="{canvas_w}" height="{canvas_h}">',
        '  <defs>',
        '    <linearGradient id="cloudPink" x1="0%" y1="100%" x2="0%" y2="0%">',
        f'      <stop offset="0%" stop-color="{PALETTE["magenta"]}" stop-opacity="0.8" />',
        f'      <stop offset="45%" stop-color="{PALETTE["rose_pink"]}" stop-opacity="0.85" />',
        f'      <stop offset="85%" stop-color="{PALETTE["candy_pink"]}" stop-opacity="0.95" />',
        f'      <stop offset="100%" stop-color="#FFFFFF" stop-opacity="0.9" />',
        '    </linearGradient>',
        '  </defs>',
        '  <g id="cotton-candy-clouds">'
    ]
    
    # Cloud puff clusters (3 major clusters)
    clusters = [
        (450, 650, 320),
        (1200, 580, 420),
        (1950, 640, 350)
    ]
    
    for (cx, cy, base_r) in clusters:
        lines.append(f'  <g opacity="0.9">')
        # multiple overlapping soft circles
        offsets = [
            (0, 0, base_r),
            (-base_r*0.65, base_r*0.1, base_r*0.75),
            (base_r*0.65, base_r*0.15, base_r*0.78),
            (-base_r*0.35, -base_r*0.45, base_r*0.68),
            (base_r*0.35, -base_r*0.4, base_r*0.7),
            (0, -base_r*0.55, base_r*0.62)
        ]
        for (ox, oy, orad) in offsets:
            lines.append(f'    <circle cx="{cx+ox}" cy="{cy+oy}" r="{orad}" fill="url(#cloudPink)"/>')
        lines.append('  </g>')
        
    lines.append('  </g>')
    lines.append('</svg>')
    return "\n".join(lines)

# ==========================================
# 8. HYPNOTIC SWIRL DISC
# ==========================================
def generate_hypnotic_swirl_disc_svg(canvas_dim=2000):
    cx = canvas_dim / 2.0
    cy = canvas_dim / 2.0
    r_outer = 950.0
    num_arms = 20
    
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_dim} {canvas_dim}" width="{canvas_dim}" height="{canvas_dim}">',
        '  <defs>',
        '    <linearGradient id="discPurple" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'      <stop offset="0%" stop-color="{PALETTE["plum"]}" />',
        f'      <stop offset="50%" stop-color="{PALETTE["violet_deep"]}" />',
        f'      <stop offset="100%" stop-color="{PALETTE["mahogany"]}" />',
        '    </linearGradient>',
        '    <linearGradient id="discLilac" x1="0%" y1="0%" x2="100%" y2="100%">',
        f'      <stop offset="0%" stop-color="{PALETTE["lilac_purple"]}" />',
        f'      <stop offset="50%" stop-color="{PALETTE["rose_pink"]}" />',
        f'      <stop offset="100%" stop-color="{PALETTE["candy_pink"]}" />',
        '    </linearGradient>',
        '  </defs>',
        '  <g id="hypnotic-swirl-disc">'
    ]
    
    lines.append(f'  <circle cx="{cx}" cy="{cy}" r="{r_outer}" fill="{PALETTE["plum"]}"/>')
    
    for i in range(num_arms):
        a_start = (i / num_arms) * 2 * math.pi
        a_end = ((i + 1) / num_arms) * 2 * math.pi
        
        # spiral curvature via cubic bezier
        x0, y0 = cx, cy
        
        # Outer rim points with angular twist
        twist = 1.35
        x1 = cx + math.cos(a_start + twist) * r_outer
        y1 = cy + math.sin(a_start + twist) * r_outer
        
        cpx = cx + math.cos(a_start + twist*0.5) * (r_outer * 0.45)
        cpy = cy + math.sin(a_start + twist*0.5) * (r_outer * 0.45)
        
        x2 = cx + math.cos(a_end + twist) * r_outer
        y2 = cy + math.sin(a_end + twist) * r_outer
        
        d = f"M {x0} {y0} Q {cpx} {cpy} {x1} {y1} A {r_outer} {r_outer} 0 0 1 {x2} {y2} Q {cpx} {cpy} {x0} {y0} Z"
        fill_col = "url(#discLilac)" if (i % 2 == 0) else "url(#discPurple)"
        lines.append(f'  <path d="{d}" fill="{fill_col}"/>')
        
    lines.append(f'  <circle cx="{cx}" cy="{cy}" r="110" fill="{PALETTE["rose_pink"]}"/>')
    lines.append(f'  <circle cx="{cx}" cy="{cy}" r="50" fill="{PALETTE["cream"]}"/>')
    lines.append('  </g>')
    lines.append('</svg>')
    return "\n".join(lines)

# ==========================================
# 9. EXPANDED CANVAS BACKGROUND PRESETS
# ==========================================
def generate_background_svg(width=2048, height=2048, theme="deep_plum_stage"):
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
        '  <defs>'
    ]
    
    if theme == "deep_plum_stage":
        lines.extend([
            f'    <radialGradient id="stageGlow" cx="50%" cy="45%" r="75%">',
            f'      <stop offset="0%" stop-color="{PALETTE["crimson"]}" />',
            f'      <stop offset="45%" stop-color="{PALETTE["plum"]}" />',
            f'      <stop offset="85%" stop-color="{PALETTE["mahogany"]}" />',
            f'      <stop offset="100%" stop-color="#140203" />',
            f'    </radialGradient>',
            f'    <linearGradient id="warmSpotlight" x1="50%" y1="100%" x2="50%" y2="0%">',
            f'      <stop offset="0%" stop-color="{PALETTE["marigold"]}" stop-opacity="0.45" />',
            f'      <stop offset="50%" stop-color="{PALETTE["bronze"]}" stop-opacity="0.2" />',
            f'      <stop offset="100%" stop-color="{PALETTE["plum"]}" stop-opacity="0.0" />',
            f'    </linearGradient>'
        ])
    elif theme == "amber_caramel_sunset":
        lines.extend([
            f'    <radialGradient id="amberGlow" cx="50%" cy="30%" r="80%">',
            f'      <stop offset="0%" stop-color="{PALETTE["gold_vivid"]}" />',
            f'      <stop offset="35%" stop-color="{PALETTE["marigold"]}" />',
            f'      <stop offset="70%" stop-color="{PALETTE["bronze"]}" />',
            f'      <stop offset="92%" stop-color="{PALETTE["crimson"]}" />',
            f'      <stop offset="100%" stop-color="{PALETTE["plum"]}" />',
            f'    </radialGradient>'
        ])
    elif theme == "golden_ticket_gala":
        lines.extend([
            f'    <linearGradient id="ticketGala" x1="0%" y1="0%" x2="100%" y2="100%">',
            f'      <stop offset="0%" stop-color="{PALETTE["mahogany"]}" />',
            f'      <stop offset="30%" stop-color="{PALETTE["plum"]}" />',
            f'      <stop offset="70%" stop-color="{PALETTE["crimson"]}" />',
            f'      <stop offset="100%" stop-color="{PALETTE["mahogany"]}" />',
            f'    </linearGradient>',
            f'    <linearGradient id="goldBorder" x1="0%" y1="0%" x2="100%" y2="100%">',
            f'      <stop offset="0%" stop-color="{PALETTE["canary"]}" />',
            f'      <stop offset="25%" stop-color="{PALETTE["gold_vivid"]}" />',
            f'      <stop offset="75%" stop-color="{PALETTE["champagne"]}" />',
            f'      <stop offset="100%" stop-color="{PALETTE["bronze"]}" />',
            f'    </linearGradient>'
        ])
    elif theme == "hypnotic_purple_swirl":
        lines.extend([
            f'    <linearGradient id="swirlArmLilac" x1="0%" y1="0%" x2="100%" y2="100%">',
            f'      <stop offset="0%" stop-color="{PALETTE["candy_pink"]}" />',
            f'      <stop offset="35%" stop-color="{PALETTE["rose_pink"]}" />',
            f'      <stop offset="75%" stop-color="{PALETTE["lilac_purple"]}" />',
            f'      <stop offset="100%" stop-color="{PALETTE["violet_deep"]}" />',
            f'    </linearGradient>',
            f'    <linearGradient id="swirlArmPlum" x1="0%" y1="0%" x2="100%" y2="100%">',
            f'      <stop offset="0%" stop-color="{PALETTE["plum"]}" />',
            f'      <stop offset="70%" stop-color="{PALETTE["violet_deep"]}" />',
            f'      <stop offset="100%" stop-color="{PALETTE["mahogany"]}" />',
            f'    </linearGradient>',
            f'    <radialGradient id="swirlCenterGlow" cx="50%" cy="50%" r="40%">',
            f'      <stop offset="0%" stop-color="{PALETTE["candy_pink"]}" stop-opacity="0.8" />',
            f'      <stop offset="40%" stop-color="{PALETTE["rose_pink"]}" stop-opacity="0.4" />',
            f'      <stop offset="100%" stop-color="{PALETTE["plum"]}" stop-opacity="0.0" />',
            f'    </radialGradient>'
        ])
    elif theme == "fantasy_confectionery_stage":
        lines.extend([
            f'    <radialGradient id="stagePastelGlow" cx="50%" cy="40%" r="70%">',
            f'      <stop offset="0%" stop-color="{PALETTE["cream"]}" />',
            f'      <stop offset="30%" stop-color="{PALETTE["candy_pink"]}" />',
            f'      <stop offset="60%" stop-color="{PALETTE["mint"]}" />',
            f'      <stop offset="85%" stop-color="{PALETTE["lilac_purple"]}" />',
            f'      <stop offset="100%" stop-color="{PALETTE["plum"]}" />',
            f'    </radialGradient>',
            f'    <linearGradient id="curtainPinkGrad" x1="0%" y1="0%" x2="0%" y2="100%">',
            f'      <stop offset="0%" stop-color="{PALETTE["crimson"]}" />',
            f'      <stop offset="50%" stop-color="{PALETTE["magenta"]}" />',
            f'      <stop offset="90%" stop-color="{PALETTE["rose_pink"]}" />',
            f'      <stop offset="100%" stop-color="{PALETTE["plum"]}" />',
            f'    </linearGradient>',
            f'    <linearGradient id="goldTrimGrad" x1="0%" y1="0%" x2="100%" y2="0%">',
            f'      <stop offset="0%" stop-color="{PALETTE["gold_vivid"]}" />',
            f'      <stop offset="100%" stop-color="{PALETTE["canary"]}" />',
            f'    </linearGradient>'
        ])
    elif theme == "confectionery_icon_wallpaper":
        lines.extend([
            f'    <radialGradient id="wallpaperBg" cx="50%" cy="50%" r="75%">',
            f'      <stop offset="0%" stop-color="{PALETTE["violet_deep"]}" />',
            f'      <stop offset="50%" stop-color="{PALETTE["plum"]}" />',
            f'      <stop offset="100%" stop-color="#1B021E" />',
            f'    </radialGradient>'
        ])
        
    lines.append('  </defs>')
    
    # RENDER BACKGROUND ACCORDING TO THEME
    if theme == "deep_plum_stage":
        lines.append(f'  <rect width="{width}" height="{height}" fill="url(#stageGlow)"/>')
        poly = f"{width*0.5},{height*0.95} {width*0.1},{height*0.05} {width*0.9},{height*0.05}"
        lines.append(f'  <polygon points="{poly}" fill="url(#warmSpotlight)"/>')
        lines.append(f'  <rect x="50" y="50" width="{width-100}" height="{height-100}" fill="none" stroke="{PALETTE["gold_vivid"]}" stroke-width="2.5" opacity="0.35"/>')
        lines.append(f'  <rect x="75" y="75" width="{width-150}" height="{height-150}" fill="none" stroke="{PALETTE["champagne"]}" stroke-width="1.5" opacity="0.2"/>')
        
    elif theme == "amber_caramel_sunset":
        lines.append(f'  <rect width="{width}" height="{height}" fill="url(#amberGlow)"/>')
        p_wave = f"M 0 {height*0.75} Q {width*0.25} {height*0.65} {width*0.5} {height*0.8} T {width} {height*0.72} L {width} {height} L 0 {height} Z"
        lines.append(f'  <path d="{p_wave}" fill="{PALETTE["plum"]}" opacity="0.85"/>')
        lines.append(f'  <rect x="40" y="40" width="{width-80}" height="{height-80}" fill="none" stroke="{PALETTE["canary"]}" stroke-width="2" opacity="0.4"/>')
        
    elif theme == "golden_ticket_gala":
        lines.append(f'  <rect width="{width}" height="{height}" fill="url(#ticketGala)"/>')
        pad = 80
        lines.append(f'  <rect x="{pad}" y="{pad}" width="{width-pad*2}" height="{height-pad*2}" fill="none" stroke="url(#goldBorder)" stroke-width="10"/>')
        lines.append(f'  <rect x="{pad+25}" y="{pad+25}" width="{width-(pad+25)*2}" height="{height-(pad+25)*2}" fill="none" stroke="{PALETTE["gold_vivid"]}" stroke-width="3" stroke-dasharray="14,14" opacity="0.65"/>')
        for cx, cy in [(pad, pad), (width-pad, pad), (pad, height-pad), (width-pad, height-pad)]:
            lines.append(f'  <circle cx="{cx}" cy="{cy}" r="22" fill="url(#goldBorder)"/>')
            lines.append(f'  <circle cx="{cx}" cy="{cy}" r="12" fill="{PALETTE["plum"]}"/>')
            
    elif theme == "hypnotic_purple_swirl":
        # Base deep violet fill
        lines.append(f'  <rect width="{width}" height="{height}" fill="{PALETTE["plum"]}"/>')
        cx, cy = width / 2.0, height / 2.0
        r_reach = math.hypot(width, height) * 0.75
        num_spiral_arms = 24
        twist_rad = 1.65
        
        for i in range(num_spiral_arms):
            a_s = (i / num_spiral_arms) * 2 * math.pi
            a_e = ((i + 1) / num_spiral_arms) * 2 * math.pi
            
            x1 = cx + math.cos(a_s + twist_rad) * r_reach
            y1 = cy + math.sin(a_s + twist_rad) * r_reach
            
            cpx = cx + math.cos(a_s + twist_rad * 0.45) * (r_reach * 0.4)
            cpy = cy + math.sin(a_s + twist_rad * 0.45) * (r_reach * 0.4)
            
            x2 = cx + math.cos(a_e + twist_rad) * r_reach
            y2 = cy + math.sin(a_e + twist_rad) * r_reach
            
            d_arm = f"M {cx} {cy} Q {cpx} {cpy} {x1} {y1} L {x2} {y2} Q {cpx} {cpy} {cx} {cy} Z"
            arm_col = "url(#swirlArmLilac)" if (i % 2 == 0) else "url(#swirlArmPlum)"
            lines.append(f'  <path d="{d_arm}" fill="{arm_col}"/>')
            
        # Center glow burst
        lines.append(f'  <circle cx="{cx}" cy="{cy}" r="{width*0.4}" fill="url(#swirlCenterGlow)"/>')
        
    elif theme == "fantasy_confectionery_stage":
        # Pastel confectionery swirl base
        lines.append(f'  <rect width="{width}" height="{height}" fill="url(#stagePastelGlow)"/>')
        cx, cy = width / 2.0, height * 0.52
        r_sw = math.hypot(width, height) * 0.7
        num_pastels = 20
        twist = 1.2
        
        for i in range(num_pastels):
            a_s = (i / num_pastels) * 2 * math.pi
            a_e = ((i + 1) / num_pastels) * 2 * math.pi
            
            x1 = cx + math.cos(a_s + twist) * r_sw
            y1 = cy + math.sin(a_s + twist) * r_sw
            cpx = cx + math.cos(a_s + twist * 0.5) * (r_sw * 0.5)
            cpy = cy + math.sin(a_s + twist * 0.5) * (r_sw * 0.5)
            x2 = cx + math.cos(a_e + twist) * r_sw
            y2 = cy + math.sin(a_e + twist) * r_sw
            
            d_p = f"M {cx} {cy} Q {cpx} {cpy} {x1} {y1} L {x2} {y2} Q {cpx} {cpy} {cx} {cy} Z"
            colors = [PALETTE["candy_pink"], PALETTE["mint"], PALETTE["cream"], PALETTE["rose_pink"]]
            lines.append(f'  <path d="{d_p}" fill="{colors[i % 4]}" opacity="0.35"/>')
            
        # TOP DRAPED THEATER CURTAINS
        num_scallops = 5
        w_sc = width / num_scallops
        d_depth = height * 0.22
        
        for i in range(num_scallops):
            x_l = i * w_sc
            x_r = (i + 1) * w_sc
            x_m = (x_l + x_r) / 2.0
            
            d_curtain = f"M {x_l} 0 L {x_r} 0 L {x_r} 30 Q {x_m} {d_depth} {x_l} 30 Z"
            lines.append(f'  <path d="{d_curtain}" fill="url(#curtainPinkGrad)" opacity="0.95"/>')
            lines.append(f'  <path d="M {x_l} 30 Q {x_m} {d_depth} {x_r} 30" fill="none" stroke="url(#goldTrimGrad)" stroke-width="8"/>')
            
        # Top banner rail
        lines.append(f'  <rect x="0" y="0" width="{width}" height="28" fill="{PALETTE["mahogany"]}"/>')
        lines.append(f'  <rect x="0" y="28" width="{width}" height="6" fill="url(#goldTrimGrad)"/>')
        
    elif theme == "confectionery_icon_wallpaper":
        lines.append(f'  <rect width="{width}" height="{height}" fill="url(#wallpaperBg)"/>')
        # Repeated motif grid
        grid_step = 240
        cols = int(width / grid_step) + 2
        rows = int(height / grid_step) + 2
        
        np.random.seed(44)
        for r in range(rows):
            for c in range(cols):
                gx = c * grid_step + (120 if r % 2 == 1 else 0)
                gy = r * grid_step
                
                motif_type = (r + c) % 5
                lines.append(f'  <g transform="translate({gx}, {gy})">')
                if motif_type == 0:
                    # Mini candy swirl
                    lines.append(f'    <circle cx="0" cy="0" r="28" fill="{PALETTE["rose_pink"]}" opacity="0.85"/>')
                    lines.append(f'    <circle cx="0" cy="0" r="18" fill="{PALETTE["canary"]}" opacity="0.85"/>')
                    lines.append(f'    <circle cx="0" cy="0" r="8" fill="{PALETTE["plum"]}"/>')
                elif motif_type == 1:
                    # Magician hat mini
                    lines.append(f'    <ellipse cx="0" cy="18" rx="32" ry="10" fill="{PALETTE["mahogany"]}" opacity="0.9"/>')
                    lines.append(f'    <path d="M -22 18 L -16 -24 L 16 -24 L 22 18 Z" fill="{PALETTE["crimson"]}" opacity="0.9"/>')
                    lines.append(f'    <rect x="-18" y="8" width="36" height="6" fill="{PALETTE["gold_vivid"]}"/>')
                elif motif_type == 2:
                    # 4-point magic star
                    sz = 26
                    pure_star = f"M 0 {-sz} Q 4 -4 {sz} 0 Q 4 4 0 {sz} Q -4 4 {-sz} 0 Q -4 -4 0 {-sz} Z"
                    lines.append(f'    <path d="{pure_star}" fill="{PALETTE["gold_vivid"]}" opacity="0.9"/>')
                    lines.append(f'    <circle cx="0" cy="0" r="4" fill="#FFFFFF"/>')
                elif motif_type == 3:
                    # Sweet cloud mini
                    lines.append(f'    <circle cx="-14" cy="6" r="16" fill="{PALETTE["candy_pink"]}" opacity="0.85"/>')
                    lines.append(f'    <circle cx="14" cy="6" r="16" fill="{PALETTE["candy_pink"]}" opacity="0.85"/>')
                    lines.append(f'    <circle cx="0" cy="-6" r="20" fill="{PALETTE["candy_pink"]}" opacity="0.85"/>')
                    lines.append(f'    <polygon points="-4,-2 8,-2 -2,18" fill="{PALETTE["canary"]}"/>')
                elif motif_type == 4:
                    # Gift box mini
                    lines.append(f'    <rect x="-18" y="-14" width="36" height="32" rx="4" fill="{PALETTE["magenta"]}" opacity="0.85"/>')
                    lines.append(f'    <line x1="0" y1="-14" x2="0" y2="18" stroke="{PALETTE["canary"]}" stroke-width="6"/>')
                    lines.append(f'    <line x1="-18" y1="2" x2="18" y2="2" stroke="{PALETTE["canary"]}" stroke-width="6"/>')
                lines.append('  </g>')
                
    lines.append('</svg>')
    return "\n".join(lines)

def main():
    base_dir = "assets/brandkit_elements"
    svg_dir = os.path.join(base_dir, "svg")
    png_dir = os.path.join(base_dir, "png")
    bg_dir = os.path.join(base_dir, "backgrounds")
    
    os.makedirs(svg_dir, exist_ok=True)
    os.makedirs(png_dir, exist_ok=True)
    os.makedirs(bg_dir, exist_ok=True)
    
    print("==================================================================")
    print(" GENERATING EXPANDED SUPPORTING BRAND KIT ASSETS (DIES NATALIS 44)")
    print("==================================================================")
    
    # 1. Magic Burst Rays
    print("\n[1/8] Generating Magic Burst Rays...")
    burst_svg = generate_magic_burst_svg(2400, 2400)
    burst_svg_file = os.path.join(svg_dir, "magic-burst-rays.svg")
    burst_png_file = os.path.join(png_dir, "magic-burst-rays.png")
    with open(burst_svg_file, "w") as f:
        f.write(burst_svg)
    render_svg_to_png(burst_svg_file, burst_png_file, 2400, 2400)
    print(f"✓ {burst_svg_file} & {burst_png_file}")
    
    # 2. Floating Magic Ribbons & Waves
    print("\n[2/8] Generating Floating Magic Ribbons & Waves...")
    ribbon_svg = generate_magic_ribbon_svg(2400, 1200)
    ribbon_svg_file = os.path.join(svg_dir, "floating-magic-ribbons.svg")
    ribbon_png_file = os.path.join(png_dir, "floating-magic-ribbons.png")
    with open(ribbon_svg_file, "w") as f:
        f.write(ribbon_svg)
    render_svg_to_png(ribbon_svg_file, ribbon_png_file, 2400, 1200)
    print(f"✓ {ribbon_svg_file} & {ribbon_png_file}")
    
    # 3. Confectionery Swirl Rosette
    print("\n[3/8] Generating Confectionery Swirl Rosette...")
    swirl_svg = generate_swirl_svg(2000)
    swirl_svg_file = os.path.join(svg_dir, "confectionery-swirl-badge.svg")
    swirl_png_file = os.path.join(png_dir, "confectionery-swirl-badge.png")
    with open(swirl_svg_file, "w") as f:
        f.write(swirl_svg)
    render_svg_to_png(swirl_svg_file, swirl_png_file, 2000, 2000)
    print(f"✓ {swirl_svg_file} & {swirl_png_file}")
    
    # 4. Magic Sparkles & Stardust Clusters
    print("\n[4/8] Generating Magic Sparkles & Stardust Clusters...")
    sparkle_svg = generate_sparkles_cluster_svg(2000)
    sparkle_svg_file = os.path.join(svg_dir, "magic-sparkles-cluster.svg")
    sparkle_png_file = os.path.join(png_dir, "magic-sparkles-cluster.png")
    with open(sparkle_svg_file, "w") as f:
        f.write(sparkle_svg)
    render_svg_to_png(sparkle_svg_file, sparkle_png_file, 2000, 2000)
    print(f"✓ {sparkle_svg_file} & {sparkle_png_file}")
    
    # 5. Geometric Watermark Blueprint Arcs
    print("\n[5/8] Generating Geometric Blueprint Watermark Arcs...")
    for cmode in ["gold", "plum"]:
        wm_svg = generate_watermark_arcs_svg(2800, 2000, color_mode=cmode)
        wm_svg_file = os.path.join(svg_dir, f"watermark-arcs-{cmode}.svg")
        wm_png_file = os.path.join(png_dir, f"watermark-arcs-{cmode}.png")
        with open(wm_svg_file, "w") as f:
            f.write(wm_svg)
        render_svg_to_png(wm_svg_file, wm_png_file, 2800, 2000)
        print(f"✓ {wm_svg_file} & {wm_png_file}")
        
    # 6. Theater Curtain Drape Overlay (NEW!)
    print("\n[6/8] Generating Theater Curtain Drape Overlay...")
    curtain_svg = generate_curtain_drape_svg(2400, 800)
    curtain_svg_file = os.path.join(svg_dir, "theater-curtain-drape.svg")
    curtain_png_file = os.path.join(png_dir, "theater-curtain-drape.png")
    with open(curtain_svg_file, "w") as f:
        f.write(curtain_svg)
    render_svg_to_png(curtain_svg_file, curtain_png_file, 2400, 800)
    print(f"✓ {curtain_svg_file} & {curtain_png_file}")
    
    # 7. Cotton Candy Clouds Overlay (NEW!)
    print("\n[7/8] Generating Cotton Candy Clouds Overlay...")
    clouds_svg = generate_cotton_candy_clouds_svg(2400, 1000)
    clouds_svg_file = os.path.join(svg_dir, "cotton-candy-clouds.svg")
    clouds_png_file = os.path.join(png_dir, "cotton-candy-clouds.png")
    with open(clouds_svg_file, "w") as f:
        f.write(clouds_svg)
    render_svg_to_png(clouds_svg_file, clouds_png_file, 2400, 1000)
    print(f"✓ {clouds_svg_file} & {clouds_png_file}")
    
    # 8. Hypnotic Swirl Disc (NEW!)
    print("\n[8/8] Generating Hypnotic Swirl Disc...")
    hdisc_svg = generate_hypnotic_swirl_disc_svg(2000)
    hdisc_svg_file = os.path.join(svg_dir, "hypnotic-swirl-disc.svg")
    hdisc_png_file = os.path.join(png_dir, "hypnotic-swirl-disc.png")
    with open(hdisc_svg_file, "w") as f:
        f.write(hdisc_svg)
    render_svg_to_png(hdisc_svg_file, hdisc_png_file, 2000, 2000)
    print(f"✓ {hdisc_svg_file} & {hdisc_png_file}")
    
    # 9. EXPANDED PRESET BACKGROUNDS (FEED 1:1 & STORY 9:16)
    print("\n=== GENERATING EXPANDED BACKGROUND PRESETS ===")
    bg_configs = [
        ("deep_plum_stage", "bg-deep-plum-stage", 2048, 2048),
        ("deep_plum_stage", "bg-deep-plum-stage-story", 1080, 1920),
        ("amber_caramel_sunset", "bg-amber-sunset", 2048, 2048),
        ("amber_caramel_sunset", "bg-amber-sunset-story", 1080, 1920),
        ("golden_ticket_gala", "bg-golden-ticket-gala", 2048, 2048),
        ("golden_ticket_gala", "bg-golden-ticket-gala-story", 1080, 1920),
        # NEW HIGH-CONTRAST PRESETS FOR GOLD LOGO:
        ("hypnotic_purple_swirl", "bg-hypnotic-purple-swirl", 2048, 2048),
        ("hypnotic_purple_swirl", "bg-hypnotic-purple-swirl-story", 1080, 1920),
        ("fantasy_confectionery_stage", "bg-fantasy-confectionery-stage", 2048, 2048),
        ("fantasy_confectionery_stage", "bg-fantasy-confectionery-stage-story", 1080, 1920),
        ("confectionery_icon_wallpaper", "bg-confectionery-icon-wallpaper", 2048, 2048),
        ("confectionery_icon_wallpaper", "bg-confectionery-icon-wallpaper-story", 1080, 1920)
    ]
    
    for (theme, name, w, h) in bg_configs:
        bg_svg = generate_background_svg(w, h, theme=theme)
        bg_svg_file = os.path.join(bg_dir, f"{name}.svg")
        bg_png_file = os.path.join(bg_dir, f"{name}.png")
        with open(bg_svg_file, "w") as f:
            f.write(bg_svg)
        render_svg_to_png(bg_svg_file, bg_png_file, w, h)
        print(f"✓ {bg_svg_file} & {bg_png_file} ({w}x{h})")
        
    print("\n=== AUDIT TRANSPARANSI ASET ORNAMEN ===")
    for check_png in [
        burst_png_file,
        ribbon_png_file,
        swirl_png_file,
        sparkle_png_file,
        curtain_png_file,
        clouds_png_file,
        hdisc_png_file
    ]:
        im = Image.open(check_png)
        arr = np.array(im)
        alpha = arr[:, :, 3]
        print(f"{os.path.basename(check_png)}: Alpha={(alpha>0).sum()} | Transparent={(alpha==0).sum()}")

if __name__ == "__main__":
    main()
