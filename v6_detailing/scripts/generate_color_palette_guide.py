#!/usr/bin/env python3
"""
generate_color_palette_guide.py
Menghasilkan diagram dan kartu panduan palet warna resmi (Official Brand Color Palette Guide)
dalam format SVG vektor dan PNG resolusi tinggi (2400 x 1450 px), menggantikan coolors.jpeg.
"""

import html
import subprocess
from pathlib import Path

WORKSPACE = Path("/Users/ardianryan/Documents/diesnat44project")
SVG_OUTPUT_1 = WORKSPACE / "assets/brandkit_elements/svg/brand-color-palette-guide.svg"
SVG_OUTPUT_2 = WORKSPACE / "assets/svg/brand-color-palette.svg"
PNG_OUTPUT_1 = WORKSPACE / "assets/brandkit_elements/png/brand-color-palette-guide.png"
PNG_OUTPUT_2 = WORKSPACE / "assets/png/brand-color-palette.png"

COLORS = [
    {
        "hex": "#310603",
        "name": "Obsidian Mahogany",
        "role": "Deep Shadow & Silhouette",
        "rgb": "49, 6, 3",
        "cmyk": "48, 88, 76, 75",
        "hsl": "4°, 88%, 10%",
        "text_color": "#FFFFFF",
        "sub_color": "#F7D160"
    },
    {
        "hex": "#7D1B05",
        "name": "Deep Crimson Rust",
        "role": "Fire Core & Depth",
        "rgb": "125, 27, 5",
        "cmyk": "24, 96, 100, 27",
        "hsl": "11°, 92%, 25%",
        "text_color": "#FFFFFF",
        "sub_color": "#FDF39D"
    },
    {
        "hex": "#B6580B",
        "name": "Rich Amber Bronze",
        "role": "Facet Crease & Warm Shadow",
        "rgb": "182, 88, 11",
        "cmyk": "18, 73, 100, 7",
        "hsl": "27°, 89%, 38%",
        "text_color": "#FFFFFF",
        "sub_color": "#FFE885"
    },
    {
        "hex": "#E09D17",
        "name": "Marigold Warm Gold",
        "role": "Primary Body & Ribbon Mid",
        "rgb": "224, 157, 23",
        "cmyk": "9, 39, 99, 0",
        "hsl": "40°, 81%, 48%",
        "text_color": "#200401",
        "sub_color": "#4A1803"
    },
    {
        "hex": "#F5C538",
        "name": "Vivid Royal Gold",
        "role": "Medial Spine & Brilliance",
        "rgb": "245, 197, 56",
        "cmyk": "3, 21, 84, 0",
        "hsl": "45°, 90%, 59%",
        "text_color": "#260601",
        "sub_color": "#5C2003"
    },
    {
        "hex": "#F7D160",
        "name": "Champagne Highlight",
        "role": "Apex Crest & Beam Light",
        "rgb": "247, 209, 96",
        "cmyk": "2, 16, 68, 0",
        "hsl": "45°, 90%, 67%",
        "text_color": "#2B0702",
        "sub_color": "#632505"
    },
    {
        "hex": "#FDF39D",
        "name": "Pale Canary Vanilla",
        "role": "Specular Tip & Starlight Glint",
        "rgb": "253, 243, 157",
        "cmyk": "1, 2, 44, 0",
        "hsl": "54°, 96%, 80%",
        "text_color": "#330802",
        "sub_color": "#692906"
    },
    {
        "hex": "#360538",
        "name": "Midnight Imperial Plum",
        "role": "Velvet Stage & Gala Background",
        "rgb": "54, 5, 56",
        "cmyk": "72, 98, 38, 56",
        "hsl": "298°, 84%, 12%",
        "text_color": "#FFFFFF",
        "sub_color": "#F7D160"
    }
]

ACCENT_COLORS = [
    {
        "hex": "#A0D9CA",
        "name": "Confectionery Mint",
        "role": "Whimsical Swirl & Poster Fan Accent",
        "rgb": "160, 217, 202",
        "text": "#113B32"
    },
    {
        "hex": "#F5B8CB",
        "name": "Cotton Candy Pink",
        "role": "Whimsical Bonbon & Floral Accent",
        "rgb": "245, 184, 203",
        "text": "#4A1226"
    },
    {
        "hex": "#FFF5D6",
        "name": "Vanilla Custard Cream",
        "role": "Soft Warm Poster Background",
        "rgb": "255, 245, 214",
        "text": "#4A3205"
    }
]

def clean(text: str) -> str:
    return html.escape(str(text))

