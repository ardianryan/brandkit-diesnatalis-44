#!/usr/bin/env python3
"""
generate_modular_brandkit_items.py
----------------------------------
Membangun Katalog Aset Per Item (Modular Elements) Lengkap format SVG & PNG:
1. Topi Pesulap Beludru Ungu & Pita Emas (Magic Top Hat)
2. Tongkat Pesulap Emas & Mahoni (Golden Cane / Wand)
3. Permen Lolipop Spiral Pastel Mint & Pink (Swirl Lollipop)
4. Permen Bungkus Bonbon Pink & Emas (Wrapped Bonbon Candy Pink)
5. Permen Bungkus Bonbon Karamel Emas (Wrapped Bonbon Candy Gold)
6. Tiket Emas Vintage Dies Natalis 44 (Golden Ticket Badge)
7. Bunga Mawar Gula Konfeksi Magenta (Confectionery Sugar Rose)
8. Kacamata Bulat Eksentrik Emas (Whimsical Round Spectacles)
9. Botol Elixir Sirup Magis Kristal (Magic Potion Flask)
10. Gugusan Bintang Kilau Emas Retro (Stardust Sparkle Stars)

Merender seluruh SVG menjadi PNG transparan 32-bit (resolusi 1200x1200px)
menggunakan Headless Google Chrome untuk kualitas rendering anti-aliasing sempurna.

Dies Natalis ke-44 SMA Negeri 1 Gedeg (1982 - 2026)
"""

import os
import subprocess
import tempfile

WORKSPACE = "/Users/ardianryan/Documents/diesnat44project"
SVG_DIR = os.path.join(WORKSPACE, "assets/brandkit_elements/svg")
PNG_DIR = os.path.join(WORKSPACE, "assets/brandkit_elements/png")
CHROME_BIN = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

for d in [SVG_DIR, PNG_DIR]:
    os.makedirs(d, exist_ok=True)


def render_svg_to_png(svg_path, png_path, width=1200, height=1200):
    """Merender berkas SVG menjadi PNG 32-bit transparan murni via Google Chrome headless."""
    abs_svg = os.path.abspath(svg_path)
    abs_out = os.path.abspath(png_path)
    cmd = [
        CHROME_BIN,
        "--headless",
        "--disable-gpu",
        "--default-background-color=00000000",
        f"--window-size={width},{height}",
        f"--screenshot={abs_out}",
        f"file://{abs_svg}"
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)


# ==============================================================================
# DEFINISI SVG ELEMEN MODULAR SATUAN
# ==============================================================================

def get_magic_top_hat_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="100%" height="100%">
  <defs>
    <radialGradient id="hat-velvet-body" cx="45%" cy="40%" r="65%">
      <stop offset="0%" stop-color="#7A1885"/>
      <stop offset="45%" stop-color="#4E0A56"/>
      <stop offset="85%" stop-color="#28032D"/>
      <stop offset="100%" stop-color="#19011C"/>
    </radialGradient>
    <linearGradient id="hat-brim-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#691172"/>
      <stop offset="50%" stop-color="#3C0642"/>
      <stop offset="100%" stop-color="#19011C"/>
    </linearGradient>
    <linearGradient id="hat-ribbon-gold" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#B6580B"/>
      <stop offset="25%" stop-color="#F5C538"/>
      <stop offset="50%" stop-color="#FFF3B0"/>
      <stop offset="75%" stop-color="#F5C538"/>
      <stop offset="100%" stop-color="#B6580B"/>
    </linearGradient>
    <filter id="hat-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="24" stdDeviation="28" flood-color="#120114" flood-opacity="0.55"/>
    </filter>
  </defs>

  <g filter="url(#hat-shadow)">
    <!-- Brim Belakang -->
    <ellipse cx="500" cy="740" rx="380" ry="110" fill="url(#hat-brim-grad)"/>

    <!-- Badan Topi Silinder Melengkung (Crown) -->
    <path d="M 280 430
             C 270 320, 310 260, 480 250
             C 650 240, 710 310, 710 420
             L 730 680
             C 630 730, 370 730, 260 680
             Z"
          fill="url(#hat-velvet-body)"/>

    <!-- Puncak Lekukan Atas Topi (Dented Top) -->
    <ellipse cx="495" cy="275" rx="215" ry="55" fill="#3A053F"/>
    <path d="M 330 270 C 430 310, 560 310, 660 270 C 620 250, 370 250, 330 270 Z" fill="#6B1375" opacity="0.6"/>

    <!-- Highlight Lengkungan Sisi Kiri -->
    <path d="M 290 420 C 285 350, 315 285, 380 270 C 340 310, 335 480, 345 660 C 310 655, 295 520, 290 420 Z" fill="#9D29A9" opacity="0.45"/>

    <!-- Pita Emas Melingkar (Gold Ribbon) -->
    <path d="M 265 650
             C 380 700, 620 700, 725 650
             L 730 700
             C 620 750, 380 750, 260 700
             Z"
          fill="url(#hat-ribbon-gold)"/>

    <!-- Brim Depan Melengkung (Front Brim) -->
    <path d="M 120 740
             C 140 850, 860 850, 880 740
             C 780 790, 220 790, 120 740
             Z"
          fill="url(#hat-brim-grad)"/>

    <!-- Bros / Emblem Bintang Emas di Pita -->
    <g transform="translate(490, 695)">
      <polygon points="0,-28 8,-8 28,0 8,8 0,28 -8,8 -28,0 -8,-8" fill="#FFF3B0"/>
      <circle cx="0" cy="0" r="5" fill="#B6580B"/>
    </g>
  </g>
