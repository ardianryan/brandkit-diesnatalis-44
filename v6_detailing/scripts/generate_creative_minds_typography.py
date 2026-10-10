#!/usr/bin/env python3
"""
generate_creative_minds_typography.py
=============================================================================
Generates official identity typography for:
"Meet the Creative Minds"
Matching the exact visual DNA of AVERSA and DIES NATALIS:
- Playful, bouncy bubble typography (DynaPuff)
- Wonka golden chocolate fantasy aesthetic
- Multi-layer 3D mahogany bevel contour (#310603 / #7D1B05)
- Rich 5-stop metallic honey-gold gradient (#E09B17 -> #F5C538 -> #B6580B)
- Clipped inner specular gloss reflections (#FDF39D -> #F7D160 & #FFFEEA)
- Wonka diamond shimmer sparkle accents
- Output formats:
  * Title Case Stacked ("Meet the" / "Creative Minds")
  * ALL CAPS Stacked ("MEET THE" / "CREATIVE MINDS")
  * Title Case Horizontal ("Meet the Creative Minds")
  * ALL CAPS Horizontal ("MEET THE CREATIVE MINDS")
- Color variants:
  * color (Official gold & mahogany 3D bevel)
  * white (Pure white silhouette with soft depth opacity)
  * dark (Deep obsidian mahogany / slate monochrome)
- High-res PNG exports (3600px canvas) via Google Chrome Headless
=============================================================================
"""

import os
import subprocess
import numpy as np
import matplotlib.font_manager as fm
from matplotlib.textpath import TextPath
from matplotlib.path import Path

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS_DIR = "assets/fonts"
SVG_OUT_DIR = "assets/svg"
PNG_OUT_DIR = "assets/png"

os.makedirs(SVG_OUT_DIR, exist_ok=True)
os.makedirs(PNG_OUT_DIR, exist_ok=True)

def path_to_svg_d(path, scale=1.0, tx=0.0, ty=0.0, flip_y=True):
    """
    Converts matplotlib Path into exact standard SVG path commands.
    In matplotlib, Y points upwards (Cartesian), so flip_y=True converts it to SVG downwards Y.
    """
    cmds = []
    i = 0
    verts = path.vertices
    codes = path.codes
    n = len(codes)
    while i < n:
        code = codes[i]
        if code == Path.MOVETO:
            x = verts[i][0] * scale + tx
            y = (-verts[i][1] if flip_y else verts[i][1]) * scale + ty
            cmds.append(f"M {x:.2f} {y:.2f}")
            i += 1
        elif code == Path.LINETO:
            x = verts[i][0] * scale + tx
            y = (-verts[i][1] if flip_y else verts[i][1]) * scale + ty
            cmds.append(f"L {x:.2f} {y:.2f}")
            i += 1
        elif code == Path.CURVE3:
            cx = verts[i][0] * scale + tx
            cy = (-verts[i][1] if flip_y else verts[i][1]) * scale + ty
            x = verts[i+1][0] * scale + tx
            y = (-verts[i+1][1] if flip_y else verts[i+1][1]) * scale + ty
            cmds.append(f"Q {cx:.2f} {cy:.2f} {x:.2f} {y:.2f}")
            i += 2
        elif code == Path.CURVE4:
            c1x = verts[i][0] * scale + tx
            c1y = (-verts[i][1] if flip_y else verts[i][1]) * scale + ty
            c2x = verts[i+1][0] * scale + tx
            c2y = (-verts[i+1][1] if flip_y else verts[i+1][1]) * scale + ty
            x = verts[i+2][0] * scale + tx
            y = (-verts[i+2][1] if flip_y else verts[i+2][1]) * scale + ty
            cmds.append(f"C {c1x:.2f} {c1y:.2f}, {c2x:.2f} {c2y:.2f}, {x:.2f} {y:.2f}")
            i += 3
        elif code == Path.CLOSEPOLY:
            cmds.append("Z")
            i += 1
        else:
            i += 1
    return " ".join(cmds)

def get_sparkle_path(cx, cy, radius=24, thinness=0.18):
    """
    Generates a 4-point diamond star sparkle (Wonka gold shimmer).
    """
    r_outer = radius
    r_inner = radius * thinness
    pts = [
        (cx, cy - r_outer),
        (cx + r_inner, cy - r_inner),
        (cx + r_outer, cy),
        (cx + r_inner, cy + r_inner),
        (cx, cy + r_outer),
        (cx - r_inner, cy + r_inner),
        (cx - r_outer, cy),
        (cx - r_inner, cy - r_inner),
    ]
    d = f"M {pts[0][0]:.2f} {pts[0][1]:.2f} "
    d += f"Q {cx:.2f} {cy:.2f} {pts[2][0]:.2f} {pts[2][1]:.2f} "
    d += f"Q {cx:.2f} {cy:.2f} {pts[4][0]:.2f} {pts[4][1]:.2f} "
    d += f"Q {cx:.2f} {cy:.2f} {pts[6][0]:.2f} {pts[6][1]:.2f} "
    d += f"Q {cx:.2f} {cy:.2f} {pts[0][0]:.2f} {pts[0][1]:.2f} Z"
    return d

