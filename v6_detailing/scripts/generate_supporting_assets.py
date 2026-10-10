"""
Skrip Generator Aset Penyerta Brand Kit Resmi
Kategori: Supporting Brand Assets (Aset Ornamen & Kanvas Pendukung)
Proyek: Dies Natalis ke-44 SMA Negeri 1 Gedeg (1982 – 2026)
Palet Warna: Coolors Resmi (Midnight Plum, Obsidian Mahogany, Crimson Fire, Bronze, Marigold, Vivid Gold, Champagne, Canary)

Menghasilkan:
1. Magic Burst Rays (Pancaran Kerucut Cahaya Teater/Panggung)
2. Floating Magic Ribbons & Waves (Pita-pita Meliuk Melayang)
3. Confectionery Swirl Rosette (Pusaran Karamel & Roset Penomoran)
4. Magic Sparkles & Stardust Clusters (Bintang Kilau 4-Sudut)
5. Geometric Watermark Arcs (Garis Pandu Busur Piagam/Sertifikat)
6. Preset Canvas Backgrounds (Feed 2048x2048 & Story 1080x1920)
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
    "plum": "#360538"
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
# 6. CANVAS BACKGROUND PRESETS
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
        
    lines.append('  </defs>')
    
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
    
    print("==========================================================")
    print(" GENERATING SUPPORTING BRAND KIT ASSETS (DIES NATALIS 44)")
    print("==========================================================")
    
    # 1. Magic Burst Rays
    print("\n[1/6] Generating Magic Burst Rays...")
    burst_svg = generate_magic_burst_svg(2400, 2400)
    burst_svg_file = os.path.join(svg_dir, "magic-burst-rays.svg")
    burst_png_file = os.path.join(png_dir, "magic-burst-rays.png")
    with open(burst_svg_file, "w") as f:
        f.write(burst_svg)
    render_svg_to_png(burst_svg_file, burst_png_file, 2400, 2400)
    print(f"✓ {burst_svg_file} & {burst_png_file}")
    
    # 2. Floating Magic Ribbons & Waves
    print("\n[2/6] Generating Floating Magic Ribbons & Waves...")
    ribbon_svg = generate_magic_ribbon_svg(2400, 1200)
    ribbon_svg_file = os.path.join(svg_dir, "floating-magic-ribbons.svg")
    ribbon_png_file = os.path.join(png_dir, "floating-magic-ribbons.png")
    with open(ribbon_svg_file, "w") as f:
        f.write(ribbon_svg)
    render_svg_to_png(ribbon_svg_file, ribbon_png_file, 2400, 1200)
    print(f"✓ {ribbon_svg_file} & {ribbon_png_file}")
    
    # 3. Confectionery Swirl Rosette
    print("\n[3/6] Generating Confectionery Swirl Rosette...")
    swirl_svg = generate_swirl_svg(2000)
    swirl_svg_file = os.path.join(svg_dir, "confectionery-swirl-badge.svg")
    swirl_png_file = os.path.join(png_dir, "confectionery-swirl-badge.png")
    with open(swirl_svg_file, "w") as f:
        f.write(swirl_svg)
    render_svg_to_png(swirl_svg_file, swirl_png_file, 2000, 2000)
    print(f"✓ {swirl_svg_file} & {swirl_png_file}")
    
    # 4. Magic Sparkles & Stardust Clusters
    print("\n[4/6] Generating Magic Sparkles & Stardust Clusters...")
    sparkle_svg = generate_sparkles_cluster_svg(2000)
    sparkle_svg_file = os.path.join(svg_dir, "magic-sparkles-cluster.svg")
    sparkle_png_file = os.path.join(png_dir, "magic-sparkles-cluster.png")
    with open(sparkle_svg_file, "w") as f:
        f.write(sparkle_svg)
    render_svg_to_png(sparkle_svg_file, sparkle_png_file, 2000, 2000)
    print(f"✓ {sparkle_svg_file} & {sparkle_png_file}")
    
    # 5. Geometric Watermark Blueprint Arcs
    print("\n[5/6] Generating Geometric Blueprint Watermark Arcs...")
    for cmode in ["gold", "plum"]:
        wm_svg = generate_watermark_arcs_svg(2800, 2000, color_mode=cmode)
        wm_svg_file = os.path.join(svg_dir, f"watermark-arcs-{cmode}.svg")
        wm_png_file = os.path.join(png_dir, f"watermark-arcs-{cmode}.png")
        with open(wm_svg_file, "w") as f:
            f.write(wm_svg)
        render_svg_to_png(wm_svg_file, wm_png_file, 2800, 2000)
        print(f"✓ {wm_svg_file} & {wm_png_file}")
        
    # 6. Preset Backgrounds (Feed 2048x2048 & Story 1080x1920)
    print("\n[6/6] Generating Official Background Presets...")
    bg_configs = [
        ("deep_plum_stage", "bg-deep-plum-stage", 2048, 2048),
        ("deep_plum_stage", "bg-deep-plum-stage-story", 1080, 1920),
        ("amber_caramel_sunset", "bg-amber-sunset", 2048, 2048),
        ("amber_caramel_sunset", "bg-amber-sunset-story", 1080, 1920),
        ("golden_ticket_gala", "bg-golden-ticket-gala", 2048, 2048),
        ("golden_ticket_gala", "bg-golden-ticket-gala-story", 1080, 1920)
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
        sparkle_png_file
    ]:
        im = Image.open(check_png)
        arr = np.array(im)
        alpha = arr[:, :, 3]
        print(f"{os.path.basename(check_png)}: Alpha pixels={(alpha>0).sum()} | Pure transparent={(alpha==0).sum()}")

if __name__ == "__main__":
    main()