</svg>'''


def get_swirl_lollipop_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1200" width="100%" height="100%">
  <defs>
    <linearGradient id="stick-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#E2D9C8"/>
      <stop offset="40%" stop-color="#FFFFFF"/>
      <stop offset="70%" stop-color="#FDFBF7"/>
      <stop offset="100%" stop-color="#C5BAA5"/>
    </linearGradient>
    <filter id="loli-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="20" stdDeviation="24" flood-color="#1F0422" flood-opacity="0.45"/>
    </filter>
  </defs>

  <g filter="url(#loli-shadow)">
    <!-- Gagang Stik Lolipop -->
    <rect x="480" y="480" width="40" height="650" rx="20" fill="url(#stick-grad)"/>
    <!-- Spiral Stripe pada Gagang Stik -->
    <g opacity="0.85">
      <path d="M 480 540 L 520 580 L 520 620 L 480 580 Z" fill="#E09D17"/>
      <path d="M 480 660 L 520 700 L 520 740 L 480 700 Z" fill="#E09D17"/>
      <path d="M 480 780 L 520 820 L 520 860 L 480 820 Z" fill="#E09D17"/>
      <path d="M 480 900 L 520 940 L 520 980 L 480 940 Z" fill="#E09D17"/>
      <path d="M 480 1020 L 520 1060 L 520 1100 L 480 1060 Z" fill="#E09D17"/>
    </g>

    <!-- Piringan Lolipop Spiral Utama -->
    <g transform="translate(500, 380)">
      <circle cx="0" cy="0" r="320" fill="#FAF3DE"/>

      <!-- Bilah Spiral Warna-Warni Pastel & Magenta -->
      <!-- Menggunakan 12 sektor spiral melengkung -->
      <path d="M 0 0 C 120 40, 240 180, 277 160 C 314 140, 320 60, 320 0 Z" fill="#F472B6"/>
      <path d="M 0 0 C 40 120, 180 240, 160 277 C 140 314, 60 320, 0 320 Z" fill="#6CC1AA"/>
      <path d="M 0 0 C -40 120, -180 240, -160 277 C -140 314, -60 320, 0 320 Z" fill="#FAF3DE"/>
      <path d="M 0 0 C -120 40, -240 180, -277 160 C -314 140, -320 60, -320 0 Z" fill="#9333EA"/>
      <path d="M 0 0 C -120 -40, -240 -180, -277 -160 C -314 -140, -320 -60, -320 0 Z" fill="#F472B6"/>
      <path d="M 0 0 C -40 -120, -180 -240, -160 -277 C -140 -314, -60 -320, 0 -320 Z" fill="#6CC1AA"/>
      <path d="M 0 0 C 40 -120, 180 -240, 160 -277 C 140 -314, 60 -320, 0 -320 Z" fill="#FAF3DE"/>
      <path d="M 0 0 C 120 -40, 240 -180, 277 -160 C 314 -140, 320 -60, 320 0 Z" fill="#9333EA"/>

      <!-- Spiral Garis Kontur Meliuk Menambah Kedalaman -->
      <path d="M 0 0 C 80 20, 180 80, 220 180 C 260 280, 160 310, 80 310" fill="none" stroke="#E09D17" stroke-width="12" opacity="0.6"/>
      <path d="M 0 0 C -80 -20, -180 -80, -220 -180 C -260 -280, -160 -310, -80 -310" fill="none" stroke="#E09D17" stroke-width="12" opacity="0.6"/>

      <!-- Kilau Gula Refleksi Kaca (Sugar Gloss) -->
      <path d="M -180 -180 C -120 -280, 80 -300, 180 -220 C 120 -240, -60 -240, -180 -180 Z" fill="#FFFFFF" opacity="0.45"/>
      <circle cx="-120" cy="-140" r="28" fill="#FFFFFF" opacity="0.6"/>
    </g>

    <!-- Pita Kupu-Kupu Emas di Bawah Piringan -->
    <g transform="translate(500, 700)">
      <polygon points="0,0 -80,-40 -70,20 0,0" fill="#E09D17"/>
      <polygon points="0,0 80,-40 70,20 0,0" fill="#E09D17"/>
      <circle cx="0" cy="0" r="16" fill="#F5C538"/>
    </g>
  </g>
</svg>'''


def get_golden_cane_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 1200" width="100%" height="100%">
  <defs>
    <linearGradient id="cane-wood" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#1A0201"/>
      <stop offset="35%" stop-color="#4A0C08"/>
      <stop offset="70%" stop-color="#2D0604"/>
      <stop offset="100%" stop-color="#120101"/>
    </linearGradient>
    <radialGradient id="cane-gold-orb" cx="35%" cy="30%" r="70%">
      <stop offset="0%" stop-color="#FFFAD0"/>
      <stop offset="25%" stop-color="#FCE16B"/>
      <stop offset="60%" stop-color="#E09D17"/>
      <stop offset="90%" stop-color="#9C4505"/>
      <stop offset="100%" stop-color="#542102"/>
    </radialGradient>
    <filter id="cane-shadow" x="-30%" y="-20%" width="160%" height="140%">
      <feDropShadow dx="0" dy="20" stdDeviation="22" flood-color="#150217" flood-opacity="0.45"/>
    </filter>
  </defs>

  <g filter="url(#cane-shadow)">
    <!-- Batang Tongkat Mahoni Meruncing -->
    <polygon points="284,320 316,320 306,1150 294,1150" fill="url(#cane-wood)"/>
    <!-- Sepatu Ujung Bawah Tongkat (Brass Tip) -->
    <polygon points="292,1120 308,1120 304,1160 296,1160" fill="#E09D17"/>

    <!-- Cincin Kuningan Emas di Segmen Atas -->
    <rect x="280" y="320" width="40" height="24" rx="4" fill="url(#cane-gold-orb)"/>
    <rect x="276" y="348" width="48" height="14" rx="3" fill="url(#cane-gold-orb)"/>

    <!-- Ornamen Kerah Kepala Tongkat (Capital Collar) -->
    <path d="M 260 280 C 270 310, 330 310, 340 280 L 330 260 L 270 260 Z" fill="url(#cane-gold-orb)"/>

    <!-- Kepala Tongkat Bola Emas Bermahkota (Golden Orb Knob) -->
    <circle cx="300" cy="180" r="95" fill="url(#cane-gold-orb)"/>

    <!-- Cincin Berukir Melingkar pada Bola -->
    <ellipse cx="300" cy="180" rx="90" ry="25" fill="none" stroke="#FFFAD0" stroke-width="4" opacity="0.6"/>
    <!-- Puncak Mahkota Bintang Emas -->
    <g transform="translate(300, 85)">
      <polygon points="0,-25 8,-8 25,0 8,8 0,25 -8,8 -25,0 -8,-8" fill="#FFFAD0"/>
    </g>

    <!-- Kilauan Debu Cahaya Mengitari Kepala Tongkat -->
    <circle cx="210" cy="130" r="4" fill="#FDF39D" opacity="0.8"/>
    <circle cx="390" cy="150" r="5" fill="#FDF39D" opacity="0.8"/>
    <circle cx="230" cy="240" r="3" fill="#FDF39D" opacity="0.7"/>
    <circle cx="370" cy="220" r="4" fill="#FDF39D" opacity="0.7"/>
  </g>
</svg>'''


def get_wrapped_bonbon_pink_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" width="100%" height="100%">
  <defs>
    <radialGradient id="bonbon-body" cx="40%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#FFB3D9"/>
      <stop offset="35%" stop-color="#F472B6"/>
      <stop offset="70%" stop-color="#C026D3"/>
      <stop offset="100%" stop-color="#701A75"/>
    </radialGradient>
    <linearGradient id="candy-gold-ribbon" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFF3B0"/>
      <stop offset="50%" stop-color="#F5C538"/>
      <stop offset="100%" stop-color="#B6580B"/>
    </linearGradient>
    <filter id="bonbon-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="18" stdDeviation="20" flood-color="#240228" flood-opacity="0.4"/>
    </filter>
  </defs>

  <g filter="url(#bonbon-shadow)">
    <!-- Sayap Kuncup Kiri (Left Crimped Wrapper) -->
    <path d="M 330 300
             C 270 200, 160 140, 80 180
             C 120 250, 110 350, 80 420
             C 160 460, 270 400, 330 300 Z"
          fill="#F472B6" opacity="0.95"/>
    <path d="M 80 180 L 330 300 L 80 420" fill="none" stroke="#701A75" stroke-width="6" opacity="0.3"/>

    <!-- Sayap Kuncup Kanan (Right Crimped Wrapper) -->
    <path d="M 670 300
             C 730 200, 840 140, 920 180
             C 880 250, 890 350, 920 420
             C 840 460, 730 400, 670 300 Z"
          fill="#F472B6" opacity="0.95"/>
    <path d="M 920 180 L 670 300 L 920 420" fill="none" stroke="#701A75" stroke-width="6" opacity="0.3"/>

    <!-- Pita Emas Pengikat Kiri -->
    <rect x="315" y="240" width="30" height="120" rx="8" fill="url(#candy-gold-ribbon)"/>
    <!-- Pita Emas Pengikat Kanan -->
    <rect x="655" y="240" width="30" height="120" rx="8" fill="url(#candy-gold-ribbon)"/>

    <!-- Badan Permen Oval Buncit (Center Bonbon) -->
    <ellipse cx="500" cy="300" rx="200" ry="140" fill="url(#bonbon-body)"/>

    <!-- Pola Ulir Emas & Putih pada Badan Permen -->
    <path d="M 420 165 C 470 220, 470 380, 420 435" fill="none" stroke="#FAF3DE" stroke-width="18" opacity="0.75" stroke-linecap="round"/>
    <path d="M 500 160 C 550 220, 550 380, 500 440" fill="none" stroke="#F5C538" stroke-width="18" opacity="0.85" stroke-linecap="round"/>
    <path d="M 580 165 C 630 220, 630 380, 580 435" fill="none" stroke="#FAF3DE" stroke-width="18" opacity="0.75" stroke-linecap="round"/>

    <!-- Highlight Refleksi Manis -->
    <ellipse cx="460" cy="230" rx="80" ry="25" fill="#FFFFFF" opacity="0.45" transform="rotate(-15, 460, 230)"/>
  </g>
</svg>'''


