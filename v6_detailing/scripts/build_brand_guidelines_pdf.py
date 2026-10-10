#!/usr/bin/env python3
"""
build_brand_guidelines_pdf.py
Membangun Buku Pedoman Identitas Visual & Logo Guideline (Brand Book) resmi
Dies Natalis ke-44 SMAN 1 Gedeg (1982-2026) dalam format PDF A4 Landscape.

Isi Buku Pedoman:
1. Cover: Logo Master V6, Judul Resmi, Tema AVERSA, Guru: Ryan Ardian
2. Pendahuluan & Sejarah 44 Tahun Almamater
3. Filosofi & Anatomi Lambang 44 (Rajawali, Api, Sayap, Medial Spine)
4. Tema & 4 Pilar Filosofi AVERSA
5. Koleksi Varian Logo Resmi (Full Color, Linecut, Monochrome, Inverted, Grid)
6. Sistem Tata Letak Lockup (Horizontal, Vertical, Brand Combination)
7. Sistem Palet Warna Resmi (Master Chromatic Palette & Teater Fantasi)
8. Sistem Tipografi & Penyelarasan Font (Plus Jakarta Sans, Cinzel, Type Scale)
9. Area Bebas (Clear Space) & Ukuran Minimum
10. Katalog Aset Modular Pendukung (Tiket Emas, Topi, Permen, Tongkat, dll.)
11. Latar Belakang Sinematik Resmi (Pinwheel Mint & Velvet Stardust)
12. Mockup Cendera Mata & Merchandise Resmi (Polo, Tumbler, Lanyard, Pin)
13. Aturan Larangan & Kepatuhan Desain (Do's & Don'ts)
14. Hak Cipta, Legalitas & Penutup (Colophon)
"""

import base64
import os
import subprocess
from pathlib import Path

WORKSPACE = Path("/Users/ardianryan/Documents/diesnat44project")
HTML_OUT = WORKSPACE / "docs/brand_guidelines_book.html"
PDF_OUT = WORKSPACE / "docs/Brand_Guidelines_Dies_Natalis_44_SMAN1Gedeg.pdf"

