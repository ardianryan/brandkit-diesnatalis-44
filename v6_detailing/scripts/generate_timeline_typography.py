#!/usr/bin/env python3
"""
generate_timeline_typography.py
=============================================================================
Generates official identity typography for "Timeline" & "TIMELINE"
Pure 100% Match with ARKESA / AVERSA and DIES NATALIS Vector DNA:
- Authentic Honey-Gold 5-stop vertical gradient (#E09B17 -> #F5C538 -> #B6580B)
- Curved specular crest highlight (#FDF39D -> #F7D160 & #FFFEEA)
- Clean, bold, organic display curves (Titan One)
- ZERO dark chocolate 3D extrusion, ZERO brown bevel borders, ZERO cartoon sparkles
- Pure, clean vector silhouettes (color, white, dark)
- Output formats:
  * Title Case: "Timeline" (assets/svg/timeline-bubble-*.svg & assets/png/timeline-bubble-*.png)
  * ALL CAPS: "TIMELINE" (assets/svg/timeline-caps-*.svg & assets/png/timeline-caps-*.png)
- Canvas: 3200 x 1000 px, Google Chrome Headless transparent alpha rendering
=============================================================================
"""

import os
import subprocess
import matplotlib.font_manager as fm
from matplotlib.textpath import TextPath
from matplotlib.path import Path

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
FONTS_DIR = "assets/fonts"
SVG_OUT_DIR = "assets/svg"
PNG_OUT_DIR = "assets/png"

os.makedirs(SVG_OUT_DIR, exist_ok=True)
os.makedirs(PNG_OUT_DIR, exist_ok=True)

# Official Coolors Gold Spec matching AVERSA & DIES NATALIS
PALETTE = {
    "marigold": "#E09B17",
    "gold_vivid": "#F5C538",
    "champagne": "#F7D160",
    "canary": "#FDF39D",
    "bronze": "#B6580B",
    "dark_slate": "#07090F",
}

def path_to_svg_d(path, scale=1.0, tx=0.0, ty=0.0, flip_y=True):
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

def render_svg_to_png_chrome(svg_path, png_path, width, height):
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

def generate_clean_timeline_asset(variant="title", mode="color"):
    """
    variant:
      - 'title': "Timeline"
      - 'caps': "TIMELINE"
    mode:
      - 'color': Official honey gold & specular crest highlight
      - 'white': Clean white monochrome
      - 'dark': Deep obsidian slate monochrome
    """
    font_path = os.path.join(FONTS_DIR, "TitanOne.ttf")
    vw, vh = 3200, 1000

    if variant == "title":
        text_str = "Timeline"
        font_size = 380
        fp = fm.FontProperties(fname=font_path, size=font_size, weight="bold")
        tp = TextPath((0, 0), text_str, prop=fp)
        bb = tp.get_extents()

        tx = (vw - bb.width) / 2.0 - bb.x0
        ty = (vh + bb.height) / 2.0 - 20
        d_path = path_to_svg_d(tp, scale=1.0, tx=tx, ty=ty, flip_y=True)

    else: # caps
        text_str = "TIMELINE"
        font_size = 340
        fp = fm.FontProperties(fname=font_path, size=font_size, weight="bold")
        tp = TextPath((0, 0), text_str, prop=fp)
        bb = tp.get_extents()

        tx = (vw - bb.width) / 2.0 - bb.x0
        ty = (vh + bb.height) / 2.0 - 15
        d_path = path_to_svg_d(tp, scale=1.0, tx=tx, ty=ty, flip_y=True)

    defs_block = f"""
  <defs>
    <linearGradient id="aversaGoldGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['marigold']}"/>
      <stop offset="25%" stop-color="{PALETTE['gold_vivid']}"/>
      <stop offset="55%" stop-color="{PALETTE['gold_vivid']}"/>
      <stop offset="85%" stop-color="{PALETTE['marigold']}"/>
      <stop offset="100%" stop-color="{PALETTE['bronze']}"/>
    </linearGradient>
    <linearGradient id="aversaHighlightGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{PALETTE['canary']}" stop-opacity="0.92"/>
      <stop offset="65%" stop-color="{PALETTE['champagne']}" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="{PALETTE['gold_vivid']}" stop-opacity="0.0"/>
    </linearGradient>
    <clipPath id="timelineClip">
      <path d="{d_path}"/>
    </clipPath>
  </defs>"""

    svg_content = [
        f'<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw} {vh}" width="{vw}" height="{vh}">',
        f'  <title>{text_str} Logotype - AVERSA &amp; DIES NATALIS Style ({mode})</title>',
        defs_block,
    ]

    if mode == "color":
        # Pure clean Honey Gold body
        svg_content.append('  <!-- Main Letter Body (Official Honey Gold Gradient) -->')
        svg_content.append(f'  <path id="letters-body" d="{d_path}" fill="url(#aversaGoldGrad)" fill-rule="evenodd"/>')
        
        # Specular Highlight (matching AVERSA / DIES NATALIS crest gleam)
        svg_content.append('  <!-- Specular Highlights -->')
        svg_content.append('  <g id="letters-highlights" clip-path="url(#timelineClip)">')
        svg_content.append(
            f'    <path d="{d_path}" fill="none" stroke="url(#aversaHighlightGrad)" '
            f'stroke-width="28" stroke-linejoin="round" stroke-linecap="round" '
            f'transform="translate(0, 12)" opacity="0.94"/>'
        )
        svg_content.append(
            f'    <path d="{d_path}" fill="none" stroke="#FFFEEA" '
            f'stroke-width="8" stroke-linejoin="round" stroke-linecap="round" '
            f'transform="translate(0, 8)" opacity="0.82"/>'
        )
        svg_content.append('  </g>')

    elif mode == "white":
        # Pure White Silhouette
        svg_content.append('  <!-- White Silhouette -->')
        svg_content.append(f'  <path id="letters-white" d="{d_path}" fill="#FFFFFF" fill-rule="evenodd"/>')

    elif mode == "dark":
        # Pure Obsidian Dark Silhouette
        svg_content.append('  <!-- Dark Silhouette -->')
        svg_content.append(f'  <path id="letters-dark" d="{d_path}" fill="#0B0F19" fill-rule="evenodd"/>')

    svg_content.append('</svg>\n')
    full_svg = "\n".join(svg_content)

    # File naming matching existing convention
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
    print("RE-GENERATING TIMELINE LOGOTYPE ASSETS")
    print("Style: 100% Identical to ARKESA / AVERSA & DIES NATALIS")
    print("=" * 70)

    variants = ["title", "caps"]
    modes = ["color", "white", "dark"]

    for var in variants:
        for m in modes:
            print(f"\nProcessing: variant={var}, mode={m}...")
            generate_clean_timeline_asset(variant=var, mode=m)

    print("\n" + "=" * 70)
    print("SUCCESS: Clean AVERSA-style Timeline assets ready!")
    print("=" * 70)

if __name__ == "__main__":
    main()