def get_golden_ticket_badge_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" width="100%" height="100%">
  <defs>
    <linearGradient id="ticket-gold-surface" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFE885"/>
      <stop offset="25%" stop-color="#F5C538"/>
      <stop offset="50%" stop-color="#FDF39D"/>
      <stop offset="75%" stop-color="#E09D17"/>
      <stop offset="100%" stop-color="#B6580B"/>
    </linearGradient>
    <filter id="ticket-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="22" stdDeviation="24" flood-color="#240326" flood-opacity="0.5"/>
    </filter>
  </defs>

  <g filter="url(#ticket-shadow)">
    <!-- Kartu Tiket Emas dengan Sudut Berlekuk Klasik (Notched Ticket Corners) -->
    <path d="M 140 100
             L 860 100
             A 40 40 0 0 1 900 140
             L 900 260
             A 40 40 0 0 0 900 340
             L 900 460
             A 40 40 0 0 1 860 500
             L 140 500
             A 40 40 0 0 1 100 460
             L 100 340
             A 40 40 0 0 0 100 260
             L 100 140
             A 40 40 0 0 1 140 100 Z"
          fill="url(#ticket-gold-surface)"/>

    <!-- Bingkai Lis Ganda Ukir Dalam (Filigree Inset Border) -->
    <path d="M 155 125 L 845 125 L 845 475 L 155 475 Z"
          fill="none" stroke="#542102" stroke-width="4" stroke-dasharray="14,8"/>
    <path d="M 170 140 L 830 140 L 830 460 L 170 460 Z"
          fill="none" stroke="#7A3403" stroke-width="3"/>

    <!-- Teks Tipografi Ukir Emas: DIES NATALIS 44 -->
    <g fill="#4A1C02" text-anchor="middle" font-family="'Cinzel', 'Playfair Display', Georgia, serif">
      <text x="500" y="215" font-size="22" letter-spacing="6" font-weight="bold" fill="#542102">SMAN 1 GEDEG • 1982-2026</text>
      <line x1="260" y1="240" x2="740" y2="240" stroke="#7A3403" stroke-width="2" opacity="0.6"/>
      <text x="500" y="325" font-size="64" font-weight="900" letter-spacing="4" fill="#3D1501">DIES NATALIS</text>
      <line x1="320" y1="355" x2="680" y2="355" stroke="#7A3403" stroke-width="2" opacity="0.6"/>
      <text x="500" y="420" font-size="44" font-weight="bold" fill="#692802" letter-spacing="10">★ KE-44 ★</text>
    </g>

    <!-- Ornamen Roset Bintang Sudut -->
    <circle cx="170" cy="140" r="10" fill="#4A1C02"/>
    <circle cx="830" cy="140" r="10" fill="#4A1C02"/>
    <circle cx="170" cy="460" r="10" fill="#4A1C02"/>
    <circle cx="830" cy="460" r="10" fill="#4A1C02"/>
  </g>
</svg>'''


def get_confectionery_rose_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="100%" height="100%">
  <defs>
    <radialGradient id="rose-petal-center" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FF70A6"/>
      <stop offset="40%" stop-color="#E11D48"/>
      <stop offset="80%" stop-color="#9F1239"/>
      <stop offset="100%" stop-color="#4C0519"/>
    </radialGradient>
    <filter id="rose-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="#240212" flood-opacity="0.45"/>
    </filter>
  </defs>

  <g filter="url(#rose-shadow)" transform="translate(400, 400)">
    <!-- Daun Mint Toska di Belakang -->
    <path d="M 0 0 C -120 180, -280 220, -320 140 C -260 60, -140 40, 0 0 Z" fill="#4E9F8A"/>
    <path d="M 0 0 C 120 180, 280 220, 320 140 C 260 60, 140 40, 0 0 Z" fill="#6CC1AA"/>

    <!-- Kelopak Bunga Mawar Luar (Outer Petals) -->
    <path d="M -220 -80 C -280 120, -120 280, 0 260 C 120 280, 280 120, 220 -80 C 120 -240, -120 -240, -220 -80 Z" fill="#881337"/>
    <path d="M -180 40 C -220 200, 0 250, 0 250 C 0 250, 220 200, 180 40 C 120 180, -120 180, -180 40 Z" fill="#9F1239"/>

    <!-- Kelopak Lapisan Tengah (Mid Petals) -->
    <path d="M -140 -120 C -220 -20, -180 140, 0 160 C 180 140, 220 -20, 140 -120 C 60 -180, -60 -180, -140 -120 Z" fill="#BE123C"/>
    <path d="M -90 -60 C -140 40, -120 120, 0 130 C 120 120, 140 40, 90 -60 C 40 -110, -40 -110, -90 -60 Z" fill="#E11D48"/>

    <!-- Kuncup Inti Mawar Melingkar (Inner Rose Spiral Core) -->
    <ellipse cx="0" cy="0" rx="95" ry="90" fill="url(#rose-petal-center)"/>
    <path d="M -40 -20 C -20 -60, 40 -60, 50 -20 C 60 30, -10 50, -30 20 C -40 0, -10 -20, 0 -10"
          fill="none" stroke="#FFE4E6" stroke-width="12" stroke-linecap="round"/>

    <!-- Taburan Kristal Gula Berkilau -->
    <circle cx="-110" cy="-60" r="4" fill="#FFFFFF" opacity="0.8"/>
    <circle cx="120" cy="80" r="5" fill="#FFFFFF" opacity="0.8"/>
    <circle cx="-60" cy="140" r="4" fill="#FFFFFF" opacity="0.7"/>
    <circle cx="80" cy="-110" r="5" fill="#FFFFFF" opacity="0.8"/>
  </g>
</svg>'''