def render_svg_to_png_chrome(svg_path, png_path, width, height):
    """
    Renders SVG to transparent PNG using Google Chrome Headless.
    """
    cmd = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        "--default-background-color=00000000",
        f"--window-size={width},{height}",
        f"--screenshot={png_path}",
        svg_path
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"  ✓ Rendered PNG: {png_path} ({width}x{height})")

def generate_typography_asset(style="title-stacked", mode="color"):
    """
    style:
      - 'title-stacked': Title Case 2-row ("Meet the" / "Creative Minds")
      - 'caps-stacked': ALL CAPS 2-row ("MEET THE" / "CREATIVE MINDS")
      - 'title-horizontal': Title Case 1-row ("Meet the Creative Minds")
      - 'caps-horizontal': ALL CAPS 1-row ("MEET THE CREATIVE MINDS")
    mode: 'color', 'white', 'dark'
    """
    font_path = os.path.join(FONTS_DIR, "DynaPuff.ttf")
    
    if style == "title-stacked":
        vw, vh = 3600, 2400
        # Scaled up for strong presence
        fp1 = fm.FontProperties(fname=font_path, size=290, weight="bold")
        fp2 = fm.FontProperties(fname=font_path, size=380, weight="bold")
        
        tp1 = TextPath((0, 0), "Meet the", prop=fp1)
        tp2 = TextPath((0, 0), "Creative Minds", prop=fp2)
        
        bb1 = tp1.get_extents()
        bb2 = tp2.get_extents()
        
        x1 = (vw - bb1.width) / 2.0 - bb1.x0
        x2 = (vw - bb2.width) / 2.0 - bb2.x0
        
        line_gap = 140.0
        total_content_h = bb1.height + line_gap + bb2.height
        start_y = (vh - total_content_h) / 2.0
        
        y1 = start_y + bb1.height
        y2 = y1 + line_gap + bb2.height
        
        d1 = path_to_svg_d(tp1, scale=1.0, tx=x1, ty=y1, flip_y=True)
        d2 = path_to_svg_d(tp2, scale=1.0, tx=x2, ty=y2, flip_y=True)
        combined_d = f"{d1} {d2}"
        
        sparkles = [
            (x1 - 45, y1 - bb1.height + 50, 30),
            (x1 + bb1.width + 55, y1 - bb1.height + 90, 26),
            (x2 - 50, y2 - bb2.height + 70, 38),
            (x2 + 880, y2 - bb2.height - 20, 26),
            (x2 + 1850, y2 - bb2.height + 40, 42),
            (x2 + bb2.width + 60, y2 - 90, 34),
        ]
        ext_depth = 32
        bevel_w = 20

    elif style == "caps-stacked":
        vw, vh = 3600, 2400
        fp1 = fm.FontProperties(fname=font_path, size=290, weight="bold")
        fp2 = fm.FontProperties(fname=font_path, size=370, weight="bold")
        
        tp1 = TextPath((0, 0), "MEET THE", prop=fp1)
        tp2 = TextPath((0, 0), "CREATIVE MINDS", prop=fp2)
        
        bb1 = tp1.get_extents()
        bb2 = tp2.get_extents()
        
        x1 = (vw - bb1.width) / 2.0 - bb1.x0
        x2 = (vw - bb2.width) / 2.0 - bb2.x0
        
        line_gap = 150.0
        total_content_h = bb1.height + line_gap + bb2.height
        start_y = (vh - total_content_h) / 2.0
        
        y1 = start_y + bb1.height
        y2 = y1 + line_gap + bb2.height
        
        d1 = path_to_svg_d(tp1, scale=1.0, tx=x1, ty=y1, flip_y=True)
        d2 = path_to_svg_d(tp2, scale=1.0, tx=x2, ty=y2, flip_y=True)
        combined_d = f"{d1} {d2}"
        
        sparkles = [
            (x1 - 50, y1 - bb1.height + 60, 32),
            (x1 + bb1.width + 55, y1 - bb1.height + 80, 28),
            (x2 - 55, y2 - bb2.height + 60, 40),
            (x2 + 760, y2 - bb2.height - 25, 26),
            (x2 + 1720, y2 - bb2.height + 40, 42),
            (x2 + bb2.width + 65, y2 - 70, 36),
        ]
        ext_depth = 34
        bevel_w = 22

    elif style == "title-horizontal":
        vw, vh = 4400, 1200
        fp = fm.FontProperties(fname=font_path, size=300, weight="bold")
        tp = TextPath((0, 0), "Meet the Creative Minds", prop=fp)
        bb = tp.get_extents()
        
        x = (vw - bb.width) / 2.0 - bb.x0
        y = (vh + bb.height) / 2.0 - 20
        
        combined_d = path_to_svg_d(tp, scale=1.0, tx=x, ty=y, flip_y=True)
        
        sparkles = [
            (x - 55, y - bb.height + 60, 36),
            (x + 1200, y - bb.height - 15, 26),
            (x + 2650, y - bb.height + 40, 32),
            (x + bb.width + 60, y - 70, 36),
        ]
        ext_depth = 30
        bevel_w = 18

    else: # caps-horizontal
        vw, vh = 4600, 1200
        fp = fm.FontProperties(fname=font_path, size=280, weight="bold")
        tp = TextPath((0, 0), "MEET THE CREATIVE MINDS", prop=fp)
        bb = tp.get_extents()
        
        x = (vw - bb.width) / 2.0 - bb.x0
        y = (vh + bb.height) / 2.0 - 20
        
        combined_d = path_to_svg_d(tp, scale=1.0, tx=x, ty=y, flip_y=True)
        
        sparkles = [
            (x - 60, y - bb.height + 60, 38),
            (x + 1150, y - bb.height - 20, 26),
            (x + 2580, y - bb.height + 35, 34),
            (x + bb.width + 65, y - 60, 38),
        ]
        ext_depth = 30
        bevel_w = 18

    defs_block = """
  <defs>
    <linearGradient id="cmGoldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E09B17" />
      <stop offset="25%" stop-color="#F5C538" />
      <stop offset="55%" stop-color="#F5C538" />
      <stop offset="85%" stop-color="#E09B17" />
      <stop offset="100%" stop-color="#B6580B" />
    </linearGradient>
    <linearGradient id="cmBevelGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#7D1B05" />
      <stop offset="100%" stop-color="#310603" />
    </linearGradient>
    <linearGradient id="cmHighlightGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FDF39D" stop-opacity="0.95" />
      <stop offset="65%" stop-color="#F7D160" stop-opacity="0.55" />
      <stop offset="100%" stop-color="#F5C538" stop-opacity="0.0" />
    </linearGradient>
    <linearGradient id="cmSparkleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="45%" stop-color="#FDF39D" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <clipPath id="lettersClip">
      <path d="{combined_d_escaped}"/>
    </clipPath>
  </defs>""".replace("{combined_d_escaped}", combined_d)

    svg_content = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw} {vh}" width="{vw}" height="{vh}">',
        f'  <title>Meet the Creative Minds ({style} - {mode})</title>',
        defs_block,
    ]

    if mode == "color":
        # 1. 3D Solid Mahogany Extrusion Block
        svg_content.append('  <!-- 3D Mahogany Extrusion Block -->')
        svg_content.append('  <g id="3d-extrusion">')
        step_offsets = list(range(ext_depth, 2, -4))
        for off in step_offsets:
            svg_content.append(
                f'    <path d="{combined_d}" fill="#310603" stroke="#310603" stroke-width="{ext_depth}" '
                f'stroke-linejoin="round" stroke-linecap="round" transform="translate(0, {off})"/>'
            )
        svg_content.append('  </g>')

        # 2. Rich Rust / Mahogany Bevel Contour
        svg_content.append('  <!-- Bevel Rim -->')
        svg_content.append(
            f'  <path id="bevel-rim" d="{combined_d}" fill="#7D1B05" stroke="#7D1B05" '
            f'stroke-width="{bevel_w}" stroke-linejoin="round" stroke-linecap="round"/>'
        )

        # 3. Main Honey-Gold Letter Body
        svg_content.append('  <!-- Golden Letter Body -->')
        svg_content.append(
            f'  <path id="letters-body" d="{combined_d}" fill="url(#cmGoldGrad)" '
            f'stroke="#E09B17" stroke-width="4" stroke-linejoin="round"/>'
        )

        # 4. Inner Specular Gloss Highlights (Clipped to letter body for clean bevel reflection)
        svg_content.append('  <!-- Inner Specular Gloss Reflections -->')
        svg_content.append('  <g clip-path="url(#lettersClip)">')
        # Soft top glow rim
        svg_content.append(
            f'    <path d="{combined_d}" fill="none" stroke="url(#cmHighlightGrad)" '
            f'stroke-width="26" stroke-linejoin="round" stroke-linecap="round" '
            f'transform="translate(0, 10)" opacity="0.92"/>'
        )
        # Sharp white specular crest
        svg_content.append(
            f'    <path d="{combined_d}" fill="none" stroke="#FFFEEA" '
            f'stroke-width="8" stroke-linejoin="round" stroke-linecap="round" '
            f'transform="translate(0, 6)" opacity="0.80"/>'
        )
        svg_content.append('  </g>')

        # 5. Wonka Candy Shimmer Diamond Sparkles
        svg_content.append('  <!-- Wonka Shimmer Diamond Sparkles -->')
        svg_content.append('  <g id="sparkles">')
        for (sx, sy, srad) in sparkles:
            sp_d = get_sparkle_path(sx, sy, radius=srad)
            svg_content.append(f'    <path d="{sp_d}" fill="url(#cmSparkleGrad)"/>')
            svg_content.append(f'    <circle cx="{sx:.2f}" cy="{sy:.2f}" r="{srad*0.25:.2f}" fill="#FFFFFF"/>')
        svg_content.append('  </g>')

    elif mode == "white":
        # Pure White Monochrome (Ideal for dark velvet / royal purple backgrounds)
        svg_content.append('  <!-- 3D Shadow Layer -->')
        svg_content.append(
            f'  <path d="{combined_d}" fill="rgba(255,255,255,0.18)" '
            f'transform="translate(0, 18)"/>'
        )
        svg_content.append('  <!-- Main White Body -->')
        svg_content.append(
            f'  <path d="{combined_d}" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"/>'
        )
        svg_content.append('  <!-- Sparkles -->')
        svg_content.append('  <g id="sparkles">')
        for (sx, sy, srad) in sparkles:
            sp_d = get_sparkle_path(sx, sy, radius=srad)
            svg_content.append(f'    <path d="{sp_d}" fill="#FFFFFF"/>')
        svg_content.append('  </g>')

    elif mode == "dark":
        # Deep Obsidian Mahogany / Dark Slate (Ideal for light backgrounds)
        svg_content.append('  <!-- 3D Shadow Layer -->')
        svg_content.append(
            f'  <path d="{combined_d}" fill="#07090F" '
            f'transform="translate(0, 18)"/>'
        )
        svg_content.append('  <!-- Main Dark Body -->')
        svg_content.append(
            f'  <path d="{combined_d}" fill="#310603" stroke="#310603" stroke-width="6" stroke-linejoin="round"/>'
        )
        svg_content.append(
            f'  <path d="{combined_d}" fill="none" stroke="#7D1B05" stroke-width="4" '
            f'stroke-linejoin="round"/>'
        )
        svg_content.append('  <!-- Sparkles -->')
        svg_content.append('  <g id="sparkles">')
        for (sx, sy, srad) in sparkles:
            sp_d = get_sparkle_path(sx, sy, radius=srad)
            svg_content.append(f'    <path d="{sp_d}" fill="#B6580B"/>')
        svg_content.append('  </g>')

    svg_content.append('</svg>')
    return "\n".join(svg_content), vw, vh