def build_svg_palette() -> str:
    width = 2400
    height = 1450
    header_h = 160
    accent_bar_h = 130
    footer_h = 60
    columns_y = header_h
    columns_h = height - header_h - accent_bar_h - footer_h  # 1100 px
    num_cols = len(COLORS)
    col_w = width / num_cols  # 300 px each

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">')
    svg.append('  <defs>')
    svg.append('    <style><![CDATA[')
    svg.append("      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=Cinzel:wght@700;900&display=swap');")
    svg.append("      text { font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif; }")
    svg.append("      .cinzel { font-family: 'Cinzel', Georgia, serif; }")
    svg.append('    ]]></style>')
    svg.append('  </defs>')

    # Background canvas
    svg.append(f'  <rect width="{width}" height="{height}" fill="#16081A"/>')

    # Top Header
    svg.append('  <!-- Header Bar -->')
    svg.append('  <g id="header">')
    svg.append(f'    <rect width="{width}" height="{header_h}" fill="#240729"/>')
    svg.append(f'    <line x1="0" y1="{header_h}" x2="{width}" y2="{header_h}" stroke="#F5C538" stroke-width="3" opacity="0.8"/>')
    
    # Institution & Event Title
    svg.append('    <text x="80" y="65" fill="#FFEAA0" font-size="20" font-weight="700" letter-spacing="4" class="cinzel">SMA NEGERI 1 GEDEG • 1982–2026</text>')
    svg.append('    <text x="80" y="115" fill="#FFFFFF" font-size="36" font-weight="900" letter-spacing="1">DIES NATALIS KE-44 — OFFICIAL COLOR PALETTE SPECIFICATION</text>')
    
    # Right-side Badges
    svg.append(f'    <g transform="translate({width - 480}, 45)">')
    svg.append('      <rect width="400" height="70" rx="35" fill="#3D1445" stroke="#F5C538" stroke-width="2"/>')
    svg.append('      <circle cx="40" cy="35" r="14" fill="#F5C538"/>')
    svg.append('      <text x="70" y="32" fill="#FFEAA0" font-size="14" font-weight="800" letter-spacing="2">W3C DESIGN TOKEN SYSTEM</text>')
    svg.append('      <text x="70" y="52" fill="#E2D4E6" font-size="12" font-weight="600">Golden Harmony &amp; Velvet Stage</text>')
    svg.append('    </g>')
    svg.append('  </g>')

    # 8 Main Color Swatch Columns
    svg.append('  <!-- 8 Main Chromatic Swatch Columns -->')
    for i, col in enumerate(COLORS):
        x = i * col_w
        y = columns_y
        w = col_w
        h = columns_h
        hex_code = col["hex"]
        name = clean(col["name"])
        role = clean(col["role"])
        rgb = clean(col["rgb"])
        cmyk = clean(col["cmyk"])
        hsl = clean(col["hsl"])
        tc = col["text_color"]
        sc = col["sub_color"]

        svg.append(f'  <g id="col-{i+1}-{hex_code[1:]}">')
        svg.append(f'    <rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" fill="{hex_code}"/>')

        # Subtle column divider
        if i > 0:
            svg.append(f'    <line x1="{x:.1f}" y1="{y}" x2="{x:.1f}" y2="{y+h}" stroke="#000000" stroke-width="1.5" opacity="0.15"/>')

        # Big Hex display (vertical rotated style like Coolors)
        hex_rot_x = x + w / 2
        hex_rot_y = y + h * 0.45
        svg.append(f'    <g transform="rotate(-90, {hex_rot_x:.1f}, {hex_rot_y:.1f})">')
        svg.append(f'      <text x="{hex_rot_x:.1f}" y="{hex_rot_y:.1f}" text-anchor="middle" dominant-baseline="central" fill="{tc}" font-size="46" font-weight="900" letter-spacing="3">{clean(hex_code.upper())}</text>')
        svg.append('    </g>')

        # Top of column: Color Name & Role
        svg.append(f'    <g transform="translate({x + 24:.1f}, {y + 40})">')
        svg.append(f'      <text x="0" y="24" fill="{tc}" font-size="20" font-weight="900" letter-spacing="0.5">{name}</text>')
        svg.append(f'      <text x="0" y="48" fill="{sc}" font-size="13" font-weight="700" letter-spacing="0.5">{role}</text>')
        svg.append('    </g>')

        # Bottom of column: Color values info card (RGB, CMYK, HSL)
        card_y = y + h - 165
        card_w = w - 40
        card_x = x + 20
        svg.append(f'    <g transform="translate({card_x:.1f}, {card_y})">')
        # Pill card background for contrast readability
        bg_card_fill = "#000000" if tc == "#FFFFFF" else "#FFFFFF"
        bg_card_op = "0.25" if tc == "#FFFFFF" else "0.35"
        svg.append(f'      <rect width="{card_w:.1f}" height="145" rx="14" fill="{bg_card_fill}" opacity="{bg_card_op}"/>')
        
        # Color metrics
        svg.append(f'      <text x="18" y="34" fill="{tc}" font-size="13" font-weight="800">RGB: <tspan font-weight="600">{rgb}</tspan></text>')
        svg.append(f'      <text x="18" y="62" fill="{tc}" font-size="13" font-weight="800">CMYK: <tspan font-weight="600">{cmyk}</tspan></text>')
        svg.append(f'      <text x="18" y="90" fill="{tc}" font-size="13" font-weight="800">HSL: <tspan font-weight="600">{hsl}</tspan></text>')
        svg.append(f'      <text x="18" y="120" fill="{sc}" font-size="12" font-weight="800">INDEX #{i+1} OF 8</text>')
        svg.append('    </g>')

        svg.append('  </g>')

    # Bottom Theatrical Whimsical Accent Palette Bar
    accent_y = header_h + columns_h
    svg.append('  <!-- Theatrical Supporting Accent Palette Bar -->')
    svg.append(f'  <g id="accent-palette-bar" transform="translate(0, {accent_y})">')
    svg.append(f'    <rect width="{width}" height="{accent_bar_h}" fill="#19061F"/>')
    svg.append(f'    <line x1="0" y1="0" x2="{width}" y2="0" stroke="#F5C538" stroke-width="2" opacity="0.6"/>')
    
    # Left Label
    svg.append('    <text x="80" y="52" fill="#FFEAA0" font-size="16" font-weight="800" letter-spacing="2" class="cinzel">PALET AKSEN PENDUKUNG TEATER FANTASI</text>')
    svg.append('    <text x="80" y="82" fill="#D3BCD9" font-size="14" font-weight="600">Nuansa Sinematik Panggung &amp; Ornamen Festival</text>')

    # 3 Accent Swatch Badges
    accent_start_x = 800
    accent_w = (width - accent_start_x - 80) / 3
    for j, acc in enumerate(ACCENT_COLORS):
        ax = accent_start_x + j * accent_w
        svg.append(f'    <g transform="translate({ax:.1f}, 20)">')
        svg.append(f'      <rect width="{accent_w - 24:.1f}" height="90" rx="16" fill="{acc["hex"]}" stroke="#FFFFFF" stroke-width="1.5" opacity="0.95"/>')
        svg.append(f'      <text x="24" y="34" fill="{acc["text"]}" font-size="18" font-weight="900">{clean(acc["hex"].upper())}</text>')
        svg.append(f'      <text x="24" y="56" fill="{acc["text"]}" font-size="13" font-weight="800">{clean(acc["name"])}</text>')
        svg.append(f'      <text x="24" y="74" fill="{acc["text"]}" font-size="11" font-weight="600" opacity="0.85">{clean(acc["role"])}</text>')
        svg.append('    </g>')
    svg.append('  </g>')

    # Footer
    svg.append(f'  <!-- Footer -->')
    svg.append(f'  <g id="footer" transform="translate(0, {height - footer_h})">')
    svg.append(f'    <rect width="{width}" height="{footer_h}" fill="#0F0314"/>')
    svg.append(f'    <text x="80" y="36" fill="#8E7896" font-size="13" font-weight="600">SMAN 1 Gedeg Brand Identity © 2026 • Official Master Palette • All Rights Reserved</text>')
    svg.append(f'    <text x="{width - 80}" y="36" text-anchor="end" fill="#F5C538" font-size="13" font-weight="700">PENGGANTI RESMI COOLORS.JPEG • HIGH RESOLUTION VECTOR STANDARDS</text>')
    svg.append('  </g>')

    svg.append('</svg>')
    return "\n".join(svg)

def render_svg_to_png(svg_path: Path, png_path: Path, width: int = 2400, height: int = 1450):
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    png_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--screenshot={png_path.resolve()}",
        f"file://{svg_path.resolve()}"
    ]
    subprocess.run(cmd, check=True)
    print(f"Rendered PNG: {png_path} ({width}x{height})")

def main():
    svg_content = build_svg_palette()

    # Save SVG to both brandkit and core assets
    for svg_file in [SVG_OUTPUT_1, SVG_OUTPUT_2]:
        svg_file.parent.mkdir(parents=True, exist_ok=True)
        svg_file.write_text(svg_content, encoding="utf-8")
        print(f"Saved SVG: {svg_file}")

    # Render PNG
    render_svg_to_png(SVG_OUTPUT_1, PNG_OUTPUT_1, 2400, 1450)
    render_svg_to_png(SVG_OUTPUT_2, PNG_OUTPUT_2, 2400, 1450)

if __name__ == "__main__":
    main()