def get_whimsical_glasses_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 500" width="100%" height="100%">
  <defs>
    <linearGradient id="glasses-gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF3B0"/>
      <stop offset="30%" stop-color="#F5C538"/>
      <stop offset="70%" stop-color="#E09D17"/>
      <stop offset="100%" stop-color="#9C4505"/>
    </linearGradient>
    <filter id="glasses-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="#1E0320" flood-opacity="0.4"/>
    </filter>
  </defs>

  <g filter="url(#glasses-shadow)">
    <!-- Gagang Kiri & Kanan Tipis Melengkung -->
    <path d="M 120 250 C 40 220, 20 160, 60 120" fill="none" stroke="url(#glasses-gold)" stroke-width="14" stroke-linecap="round"/>
    <path d="M 880 250 C 960 220, 980 160, 940 120" fill="none" stroke="url(#glasses-gold)" stroke-width="14" stroke-linecap="round"/>

    <!-- Jembatan Hidung Melengkung (Bridge) -->
    <path d="M 430 230 C 470 190, 530 190, 570 230" fill="none" stroke="url(#glasses-gold)" stroke-width="18" stroke-linecap="round"/>

    <!-- Lensa & Bingkai Kiri Bulat -->
    <circle cx="300" cy="250" r="140" fill="#FAF3DE" opacity="0.25"/>
    <circle cx="300" cy="250" r="140" fill="none" stroke="url(#glasses-gold)" stroke-width="22"/>
    <circle cx="300" cy="250" r="126" fill="none" stroke="#542102" stroke-width="4" opacity="0.5"/>
    <!-- Highlight Kaca Kiri -->
    <path d="M 220 180 C 260 150, 340 150, 380 180" fill="none" stroke="#FFFFFF" stroke-width="12" opacity="0.65" stroke-linecap="round"/>

    <!-- Lensa & Bingkai Kanan Bulat -->
    <circle cx="700" cy="250" r="140" fill="#FAF3DE" opacity="0.25"/>
    <circle cx="700" cy="250" r="140" fill="none" stroke="url(#glasses-gold)" stroke-width="22"/>
    <circle cx="700" cy="250" r="126" fill="none" stroke="#542102" stroke-width="4" opacity="0.5"/>
    <!-- Highlight Kaca Kanan -->
    <path d="M 620 180 C 660 150, 740 150, 780 180" fill="none" stroke="#FFFFFF" stroke-width="12" opacity="0.65" stroke-linecap="round"/>
  </g>
</svg>'''


def get_stardust_sparkle_cluster_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="100%" height="100%">
  <defs>
    <radialGradient id="sparkle-gold-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="20%" stop-color="#FFFAD0"/>
      <stop offset="50%" stop-color="#F5C538"/>
      <stop offset="100%" stop-color="#F5C538" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <g>
    <!-- Bintang Utama Pusat Besar (4-Point Retro Star) -->
    <g transform="translate(500, 500)">
      <circle cx="0" cy="0" r="180" fill="url(#sparkle-gold-glow)"/>
      <polygon points="0,-240 28,-35 240,0 28,35 0,240 -28,35 -240,0 -28,-35" fill="#FFFAD0"/>
      <polygon points="0,-160 18,-25 160,0 18,25 0,160 -18,25 -160,0 -18,-25" fill="#FFFFFF"/>
      <!-- Sinar Diagonal Lembut -->
      <polygon points="-90,-90 -10,-10 90,90 10,10" fill="#F5C538" opacity="0.75"/>
      <polygon points="90,-90 10,-10 -90,90 -10,10" fill="#F5C538" opacity="0.75"/>
      <circle cx="0" cy="0" r="24" fill="#FFFFFF"/>
    </g>

    <!-- Bintang Satelit Kanan Atas -->
    <g transform="translate(780, 260)">
      <polygon points="0,-110 14,-18 110,0 14,18 0,110 -14,18 -110,0 -14,-18" fill="#FFFAD0"/>
      <circle cx="0" cy="0" r="10" fill="#FFFFFF"/>
    </g>

    <!-- Bintang Satelit Kiri Bawah -->
    <g transform="translate(220, 740)">
      <polygon points="0,-95 12,-15 95,0 12,15 0,95 -12,15 -95,0 -12,-15" fill="#FFFAD0"/>
      <circle cx="0" cy="0" r="8" fill="#FFFFFF"/>
    </g>

    <!-- Taburan Bintang Kecil & Debu Emas -->
    <circle cx="320" cy="320" r="14" fill="#F5C538"/>
    <circle cx="680" cy="680" r="16" fill="#F5C538"/>
    <circle cx="750" cy="480" r="10" fill="#FFFAD0"/>
    <circle cx="280" cy="560" r="12" fill="#FFFAD0"/>
    <circle cx="480" cy="180" r="8" fill="#FFFFFF"/>
    <circle cx="520" cy="820" r="9" fill="#FFFFFF"/>
  </g>
</svg>'''


# ==============================================================================
# ELEMEN BARU: PERMEN, COKELAT & UTILITAS DESAIN
# ==============================================================================

