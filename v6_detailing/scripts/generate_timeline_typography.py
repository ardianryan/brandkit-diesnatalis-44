#!/usr/bin/env python3
"""
generate_timeline_typography.py
=============================================================================
Generates official identity typography for:
"Timeline" & "TIMELINE"
Matching the exact visual DNA of AVERSA, DIES NATALIS, and MEET THE CREATIVE MINDS:
- Playful, bouncy bubble typography (DynaPuff Bold)
- Wonka golden chocolate fantasy aesthetic
- Multi-layer 3D mahogany bevel contour (#310603 / #7D1B05)
- Rich 5-stop metallic honey-gold gradient (#E09B17 -> #F5C538 -> #B6580B)
- Clipped inner specular gloss reflections (#FDF39D -> #F7D160 & #FFFEEA)
- Wonka diamond shimmer sparkle accents
- Output formats:
  * Title Case: "Timeline"
  * ALL CAPS: "TIMELINE"
- Color variants for each format:
  * color (Official gold & mahogany 3D bevel)
  * white (Pure white silhouette with soft depth opacity)
  * dark (Deep obsidian mahogany / slate monochrome)
- High-res PNG exports (3200px canvas) via Google Chrome Headless
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

def generate_timeline_asset(variant="title", mode="color"):
    """
    variant:
      - 'title': Title Case ("Timeline")
      - 'caps': ALL CAPS ("TIMELINE")
    mode:
      - 'color': Official honey gold & mahogany 3D bevel
      - 'white': Pure white silhouette with depth opacity
      - 'dark': Deep obsidian mahogany / jet black
    """
    font_path = os.path.join(FONTS_DIR, "DynaPuff.ttf")
    vw, vh = 3200, 1100
    
    if variant == "title":
        text_str = "Timeline"
        font_size = 420
        fp = fm.FontProperties(fname=font_path, size=font_size, weight="bold")
        tp = TextPath((0, 0), text_str, prop=fp)
        bb = tp.get_extents()
        
        tx = (vw - bb.width) / 2.0 - bb.x0
        ty = (vh + bb.height) / 2.0 - 25
        
        d_path = path_to_svg_d(tp, scale=1.0, tx=tx, ty=ty, flip_y=True)
        
        sparkles = [
            (tx - 35, ty - bb.height + 65, 34),              # Near top of 'T'
            (tx + 420, ty - bb.height - 15, 26),             # Above 'i' dot
            (tx + bb.width * 0.52, ty - bb.height + 25, 30), # Above 'l'
            (tx + bb.width + 45, ty - 50, 36),               # After 'e'
            (tx + bb.width * 0.28, ty + 15, 22),             # Under 'm'
        ]
        ext_depth = 34
        bevel_w = 22

    else: # caps
        text_str = "TIMELINE"
        font_size = 390
        fp = fm.FontProperties(fname=font_path, size=font_size, weight="bold")
        tp = TextPath((0, 0), text_str, prop=fp)
        bb = tp.get_extents()
        
        tx = (vw - bb.width) / 2.0 - bb.x0
        ty = (vh + bb.height) / 2.0 - 20
        
        d_path = path_to_svg_d(tp, scale=1.0, tx=tx, ty=ty, flip_y=True)
        
        sparkles = [
            (tx - 35, ty - bb.height + 60, 36),              # Near top of 'T'
            (tx + 720, ty - bb.height - 20, 26),             # Above 'M'
            (tx + bb.width * 0.62, ty - bb.height + 30, 32), # Above 'L'
            (tx + bb.width + 45, ty - 55, 36),               # After 'E'
            (tx + bb.width * 0.35, ty + 15, 22),             # Under 'E'
        ]
        ext_depth = 34
        bevel_w = 22

    defs_block = f"""
  <defs>
    <linearGradient id="tlGoldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#E09B17" />
      <stop offset="25%" stop-color="#F5C538" />
      <stop offset="55%" stop-color="#F5C538" />
      <stop offset="85%" stop-color="#E09B17" />
      <stop offset="100%" stop-color="#B6580B" />
    </linearGradient>
    <linearGradient id="tlBevelGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#7D1B05" />
      <stop offset="100%" stop-color="#310603" />
    </linearGradient>
    <linearGradient id="tlHighlightGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FDF39D" stop-opacity="0.95" />
      <stop offset="65%" stop-color="#F7D160" stop-opacity="0.55" />
      <stop offset="100%" stop-color="#F5C538" stop-opacity="0.0" />
    </linearGradient>
    <linearGradient id="tlSparkleGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF" />
      <stop offset="45%" stop-color="#FDF39D" />
      <stop offset="100%" stop-color="#F5C538" />
    </linearGradient>
    <clipPath id="tlClip">
      <path d="{d_path}"/>
    </clipPath>
  </defs>"""

    svg_content = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw} {vh}" width="{vw}" height="{vh}">',
        f'  <title>{text_str} Typography ({variant} - {mode})</title>',
        defs_block,
    ]

    if mode == "color":
        # 1. 3D Solid Mahogany Extrusion Block
        svg_content.append('  <!-- 3D Mahogany Extrusion Block -->')
        svg_content.append('  <g id="3d-extrusion">')
        step_offsets = list(range(ext_depth, 2, -4))
        for off in step_offsets:
            svg_content.append(
                f'    <path d="{d_path}" fill="#310603" stroke="#310603" stroke-width="{ext_depth}" '
                f'stroke-linejoin="round" stroke-linecap="round" transform="translate(0, {off})"/>'
            )
        svg_content.append('  </g>')

        # 2. Rich Rust / Mahogany Bevel Contour
        svg_content.append('  <!-- Bevel Rim -->')
        svg_content.append(
            f'  <path id="bevel-rim" d="{d_path}" fill="#7D1B05" stroke="#7D1B05" '
            f'stroke-width="{bevel_w}" stroke-linejoin="round" stroke-linecap="round"/>'
        )

        # 3. Main Honey-Gold Letter Body
        svg_content.append('  <!-- Golden Letter Body -->')
        svg_content.append(
            f'  <path id="letters-body" d="{d_path}" fill="url(#tlGoldGrad)" '
            f'stroke="#E09B17" stroke-width="4" stroke-linejoin="round"/>'
        )

        # 4. Inner Specular Gloss Highlights (Clipped to letter body for clean bevel reflection)
        svg_content.append('  <!-- Inner Specular Gloss Reflections -->')
        svg_content.append('  <g clip-path="url(#tlClip)">')
        # Soft top glow rim
        svg_content.append(
            f'    <path d="{d_path}" fill="none" stroke="url(#tlHighlightGrad)" '
            f'stroke-width="26" stroke-linejoin="round" stroke-linecap="round" '
            f'transform="translate(0, 10)" opacity="0.92"/>'
        )
        # Sharp white specular crest
        svg_content.append(
            f'    <path d="{d_path}" fill="none" stroke="#FFFEEA" '
            f'stroke-width="8" stroke-linejoin="round" stroke-linecap="round" '
            f'transform="translate(0, 6)" opacity="0.80"/>'
        )
        svg_content.append('  </g>')

        # 5. Wonka Candy Shimmer Diamond Sparkles
        svg_content.append('  <!-- Wonka Shimmer Diamond Sparkles -->')
        svg_content.append('  <g id="sparkles">')
        for (sx, sy, srad) in sparkles:
            sp_d = get_sparkle_path(sx, sy, radius=srad)
            svg_content.append(f'    <path d="{sp_d}" fill="url(#tlSparkleGrad)"/>')
            svg_content.append(f'    <circle cx="{sx:.2f}" cy="{sy:.2f}" r="{srad*0.25:.2f}" fill="#FFFFFF"/>')
        svg_content.append('  </g>')

    elif mode == "white":
        # Pure White Monochrome (Ideal for dark velvet / royal purple backgrounds)
        svg_content.append('  <!-- 3D Shadow Layer -->')
        svg_content.append(
            f'  <path d="{d_path}" fill="rgba(255,255,255,0.18)" '
            f'transform="translate(0, 18)"/>'
        )
        svg_content.append('  <!-- Main White Body -->')
        svg_content.append(
            f'  <path d="{d_path}" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="4" stroke-linejoin="round"/>'
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
            f'  <path d="{d_path}" fill="#07090F" '
            f'transform="translate(0, 18)"/>'
        )
        svg_content.append('  <!-- Main Dark Body -->')
        svg_content.append(
            f'  <path d="{d_path}" fill="#310603" stroke="#07090F" stroke-width="4" stroke-linejoin="round"/>'
        )
        svg_content.append('  <!-- Sparkles -->')
        svg_content.append('  <g id="sparkles">')
        for (sx, sy, srad) in sparkles:
            sp_d = get_sparkle_path(sx, sy, radius=srad)
            svg_content.append(f'    <path d="{sp_d}" fill="#B6580B"/>')
        svg_content.append('  </g>')

    svg_content.append('</svg>\n')
    full_svg = "\n".join(svg_content)

    # File naming convention
    suffix = "bubble" if variant == "title" else "caps"
    svg_filename = f"timeline-{suffix}-{mode}.svg"
    png_filename = f"timeline-{suffix}-{mode}.png"
    
    svg_path = os.path.join(SVG_OUT_DIR, svg_filename)
    png_path = os.path.join(PNG_OUT_DIR, png_filename)
    
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(full_svg)
    print(f"✓ Saved SVG: {svg_path}")

    # Render PNG
    render_svg_to_png_chrome(svg_path, png_path, vw, vh)

def main():
    print("=" * 70)
    print("GENERATING TIMELINE IDENTITY TYPOGRAPHY ASSETS")
    print("Matching exact AVERSA & Wonka Honey Gold DNA")
    print("=" * 70)

    variants = ["title", "caps"]
    modes = ["color", "white", "dark"]

    for var in variants:
        for m in modes:
            print(f"\nProcessing: variant={var}, mode={m}...")
            generate_timeline_asset(variant=var, mode=m)

    print("\n" + "=" * 70)
    print("SUCCESS: All Timeline Typography assets generated successfully!")
    print("=" * 70)

if __name__ == "__main__":
    main()