def main():
    print("=================================================================")
    print("PRODUCING MASTER 'Meet the Creative Minds' BRAND ASSETS")
    print("=================================================================")
    
    # 4 Style configurations:
    # 1. title-stacked (Standard Primary Lockup) -> creative-minds-bubble-*
    # 2. caps-stacked (High-Impact Headline Lockup) -> creative-minds-caps-*
    # 3. title-horizontal (Header / Bumper Lockup) -> creative-minds-horizontal-*
    # 4. caps-horizontal (Wide Banner Caps Lockup) -> creative-minds-horizontal-caps-*
    
    tasks = [
        ("title-stacked", "creative-minds-bubble"),
        ("caps-stacked", "creative-minds-caps"),
        ("title-horizontal", "creative-minds-horizontal"),
        ("caps-horizontal", "creative-minds-horizontal-caps"),
    ]
    
    modes = ["color", "white", "dark"]
    
    for style, prefix in tasks:
        print(f"\nProcessing style: {style} -> {prefix}-*")
        for mode in modes:
            svg_filename = f"{prefix}-{mode}.svg"
            png_filename = f"{prefix}-{mode}.png"
            
            svg_path = os.path.join(SVG_OUT_DIR, svg_filename)
            png_path = os.path.join(PNG_OUT_DIR, png_filename)
            
            svg_data, vw, vh = generate_typography_asset(style=style, mode=mode)
            
            with open(svg_path, "w", encoding="utf-8") as f:
                f.write(svg_data)
            print(f"  ✓ SVG: {svg_path}")
            
            render_svg_to_png_chrome(svg_path, png_path, vw, vh)
            
    print("\n✓ ALL 12 MASTER ASSETS (SVG + PNG) PRODUCED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