def get_golden_chocolate_bar_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 1200" width="100%" height="100%">
  <defs>
    <linearGradient id="choc-block-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#542314"/>
      <stop offset="40%" stop-color="#3A150B"/>
      <stop offset="100%" stop-color="#200A04"/>
    </linearGradient>
    <linearGradient id="choc-bevel-light" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#73321E"/>
      <stop offset="100%" stop-color="#3A150B"/>
    </linearGradient>
    <linearGradient id="choc-bevel-dark" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#2A0E06"/>
      <stop offset="100%" stop-color="#140401"/>
    </linearGradient>
    <linearGradient id="gold-foil-grad" x1="0%" y1="0%" x2="100%" y2="80%">
      <stop offset="0%" stop-color="#FFF2A3"/>
      <stop offset="25%" stop-color="#E2A21B"/>
      <stop offset="50%" stop-color="#FFF9D2"/>
      <stop offset="75%" stop-color="#C2820A"/>
      <stop offset="100%" stop-color="#FFF2A3"/>
    </linearGradient>
    <linearGradient id="wrapper-plum-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#550858"/>
      <stop offset="50%" stop-color="#360538"/>
      <stop offset="100%" stop-color="#1C021E"/>
    </linearGradient>
    <filter id="choc-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="24" stdDeviation="30" flood-color="#120114" flood-opacity="0.6"/>
    </filter>
  </defs>

  <g filter="url(#choc-shadow)" transform="translate(600, 600) rotate(-14) translate(-600, -600)">
    <!-- 1. Balok Cokelat Utama (Chocolate Slab) -->
    <rect x="360" y="240" width="480" height="700" rx="20" fill="url(#choc-block-grad)"/>

    <!-- Petak-petak Cokelat (Chocolate Tiles) -->
    <!-- Baris 1 -->
    <g transform="translate(390, 270)">
      <rect x="0" y="0" width="125" height="135" rx="8" fill="url(#choc-block-grad)"/>
      <polygon points="0,0 125,0 105,18 20,18" fill="url(#choc-bevel-light)"/>
      <polygon points="0,0 20,18 20,117 0,135" fill="url(#choc-bevel-light)"/>
      <polygon points="125,0 125,135 105,117 105,18" fill="url(#choc-bevel-dark)"/>
      <polygon points="0,135 125,135 105,117 20,117" fill="url(#choc-bevel-dark)"/>
      <rect x="20" y="18" width="85" height="99" rx="4" fill="#3D170D"/>
      <circle cx="62" cy="67" r="14" fill="#4E2013" opacity="0.8"/>
    </g>
    <g transform="translate(535, 270)">
      <rect x="0" y="0" width="125" height="135" rx="8" fill="url(#choc-block-grad)"/>
      <polygon points="0,0 125,0 105,18 20,18" fill="url(#choc-bevel-light)"/>
      <polygon points="0,0 20,18 20,117 0,135" fill="url(#choc-bevel-light)"/>
      <polygon points="125,0 125,135 105,117 105,18" fill="url(#choc-bevel-dark)"/>
      <polygon points="0,135 125,135 105,117 20,117" fill="url(#choc-bevel-dark)"/>
      <rect x="20" y="18" width="85" height="99" rx="4" fill="#3D170D"/>
      <circle cx="62" cy="67" r="14" fill="#4E2013" opacity="0.8"/>
    </g>
    <g transform="translate(680, 270)">
      <rect x="0" y="0" width="125" height="135" rx="8" fill="url(#choc-block-grad)"/>
      <polygon points="0,0 125,0 105,18 20,18" fill="url(#choc-bevel-light)"/>
      <polygon points="0,0 20,18 20,117 0,135" fill="url(#choc-bevel-light)"/>
      <polygon points="125,0 125,135 105,117 105,18" fill="url(#choc-bevel-dark)"/>
      <polygon points="0,135 125,135 105,117 20,117" fill="url(#choc-bevel-dark)"/>
      <rect x="20" y="18" width="85" height="99" rx="4" fill="#3D170D"/>
      <circle cx="62" cy="67" r="14" fill="#4E2013" opacity="0.8"/>
    </g>

    <!-- Baris 2 -->
    <g transform="translate(390, 425)">
      <rect x="0" y="0" width="125" height="135" rx="8" fill="url(#choc-block-grad)"/>
      <polygon points="0,0 125,0 105,18 20,18" fill="url(#choc-bevel-light)"/>
      <polygon points="0,0 20,18 20,117 0,135" fill="url(#choc-bevel-light)"/>
      <polygon points="125,0 125,135 105,117 105,18" fill="url(#choc-bevel-dark)"/>
      <polygon points="0,135 125,135 105,117 20,117" fill="url(#choc-bevel-dark)"/>
      <rect x="20" y="18" width="85" height="99" rx="4" fill="#3D170D"/>
      <circle cx="62" cy="67" r="14" fill="#4E2013" opacity="0.8"/>
    </g>
    <g transform="translate(535, 425)">
      <rect x="0" y="0" width="125" height="135" rx="8" fill="url(#choc-block-grad)"/>
      <polygon points="0,0 125,0 105,18 20,18" fill="url(#choc-bevel-light)"/>
      <polygon points="0,0 20,18 20,117 0,135" fill="url(#choc-bevel-light)"/>
      <polygon points="125,0 125,135 105,117 105,18" fill="url(#choc-bevel-dark)"/>
      <polygon points="0,135 125,135 105,117 20,117" fill="url(#choc-bevel-dark)"/>
      <rect x="20" y="18" width="85" height="99" rx="4" fill="#3D170D"/>
      <circle cx="62" cy="67" r="14" fill="#4E2013" opacity="0.8"/>
    </g>
    <g transform="translate(680, 425)">
      <rect x="0" y="0" width="125" height="135" rx="8" fill="url(#choc-block-grad)"/>
      <polygon points="0,0 125,0 105,18 20,18" fill="url(#choc-bevel-light)"/>
      <polygon points="0,0 20,18 20,117 0,135" fill="url(#choc-bevel-light)"/>
      <polygon points="125,0 125,135 105,117 105,18" fill="url(#choc-bevel-dark)"/>
      <polygon points="0,135 125,135 105,117 20,117" fill="url(#choc-bevel-dark)"/>
      <rect x="20" y="18" width="85" height="99" rx="4" fill="#3D170D"/>
      <circle cx="62" cy="67" r="14" fill="#4E2013" opacity="0.8"/>
    </g>

    <!-- 2. Lapisan Foil Aluminium Emas Berlipit (Golden Foil Layer) -->
    <path d="M 340 540 
             L 375 500 L 430 535 L 490 495 L 560 540 L 630 490 L 710 535 L 770 490 L 855 530
             L 865 720 L 335 720 Z" 
          fill="url(#gold-foil-grad)" stroke="#B67B08" stroke-width="2"/>
    <path d="M 350 525 L 420 540 L 490 510 L 560 550 L 640 505 L 720 545 L 845 510" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.6"/>

    <!-- 3. Bungkus Luar Ungu Beludru (Outer Plum Wrapper) -->
    <rect x="335" y="600" width="530" height="360" rx="12" fill="url(#wrapper-plum-grad)"/>
    <rect x="350" y="615" width="500" height="330" rx="8" fill="none" stroke="#F5C538" stroke-width="3" stroke-dasharray="8 4"/>

    <!-- Pita Label Tengah Emas -->
    <rect x="370" y="670" width="460" height="150" rx="10" fill="#200324" stroke="#F5C538" stroke-width="2"/>
    <text x="600" y="735" font-family="'Cinzel', Georgia, serif" font-size="34" font-weight="900" fill="#F5C538" text-anchor="middle" letter-spacing="4">SMAN 1 GEDEG</text>
    <text x="600" y="775" font-family="'Cinzel', Georgia, serif" font-size="22" font-weight="700" fill="#FFEAA0" text-anchor="middle" letter-spacing="3">★ DIES NATALIS 44 ★</text>
  </g>
</svg>'''


def get_swirl_candy_cane_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1400" width="100%" height="100%">
  <defs>
    <linearGradient id="cane-base-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#EBE3D3"/>
      <stop offset="35%" stop-color="#FFFFFF"/>
      <stop offset="70%" stop-color="#FFFDF5"/>
      <stop offset="100%" stop-color="#D9CBB0"/>
    </linearGradient>
    <linearGradient id="stripe-mint-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#B2E7DB"/>
      <stop offset="50%" stop-color="#77C9B6"/>
      <stop offset="100%" stop-color="#469C89"/>
    </linearGradient>
    <linearGradient id="stripe-red-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#BD2A3C"/>
      <stop offset="50%" stop-color="#8C1322"/>
      <stop offset="100%" stop-color="#5E0813"/>
    </linearGradient>
    <linearGradient id="ribbon-bow-gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF3B0"/>
      <stop offset="45%" stop-color="#F5C538"/>
      <stop offset="100%" stop-color="#B6580B"/>
    </linearGradient>
    <filter id="cane-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="20" stdDeviation="24" flood-color="#120114" flood-opacity="0.45"/>
    </filter>
  </defs>

  <g filter="url(#cane-shadow)">
    <!-- Tongkat Dasar (Cane Base Shape) -->
    <!-- Menggunakan path tebal bergaris ganda dengan clip-path untuk spiral stripes -->
    <path d="M 680 1250 L 680 500 C 680 200, 320 200, 320 500 L 320 580"
          fill="none" stroke="url(#cane-base-grad)" stroke-width="140" stroke-linecap="round"/>

    <!-- Strip Garis Mint & Red (Simulasi Spiral Striping via overlay stroke segmen) -->
    <!-- Garis Spiral Merah -->
    <path d="M 620 1200 L 740 1140" stroke="url(#stripe-red-grad)" stroke-width="32" stroke-linecap="round"/>
    <path d="M 620 1060 L 740 1000" stroke="url(#stripe-mint-grad)" stroke-width="32" stroke-linecap="round"/>
    <path d="M 620 920 L 740 860" stroke="url(#stripe-red-grad)" stroke-width="32" stroke-linecap="round"/>
    <path d="M 620 780 L 740 720" stroke="url(#stripe-mint-grad)" stroke-width="32" stroke-linecap="round"/>
    <path d="M 620 640 L 740 580" stroke="url(#stripe-red-grad)" stroke-width="32" stroke-linecap="round"/>
    <path d="M 645 490 L 735 435" stroke="url(#stripe-mint-grad)" stroke-width="32" stroke-linecap="round"/>
    
    <!-- Lengkungan Atas Striping -->
    <path d="M 620 330 L 690 260" stroke="url(#stripe-red-grad)" stroke-width="32" stroke-linecap="round"/>
    <path d="M 520 230 L 550 150" stroke="url(#stripe-mint-grad)" stroke-width="32" stroke-linecap="round"/>
    <path d="M 390 230 L 360 160" stroke="url(#stripe-red-grad)" stroke-width="32" stroke-linecap="round"/>
    <path d="M 270 330 L 350 370" stroke="url(#stripe-mint-grad)" stroke-width="32" stroke-linecap="round"/>
    <path d="M 260 480 L 380 490" stroke="url(#stripe-red-grad)" stroke-width="32" stroke-linecap="round"/>

    <!-- Kilau Mengkilap Tabung (Gloss Highlight) -->
    <path d="M 650 1240 L 650 500 C 650 250, 350 250, 350 500 L 350 570"
          fill="none" stroke="#FFFFFF" stroke-width="16" opacity="0.65" stroke-linecap="round"/>

    <!-- Pita Kupu-Kupu Emas di Leher Tongkat -->
    <g transform="translate(680, 520)">
      <!-- Sayap Pita Kiri & Kanan -->
      <path d="M 0 0 C -80 -80, -140 -20, -110 40 C -80 70, -20 20, 0 0 Z" fill="url(#ribbon-bow-gold)"/>
      <path d="M 0 0 C 80 -80, 140 -20, 110 40 C 80 70, 20 20, 0 0 Z" fill="url(#ribbon-bow-gold)"/>
      <!-- Ekor Pita -->
      <path d="M -15 20 L -50 130 L -10 110 L 0 130 L 15 20 Z" fill="#D49012"/>
      <path d="M 15 20 L 50 130 L 10 110 L 0 130 L -15 20 Z" fill="#D49012"/>
      <!-- Simpul Tengah Bulat -->
      <circle cx="0" cy="5" r="24" fill="#FFF2A3" stroke="#B6580B" stroke-width="3"/>
    </g>
  </g>
</svg>'''