def get_base64_img(rel_path: str) -> str:
    p = WORKSPACE / rel_path
    if not p.exists():
        print(f"Warning: image not found: {p}")
        return ""
    mime = "image/png" if p.suffix.lower() == ".png" else "image/jpeg"
    if p.suffix.lower() == ".svg":
        mime = "image/svg+xml"
    data = base64.b64encode(p.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{data}"

def build_html():
    # Asset Base64 images for fail-safe embedding
    img_logo_color = get_base64_img("assets/png/logo-color-2048.png")
    img_logo_linecut = get_base64_img("assets/png/logo-linecut-black.png")
    img_logo_mono_black = get_base64_img("assets/png/logo-monochrome-black.png")
    img_logo_mono_white = get_base64_img("assets/png/logo-monochrome-white.png")
    img_logo_grid = get_base64_img("assets/png/logo-with-grid.png")
    img_logo_horizontal = get_base64_img("assets/png/logo-horizontal-color.png")
    img_logo_vertical = get_base64_img("assets/png/logo-vertical-color.png")
    
    img_aversa_wordmark = get_base64_img("assets/png/aversa-standalone-color.png")
    img_aversa_vertical = get_base64_img("assets/png/aversa-logotype-vertical.png")
    img_aversa_horizontal = get_base64_img("assets/png/aversa-logotype-horizontal.png")
    img_aversa_combo = get_base64_img("assets/png/aversa-brand-combination.png")
    
    img_palette_guide = get_base64_img("assets/brandkit_elements/png/brand-color-palette-guide.png")
    
    img_ticket = get_base64_img("assets/brandkit_elements/png/item-golden-ticket-badge.png")
    img_hat = get_base64_img("assets/brandkit_elements/png/item-magic-top-hat.png")
    img_lollipop = get_base64_img("assets/brandkit_elements/png/item-swirl-lollipop.png")
    img_cane = get_base64_img("assets/brandkit_elements/png/item-golden-cane.png")
    img_bonbon = get_base64_img("assets/brandkit_elements/png/item-wrapped-bonbon-pink.png")
    img_rose = get_base64_img("assets/brandkit_elements/png/item-confectionery-rose.png")
    img_glasses = get_base64_img("assets/brandkit_elements/png/item-whimsical-glasses.png")
    img_stardust = get_base64_img("assets/brandkit_elements/png/item-stardust-sparkle-stars.png")
    
    img_bg_pinwheel = get_base64_img("assets/brandkit_elements/backgrounds/bg-theatrical-pinwheel-mint.png")
    img_bg_velvet = get_base64_img("assets/brandkit_elements/backgrounds/bg-imperial-velvet-stardust.png")
    
    img_mockup_polo = get_base64_img("assets/mockups/mockup_kaos_polo.jpg")
    img_mockup_tumbler = get_base64_img("assets/mockups/mockup_tumbler.jpg")
    img_mockup_lanyard = get_base64_img("assets/mockups/mockup_lanyard_idcard.jpg")
    img_mockup_totebag = get_base64_img("assets/mockups/mockup_totebag_pin.jpg")

    html = f"""<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8">
  <title>Buku Pedoman Identitas Visual Dies Natalis ke-44 SMAN 1 Gedeg</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    @page {{
      size: 297mm 210mm;
      margin: 0;
    }}
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    body {{
      font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
      color: #FFFFFF;
      background: #0B040D;
      font-size: 13px;
      line-height: 1.5;
    }}
    .cinzel {{
      font-family: 'Cinzel', Georgia, serif;
    }}
    .playfair {{
      font-family: 'Playfair Display', Georgia, serif;
    }}
    
    /* Page Layout */
    .page {{
      width: 297mm;
      height: 210mm;
      position: relative;
      overflow: hidden;
      page-break-after: always;
      display: flex;
      flex-direction: column;
      background: #150619;
      padding: 16mm 20mm;
    }}
    
    /* Page Header */
    .page-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1.5px solid rgba(245, 197, 56, 0.4);
      padding-bottom: 4mm;
      margin-bottom: 6mm;
    }}
    .header-tagline {{
      font-size: 9px;
      letter-spacing: 3px;
      color: #F7D160;
      font-weight: 700;
      text-transform: uppercase;
    }}
    .header-title {{
      font-size: 18px;
      font-weight: 800;
      color: #FFFFFF;
      letter-spacing: 0.5px;
    }}
    .header-meta {{
      text-align: right;
      font-size: 9px;
      color: #D4B8DE;
      letter-spacing: 1.5px;
      font-weight: 600;
    }}
    
    /* Page Footer */
    .page-footer {{
      position: absolute;
      bottom: 8mm;
      left: 20mm;
      right: 20mm;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid rgba(255, 255, 255, 0.1);
      padding-top: 3mm;
      font-size: 8.5px;
      color: #A38CAE;
    }}
    .page-num {{
      font-weight: 800;
      color: #F5C538;
      font-size: 10px;
    }}
    
    /* Cards and Grids */
    .content-area {{
      flex: 1;
      display: flex;
      flex-direction: column;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 6mm;
      height: 100%;
    }}
    .grid-3 {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 5mm;
      height: 100%;
    }}
    .grid-4 {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 4mm;
      height: 100%;
    }}
    .card {{
      background: rgba(45, 12, 53, 0.5);
      border: 1px solid rgba(245, 197, 56, 0.25);
      border-radius: 8px;
      padding: 5mm;
      display: flex;
      flex-direction: column;
    }}
    .card-title {{
      font-size: 13px;
      font-weight: 800;
      color: #FDF39D;
      margin-bottom: 2mm;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .badge {{
      display: inline-block;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 8px;
      font-weight: 800;
      letter-spacing: 1px;
      background: #4A1255;
      color: #FFEAA0;
      border: 1px solid #E09D17;
      text-transform: uppercase;
    }}
    
    /* Typography Styles */
    h1, h2, h3, h4 {{
      color: #FFFFFF;
    }}
    p {{
      color: #E6D8EB;
      margin-bottom: 2mm;
    }}
    
    /* COVER PAGE SPECIAL */
    .cover-page {{
      background: radial-gradient(circle at 50% 40%, #360538 0%, #1a021c 60%, #0c010d 100%);
      padding: 20mm;
      justify-content: space-between;
      align-items: center;
      text-align: center;
    }}
    .cover-logo-wrapper {{
      margin-top: 10mm;
      position: relative;
    }}
    .cover-logo {{
      width: 70mm;
      height: auto;
      filter: drop-shadow(0 15px 35px rgba(245, 197, 56, 0.35));
    }}
    .cover-badge {{
      display: inline-block;
      padding: 3mm 8mm;
      border-radius: 20px;
      background: rgba(245, 197, 56, 0.12);
      border: 1.5px solid #F5C538;
      color: #FFEAA0;
      font-size: 11px;
      font-weight: 800;
      letter-spacing: 3px;
      margin-bottom: 4mm;
    }}
    .cover-title {{
      font-size: 32px;
      font-weight: 900;
      letter-spacing: 1.5px;
      color: #FFFFFF;
      text-transform: uppercase;
      line-height: 1.2;
      margin-bottom: 2mm;
    }}
    .cover-subtitle {{
      font-size: 18px;
      font-weight: 700;
      color: #F7D160;
      letter-spacing: 2px;
      margin-bottom: 4mm;
    }}
    .cover-theme {{
      font-size: 26px;
      font-weight: 900;
      color: #FFFFFF;
      letter-spacing: 6px;
      text-shadow: 0 4px 15px rgba(245, 197, 56, 0.4);
    }}
    .cover-footer {{
      border-top: 1px solid rgba(245, 197, 56, 0.4);
      padding-top: 5mm;
      width: 100%;
      display: flex;
      justify-content: space-between;
      font-size: 10px;
      color: #CDB3D6;
    }}
    
    /* Image Preview Boxes */
    .img-box {{
      background: #0E0211;
      border: 1px solid rgba(245, 197, 56, 0.2);
      border-radius: 6px;
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: hidden;
      padding: 3mm;
    }}
    .img-box img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }}
    .img-box.light {{
      background: #FDFBF7;
    }}
    
    /* Pillar Cards */
    .pillar-num {{
      font-size: 20px;
      font-weight: 900;
      color: #F5C538;
      font-family: 'Cinzel', serif;
      margin-bottom: 1mm;
    }}
    
    /* Table Styling */
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 10px;
      margin-top: 2mm;
    }}
    th {{
      background: #3B0E47;
      color: #FDF39D;
      text-align: left;
      padding: 5px 8px;
      font-weight: 800;
      letter-spacing: 0.5px;
      border-bottom: 2px solid #F5C538;
    }}
    td {{
      padding: 5px 8px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      color: #E2D4E6;
    }}
    tr:nth-child(even) td {{
      background: rgba(255, 255, 255, 0.02);
    }}
  </style>
</head>
<body>

  <!-- ==================== HALAMAN 1: COVER ==================== -->
  <div class="page cover-page">
    <div style="width: 100%; text-align: center;">
      <div class="cover-badge cinzel">EDISI RESMI • PEDOMAN IDENTITAS VISUAL</div>
      <div class="cover-title">BUKU PEDOMAN IDENTITAS VISUAL &amp; LOGO GUIDELINE</div>
      <div class="cover-subtitle cinzel">DIES NATALIS KE-44 SMA NEGERI 1 GEDEG (1982–2026)</div>
      <div class="cover-theme playfair">TEMA UTAMA: AVERSA</div>
    </div>
    
    <div class="cover-logo-wrapper">
      <img src="{img_logo_color}" class="cover-logo" alt="Logo Dies Natalis 44 Master V6">
    </div>

    <div class="cover-footer">
      <div>
        <strong style="color: #F7D160;">SMA NEGERI 1 GEDEG</strong><br>
        Kec. Gedeg, Kabupaten Mojokerto, Jawa Timur
      </div>
      <div style="text-align: center;">
        <span class="cinzel" style="color: #FFFFFF; font-weight: 700; letter-spacing: 2px;">KARYA DESAIN RESMI ALMAMATER</span><br>
        Guru Pengampu: <strong>Ryan Ardian</strong>
      </div>
      <div style="text-align: right;">
        <strong style="color: #F5C538;">STANDAR MASTER V6 FINAL</strong><br>
        Lisensi Tertutup Eksklusif (All Rights Reserved)
      </div>
    </div>
  </div>


  <!-- ==================== HALAMAN 2: PENDAHULUAN & SEJARAH ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 1 • PENDAHULUAN</div>
        <div class="header-title">SEJARAH 44 TAHUN &amp; URGENSI BUKU PEDOMAN</div>
      </div>
      <div class="header-meta">DIES NATALIS KE-44 • SMAN 1 GEDEG</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="card">
          <div class="card-title cinzel">TONGGAK SEJARAH 44 TAHUN (1982–2026)</div>
          <p style="text-align: justify; margin-bottom: 3mm;">
            Sejak didirikan pada tahun <strong>1982</strong>, SMA Negeri 1 Gedeg telah mengukir perjalanan panjang pengabdian dalam mencerdaskan kehidupan bangsa di Kabupaten Mojokerto. Memasuki usia ke-44 tahun pada tahun <strong>2026</strong>, almamater meneguhkan kedewasaan institusi dalam memadukan keteguhan akhlak budi pekerti dengan keunggulan inovasi ilmu pengetahuan abad ke-21.
          </p>
          <p style="text-align: justify; margin-bottom: 3mm;">
            Peringatan <strong>Dies Natalis ke-44</strong> bukan sekadar perayaan seremonial biasa, melainkan momentum akselerasi prestasi akbar civitas akademika untuk terus melesat, terbang tinggi melintasi batas tantangan, dan melahirkan generasi emas yang berdaya saing global.
          </p>
          <div style="margin-top: auto; padding: 3mm; background: rgba(245, 197, 56, 0.08); border-left: 3px solid #F5C538; border-radius: 4px;">
            <strong style="color: #FFEAA0;">Pilar Moral Almamater:</strong><br>
            <span style="font-size: 11px; color: #EADCEF;">Religius, Berbudi Luhur, Cerdas Intelektual, Berbudaya Lingkungan, dan Berwawasan Global.</span>
          </div>
        </div>

        <div class="card">
          <div class="card-title cinzel">MAKSUD &amp; TUJUAN BUKU PEDOMAN MEREK</div>
          <p style="text-align: justify; margin-bottom: 3mm;">
            Buku Pedoman Identitas Visual (*Brand Guidelines &amp; Logo Book*) ini diterbitkan sebagai panduan baku teknis dan estetika bagi seluruh pihak panitia, desainer grafis, mitra percetakan, dan civitas akademika SMA Negeri 1 Gedeg dalam mengimplementasikan lambang resmi.
          </p>
          
          <div style="display: flex; flex-direction: column; gap: 3mm; margin-top: 2mm;">
            <div style="display: flex; gap: 8px; align-items: flex-start;">
              <span class="badge" style="background:#5C186B;">1. KONSISTENSI</span>
              <p style="font-size: 11px; margin: 0;">Menjamin keutuhan visual lambang di seluruh media cetak, kain, logam, dan platform digital.</p>
            </div>
            <div style="display: flex; gap: 8px; align-items: flex-start;">
              <span class="badge" style="background:#5C186B;">2. WIBAWA</span>
              <p style="font-size: 11px; margin: 0;">Menjaga marwah akademik 44 tahun almamater agar terhindar dari distorsi, perubahan warna serampangan, atau salah penempatan.</p>
            </div>
            <div style="display: flex; gap: 8px; align-items: flex-start;">
              <span class="badge" style="background:#5C186B;">3. EFISIENSI</span>
              <p style="font-size: 11px; margin: 0;">Mempercepat proses produksi atribut dan cendera mata dengan standar berkas vektor SVG matematis dan raster ultra-HD.</p>
            </div>
          </div>

          <div style="margin-top: auto; padding: 2.5mm; background: rgba(0,0,0,0.3); border-radius: 4px; text-align: center; border: 1px dashed rgba(245, 197, 56, 0.3);">
            <span style="font-size: 10px; color: #F7D160; font-weight: 700;">DIPRODUKSI DENGAN STANDAR KOMPUTASIONAL VEKTOR PYTHON V6 FINAL</span>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 02</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 3: FILOSOFI & ANATOMI LAMBANG 44 ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 2 • ANATOMI &amp; MAKNA</div>
        <div class="header-title">FILOSOFI LIMA PILAR LAMBANG 44 (MASTER V6)</div>
      </div>
      <div class="header-meta">DEEP MEANING OF THE 44 EMBLEM</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="card" style="align-items: center; justify-content: center; padding: 4mm;">
          <div class="img-box" style="width: 100%; height: 110mm; background: #0E0211;">
            <img src="{img_logo_color}" style="max-height: 98mm;" alt="Anatomi Logo 44">
          </div>
          <div style="margin-top: 3mm; font-size: 10px; color: #FFEAA0; text-align: center;">
            <strong>FIGUR KEMBAR 44 DENGAN MEDIAL SPINE BUSUR KONSENTRIS SIMETRIS</strong>
          </div>
        </div>

        <div class="card" style="justify-content: space-between;">
          <div>
            <div class="card-title cinzel">LIMA PILAR ANATOMI LAMBANG</div>
            <div style="display: flex; flex-direction: column; gap: 2.5mm; margin-top: 2mm;">
              <div>
                <div class="pillar-num">01. STILASI ANGKA KEMBAR "44"</div>
                <p style="font-size: 11px;">Pilar historis kiri dan pilar dinamis kanan melambangkan usia ke-44 tahun kedewasaan almamater dalam memadukan tradisi dengan modernitas.</p>
              </div>
              <div>
                <div class="pillar-num">02. KEPALA &amp; TATAPAN RAJAWALI</div>
                <p style="font-size: 11px;">Paruh tajam yang menatap ke ufuk kanan atas melambangkan keberanian moral, ketajaman visi intelektual, dan wibawa kepemimpinan almamater.</p>
              </div>
              <div>
                <div class="pillar-num">03. LIDAH API ABADI BERKOBAR</div>
                <p style="font-size: 11px;">Sulur kobaran api melambangkan daya juang pantang padam, resiliensi tinggi, dan kreativitas tanpa batas civitas akademika.</p>
              </div>
              <div>
                <div class="pillar-num">04. SAYAP AERODINAMIS MELESAT</div>
                <p style="font-size: 11px;">Garis sayap menyapu ke kuadran atas melambangkan akselerasi prestasi siswa dan dorongan menuju era keemasan almamater.</p>
              </div>
              <div>
                <div class="pillar-num">05. MEDIAL SPINE SIMETRIS (V6)</div>
                <p style="font-size: 11px;">Penyempurnaan garis faset trimatra tengah dengan busur lingkaran murni menghasilkan efek kedalaman faset 3D yang kokoh dan berwibawa.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 03</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 4: TEMA RESMI & FILOSOFI AVERSA ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 3 • TEMA BESAR</div>
        <div class="header-title">LOGOTYPE RESMI &amp; EMPAT PILAR FILOSOFI "AVERSA"</div>
      </div>
      <div class="header-meta">THE SPIRIT OF AVERSA (1982–2026)</div>
    </div>

    <div class="content-area">
      <!-- Top Box: Wordmark Aversa -->
      <div class="card" style="margin-bottom: 5mm; padding: 4mm; align-items: center; background: #200526;">
        <div class="img-box" style="width: 100%; height: 35mm; background: transparent; border: none;">
          <img src="{img_aversa_wordmark}" style="max-height: 32mm;" alt="Wordmark Aversa">
        </div>
        <div style="font-size: 10px; color: #F7D160; margin-top: 1mm; font-weight: 700; letter-spacing: 2px;">
          REKONSTRUKSI BEZIER C1 MOLTEN GOLD FLUID BUBBLE TYPOGRAPHY DARI SKETSA ASLI
        </div>
      </div>

      <!-- Bottom Grid: 4 Pillars of Aversa -->
      <div class="grid-4" style="flex: 1;">
        <div class="card" style="border-top: 3px solid #E09D17;">
          <div class="pillar-num">PILAR 1</div>
          <div class="card-title" style="font-size: 12px; color: #FFEAA0;">SEMANGAT TERUS BERKEMBANG</div>
          <p style="font-size: 10.5px; text-align: justify;">
            Melambangkan dorongan internal tanpa henti bagi civitas akademika untuk senantiasa mengasah potensi diri, memperluas wawasan keilmuan, dan bertumbuh secara dinamis menghadapi disrupsi zaman.
          </p>
        </div>

        <div class="card" style="border-top: 3px solid #F5C538;">
          <div class="pillar-num">PILAR 2</div>
          <div class="card-title" style="font-size: 12px; color: #FFEAA0;">MEMILIKI VISI YANG JELAS</div>
          <p style="font-size: 10.5px; text-align: justify;">
            Arah kompas masa depan yang terukur dan berfokus pada capaian prestasi akademik serta akhlak mulia, selaras dengan tatapan tajam burung rajawali ke ufuk masa depan.
          </p>
        </div>

        <div class="card" style="border-top: 3px solid #F7D160;">
          <div class="pillar-num">PILAR 3</div>
          <div class="card-title" style="font-size: 12px; color: #FFEAA0;">MEMBANGUN SOLIDARITAS</div>
          <p style="font-size: 10.5px; text-align: justify;">
            Ikatan persaudaraan yang erat, inklusif, dan saling menguatkan antara siswa, guru, staf, alumni, dan orang tua dalam naungan keluarga besar SMA Negeri 1 Gedeg.
          </p>
        </div>

        <div class="card" style="border-top: 3px solid #FDF39D;">
          <div class="pillar-num">PILAR 4</div>
          <div class="card-title" style="font-size: 12px; color: #FFEAA0;">TINDAKAN NYATA &amp; PERUBAHAN</div>
          <p style="font-size: 10.5px; text-align: justify;">
            Ketegasan sikap untuk tidak berhenti pada wacana, melainkan berani mengeksekusi ide, melahirkan inovasi kreatif, dan mewujudkan transformasi nyata yang berdampak luhur bagi bangsa.
          </p>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 04</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 5: KOLEKSI VARIAN LOGO RESMI 44 ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 4 • IDENTITAS VISUAL</div>
        <div class="header-title">KOLEKSI VARIAN LOGO RESMI (THE MASTER 44 LOGO SUITE)</div>
      </div>
      <div class="header-meta">STANDARD GRAPHIC ASSETS</div>
    </div>

    <div class="content-area">
      <div class="grid-4" style="height: 100%;">
        <!-- Varian 1: Master Color -->
        <div class="card">
          <div class="img-box" style="height: 55mm; background: #120317;">
            <img src="{img_logo_color}" alt="Master Color">
          </div>
          <div style="margin-top: 3mm;">
            <span class="badge" style="background:#B6580B;">MASTER COLOR (V6)</span>
            <div class="card-title" style="font-size: 11px; margin-top: 1.5mm;">SIMBOL WARNA UTAMA</div>
            <p style="font-size: 9.5px;">Gradasi emas faset penuh. Digunakan untuk spanduk panggung, media sosial, buku kenangan, plakat gala.</p>
          </div>
        </div>

        <!-- Varian 2: Linecut Black -->
        <div class="card">
          <div class="img-box light" style="height: 55mm;">
            <img src="{img_logo_linecut}" alt="Linecut Black">
          </div>
          <div style="margin-top: 3mm;">
            <span class="badge" style="background:#334155;">LINE-CUT LASER</span>
            <div class="card-title" style="font-size: 11px; margin-top: 1.5mm;">KONTUR PRESISI GARIS</div>
            <p style="font-size: 9.5px;">Garis kontur rambut presisi. Diperuntukkan bagi grafir laser tumbler, cap stempel resmi, dan bordir.</p>
          </div>
        </div>

        <!-- Varian 3: Monochrome Inverted -->
        <div class="card">
          <div class="img-box" style="height: 55mm; background: #000000;">
            <img src="{img_logo_mono_white}" alt="Monochrome White">
          </div>
          <div style="margin-top: 3mm;">
            <span class="badge" style="background:#4A1255;">MONOKROM PUTIH</span>
            <div class="card-title" style="font-size: 11px; margin-top: 1.5mm;">INVERTED HIGH CONTRAST</div>
            <p style="font-size: 9.5px;">Putih murni untuk penempatan di atas latar belakang foto gelap, kain polo hitam, atau video bumper.</p>
          </div>
        </div>

        <!-- Varian 4: Geometric Grid -->
        <div class="card">
          <div class="img-box light" style="height: 55mm;">
            <img src="{img_logo_grid}" alt="Logo with Grid">
          </div>
          <div style="margin-top: 3mm;">
            <span class="badge" style="background:#1E3A8A;">BLUEPRINT GRID</span>
            <div class="card-title" style="font-size: 11px; margin-top: 1.5mm;">KISI GEOMETRIS BUSUR</div>
            <p style="font-size: 9.5px;">Pedoman konstruksi rasio busur lingkaran konsentris dan proporsi medial spine matematis.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 05</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 6: TATA LETAK LOCKUP (HORIZONTAL & VERTICAL) ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 5 • SISTEM TATA LETAK</div>
        <div class="header-title">SUSUNAN RESMI LOCKUP (HORIZONTAL, VERTICAL &amp; COMBINATION)</div>
      </div>
      <div class="header-meta">CO-BRANDING &amp; LOCKUP ARCHITECTURE</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="card">
          <div class="card-title cinzel">1. HORIZONTAL &amp; VERTICAL INSTITUSI</div>
          <div class="img-box" style="height: 48mm; margin-bottom: 3mm; background: #1A0521;">
            <img src="{img_logo_horizontal}" style="max-height: 40mm;" alt="Horizontal Lockup">
          </div>
          <p style="font-size: 10px; margin-bottom: 3mm;">
            <strong>Horizontal Lockup:</strong> Simbol di sebelah kiri diikuti identitas teks almamater di kanan. Sangat dianjurkan untuk spanduk jalan, kop surat dinas, dan header situs web.
          </p>
          <div class="img-box" style="height: 45mm; background: #1A0521;">
            <img src="{img_logo_vertical}" style="max-height: 40mm;" alt="Vertical Lockup">
          </div>
          <p style="font-size: 10px; margin-top: 2mm;">
            <strong>Vertical Lockup:</strong> Susunan sentral bertingkat untuk sampul buku panduan, piagam penghargaan, dan poster seremonial.
          </p>
        </div>

        <div class="card">
          <div class="card-title cinzel">2. INTEGRASI LOGOTYPE AVERSA</div>
          <div class="img-box" style="height: 48mm; margin-bottom: 3mm; background: #1A0521;">
            <img src="{img_aversa_horizontal}" style="max-height: 40mm;" alt="Aversa Horizontal">
          </div>
          <p style="font-size: 10px; margin-bottom: 3mm;">
            <strong>AVERSA Logotype Horizontal:</strong> Wordmark AVERSA berdampingan dengan identitas teks institusi sekolah untuk backdrop panggung pentas seni.
          </p>
          <div class="img-box" style="height: 45mm; background: #1A0521;">
            <img src="{img_aversa_combo}" style="max-height: 40mm;" alt="Aversa Combination">
          </div>
          <p style="font-size: 10px; margin-top: 2mm;">
            <strong>Brand Combination Lockup:</strong> Puncak hierarki gabungan Lambang Rajawali V6 + Wordmark AVERSA + Teks SMAN 1 Gedeg.
          </p>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 06</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 7: SISTEM PALET WARNA RESMI ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 6 • IDENTITAS WARNA</div>
        <div class="header-title">SISTEM PALET WARNA RESMI (MASTER CHROMATIC SPECIFICATION)</div>
      </div>
      <div class="header-meta">PENGGANTI RESMI COOLORS.JPEG</div>
    </div>

    <div class="content-area">
      <div class="card" style="padding: 2.5mm; margin-bottom: 4mm;">
        <div class="img-box" style="height: 65mm; background: transparent; border: none;">
          <img src="{img_palette_guide}" style="max-height: 64mm; width: 100%; object-fit: contain;" alt="Brand Color Palette Guide">
        </div>
      </div>

      <div class="card" style="flex: 1; padding: 3mm;">
        <div class="card-title cinzel" style="font-size: 11px;">SPESIFIKASI 8 WARNA INTI ALMAMATER &amp; AKSEN TEATER FANTASI</div>
        <table>
          <thead>
            <tr>
              <th>Indeks</th>
              <th>Nama Resmi Warna</th>
              <th>Kode HEX</th>
              <th>Nilai RGB</th>
              <th>Nilai CMYK</th>
              <th>Nilai HSL</th>
              <th>Peran &amp; Penggunaan Baku</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>#1</strong></td>
              <td><strong>Obsidian Mahogany</strong></td>
              <td><code>#310603</code></td>
              <td>49, 6, 3</td>
              <td>48, 88, 76, 75</td>
              <td>4°, 88%, 10%</td>
              <td>Batas siluet luar terdalam, bayangan faset 3D, teks gelap kontras tinggi</td>
            </tr>
            <tr>
              <td><strong>#2</strong></td>
              <td><strong>Deep Crimson Rust</strong></td>
              <td><code>#7D1B05</code></td>
              <td>125, 27, 5</td>
              <td>24, 96, 100, 27</td>
              <td>11°, 92%, 25%</td>
              <td>Pangkal lidah api berkobar, kedalaman bayangan faset hangat</td>
            </tr>
            <tr>
              <td><strong>#3</strong></td>
              <td><strong>Rich Amber Bronze</strong></td>
              <td><code>#B6580B</code></td>
              <td>182, 88, 11</td>
              <td>18, 73, 100, 7</td>
              <td>27°, 89%, 38%</td>
              <td>Transisi lekukan lipatan pita faset dan bayangan keemasan</td>
            </tr>
            <tr>
              <td><strong>#4</strong></td>
              <td><strong>Marigold Warm Gold</strong></td>
              <td><code>#E09D17</code></td>
              <td>224, 157, 23</td>
              <td>9, 39, 99, 0</td>
              <td>40°, 81%, 48%</td>
              <td>Warna tubuh utama angka 44 &amp; sayap almamater (Aura Kemuliaan)</td>
            </tr>
            <tr>
              <td><strong>#5</strong></td>
              <td><strong>Vivid Royal Gold</strong></td>
              <td><code>#F5C538</code></td>
              <td>245, 197, 56</td>
              <td>3, 21, 84, 0</td>
              <td>45°, 90%, 59%</td>
              <td>Tulang punggung simetris (Medial Spine) &amp; aksentuasi dinamis utama</td>
            </tr>
            <tr>
              <td><strong>#6</strong></td>
              <td><strong>Champagne Highlight</strong></td>
              <td><code>#F7D160</code></td>
              <td>247, 209, 96</td>
              <td>2, 16, 68, 0</td>
              <td>45°, 90%, 67%</td>
              <td>Sorotan cahaya puncak (specular highlight), siluet paruh rajawali</td>
            </tr>
            <tr>
              <td><strong>#7</strong></td>
              <td><strong>Pale Canary Vanilla</strong></td>
              <td><code>#FDF39D</code></td>
              <td>253, 243, 157</td>
              <td>1, 2, 44, 0</td>
              <td>54°, 96%, 80%</td>
              <td>Pendaran cahaya tertinggi, bintang stardust, kilau tatapan mata</td>
            </tr>
            <tr>
              <td><strong>#8</strong></td>
              <td><strong>Midnight Imperial Plum</strong></td>
              <td><code>#360538</code></td>
              <td>54, 5, 56</td>
              <td>72, 98, 38, 56</td>
              <td>298°, 84%, 12%</td>
              <td>Latar belakang beludru panggung gala &amp; cinderamata mewah almamater</td>
            </tr>
            <tr>
              <td colspan="7" style="background: rgba(245, 197, 56, 0.08); color: #FFEAA0; font-weight: bold;">
                ★ Aksen Teater Fantasi: Confectionery Mint (<code>#A0D9CA</code>) • Cotton Candy Pink (<code>#F5B8CB</code>) • Vanilla Custard (<code>#FFF5D6</code>)
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 07</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 8: SISTEM TIPOGRAFI & PENYELARASAN FONT ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 7 • TIPOGRAFI</div>
        <div class="header-title">SISTEM TIPOGRAFI &amp; PEDOMAN PENYELARASAN FONT</div>
      </div>
      <div class="header-meta">HIERARCHY &amp; TYPE GOVERNANCE</div>
    </div>

    <div class="content-area">
      <div class="grid-3" style="margin-bottom: 4mm;">
        <!-- Font 1 -->
        <div class="card" style="border-top: 3px solid #F5C538;">
          <span class="badge">FONT UTAMA KORPORAT</span>
          <div class="card-title" style="margin-top: 2mm; font-size: 15px;">Plus Jakarta Sans</div>
          <p style="font-size: 10px; color: #D6BDDF;">Sans-serif geometris modern berstandar internasional dengan keterbacaan prima pada media cetak mikro dan layar ponsel.</p>
          <div style="margin-top: auto; padding: 2mm; background: rgba(0,0,0,0.3); border-radius: 4px; font-size: 9.5px;">
            <strong>ExtraBold (800)</strong>: Judul &amp; Display<br>
            <strong>SemiBold (600)</strong>: Sub-judul &amp; Label<br>
            <strong>Regular (400)</strong>: Teks Paragraf Bodi
          </div>
        </div>

        <!-- Font 2 -->
        <div class="card" style="border-top: 3px solid #E09D17;">
          <span class="badge">FONT SEREMONIAL RESMI</span>
          <div class="card-title cinzel" style="margin-top: 2mm; font-size: 15px; color:#FFEAA0;">Cinzel</div>
          <p style="font-size: 10px; color: #D6BDDF;">Serif proporsi prasasti Romawi klasik untuk menegaskan wibawa akademik 44 tahun SMAN 1 Gedeg.</p>
          <div style="margin-top: auto; padding: 2mm; background: rgba(0,0,0,0.3); border-radius: 4px; font-size: 9.5px;">
            <strong>Format Wajib:</strong> Huruf Kapital (ALL CAPS)<br>
            <strong>Tracking:</strong> Lebar (+150 hingga +250)<br>
            <strong>Peruntukan:</strong> Piagam, Tiket Emas, Prasasti
          </div>
        </div>

        <!-- Font 3 -->
        <div class="card" style="border-top: 3px solid #F7D160;">
          <span class="badge">FONT PENTAS FESTIVAL</span>
          <div class="card-title playfair" style="margin-top: 2mm; font-size: 15px; color:#FFEAA0;">Playfair / AVERSA</div>
          <p style="font-size: 10px; color: #D6BDDF;">Serif transisional dramatis kontras tinggi dan tipografi cair kustom untuk tajuk pementasan seni kreatif.</p>
          <div style="margin-top: auto; padding: 2mm; background: rgba(0,0,0,0.3); border-radius: 4px; font-size: 9.5px;">
            <strong>Bobot:</strong> Black 900 / ExtraBold Italic<br>
            <strong>Peran:</strong> Tajuk Pentas Seni AVERSA<br>
            <strong>Karakter:</strong> Sinematik, Meriah, Dinamis
          </div>
        </div>
      </div>

      <div class="card" style="flex: 1; padding: 3mm;">
        <div class="card-title cinzel" style="font-size: 11px;">SKALA UKURAN &amp; HIERARKI TEKS (TYPE SCALE STANDARDS)</div>
        <table>
          <thead>
            <tr>
              <th>Tingkatan Hierarki</th>
              <th>Ukuran Web / Gawai</th>
              <th>Ukuran Cetak / A4</th>
              <th>Bobot Font</th>
              <th>Spasi Huruf (Letter-Spacing)</th>
              <th>Contoh Penggunaan Baku</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Display Hero</strong></td>
              <td><code>56px – 72px</code></td>
              <td><code>36pt – 48pt</code></td>
              <td>ExtraBold (800) / Black</td>
              <td><code>-0.02em</code></td>
              <td>Spanduk Panggung Utama, Baliho Gerbang Masuk</td>
            </tr>
            <tr>
              <td><strong>Heading 1 (H1)</strong></td>
              <td><code>40px – 48px</code></td>
              <td><code>26pt – 30pt</code></td>
              <td>ExtraBold (800)</td>
              <td><code>-0.01em</code></td>
              <td>Tajuk Bab Pedoman, Judul Poster Acara</td>
            </tr>
            <tr>
              <td><strong>Heading 2 (H2)</strong></td>
              <td><code>28px – 32px</code></td>
              <td><code>18pt – 22pt</code></td>
              <td>Bold (700)</td>
              <td><code>0em</code></td>
              <td>Sub-judul Kategori Lomba, Nama Bidang Panitia</td>
            </tr>
            <tr>
              <td><strong>Heading 3 (H3)</strong></td>
              <td><code>20px – 24px</code></td>
              <td><code>14pt – 16pt</code></td>
              <td>SemiBold (600)</td>
              <td><code>0em</code></td>
              <td>Kartu Pengumuman, Tanggal &amp; Waktu Kegiatan</td>
            </tr>
            <tr>
              <td><strong>Body Standard</strong></td>
              <td><code>15px – 16px</code></td>
              <td><code>10pt – 11pt</code></td>
              <td>Regular (400)</td>
              <td><code>0em</code></td>
              <td>Naskah Surat Dinas, Paragraf Narasi, Dokumen Proposal</td>
            </tr>
            <tr>
              <td><strong>Ceremonial Caps</strong></td>
              <td><code>18px – 28px</code></td>
              <td><code>12pt – 18pt</code></td>
              <td>Cinzel Bold (700)</td>
              <td><code>+0.20em (Lebar)</code></td>
              <td>Nama Lembaga, Lencana Tiket Emas, Sertifikat Juara</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 08</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 9: AREA AMAN & UKURAN MINIMUM ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 8 • ATURAN INTEGRITAS</div>
        <div class="header-title">AREA BEBAS (CLEAR SPACE) &amp; UKURAN MINIMUM PRODUKSI</div>
      </div>
      <div class="header-meta">ISOLATION ZONE &amp; SCALING LIMITS</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="card">
          <div class="card-title cinzel">1. AREA BEBAS (CLEAR SPACE ISOLATION)</div>
          <div class="img-box" style="height: 60mm; margin-bottom: 3mm; background: #120317; border: 1.5px dashed #F5C538;">
            <div style="position: relative; width: 60mm; height: 50mm; display: flex; justify-content: center; align-items: center;">
              <img src="{img_logo_color}" style="max-height: 42mm;" alt="Clear Space Logo">
              <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; border: 1px dashed rgba(245,197,56,0.6); pointer-events: none;"></div>
            </div>
          </div>
          <p style="text-align: justify; font-size: 10.5px;">
            Area bebas (*Clear Space*) adalah batas zona steril di sekeliling lambang yang tidak boleh dimasuki oleh elemen visual lain seperti teks, logo sponsor, ilustrasi, garis pemisah, atau tepi bidang potong cetak.
          </p>
          <div style="margin-top: auto; padding: 3mm; background: rgba(245, 197, 56, 0.08); border-radius: 4px; font-size: 10px;">
            <strong style="color: #FFEAA0;">Rumus Baku Zona Isolasi:</strong><br>
            Batas zona aman ditetapkan sebesar <strong>X = 1/4 tinggi total lambang</strong> pada seluruh sisi (atas, kanan, bawah, kiri).
          </div>
        </div>

        <div class="card">
          <div class="card-title cinzel">2. BATAS UKURAN MINIMUM PRODUKSI</div>
          <p style="text-align: justify; font-size: 10.5px; margin-bottom: 4mm;">
            Guna menjamin ketajaman faset 3D, siluet paruh rajawali, dan lengkungan lidah api tetap terbaca sempurna, penggunaan lambang dibatasi oleh ukuran ambang minimum:
          </p>

          <div style="display: flex; gap: 4mm; margin-bottom: 4mm;">
            <div class="img-box" style="flex: 1; padding: 4mm; flex-direction: column; text-align: center;">
              <img src="{img_logo_color}" style="height: 32px; width: auto; margin-bottom: 2mm;" alt="Min Digital">
              <strong style="color: #F5C538; font-size: 11px;">MEDIA DIGITAL</strong>
              <span style="font-size: 10px; color: #D6BDDF;">Tinggi Min: <strong>32 Piksel</strong><br>(Favicon / Thumbnail Aplikasi)</span>
            </div>

            <div class="img-box light" style="flex: 1; padding: 4mm; flex-direction: column; text-align: center;">
              <img src="{img_logo_linecut}" style="height: 40px; width: auto; margin-bottom: 2mm;" alt="Min Print">
              <strong style="color: #310603; font-size: 11px;">MEDIA CETAK FISIK</strong>
              <span style="font-size: 10px; color: #555555;">Tinggi Min: <strong>14 Milimeter</strong><br>(Lencana Pin Enamel Logam)</span>
            </div>
          </div>

          <div style="margin-top: auto; padding: 3mm; background: rgba(0,0,0,0.4); border-left: 3px solid #F5C538; border-radius: 4px; font-size: 9.5px;">
            <strong>Catatan Khusus Line-Cut:</strong><br>
            Untuk media cetak berukuran di bawah 25 mm atau teknik gravir logam mikro, gunakan varian <code>logo-linecut-black.svg</code> agar celah faset tidak tersumbat tinta.
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 09</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 10: KATALOG ASET MODULAR PENDUKUNG ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 9 • ELEMEN BRANDKIT</div>
        <div class="header-title">KATALOG ASET MODULAR PENDUKUNG (THEATRICAL ASSET SUITE)</div>
      </div>
      <div class="header-meta">STANDALONE MODULAR ELEMENTS</div>
    </div>

    <div class="content-area">
      <div class="grid-4" style="height: 100%;">
        <!-- Item 1: Ticket -->
        <div class="card" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_ticket}" alt="Golden Ticket">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10.5px;">TIKET EMAS KLASIK</strong>
            <p style="font-size: 8.5px; margin-top: 1mm;">Lencana tiket emas dengan sudut berlekuk &amp; filigree border.</p>
          </div>
        </div>

        <!-- Item 2: Magic Hat -->
        <div class="card" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_hat}" alt="Top Hat">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10.5px;">TOPI PESULAP BELUDRU</strong>
            <p style="font-size: 8.5px; margin-top: 1mm;">Topi pesulap beludru plum dengan pita emas berkilau.</p>
          </div>
        </div>

        <!-- Item 3: Lollipop -->
        <div class="card" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_lollipop}" alt="Swirl Lollipop">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10.5px;">PERMEN SPIRAL PASTEL</strong>
            <p style="font-size: 8.5px; margin-top: 1mm;">Lolipop spiral putar mint toska, pink, dan vanilla.</p>
          </div>
        </div>

        <!-- Item 4: Golden Cane -->
        <div class="card" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_cane}" alt="Golden Cane">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10.5px;">TONGKAT PESULAP MAHONI</strong>
            <p style="font-size: 8.5px; margin-top: 1mm;">Tongkat kayu mahoni dengan kenop bola emas murni.</p>
          </div>
        </div>

        <!-- Item 5: Bonbon Pink -->
        <div class="card" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_bonbon}" alt="Wrapped Bonbon">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10.5px;">PERMEN BONBON PINK</strong>
            <p style="font-size: 8.5px; margin-top: 1mm;">Permen bungkus satin pink dengan ikatan pita emas.</p>
          </div>
        </div>

        <!-- Item 6: Rose -->
        <div class="card" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_rose}" alt="Confectionery Rose">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10.5px;">MAWAR GULA KRISTAL</strong>
            <p style="font-size: 8.5px; margin-top: 1mm;">Kelopak mawar merah anggur manis &amp; daun toska.</p>
          </div>
        </div>

        <!-- Item 7: Glasses -->
        <div class="card" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_glasses}" alt="Whimsical Glasses">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10.5px;">KACAMATA EKSENTRIK</strong>
            <p style="font-size: 8.5px; margin-top: 1mm;">Bingkai bundar kuningan emas dengan lensa kilau.</p>
          </div>
        </div>

        <!-- Item 8: Stardust -->
        <div class="card" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_stardust}" alt="Stardust Stars">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10.5px;">BINTANG STARDUST EMAS</strong>
            <p style="font-size: 8.5px; margin-top: 1mm;">Gugusan bintang empat sudut retro berkilau keemasan.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 10</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 11: LATAR BELAKANG SINEMATIK ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 10 • LATAR BELAKANG</div>
        <div class="header-title">LATAR BELAKANG SINEMATIK RESMI (THEATRICAL BACKDROPS)</div>
      </div>
      <div class="header-meta">FEED (1:1) &amp; STORY (9:16) TEMPLATES</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="card">
          <div class="card-title cinzel">1. THEATRICAL PINWHEEL MINT &amp; VANILLA</div>
          <div class="img-box" style="height: 65mm; margin-bottom: 3mm;">
            <img src="{img_bg_pinwheel}" style="max-height: 60mm;" alt="Pinwheel Mint Background">
          </div>
          <p style="font-size: 10.5px; text-align: justify;">
            <strong>Konsep Visual:</strong> Mengadaptasi nuansa sinematik poster fantasi bernuansa kincir spiral toska mint pastel (<code>#A0D9CA</code>) dan krem vanilla hangat (<code>#FFF5D6</code>).
          </p>
          <div style="margin-top: auto; padding: 2.5mm; background: rgba(0,0,0,0.3); border-radius: 4px; font-size: 9.5px;">
            <strong>Peruntukan:</strong> Feed pengumuman gembira, poster festival kuliner kreasi siswa, dan kartu ucapan dies natalis ceria.
          </div>
        </div>

        <div class="card">
          <div class="card-title cinzel">2. IMPERIAL VELVET STARDUST NIGHT</div>
          <div class="img-box" style="height: 65mm; margin-bottom: 3mm;">
            <img src="{img_bg_velvet}" style="max-height: 60mm;" alt="Imperial Velvet Stardust">
          </div>
          <p style="font-size: 10.5px; text-align: justify;">
            <strong>Konsep Visual:</strong> Mengadaptasi poster teaser malam megah bernuansa ungu beludru pekat (<code>#360538</code>) dengan lengkungan taburan debu bintang emas bercahaya.
          </p>
          <div style="margin-top: auto; padding: 2.5mm; background: rgba(0,0,0,0.3); border-radius: 4px; font-size: 9.5px;">
            <strong>Peruntukan:</strong> Malam puncak inagurasi, backdrop panggung gala dinner, sampul proposal sponsorship, dan plakat resmi.
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 11</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 12: IMPLEMENTASI CENDERA MATA ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 11 • APLIKASI PRODUK</div>
        <div class="header-title">APLIKASI IDENTITAS PADA CENDERA MATA &amp; MERCHANDISE RESMI</div>
      </div>
      <div class="header-meta">OFFICIAL MERCHANDISE SUITE</div>
    </div>

    <div class="content-area">
      <div class="grid-4" style="height: 100%;">
        <!-- Mockup 1: Polo -->
        <div class="card">
          <div class="img-box" style="height: 52mm;">
            <img src="{img_mockup_polo}" alt="Kaos Polo">
          </div>
          <div style="margin-top: 2.5mm;">
            <span class="badge" style="background:#4A1255;">SERAGAM PANITIA</span>
            <div class="card-title" style="font-size: 11px; margin-top: 1mm;">KAOS POLO &amp; T-SHIRT</div>
            <p style="font-size: 9px;">Bordir komputer benang rayon emas diameter 65 mm di dada kiri. Bahan Lacoste Cotton Pique hitam.</p>
          </div>
        </div>

        <!-- Mockup 2: Tumbler -->
        <div class="card">
          <div class="img-box" style="height: 52mm;">
            <img src="{img_mockup_tumbler}" alt="Tumbler Termal">
          </div>
          <div style="margin-top: 2.5mm;">
            <span class="badge" style="background:#B6580B;">CENDERA MATA VIP</span>
            <div class="card-title" style="font-size: 11px; margin-top: 1mm;">TUMBLER STAINLESS</div>
            <p style="font-size: 9px;">Double-wall stainless 304 finishing matte plum dengan grafir laser serat line-cut tinggi 80 mm.</p>
          </div>
        </div>

        <!-- Mockup 3: Lanyard -->
        <div class="card">
          <div class="img-box" style="height: 52mm;">
            <img src="{img_mockup_lanyard}" alt="Lanyard ID Card">
          </div>
          <div style="margin-top: 2.5mm;">
            <span class="badge" style="background:#5C186B;">ATRIBUT PANITIA</span>
            <div class="card-title" style="font-size: 11px; margin-top: 1mm;">LANYARD &amp; ID CARD</div>
            <p style="font-size: 9px;">Pita satin kilap 20 mm Midnight Plum bolak-balik. Kartu PVC 0,8 mm laminasi dof standar ISO.</p>
          </div>
        </div>

        <!-- Mockup 4: Tote Bag & Pin -->
        <div class="card">
          <div class="img-box" style="height: 52mm;">
            <img src="{img_mockup_totebag}" alt="Tote Bag & Pin">
          </div>
          <div style="margin-top: 2.5mm;">
            <span class="badge" style="background:#E09D17; color:#310603;">PAKET ALUMNI</span>
            <div class="card-title" style="font-size: 11px; margin-top: 1mm;">TOTE BAG &amp; ENAMEL PIN</div>
            <p style="font-size: 9px;">Kanvas katun organik 14 oz natural white dengan pin logam sepuhan emas 24K die-struck.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 12</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 13: ATURAN LARANGAN (DO'S & DON'TS) ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 12 • PANDUAN KEPATUHAN</div>
        <div class="header-title">ATURAN PENGGUNAAN &amp; LARANGAN FATAL (DO'S &amp; DON'TS)</div>
      </div>
      <div class="header-meta">BRAND COMPLIANCE RULES</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="card" style="border: 1.5px solid #EF4444; background: rgba(77, 10, 10, 0.35);">
          <div class="card-title" style="color: #FCA5A5; font-size: 13px;">❌ ENAM LARANGAN FATAL (DON'TS)</div>
          <div style="display: flex; flex-direction: column; gap: 2.5mm; margin-top: 2mm;">
            <div style="font-size: 10.5px;">
              <strong>1. Dilarang Menarik Proporsi (Stretch / Squash):</strong><br>
              Menarik lambang secara horizontal atau vertikal merusak keharmonisan geometris busur lingkaran.
            </div>
            <div style="font-size: 10.5px;">
              <strong>2. Dilarang Mengubah Arah Hadap / Memutar Lambang:</strong><br>
              Paruh rajawali dan akselerasi sayap wajib selalu menghadap ke arah kanan atas (masa depan).
            </div>
            <div style="font-size: 10.5px;">
              <strong>3. Dilarang Mengganti Urutan Gradasi Warna Faset:</strong><br>
              Seluruh faset emas wajib mematuhi sistem gradasi 8 warna resmi Coolors.
            </div>
            <div style="font-size: 10.5px;">
              <strong>4. Dilarang Menambahkan Efek Bayangan Kasar (Heavy Shadow):</strong><br>
              Drop shadow hitam pekat yang tidak natural akan mengaburkan garis batas faset.
            </div>
            <div style="font-size: 10.5px;">
              <strong>5. Dilarang Menaruh di Atas Latar Tabrakan:</strong><br>
              Hindari menaruh logo warna di atas warna merah menyala, hijau stabilo, atau corak ramai.
            </div>
            <div style="font-size: 10.5px;">
              <strong>6. Dilarang Menggunakan Font Komikal / Tidak Resmi:</strong><br>
              Dilarang memakai font dekoratif sembarangan seperti Comic Sans, Papyrus, atau Brush Script.
            </div>
          </div>
        </div>

        <div class="card" style="border: 1.5px solid #10B981; background: rgba(6, 78, 59, 0.35);">
          <div class="card-title" style="color: #6EE7B7; font-size: 13px;">✅ PANDUAN PENGGUNAAN BENAR (DO'S)</div>
          <div style="display: flex; flex-direction: column; gap: 2.5mm; margin-top: 2mm;">
            <div style="font-size: 10.5px;">
              <strong>1. Selalu Gunakan Berkas Vektor SVG untuk Cetak:</strong><br>
              Gunakan berkas di direktori <code>assets/svg/</code> untuk pencetakan spanduk, banner, atau kaos agar tidak pecah.
            </div>
            <div style="font-size: 10.5px;">
              <strong>2. Terapkan Monokrom Putih di Atas Foto Gelap:</strong><br>
              Gunakan varian <code>logo-monochrome-white.svg</code> bila diletakkan di atas dokumentasi foto kegiatan sekolah.
            </div>
            <div style="font-size: 10.5px;">
              <strong>3. Jaga Area Aman (Clear Space) Sebesar 1/4 Tinggi:</strong><br>
              Pastikan selalu ada ruang bernapas yang cukup di sekeliling lambang tanpa gangguan ornamen.
            </div>
            <div style="font-size: 10.5px;">
              <strong>4. Gunakan Font Plus Jakarta Sans &amp; Cinzel:</strong><br>
              Patuhi hierarki tipografi resmi almamater untuk menjaga konsistensi publikasi.
            </div>
            <div style="font-size: 10.5px;">
              <strong>5. Terapkan Latar Belakang Resmi:</strong><br>
              Manfaatkan template feed &amp; story resmi (Pinwheel Mint &amp; Velvet Stardust) untuk publikasi medsos.
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 13</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 14: HAK CIPTA, LEGALITAS & PENUTUP ==================== -->
  <div class="page" style="justify-content: space-between;">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 13 • LEGALITAS &amp; ATRIBUSI</div>
        <div class="header-title">HAK CIPTA, STATUS LISENSI &amp; TANDA PENGESAHAN (COLOPHON)</div>
      </div>
      <div class="header-meta">LEGAL NOTICE &amp; SPECIFICATIONS</div>
    </div>

    <div class="content-area">
      <div class="grid-2" style="margin-bottom: 4mm;">
        <div class="card">
          <div class="card-title cinzel">PERNYATAAN HAK CIPTA EKSKLUSIF</div>
          <p style="text-align: justify; font-size: 10.5px;">
            Seluruh lambang, gambar vektor, skrip komputasi algoritma, tata letak lockup, dokumen pedoman identitas visual, serta materi pendukung Dies Natalis ke-44 ini dilindungi oleh Undang-Undang Hak Cipta Republik Indonesia (UU No. 28 Tahun 2014).
          </p>
          <div style="margin-top: 3mm; padding: 3mm; background: rgba(245, 197, 56, 0.08); border-left: 3px solid #F5C538; border-radius: 4px; font-size: 10px;">
            <strong style="color: #FFEAA0;">Status Kepemilikan &amp; Lisensi:</strong><br>
            <strong>PROPRIETARY / ALL RIGHTS RESERVED (LISENSI TERTUTUP EKSKLUSIF)</strong><br>
            Hak kekayaan intelektual sepenuhnya dimiliki secara bersama oleh <strong>SMA Negeri 1 Gedeg</strong> dan <strong>Ryan Ardian</strong>. Dilarang keras menyalin, memperbanyak, memperjualbelikan, atau memanfaatkan materi ini untuk kepentingan komersial pihak ketiga tanpa persetujuan tertulis resmi.
          </div>
        </div>

        <div class="card">
          <div class="card-title cinzel">ATRIBUSI KARYA &amp; SPESIFIKASI TEKNIS</div>
          <table>
            <tbody>
              <tr>
                <td><strong>Institusi Almamater</strong></td>
                <td>SMA Negeri 1 Gedeg (Kab. Mojokerto, Jawa Timur)</td>
              </tr>
              <tr>
                <td><strong>Perancang / Desainer</strong></td>
                <td><strong>Ryan Ardian</strong> (Guru SMAN 1 Gedeg)</td>
              </tr>
              <tr>
                <td><strong>Masa Dies Natalis</strong></td>
                <td>1982 – 2026 (Genap 44 Tahun Pengabdian)</td>
              </tr>
              <tr>
                <td><strong>Tema Resmi</strong></td>
                <td><strong>AVERSA</strong> (Berkembang, Visi, Solidaritas, Tindakan)</td>
              </tr>
              <tr>
                <td><strong>Versi Master Lambang</strong></td>
                <td>Versi V6 Final (Symmetrical Medial Spine &amp; 3D Facets)</td>
              </tr>
              <tr>
                <td><strong>Format Berkas Tersedia</strong></td>
                <td>SVG Vektor W3C, PNG Ultra-HD 2048px, PDF Cetak A4</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Signatures Box -->
      <div class="card" style="padding: 4mm; background: #200526;">
        <div style="display: flex; justify-content: space-around; text-align: center; font-size: 10.5px;">
          <div>
            <span style="color: #D4B8DE;">Mengetahui,</span><br>
            <strong style="color: #FFEAA0;">Kepala SMA Negeri 1 Gedeg</strong><br>
            <div style="height: 18mm;"></div>
            <strong style="text-decoration: underline; color: #FFFFFF;">...................................................</strong><br>
            <span style="font-size: 9px; color: #A891B0;">NIP. ...................................................</span>
          </div>

          <div>
            <span style="color: #D4B8DE;">Disusun Oleh,</span><br>
            <strong style="color: #FFEAA0;">Guru Pengampu / Desainer Lambang</strong><br>
            <div style="height: 18mm;"></div>
            <strong style="text-decoration: underline; color: #FFFFFF;">RYAN ARDIAN</strong><br>
            <span style="font-size: 9px; color: #F5C538;">SMA Negeri 1 Gedeg</span>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 14 (SELESAI)</div>
    </div>
  </div>

</body>
</html>
"""
    return html

def render_html_to_pdf(html_path: Path, pdf_path: Path):
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_path.resolve()}",
        f"file://{html_path.resolve()}"
    ]
    subprocess.run(cmd, check=True)
    print(f"Generated PDF: {pdf_path}")

def main():
    print("=== BUILDING DIES NATALIS 44 BRAND GUIDELINES BOOK (PDF) ===")
    html_content = build_html()
    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(html_content, encoding="utf-8")
    print(f"Saved HTML Book: {HTML_OUT}")

    render_html_to_pdf(HTML_OUT, PDF_OUT)

    if PDF_OUT.exists():
        size_mb = PDF_OUT.stat().st_size / (1024 * 1024)
        print(f"PDF Output Ready: {PDF_OUT} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