def get_gourmet_praline_truffle_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="100%" height="100%">
  <defs>
    <radialGradient id="truffle-body" cx="40%" cy="35%" r="65%">
      <stop offset="0%" stop-color="#5E2316"/>
      <stop offset="35%" stop-color="#3D130A"/>
      <stop offset="75%" stop-color="#230803"/>
      <stop offset="100%" stop-color="#110301"/>
    </radialGradient>
    <linearGradient id="cup-pleat-gold" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#9C6B0D"/>
      <stop offset="25%" stop-color="#F5C538"/>
      <stop offset="50%" stop-color="#FFEFA3"/>
      <stop offset="75%" stop-color="#F5C538"/>
      <stop offset="100%" stop-color="#805304"/>
    </linearGradient>
    <linearGradient id="caramel-drizzle" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF2A3"/>
      <stop offset="50%" stop-color="#E09D17"/>
      <stop offset="100%" stop-color="#9E5D04"/>
    </linearGradient>
    <filter id="truffle-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="24" stdDeviation="28" flood-color="#120114" flood-opacity="0.55"/>
    </filter>
  </defs>

  <g filter="url(#truffle-shadow)">
    <!-- Cangkir Kertas Berlipit Emas (Pleated Paper Cup) -->
    <g transform="translate(500, 680)">
      <ellipse cx="0" cy="80" rx="360" ry="110" fill="#1C0320" opacity="0.4"/>
      <!-- Badan Mangkuk Kertas -->
      <path d="M -320 20 L -250 110 C -120 160, 120 160, 250 110 L 320 20 C 180 60, -180 60, -320 20 Z" fill="url(#cup-pleat-gold)"/>
      <!-- Lipatan-lipatan Vertikal -->
      <path d="M -290 30 L -220 120 M -230 40 L -160 135 M -160 45 L -90 145 M -80 48 L -20 150 M 0 50 L 0 152 M 80 48 L 20 150 M 160 45 L 90 145 M 230 40 L 160 135 M 290 30 L 220 120"
            stroke="#6B4103" stroke-width="4" opacity="0.7"/>
    </g>

    <!-- Bola Cokelat Truffle Bulat Mengilap -->
    <circle cx="500" cy="500" r="260" fill="url(#truffle-body)"/>

    <!-- Highlight Lengkungan Bola -->
    <ellipse cx="440" cy="380" rx="160" ry="90" fill="#7A3222" opacity="0.35" transform="rotate(-20, 440, 380)"/>
    <ellipse cx="410" cy="340" rx="60" ry="30" fill="#FFFFFF" opacity="0.25" transform="rotate(-20, 410, 340)"/>

    <!-- Saus Karamel Melingkar di Atasnya (Caramel Drizzle Wave) -->
    <path d="M 340 460 C 400 400, 480 580, 560 420 C 610 320, 680 470, 720 400"
          fill="none" stroke="url(#caramel-drizzle)" stroke-width="26" stroke-linecap="round"/>
    <path d="M 380 530 C 440 480, 510 620, 610 490 C 660 410, 700 520, 730 480"
          fill="none" stroke="url(#caramel-drizzle)" stroke-width="16" stroke-linecap="round"/>

    <!-- Serpihan Debu Emas (Edible Gold Flakes) -->
    <polygon points="480,360 495,370 485,385 470,375" fill="#FFF5B8"/>
    <polygon points="530,340 545,350 535,365 520,355" fill="#F5C538"/>
    <polygon points="460,420 472,428 465,440 452,432" fill="#F5C538"/>
    <polygon points="560,400 575,410 568,422 552,415" fill="#FFF5B8"/>
    <polygon points="510,430 520,438 515,448 502,442" fill="#FFF5B8"/>
  </g>
</svg>'''


def get_confectionery_sugar_gem_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" width="100%" height="100%">
  <defs>
    <linearGradient id="gem-mint-light" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#D4F5ED"/>
      <stop offset="50%" stop-color="#A0D9CA"/>
      <stop offset="100%" stop-color="#6DBCA9"/>
    </linearGradient>
    <linearGradient id="gem-mint-mid" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#80CBB9"/>
      <stop offset="100%" stop-color="#469C89"/>
    </linearGradient>
    <linearGradient id="gem-mint-dark" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#357D6D"/>
      <stop offset="100%" stop-color="#1B4D42"/>
    </linearGradient>
    <filter id="gem-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="20" stdDeviation="26" flood-color="#082A22" flood-opacity="0.5"/>
    </filter>
  </defs>

  <g filter="url(#gem-shadow)">
    <!-- Faset Kristal Permata Permen (Octagonal Gem Facets) -->
    <!-- Table Face (Muka Tengah Atas) -->
    <polygon points="360,280 640,280 740,380 740,620 640,720 360,720 260,620 260,380" fill="url(#gem-mint-mid)"/>

    <!-- Faset Mahkota (Crown Facets) -->
    <polygon points="360,280 640,280 570,350 430,350" fill="url(#gem-mint-light)"/>
    <polygon points="640,280 740,380 650,430 570,350" fill="#90D5C5"/>
    <polygon points="740,380 740,620 650,570 650,430" fill="url(#gem-mint-mid)"/>
    <polygon points="740,620 640,720 570,650 650,570" fill="url(#gem-mint-dark)"/>
    <polygon points="640,720 360,720 430,650 570,650" fill="#255E52"/>
    <polygon points="360,720 260,620 350,570 430,650" fill="url(#gem-mint-dark)"/>
    <polygon points="260,620 260,380 350,430 350,570" fill="#58AC9A"/>
    <polygon points="260,380 360,280 430,350 350,430" fill="url(#gem-mint-light)"/>

    <!-- Meja Tengah Kristal (Inner Table) -->
    <polygon points="430,350 570,350 650,430 650,570 570,650 430,650 350,570 350,430" fill="#E6FAF5"/>

    <!-- Kilau Sudut Berlian (Sparkle Glints) -->
    <polygon points="430,350 470,380 400,410" fill="#FFFFFF" opacity="0.9"/>
    <polygon points="570,350 610,390 540,390" fill="#FFFFFF" opacity="0.75"/>
    <circle cx="360" cy="280" r="16" fill="#FFFFFF"/>
    <circle cx="640" cy="280" r="12" fill="#FFFFFF"/>
  </g>
</svg>'''


def get_molten_chocolate_drip_border_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 500" width="100%" height="100%">
  <defs>
    <linearGradient id="drip-choc-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#4E1C10"/>
      <stop offset="60%" stop-color="#2D0B04"/>
      <stop offset="100%" stop-color="#140301"/>
    </linearGradient>
    <linearGradient id="drip-caramel-grad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFEAA0"/>
      <stop offset="50%" stop-color="#E09D17"/>
      <stop offset="100%" stop-color="#9C5D05"/>
    </linearGradient>
    <filter id="drip-shadow" x="-5%" y="-10%" width="110%" height="130%">
      <feDropShadow dx="0" dy="16" stdDeviation="18" flood-color="#120114" flood-opacity="0.5"/>
    </filter>
  </defs>

  <g filter="url(#drip-shadow)">
    <!-- 1. Lapisan Belakang: Lelehan Karamel Emas -->
    <path d="M 0 0 L 1600 0 L 1600 120
             C 1520 150, 1480 320, 1440 320 C 1400 320, 1370 160, 1310 160
             C 1260 160, 1220 270, 1180 270 C 1140 270, 1110 150, 1050 150
             C 990 150, 960 380, 900 380 C 850 380, 830 180, 770 180
             C 720 180, 680 340, 640 340 C 600 340, 580 150, 520 150
             C 470 150, 440 290, 400 290 C 360 290, 330 140, 260 140
             C 210 140, 180 350, 130 350 C 90 350, 60 160, 0 160 Z"
          fill="url(#drip-caramel-grad)"/>

    <!-- 2. Lapisan Depan: Lelehan Cokelat Kental Utama -->
    <path d="M 0 0 L 1600 0 L 1600 80
             C 1550 120, 1510 240, 1470 240 C 1430 240, 1410 120, 1360 120
             C 1310 120, 1280 360, 1230 360 C 1180 360, 1160 100, 1100 100
             C 1050 100, 1020 260, 970 260 C 930 260, 900 120, 840 120
             C 790 120, 760 440, 700 440 C 650 440, 630 130, 570 130
             C 520 130, 490 280, 440 280 C 400 280, 380 90, 320 90
             C 270 90, 240 380, 180 380 C 130 380, 110 110, 0 110 Z"
          fill="url(#drip-choc-grad)"/>

    <!-- 3. Highlight Kilau Lengkungan Cokelat (Gloss Highlights) -->
    <path d="M 40 40 Q 200 40 350 40" stroke="#7A3222" stroke-width="12" fill="none" opacity="0.6"/>
    <path d="M 180 180 C 180 340, 160 360, 180 360" stroke="#7A3222" stroke-width="8" fill="none" opacity="0.7"/>
    <path d="M 700 200 C 700 400, 680 420, 700 420" stroke="#7A3222" stroke-width="10" fill="none" opacity="0.7"/>
    <path d="M 1230 180 C 1230 320, 1210 340, 1230 340" stroke="#7A3222" stroke-width="8" fill="none" opacity="0.7"/>
  </g>
</svg>'''


def get_golden_ribbon_banner_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 600" width="100%" height="100%">
  <defs>
    <linearGradient id="ribbon-front-gold" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#C2820A"/>
      <stop offset="20%" stop-color="#F5C538"/>
      <stop offset="50%" stop-color="#FFF9D2"/>
      <stop offset="80%" stop-color="#F5C538"/>
      <stop offset="100%" stop-color="#C2820A"/>
    </linearGradient>
    <linearGradient id="ribbon-back-fold" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#7A4B02"/>
      <stop offset="100%" stop-color="#3D2200"/>
    </linearGradient>
    <linearGradient id="ribbon-tail-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#A36B04"/>
      <stop offset="50%" stop-color="#F5C538"/>
      <stop offset="100%" stop-color="#8A5802"/>
    </linearGradient>
    <filter id="ribbon-shadow" x="-10%" y="-20%" width="120%" height="140%">
      <feDropShadow dx="0" dy="24" stdDeviation="28" flood-color="#120114" flood-opacity="0.55"/>
    </filter>
  </defs>

  <g filter="url(#ribbon-shadow)">
    <!-- 1. Ekor Pita Belakang Kiri (Left Swallowtail) -->
    <path d="M 280 280 L 100 240 L 160 350 L 100 460 L 280 400 Z" fill="url(#ribbon-tail-grad)" stroke="#8A5802" stroke-width="3"/>
    <!-- Lipatan Bayangan Kiri -->
    <polygon points="280,280 280,400 360,350" fill="url(#ribbon-back-fold)"/>

    <!-- 2. Ekor Pita Belakang Kanan (Right Swallowtail) -->
    <path d="M 1320 280 L 1500 240 L 1440 350 L 1500 460 L 1320 400 Z" fill="url(#ribbon-tail-grad)" stroke="#8A5802" stroke-width="3"/>
    <!-- Lipatan Bayangan Kanan -->
    <polygon points="1320,280 1320,400 1240,350" fill="url(#ribbon-back-fold)"/>

    <!-- 3. Pita Depan Lengkung Utama (Main Front Arch Ribbon) -->
    <path d="M 280 280
             C 500 220, 1100 220, 1320 280
             L 1320 400
             C 1100 340, 500 340, 280 400
             Z"
          fill="url(#ribbon-front-gold)" stroke="#8A5802" stroke-width="3"/>

    <!-- Garis Lis Jahitan Emas Halus (Filigree Dashed Inset) -->
    <path d="M 300 295 C 510 240, 1090 240, 1300 295" fill="none" stroke="#FFFFFF" stroke-width="2" opacity="0.8"/>
    <path d="M 300 385 C 510 325, 1090 325, 1300 385" fill="none" stroke="#7A4B02" stroke-width="2"/>
  </g>
</svg>'''


def get_ornate_corner_filigree_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 800" width="100%" height="100%">
  <defs>
    <linearGradient id="filigree-gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFF3B0"/>
      <stop offset="40%" stop-color="#F5C538"/>
      <stop offset="80%" stop-color="#E09D17"/>
      <stop offset="100%" stop-color="#9C5D05"/>
    </linearGradient>
    <filter id="filigree-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="16" stdDeviation="20" flood-color="#120114" flood-opacity="0.45"/>
    </filter>
  </defs>

  <g filter="url(#filigree-shadow)">
    <!-- Garis Bingkai Sudut L-Shape Dasar -->
    <path d="M 100 700 L 100 100 L 700 100" fill="none" stroke="url(#filigree-gold)" stroke-width="12" stroke-linecap="round"/>
    <path d="M 125 650 L 125 125 L 650 125" fill="none" stroke="url(#filigree-gold)" stroke-width="4" stroke-dasharray="10 6"/>

    <!-- Sulur Daun & Spiral Pojok Luar -->
    <path d="M 100 100 C 100 240, 240 100, 100 100 Z" fill="url(#filigree-gold)"/>
    <path d="M 100 100 C 160 160, 200 200, 280 280 C 220 320, 180 260, 140 220 Z" fill="url(#filigree-gold)"/>

    <!-- Sulur Daun Melingkar Atas -->
    <path d="M 280 100 C 340 60, 420 80, 450 125 C 410 140, 360 120, 280 100 Z" fill="url(#filigree-gold)"/>
    <path d="M 450 100 C 520 70, 580 80, 600 120" fill="none" stroke="url(#filigree-gold)" stroke-width="8" stroke-linecap="round"/>

    <!-- Sulur Daun Melingkar Sisi Kiri -->
    <path d="M 100 280 C 60 340, 80 420, 125 450 C 140 410, 120 360, 100 280 Z" fill="url(#filigree-gold)"/>
    <path d="M 100 450 C 70 520, 80 580, 120 600" fill="none" stroke="url(#filigree-gold)" stroke-width="8" stroke-linecap="round"/>

    <!-- Bunga / Intan Rosetta Pojok Tengah (Corner Rosette) -->
    <g transform="translate(200, 200)">
      <circle cx="0" cy="0" r="30" fill="url(#filigree-gold)"/>
      <circle cx="0" cy="0" r="14" fill="#FFFFFF"/>
      <!-- 4 Kelopak Bunga Emas -->
      <polygon points="0,-60 16,-20 0,0 -16,-20" fill="url(#filigree-gold)"/>
      <polygon points="0,60 16,20 0,0 -16,20" fill="url(#filigree-gold)"/>
      <polygon points="-60,0 -20,-16 0,0 -20,16" fill="url(#filigree-gold)"/>
      <polygon points="60,0 20,-16 0,0 20,16" fill="url(#filigree-gold)"/>
    </g>
  </g>
</svg>'''


def get_decorative_divider_line_svg():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 240" width="100%" height="100%">
  <defs>
    <linearGradient id="divider-gold-left" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#E09D17" stop-opacity="0"/>
      <stop offset="40%" stop-color="#E09D17"/>
      <stop offset="100%" stop-color="#FFF3B0"/>
    </linearGradient>
    <linearGradient id="divider-gold-right" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FFF3B0"/>
      <stop offset="60%" stop-color="#E09D17"/>
      <stop offset="100%" stop-color="#E09D17" stop-opacity="0"/>
    </linearGradient>
    <radialGradient id="star-glow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="30%" stop-color="#FFF9D2"/>
      <stop offset="70%" stop-color="#F5C538"/>
      <stop offset="100%" stop-color="#F5C538" stop-opacity="0"/>
    </radialGradient>
    <filter id="div-shadow" x="-5%" y="-20%" width="110%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="12" flood-color="#120114" flood-opacity="0.45"/>
    </filter>
  </defs>

  <g filter="url(#div-shadow)">
    <!-- Garis Kiri Meruncing ke Tengah -->
    <path d="M 80 120 L 700 120" stroke="url(#divider-gold-left)" stroke-width="4" stroke-linecap="round"/>
    <path d="M 240 108 L 680 108" stroke="url(#divider-gold-left)" stroke-width="1.5" stroke-dasharray="8 6"/>

    <!-- Garis Kanan Meruncing ke Tengah -->
    <path d="M 900 120 L 1520 120" stroke="url(#divider-gold-right)" stroke-width="4" stroke-linecap="round"/>
    <path d="M 920 108 L 1360 108" stroke="url(#divider-gold-right)" stroke-width="1.5" stroke-dasharray="8 6"/>

    <!-- Ornamen Pusat Tengah (Bintang Stardust & Intan Berlian) -->
    <g transform="translate(800, 120)">
      <circle cx="0" cy="0" r="70" fill="url(#star-glow)"/>
      <!-- Bintang 4-Sudut Emas Besar -->
      <polygon points="0,-80 12,-16 80,0 12,16 0,80 -12,16 -80,0 -12,-16" fill="#FFF9D2"/>
      <polygon points="0,-50 8,-10 50,0 8,10 0,50 -8,10 -50,0 -8,-10" fill="#FFFFFF"/>
      <!-- 2 Intan Berlian Satelit Kiri & Kanan -->
      <polygon points="-120,0 -105,-12 -90,0 -105,12" fill="#F5C538"/>
      <polygon points="120,0 105,-12 90,0 105,12" fill="#F5C538"/>
      <!-- Titik Mutiara -->
      <circle cx="-145" cy="0" r="4" fill="#FFEAA0"/>
      <circle cx="145" cy="0" r="4" fill="#FFEAA0"/>
    </g>
  </g>
</svg>'''


# ==============================================================================
# PIPELINE EKSEKUSI PEMBANGUNAN SELURUH ASET ITEM (16 ASET LENGKAP)
# ==============================================================================

ITEMS = [
    # Koleksi 1: Aset Eksisting
    ("item-magic-top-hat", get_magic_top_hat_svg, 1200, 1200),
    ("item-swirl-lollipop", get_swirl_lollipop_svg, 1200, 1400),
    ("item-golden-cane", get_golden_cane_svg, 800, 1500),
    ("item-wrapped-bonbon-pink", get_wrapped_bonbon_pink_svg, 1400, 900),
    ("item-golden-ticket-badge", get_golden_ticket_badge_svg, 1400, 900),
    ("item-confectionery-rose", get_confectionery_rose_svg, 1100, 1100),
    ("item-whimsical-glasses", get_whimsical_glasses_svg, 1400, 800),
    ("item-stardust-sparkle-stars", get_stardust_sparkle_cluster_svg, 1200, 1200),
    
    # Koleksi 2: Cokelat & Permen Fantasi
    ("item-golden-chocolate-bar", get_golden_chocolate_bar_svg, 1200, 1200),
    ("item-swirl-candy-cane", get_swirl_candy_cane_svg, 1000, 1400),
    ("item-gourmet-praline-truffle", get_gourmet_praline_truffle_svg, 1000, 1000),
    ("item-confectionery-sugar-gem", get_confectionery_sugar_gem_svg, 1000, 1000),
    ("item-molten-chocolate-drip-border", get_molten_chocolate_drip_border_svg, 1600, 500),
    
    # Koleksi 3: Utilitas & Bingkai Desain
    ("item-golden-ribbon-banner", get_golden_ribbon_banner_svg, 1600, 600),
    ("item-ornate-corner-filigree", get_ornate_corner_filigree_svg, 800, 800),
    ("item-decorative-divider-line", get_decorative_divider_line_svg, 1600, 240),
]


def build_all_items():
    print("==================================================================")
    print(" MEMBANGUN KATALOG 16 ASET MODULAR LENGKAP (SVG & TRANSPARENT PNG)")
    print("==================================================================")

    for name, svg_func, w, h in ITEMS:
        svg_code = svg_func()
        svg_file = os.path.join(SVG_DIR, f"{name}.svg")
        png_file = os.path.join(PNG_DIR, f"{name}.png")

        # 1. Simpan SVG
        with open(svg_file, "w", encoding="utf-8") as f:
            f.write(svg_code)

        # 2. Render PNG 32-bit via Chrome
        render_svg_to_png(svg_file, png_file, width=w, height=h)
        print(f"✓ {name}: {svg_file} & {png_file} ({w}x{h} px)")

    print("\n✓ SELURUH 16 ASET ITEM MODULAR TELAH BERHASIL DIPRODUKSI 100%!")


if __name__ == "__main__":
    build_all_items()

