#!/usr/bin/env python3
"""
build_brand_guidelines_pdf.py
Membangun Buku Pedoman Identitas Visual & Logo Guideline (Brand Book) resmi
Dies Natalis ke-44 SMAN 1 Gedeg (1982-2026) dengan standar editorial tinggi (Bolt Decks / Anti-Slop).

Audit Anti-Slop yang Diterapkan:
1. Menghilangkan kartu ungu generik yang seragam di semua halaman.
2. Menerapkan variasi ritme tata letak (asymmetric balance, editorial whitespace, split-screen, visual specimen).
3. Membersihkan copy dari AI-slop pompous buzzwords; menggunakan kalimat lugas, otoritatif, dan presisi.
4. Menerapkan palet warna Obsidian & Emas yang solid dengan kontras tinggi, menghindari efek blur/glassmorphism berlebihan.
5. Menampilkan spesimen tipografi nyata (specimen sheet) dan tabel spesifikasi cetak/digital konkret.
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
    img_logo_color = get_base64_img("assets/png/logo-color-2048.png")
    img_logo_linecut = get_base64_img("assets/png/logo-linecut-black.png")
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
      color: #F3ECF6;
      background: #09020C;
      font-size: 12px;
      line-height: 1.55;
    }}
    .cinzel {{
      font-family: 'Cinzel', Georgia, serif;
    }}
    .playfair {{
      font-family: 'Playfair Display', Georgia, serif;
    }}
    
    /* Page Container */
    .page {{
      width: 297mm;
      height: 210mm;
      position: relative;
      overflow: hidden;
      page-break-after: always;
      display: flex;
      flex-direction: column;
      background: #110314;
      padding: 14mm 18mm;
    }}
    
    /* Top Header Strip */
    .page-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 1px solid rgba(245, 197, 56, 0.35);
      padding-bottom: 3.5mm;
      margin-bottom: 5.5mm;
    }}
    .header-tagline {{
      font-size: 9px;
      letter-spacing: 2.5px;
      color: #E09D17;
      font-weight: 700;
      text-transform: uppercase;
    }}
    .header-title {{
      font-size: 19px;
      font-weight: 800;
      color: #FFFFFF;
      letter-spacing: 0.3px;
    }}
    .header-meta {{
      text-align: right;
      font-size: 8.5px;
      color: #A38CAE;
      letter-spacing: 1.2px;
      font-weight: 600;
    }}
    
    /* Bottom Footer Strip */
    .page-footer {{
      position: absolute;
      bottom: 7mm;
      left: 18mm;
      right: 18mm;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      padding-top: 2.5mm;
      font-size: 8.5px;
      color: #7D6B84;
    }}
    .page-num {{
      font-weight: 800;
      color: #F5C538;
      font-size: 9.5px;
      letter-spacing: 1px;
    }}
    
    /* Layout Primitives */
    .content-area {{
      flex: 1;
      display: flex;
      flex-direction: column;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 5mm;
      height: 100%;
    }}
    .grid-3 {{
      display: grid;
      grid-template-columns: 1fr 1fr 1fr;
      gap: 4.5mm;
      height: 100%;
    }}
    .grid-4 {{
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 4mm;
      height: 100%;
    }}
    
    /* Panels (Clean, Solid, Anti-Slop Surfaces) */
    .panel {{
      background: #19051E;
      border: 1px solid rgba(245, 197, 56, 0.2);
      border-radius: 6px;
      padding: 4.5mm;
      display: flex;
      flex-direction: column;
    }}
    .panel.darker {{
      background: #0E0211;
      border-color: rgba(255, 255, 255, 0.08);
    }}
    .panel.highlight {{
      background: #200627;
      border-color: #E09D17;
    }}
    .panel-header {{
      font-size: 12px;
      font-weight: 800;
      color: #FFEAA0;
      margin-bottom: 2mm;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    
    /* Labels & Badges */
    .badge {{
      display: inline-block;
      padding: 1.5px 6px;
      border-radius: 3px;
      font-size: 8px;
      font-weight: 800;
      letter-spacing: 0.8px;
      background: #3A0C44;
      color: #FFEAA0;
      border: 1px solid #E09D17;
      text-transform: uppercase;
    }}
    
    /* Typography Utilities */
    h1, h2, h3, h4 {{
      color: #FFFFFF;
    }}
    p {{
      color: #D8C7DE;
      margin-bottom: 2mm;
    }}
    strong {{
      color: #FFFFFF;
    }}
    
    /* Media Boxes */
    .img-box {{
      background: #09010C;
      border: 1px solid rgba(255, 255, 255, 0.08);
      border-radius: 4px;
      display: flex;
      justify-content: center;
      align-items: center;
      overflow: hidden;
      padding: 2.5mm;
    }}
    .img-box img {{
      max-width: 100%;
      max-height: 100%;
      object-fit: contain;
    }}
    .img-box.light {{
      background: #FAF8F5;
      border-color: #E5E0D8;
    }}
    
    /* Numbered Callout Rows */
    .callout-row {{
      display: flex;
      gap: 10px;
      margin-bottom: 2.5mm;
      align-items: flex-start;
    }}
    .callout-idx {{
      font-family: 'Cinzel', serif;
      font-size: 15px;
      font-weight: 800;
      color: #F5C538;
      min-width: 28px;
      line-height: 1;
    }}
    .callout-body {{
      flex: 1;
    }}
    .callout-title {{
      font-size: 11px;
      font-weight: 800;
      color: #FFEAA0;
      margin-bottom: 0.5mm;
    }}
    .callout-desc {{
      font-size: 9.5px;
      color: #CDBAD3;
      margin: 0;
    }}
    
    /* Table Styling */
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 9.5px;
      margin-top: 1.5mm;
    }}
    th {{
      background: #2E0B37;
      color: #FFEAA0;
      text-align: left;
      padding: 4px 6px;
      font-weight: 800;
      letter-spacing: 0.3px;
      border-bottom: 1.5px solid #F5C538;
    }}
    td {{
      padding: 3.5px 6px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.06);
      color: #D2BFD7;
    }}
    tr:nth-child(even) td {{
      background: rgba(255, 255, 255, 0.015);
    }}
    
    /* COVER PAGE EDITORIAL LUXURY */
    .cover-page {{
      background: radial-gradient(circle at 50% 45%, #2D052F 0%, #160218 55%, #080009 100%);
      padding: 18mm 20mm;
      justify-content: space-between;
      align-items: center;
      text-align: center;
    }}
    .cover-badge {{
      display: inline-block;
      padding: 2.5mm 7mm;
      border-radius: 16px;
      background: rgba(245, 197, 56, 0.1);
      border: 1px solid #F5C538;
      color: #FFEAA0;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: 2.5px;
      margin-bottom: 3mm;
    }}
    .cover-title {{
      font-size: 30px;
      font-weight: 900;
      letter-spacing: 1px;
      color: #FFFFFF;
      text-transform: uppercase;
      line-height: 1.2;
      margin-bottom: 2mm;
    }}
    .cover-subtitle {{
      font-size: 16px;
      font-weight: 700;
      color: #F7D160;
      letter-spacing: 1.5px;
      margin-bottom: 3mm;
    }}
    .cover-theme {{
      font-size: 24px;
      font-weight: 900;
      color: #FFFFFF;
      letter-spacing: 5px;
    }}
    .cover-footer {{
      border-top: 1px solid rgba(245, 197, 56, 0.3);
      padding-top: 4mm;
      width: 100%;
      display: flex;
      justify-content: space-between;
      font-size: 9.5px;
      color: #B29AB9;
    }}
  </style>
</head>
<body>

  <!-- ==================== HALAMAN 1: COVER ==================== -->
  <div class="page cover-page">
    <div style="width: 100%; text-align: center;">
      <div class="cover-badge cinzel">DOKUMEN RESMI IDENTITAS VISUAL</div>
      <div class="cover-title">BUKU PEDOMAN IDENTITAS VISUAL &amp; LOGO GUIDELINE</div>
      <div class="cover-subtitle cinzel">DIES NATALIS KE-44 SMA NEGERI 1 GEDEG (1982–2026)</div>
      <div class="cover-theme playfair">TEMA BESAR: AVERSA</div>
    </div>
    
    <div style="margin: 6mm 0;">
      <img src="{img_logo_color}" style="width: 65mm; height: auto; filter: drop-shadow(0 12px 28px rgba(245, 197, 56, 0.3));" alt="Logo Dies Natalis 44 Master V6">
    </div>

    <div class="cover-footer">
      <div>
        <strong style="color: #F7D160;">SMA NEGERI 1 GEDEG</strong><br>
        Kabupaten Mojokerto, Jawa Timur
      </div>
      <div style="text-align: center;">
        <span class="cinzel" style="color: #FFFFFF; font-weight: 700; letter-spacing: 1.5px;">STANDAR MASTER V6 FINAL</span><br>
        Perancang: <strong>Ryan Ardian</strong> (Guru SMAN 1 Gedeg)
      </div>
      <div style="text-align: right;">
        <strong style="color: #F5C538;">HAK CIPTA TERTUTUP</strong><br>
        Proprietary / All Rights Reserved
      </div>
    </div>
  </div>


  <!-- ==================== HALAMAN 2: PENDAHULUAN & SEJARAH ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 1 • KONTEKS &amp; PRINSIP</div>
        <div class="header-title">44 TAHUN PENGABDIAN &amp; LANDASAN PEDOMAN IDENTITAS</div>
      </div>
      <div class="header-meta">SMAN 1 GEDEG • 1982–2026</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="panel">
          <div class="panel-header cinzel">PERJALANAN 44 TAHUN ALMAMATER</div>
          <p style="text-align: justify; margin-bottom: 3mm;">
            Didirikan pada tahun <strong>1982</strong> di Kabupaten Mojokerto, SMA Negeri 1 Gedeg telah melewati 44 tahun perjalanan mendidik insan berprestasi dan berkarakter luhur. Peringatan Dies Natalis ke-44 pada tahun <strong>2026</strong> menegaskan kedewasaan almamater dalam memadukan keteguhan budi pekerti dengan kesiapan menyongsong abad ke-21.
          </p>
          <p style="text-align: justify; margin-bottom: 3mm;">
            Identitas visual Dies Natalis ke-44 ini dirancang untuk mencerminkan wibawa akademis, rasa percaya diri, dan energi dinamis seluruh civitas akademika dalam satu kesatuan sistem lambang yang kokoh.
          </p>
          <div style="margin-top: auto; padding: 3mm; background: rgba(0,0,0,0.3); border-left: 3px solid #E09D17; border-radius: 4px;">
            <strong style="color: #FFEAA0;">Nilai Utama SMAN 1 Gedeg:</strong><br>
            <span style="font-size: 10px; color: #D2BFD7;">Berakhlak Mulia, Unggul Akademik &amp; Vokasional, Berbudaya Lingkungan, dan Berwawasan Kebangsaan.</span>
          </div>
        </div>

        <div class="panel darker">
          <div class="panel-header cinzel">TIGA PRINSIP PENGGUNAAN IDENTITAS</div>
          <p style="text-align: justify; margin-bottom: 3.5mm;">
            Buku pedoman ini wajib dirujuk oleh seluruh panitia, perancang grafis, dan mitra vendor pengadaan atribut sekolah:
          </p>
          
          <div class="callout-row">
            <div class="callout-idx">01</div>
            <div class="callout-body">
              <div class="callout-title">KONSISTENSI INTEGRAL</div>
              <p class="callout-desc">Menjaga ketepatan warna, rasio proporsi, dan tipografi di seluruh media cetak, kain seragam, suvenir logam, dan platform digital.</p>
            </div>
          </div>

          <div class="callout-row">
            <div class="callout-idx">02</div>
            <div class="callout-body">
              <div class="callout-title">PRESTISE AKADEMIK</div>
              <p class="callout-desc">Menghindari distorsi, modifikasi sepihak, atau penambahan efek visual berlebih yang menurunkan martabat almamater.</p>
            </div>
          </div>

          <div class="callout-row">
            <div class="callout-idx">03</div>
            <div class="callout-body">
              <div class="callout-title">EFISIENSI PRODUKSI</div>
              <p class="callout-desc">Menggunakan berkas vektor master (SVG) dan raster beresolusi tinggi (PNG 2048px) agar hasil sablon, bordir, dan grafir tajam dan presisi.</p>
            </div>
          </div>

          <div style="margin-top: auto; padding: 2mm; background: rgba(245, 197, 56, 0.08); border-radius: 4px; text-align: center; border: 1px dashed rgba(245, 197, 56, 0.3);">
            <span style="font-size: 9px; color: #F7D160; font-weight: 700;">DIVERIFIKASI DENGAN STANDAR KOMPUTASIONAL VEKTOR PYTHON V6 FINAL</span>
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
        <div class="header-tagline cinzel">BAB 2 • ANATOMI LAMBANG</div>
        <div class="header-title">ANATOMI TEKNIS &amp; FILOSOFI LAMBANG UTAMA 44 (MASTER V6)</div>
      </div>
      <div class="header-meta">EMBLEM ANATOMY &amp; PHILOSOPHY</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="panel darker" style="align-items: center; justify-content: center; padding: 3mm;">
          <div class="img-box" style="width: 100%; height: 112mm; background: transparent; border: none;">
            <img src="{img_logo_color}" style="max-height: 100mm;" alt="Anatomi Logo 44">
          </div>
          <div style="font-size: 9.5px; color: #F7D160; text-align: center; margin-top: 1mm;">
            <strong>KONSTRUKSI FASET SIMETRIS BUSUR KONSENTRIS MASTER V6</strong>
          </div>
        </div>

        <div class="panel" style="justify-content: space-between;">
          <div>
            <div class="panel-header cinzel">LIMA UNSUR STRUKTURAL LAMBANG</div>
            
            <div class="callout-row">
              <div class="callout-idx">1</div>
              <div class="callout-body">
                <div class="callout-title">STILASI ANGKA KEMBAR "44"</div>
                <p class="callout-desc">Angka 4 pertama sebagai pilar fondasi historis; angka 4 kedua sebagai pilar akselerasi masa depan 44 tahun almamater.</p>
              </div>
            </div>

            <div class="callout-row">
              <div class="callout-idx">2</div>
              <div class="callout-body">
                <div class="callout-title">TATAPAN RAJAWALI VISIONER</div>
                <p class="callout-desc">Siluet kepala rajawali menatap ke arah kanan atas melambangkan ketajaman intelektual, integritas, dan keberanian moral.</p>
              </div>
            </div>

            <div class="callout-row">
              <div class="callout-idx">3</div>
              <div class="callout-body">
                <div class="callout-title">KOBARAN LIDAH API ABADI</div>
                <p class="callout-desc">Tiga sulur api menjulang melambangkan semangat belajar pantang padam, resiliensi tinggi, dan kreativitas tiada henti.</p>
              </div>
            </div>

            <div class="callout-row">
              <div class="callout-idx">4</div>
              <div class="callout-body">
                <div class="callout-title">AKSELERASI SAYAP AERODINAMIS</div>
                <p class="callout-desc">Garis aerodinamis sayap menyapu ke kuadran atas melambangkan akselerasi prestasi siswa menuju era keemasan almamater.</p>
              </div>
            </div>

            <div class="callout-row">
              <div class="callout-idx">5</div>
              <div class="callout-body">
                <div class="callout-title">MEDIAL SPINE SIMETRIS (V6)</div>
                <p class="callout-desc">Tulang punggung faset trimatra tengah disempurnakan dengan busur konsentris matematis untuk menghasilkan kedalaman 3D yang stabil.</p>
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
        <div class="header-tagline cinzel">BAB 3 • TEMA BESAR DIES NATALIS</div>
        <div class="header-title">LOGOTYPE RESMI &amp; EMPAT PILAR FILOSOFI "AVERSA"</div>
      </div>
      <div class="header-meta">THE AVERSA DOCTRINE</div>
    </div>

    <div class="content-area">
      <!-- Wordmark Box -->
      <div class="panel" style="margin-bottom: 4mm; padding: 3mm; align-items: center; background: #1C0521;">
        <div class="img-box" style="width: 100%; height: 36mm; background: transparent; border: none;">
          <img src="{img_aversa_wordmark}" style="max-height: 33mm;" alt="Wordmark Aversa">
        </div>
        <div style="font-size: 9.5px; color: #F7D160; margin-top: 1mm; font-weight: 700; letter-spacing: 1.5px;">
          REKONSTRUKSI KURVA BEZIER C1 BERGRADASI PALET EMAS CAIR DARI SKETSA ASLI
        </div>
      </div>

      <!-- 4 Pillars Grid -->
      <div class="grid-4" style="flex: 1;">
        <div class="panel" style="border-top: 3px solid #E09D17;">
          <div class="callout-idx" style="font-size: 16px;">01</div>
          <div class="callout-title" style="font-size: 11px; margin-top: 1mm;">SEMANGAT TERUS BERKEMBANG</div>
          <p style="font-size: 10px; text-align: justify; margin-top: 1.5mm;">
            Melambangkan tekad kuat civitas akademika untuk terus mengasah potensi diri, memperluas wawasan keilmuan, dan bertumbuh secara dinamis menghadapi tantangan zaman.
          </p>
        </div>

        <div class="panel" style="border-top: 3px solid #F5C538;">
          <div class="callout-idx" style="font-size: 16px;">02</div>
          <div class="callout-title" style="font-size: 11px; margin-top: 1mm;">MEMILIKI VISI YANG JELAS</div>
          <p style="font-size: 10px; text-align: justify; margin-top: 1.5mm;">
            Arah kompas masa depan yang terukur dan berorientasi pada capaian prestasi akademik serta akhlak mulia, selaras dengan tatapan rajawali ke ufuk masa depan.
          </p>
        </div>

        <div class="panel" style="border-top: 3px solid #F7D160;">
          <div class="callout-idx" style="font-size: 16px;">03</div>
          <div class="callout-title" style="font-size: 11px; margin-top: 1mm;">MEMBANGUN SOLIDARITAS</div>
          <p style="font-size: 10px; text-align: justify; margin-top: 1.5mm;">
            Ikatan persaudaraan yang kokoh, inklusif, dan saling menguatkan antar-siswa, pendidik, tenaga kependidikan, alumni, dan orang tua dalam keluarga besar SMAN 1 Gedeg.
          </p>
        </div>

        <div class="panel" style="border-top: 3px solid #FDF39D;">
          <div class="callout-idx" style="font-size: 16px;">04</div>
          <div class="callout-title" style="font-size: 11px; margin-top: 1mm;">TINDAKAN NYATA &amp; PERUBAHAN</div>
          <p style="font-size: 10px; text-align: justify; margin-top: 1.5mm;">
            Ketegasan sikap untuk tidak berhenti pada wacana, melainkan berani mengambil tindakan nyata, melahirkan karya inovatif, dan mewujudkan perubahan yang bermanfaat.
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
        <div class="header-tagline cinzel">BAB 4 • VARIAN LAMBANG</div>
        <div class="header-title">KOLEKSI EMPAT VARIAN LOGO RESMI (THE MASTER 44 SUITE)</div>
      </div>
      <div class="header-meta">REPRESENTATIONAL MATRIX</div>
    </div>

    <div class="content-area">
      <div class="grid-4" style="height: 100%;">
        <!-- Varian 1 -->
        <div class="panel">
          <div class="img-box" style="height: 52mm; background: #0E0211;">
            <img src="{img_logo_color}" alt="Master Color">
          </div>
          <div style="margin-top: 2.5mm;">
            <span class="badge" style="background:#B6580B;">MASTER COLOR V6</span>
            <div class="callout-title" style="margin-top: 1.5mm;">WARNA PENUH UTAMA</div>
            <p style="font-size: 9px;">Gradasi emas faset lengkap. Digunakan untuk spanduk panggung, media sosial, publikasi digital, buku kenangan.</p>
          </div>
        </div>

        <!-- Varian 2 -->
        <div class="panel">
          <div class="img-box light" style="height: 52mm;">
            <img src="{img_logo_linecut}" alt="Linecut Black">
          </div>
          <div style="margin-top: 2.5mm;">
            <span class="badge" style="background:#334155;">LINE-CUT GRAFIR</span>
            <div class="callout-title" style="margin-top: 1.5mm; color:#FFEAA0;">GARIS KONTUR PRESISI</div>
            <p style="font-size: 9px;">Garis kontur rambut hitam presisi untuk grafir laser tumbler, cap stempel dinas, dan bordir benang.</p>
          </div>
        </div>

        <!-- Varian 3 -->
        <div class="panel">
          <div class="img-box" style="height: 52mm; background: #000000;">
            <img src="{img_logo_mono_white}" alt="Monochrome White">
          </div>
          <div style="margin-top: 2.5mm;">
            <span class="badge" style="background:#4A1255;">MONOKROM PUTIH</span>
            <div class="callout-title" style="margin-top: 1.5mm;">INVERTED HIGH CONTRAST</div>
            <p style="font-size: 9px;">Siluet putih murni untuk penempatan di atas latar belakang foto dokumentasi, video bumper, kain hitam.</p>
          </div>
        </div>

        <!-- Varian 4 -->
        <div class="panel">
          <div class="img-box light" style="height: 52mm;">
            <img src="{img_logo_grid}" alt="Logo with Grid">
          </div>
          <div style="margin-top: 2.5mm;">
            <span class="badge" style="background:#1E3A8A;">BLUEPRINT GRID</span>
            <div class="callout-title" style="margin-top: 1.5mm; color:#FFEAA0;">KISI GEOMETRIS BUSUR</div>
            <p style="font-size: 9px;">Pedoman konstruksi rasio busur lingkaran konsentris dan proporsi matematis kurva sayap almamater.</p>
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
        <div class="header-title">SISTEM SUSUNAN LOCKUP RESMI (HORIZONTAL &amp; VERTICAL)</div>
      </div>
      <div class="header-meta">CO-BRANDING &amp; LOCKUP ARCHITECTURE</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="panel">
          <div class="panel-header cinzel">1. LOCKUP IDENTITAS INSTITUSI</div>
          <div class="img-box" style="height: 44mm; margin-bottom: 2mm; background: #130418;">
            <img src="{img_logo_horizontal}" style="max-height: 38mm;" alt="Horizontal Lockup">
          </div>
          <p style="font-size: 9.5px; margin-bottom: 2.5mm;">
            <strong>Horizontal Lockup:</strong> Simbol di sisi kiri dan identitas SMAN 1 Gedeg di sisi kanan. Digunakan untuk spanduk jalan, kop surat dinas, website, dan merchandise memanjang.
          </p>
          <div class="img-box" style="height: 42mm; background: #130418;">
            <img src="{img_logo_vertical}" style="max-height: 38mm;" alt="Vertical Lockup">
          </div>
          <p style="font-size: 9.5px; margin-top: 2mm;">
            <strong>Vertical Lockup:</strong> Susunan sentral bertingkat untuk sampul buku panduan, poster seremonial, plakat penghargaan, dan baliho vertikal.
          </p>
        </div>

        <div class="panel">
          <div class="panel-header cinzel">2. INTEGRASI DENGAN TEMA AVERSA</div>
          <div class="img-box" style="height: 44mm; margin-bottom: 2mm; background: #130418;">
            <img src="{img_aversa_horizontal}" style="max-height: 38mm;" alt="Aversa Horizontal">
          </div>
          <p style="font-size: 9.5px; margin-bottom: 2.5mm;">
            <strong>AVERSA Logotype Horizontal:</strong> Wordmark AVERSA berdampingan dengan identitas institusi untuk spanduk panggung pentas seni dan promosi media sosial.
          </p>
          <div class="img-box" style="height: 42mm; background: #130418;">
            <img src="{img_aversa_combo}" style="max-height: 38mm;" alt="Aversa Combination">
          </div>
          <p style="font-size: 9.5px; margin-top: 2mm;">
            <strong>Brand Combination Lockup:</strong> Puncak hierarki gabungan Simbol Rajawali V6 + Wordmark AVERSA + Teks SMAN 1 Gedeg untuk publikasi resmi utama.
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
      <div class="header-meta">STANDAR KROMATIK RESMI (PENGGANTI COOLORS.JPEG)</div>
    </div>

    <div class="content-area">
      <div class="panel darker" style="padding: 2mm; margin-bottom: 3.5mm;">
        <div class="img-box" style="height: 60mm; background: transparent; border: none;">
          <img src="{img_palette_guide}" style="max-height: 59mm; width: 100%; object-fit: contain;" alt="Brand Color Palette Guide">
        </div>
      </div>

      <div class="panel" style="flex: 1; padding: 2.5mm;">
        <div class="panel-header cinzel" style="font-size: 10.5px;">TABEL NILAI KROMATIK 8 WARNA UTAMA ALMAMATER</div>
        <table>
          <thead>
            <tr>
              <th>No</th>
              <th>Nama Resmi Warna</th>
              <th>HEX</th>
              <th>RGB</th>
              <th>CMYK</th>
              <th>HSL</th>
              <th>Peran Faset &amp; Penggunaan Teknis</th>
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
              <td>Batas kontur terdalam, bayangan faset 3D, teks gelap kontras tinggi</td>
            </tr>
            <tr>
              <td><strong>#2</strong></td>
              <td><strong>Deep Crimson Rust</strong></td>
              <td><code>#7D1B05</code></td>
              <td>125, 27, 5</td>
              <td>24, 96, 100, 27</td>
              <td>11°, 92%, 25%</td>
              <td>Pangkal lidah api berkobar, bayangan kedalaman faset hangat</td>
            </tr>
            <tr>
              <td><strong>#3</strong></td>
              <td><strong>Rich Amber Bronze</strong></td>
              <td><code>#B6580B</code></td>
              <td>182, 88, 11</td>
              <td>18, 73, 100, 7</td>
              <td>27°, 89%, 38%</td>
              <td>Transisi lipatan pita keemasan dan bayangan hangat</td>
            </tr>
            <tr>
              <td><strong>#4</strong></td>
              <td><strong>Marigold Warm Gold</strong></td>
              <td><code>#E09D17</code></td>
              <td>224, 157, 23</td>
              <td>9, 39, 99, 0</td>
              <td>40°, 81%, 48%</td>
              <td>Warna tubuh utama angka 44 &amp; sayap almamater</td>
            </tr>
            <tr>
              <td><strong>#5</strong></td>
              <td><strong>Vivid Royal Gold</strong></td>
              <td><code>#F5C538</code></td>
              <td>245, 197, 56</td>
              <td>3, 21, 84, 0</td>
              <td>45°, 90%, 59%</td>
              <td>Tulang punggung tengah (Medial Spine) &amp; pendaran utama</td>
            </tr>
            <tr>
              <td><strong>#6</strong></td>
              <td><strong>Champagne Highlight</strong></td>
              <td><code>#F7D160</code></td>
              <td>247, 209, 96</td>
              <td>2, 16, 68, 0</td>
              <td>45°, 90%, 67%</td>
              <td>Puncak lengkung cahaya, aksen kilau, siluet paruh rajawali</td>
            </tr>
            <tr>
              <td><strong>#7</strong></td>
              <td><strong>Pale Canary Vanilla</strong></td>
              <td><code>#FDF39D</code></td>
              <td>253, 243, 157</td>
              <td>1, 2, 44, 0</td>
              <td>54°, 96%, 80%</td>
              <td>Pendaran tertinggi ujung api, bintang stardust, kilau tatapan mata</td>
            </tr>
            <tr>
              <td><strong>#8</strong></td>
              <td><strong>Midnight Imperial Plum</strong></td>
              <td><code>#360538</code></td>
              <td>54, 5, 56</td>
              <td>72, 98, 38, 56</td>
              <td>298°, 84%, 12%</td>
              <td>Latar belakang beludru panggung gala &amp; cendera mata eksklusif</td>
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
        <div class="header-title">SISTEM TIPOGRAFI RESMI &amp; SPESIFIKASI SKALA HURUF</div>
      </div>
      <div class="header-meta">EDITORIAL TYPE SYSTEM</div>
    </div>

    <div class="content-area">
      <div class="grid-3" style="margin-bottom: 3.5mm;">
        <!-- Font 1 -->
        <div class="panel" style="border-top: 3px solid #F5C538;">
          <span class="badge">FONT KORPORAT &amp; DIGITAL</span>
          <div class="callout-title" style="margin-top: 2mm; font-size: 14px;">Plus Jakarta Sans</div>
          <p style="font-size: 9.5px; color: #D6BDDF;">Sans-serif geometris modern untuk dokumen dinas, publikasi media sosial, buku panduan, dan teks antarmuka web.</p>
          <div style="margin-top: auto; padding: 2mm; background: rgba(0,0,0,0.3); border-radius: 4px; font-size: 9px;">
            <strong>ExtraBold (800)</strong>: Judul &amp; Headline Utama<br>
            <strong>SemiBold (600)</strong>: Sub-judul &amp; Label Kategori<br>
            <strong>Regular (400)</strong>: Paragraf Bodi &amp; Narasi
          </div>
        </div>

        <!-- Font 2 -->
        <div class="panel" style="border-top: 3px solid #E09D17;">
          <span class="badge">FONT SEREMONIAL RESMI</span>
          <div class="callout-title cinzel" style="margin-top: 2mm; font-size: 14px; color:#FFEAA0;">Cinzel</div>
          <p style="font-size: 9.5px; color: #D6BDDF;">Serif berakar pada prasasti Romawi klasik untuk menegaskan wibawa akademik 44 tahun SMAN 1 Gedeg.</p>
          <div style="margin-top: auto; padding: 2mm; background: rgba(0,0,0,0.3); border-radius: 4px; font-size: 9px;">
            <strong>Format Wajib:</strong> ALL CAPS (Huruf Kapital)<br>
            <strong>Tracking:</strong> Lebar (+150 hingga +250)<br>
            <strong>Peruntukan:</strong> Piagam, Tiket Emas, Prasasti
          </div>
        </div>

        <!-- Font 3 -->
        <div class="panel" style="border-top: 3px solid #F7D160;">
          <span class="badge">FONT PENTAS FESTIVAL</span>
          <div class="callout-title playfair" style="margin-top: 2mm; font-size: 14px; color:#FFEAA0;">Playfair / AVERSA</div>
          <p style="font-size: 9.5px; color: #D6BDDF;">Serif transisional kontras tinggi dan tipografi cair untuk tajuk pementasan seni kreatif festival.</p>
          <div style="margin-top: auto; padding: 2mm; background: rgba(0,0,0,0.3); border-radius: 4px; font-size: 9px;">
            <strong>Bobot:</strong> Black (900) / ExtraBold Italic<br>
            <strong>Peran:</strong> Tajuk Seni Pentas AVERSA<br>
            <strong>Karakter:</strong> Dinamis, Teatrikal, Mewah
          </div>
        </div>
      </div>

      <div class="panel" style="flex: 1; padding: 2.5mm;">
        <div class="panel-header cinzel" style="font-size: 10.5px;">STANDAR SKALA UKURAN &amp; SPASI HURUF (TYPE SCALE MATRIX)</div>
        <table>
          <thead>
            <tr>
              <th>Tingkatan Hierarki</th>
              <th>Ukuran Layar</th>
              <th>Ukuran Cetak</th>
              <th>Bobot Font</th>
              <th>Spasi Huruf (Tracking)</th>
              <th>Peruntukan Baku</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Display Hero</strong></td>
              <td><code>56px – 72px</code></td>
              <td><code>36pt – 48pt</code></td>
              <td>ExtraBold (800)</td>
              <td><code>-0.02em</code></td>
              <td>Spanduk Panggung Utama, Baliho Gerbang Sekolah</td>
            </tr>
            <tr>
              <td><strong>Heading 1 (H1)</strong></td>
              <td><code>40px – 48px</code></td>
              <td><code>26pt – 30pt</code></td>
              <td>ExtraBold (800)</td>
              <td><code>-0.01em</code></td>
              <td>Tajuk Dokumen, Judul Poster Acara Utama</td>
            </tr>
            <tr>
              <td><strong>Heading 2 (H2)</strong></td>
              <td><code>28px – 32px</code></td>
              <td><code>18pt – 22pt</code></td>
              <td>Bold (700)</td>
              <td><code>0em</code></td>
              <td>Sub-judul Bab, Kategori Lomba, Nama Seksi Panitia</td>
            </tr>
            <tr>
              <td><strong>Heading 3 (H3)</strong></td>
              <td><code>20px – 24px</code></td>
              <td><code>14pt – 16pt</code></td>
              <td>SemiBold (600)</td>
              <td><code>0em</code></td>
              <td>Kartu Pengumuman, Jadwal &amp; Lokasi Acara</td>
            </tr>
            <tr>
              <td><strong>Body Standard</strong></td>
              <td><code>15px – 16px</code></td>
              <td><code>10pt – 11pt</code></td>
              <td>Regular (400)</td>
              <td><code>0em</code></td>
              <td>Surat Dinas, Naskah Proposal, Paragraf Artikel</td>
            </tr>
            <tr>
              <td><strong>Ceremonial Caps</strong></td>
              <td><code>18px – 28px</code></td>
              <td><code>12pt – 18pt</code></td>
              <td>Cinzel Bold (700)</td>
              <td><code>+0.20em (Lebar)</code></td>
              <td>Lencana Tiket Emas, Nama Almamater, Piagam Juara</td>
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
        <div class="header-title">AREA BEBAS (CLEAR SPACE) &amp; AMBANG UKURAN MINIMUM PRODUKSI</div>
      </div>
      <div class="header-meta">TECHNICAL BOUNDARIES</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="panel">
          <div class="panel-header cinzel">1. ZONA ISOLASI AREA BEBAS (CLEAR SPACE)</div>
          <div class="img-box darker" style="height: 56mm; margin-bottom: 2.5mm; border: 1.5px dashed #F5C538;">
            <div style="position: relative; width: 55mm; height: 46mm; display: flex; justify-content: center; align-items: center;">
              <img src="{img_logo_color}" style="max-height: 40mm;" alt="Clear Space Logo">
              <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; border: 1px dashed rgba(245,197,56,0.6); pointer-events: none;"></div>
            </div>
          </div>
          <p style="text-align: justify; font-size: 10px;">
            Area bebas (*Clear Space*) adalah batas zona steril di sekeliling lambang yang tidak boleh dimasuki oleh elemen visual lain seperti teks, logo pihak ketiga/sponsor, ornamen garis, atau tepi bidang potong cetak.
          </p>
          <div style="margin-top: auto; padding: 2.5mm; background: rgba(245, 197, 56, 0.08); border-radius: 4px; font-size: 9.5px;">
            <strong style="color: #FFEAA0;">Rumus Baku Zona Isolasi:</strong><br>
            Batas zona aman ditetapkan sebesar <strong>X = 1/4 tinggi total lambang</strong> pada seluruh sisi (atas, kanan, bawah, kiri).
          </div>
        </div>

        <div class="panel darker">
          <div class="panel-header cinzel">2. AMBANG BATAS UKURAN MINIMUM</div>
          <p style="text-align: justify; font-size: 10px; margin-bottom: 3.5mm;">
            Guna menjaga keterbacaan faset 3D, siluet paruh rajawali, dan lengkungan lidah api, penggunaan lambang dibatasi oleh ukuran ambang batas minimum:
          </p>

          <div style="display: flex; gap: 3.5mm; margin-bottom: 3.5mm;">
            <div class="panel" style="flex: 1; padding: 3mm; text-align: center; align-items: center;">
              <img src="{img_logo_color}" style="height: 32px; width: auto; margin-bottom: 2mm;" alt="Min Digital">
              <strong style="color: #F5C538; font-size: 10px;">MEDIA DIGITAL</strong>
              <span style="font-size: 9px; color: #D6BDDF;">Tinggi Min: <strong>32 Piksel</strong><br>(Favicon &amp; Thumbnail)</span>
            </div>

            <div class="panel light" style="flex: 1; padding: 3mm; text-align: center; align-items: center;">
              <img src="{img_logo_linecut}" style="height: 38px; width: auto; margin-bottom: 2mm;" alt="Min Print">
              <strong style="color: #310603; font-size: 10px;">MEDIA CETAK FISIK</strong>
              <span style="font-size: 9px; color: #555555;">Tinggi Min: <strong>14 Milimeter</strong><br>(Lencana Pin Enamel)</span>
            </div>
          </div>

          <div style="margin-top: auto; padding: 2.5mm; background: rgba(0,0,0,0.4); border-left: 3px solid #F5C538; border-radius: 4px; font-size: 9px;">
            <strong>Catatan Khusus Line-Cut:</strong><br>
            Untuk media cetak berukuran di bawah 25 mm atau teknik gravir logam mikro, gunakan varian <code>logo-linecut-black.svg</code> agar celah antar-garis faset tidak tersumbat tinta.
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
        <div class="header-tagline cinzel">BAB 9 • ASET MODULAR</div>
        <div class="header-title">KATALOG ASET MODULAR PENDUKUNG (THEATRICAL ASSET SUITE)</div>
      </div>
      <div class="header-meta">STANDALONE MODULAR ELEMENTS</div>
    </div>

    <div class="content-area">
      <div class="grid-4" style="height: 100%;">
        <!-- Item 1: Ticket -->
        <div class="panel" style="padding: 2.5mm;">
          <div class="img-box" style="height: 36mm;">
            <img src="{img_ticket}" alt="Golden Ticket">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10px;">TIKET EMAS KLASIK</strong>
            <p style="font-size: 8.5px; margin-top: 0.5mm;">Lencana tiket emas dengan sudut berlekuk &amp; bingkai ukir dalam.</p>
          </div>
        </div>

        <!-- Item 2: Magic Hat -->
        <div class="panel" style="padding: 2.5mm;">
          <div class="img-box" style="height: 36mm;">
            <img src="{img_hat}" alt="Top Hat">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10px;">TOPI PESULAP BELUDRU</strong>
            <p style="font-size: 8.5px; margin-top: 0.5mm;">Topi pesulap beludru plum dengan aksen pita keemasan.</p>
          </div>
        </div>

        <!-- Item 3: Lollipop -->
        <div class="panel" style="padding: 2.5mm;">
          <div class="img-box" style="height: 36mm;">
            <img src="{img_lollipop}" alt="Swirl Lollipop">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10px;">PERMEN SPIRAL PASTEL</strong>
            <p style="font-size: 8.5px; margin-top: 0.5mm;">Lolipop spiral putar toska mint, pink ceria, dan vanilla.</p>
          </div>
        </div>

        <!-- Item 4: Golden Cane -->
        <div class="panel" style="padding: 2.5mm;">
          <div class="img-box" style="height: 36mm;">
            <img src="{img_cane}" alt="Golden Cane">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10px;">TONGKAT PESULAP MAHONI</strong>
            <p style="font-size: 8.5px; margin-top: 0.5mm;">Tongkat kayu mahoni dengan kenop bola emas murni 24K.</p>
          </div>
        </div>

        <!-- Item 5: Bonbon Pink -->
        <div class="panel" style="padding: 2.5mm;">
          <div class="img-box" style="height: 36mm;">
            <img src="{img_bonbon}" alt="Wrapped Bonbon">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10px;">PERMEN BONBON PINK</strong>
            <p style="font-size: 8.5px; margin-top: 0.5mm;">Permen bungkus satin pink manis dengan ikatan pita emas.</p>
          </div>
        </div>

        <!-- Item 6: Rose -->
        <div class="panel" style="padding: 2.5mm;">
          <div class="img-box" style="height: 36mm;">
            <img src="{img_rose}" alt="Confectionery Rose">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10px;">MAWAR GULA KRISTAL</strong>
            <p style="font-size: 8.5px; margin-top: 0.5mm;">Kelopak mawar merah anggur manis dan daun toska segar.</p>
          </div>
        </div>

        <!-- Item 7: Glasses -->
        <div class="panel" style="padding: 2.5mm;">
          <div class="img-box" style="height: 36mm;">
            <img src="{img_glasses}" alt="Whimsical Glasses">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10px;">KACAMATA EKSENTRIK</strong>
            <p style="font-size: 8.5px; margin-top: 0.5mm;">Bingkai bundar kuningan emas dengan pantulan lensa kilau.</p>
          </div>
        </div>

        <!-- Item 8: Stardust -->
        <div class="panel" style="padding: 2.5mm;">
          <div class="img-box" style="height: 36mm;">
            <img src="{img_stardust}" alt="Stardust Stars">
          </div>
          <div style="margin-top: 2mm;">
            <strong style="color: #FFEAA0; font-size: 10px;">BINTANG STARDUST EMAS</strong>
            <p style="font-size: 8.5px; margin-top: 0.5mm;">Gugusan bintang empat sudut retro berkilau keemasan.</p>
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
        <div class="panel">
          <div class="panel-header cinzel">1. THEATRICAL PINWHEEL MINT &amp; VANILLA</div>
          <div class="img-box darker" style="height: 60mm; margin-bottom: 2.5mm;">
            <img src="{img_bg_pinwheel}" style="max-height: 56mm;" alt="Pinwheel Mint Background">
          </div>
          <p style="font-size: 10px; text-align: justify;">
            <strong>Konsep Visual:</strong> Mengadaptasi nuansa poster keceriaan bernuansa kincir spiral toska mint pastel (<code>#A0D9CA</code>) dan krem vanilla lembut (<code>#FFF5D6</code>).
          </p>
          <div style="margin-top: auto; padding: 2mm; background: rgba(0,0,0,0.3); border-radius: 4px; font-size: 9px;">
            <strong>Peruntukan:</strong> Feed pengumuman gembira, poster bazar kuliner siswa, dan kartu ucapan Dies Natalis bertema ceria.
          </div>
        </div>

        <div class="panel darker">
          <div class="panel-header cinzel">2. IMPERIAL VELVET STARDUST NIGHT</div>
          <div class="img-box darker" style="height: 60mm; margin-bottom: 2.5mm;">
            <img src="{img_bg_velvet}" style="max-height: 56mm;" alt="Imperial Velvet Stardust">
          </div>
          <p style="font-size: 10px; text-align: justify;">
            <strong>Konsep Visual:</strong> Mengadaptasi poster teaser malam megah bernuansa ungu beludru pekat (<code>#360538</code>) dengan lengkungan taburan debu bintang emas bercahaya.
          </p>
          <div style="margin-top: auto; padding: 2mm; background: rgba(0,0,0,0.3); border-radius: 4px; font-size: 9px;">
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
      <div class="header-meta">PRODUCTION SPECIFICATIONS</div>
    </div>

    <div class="content-area">
      <div class="grid-4" style="height: 100%;">
        <!-- Mockup 1 -->
        <div class="panel">
          <div class="img-box" style="height: 50mm;">
            <img src="{img_mockup_polo}" alt="Kaos Polo">
          </div>
          <div style="margin-top: 2.5mm;">
            <span class="badge" style="background:#4A1255;">SERAGAM PANITIA</span>
            <div class="callout-title" style="margin-top: 1mm;">KAOS POLO &amp; T-SHIRT</div>
            <p style="font-size: 8.5px;">Bordir komputer benang rayon emas diameter 65 mm di dada kiri. Bahan Lacoste Cotton Pique hitam.</p>
          </div>
        </div>

        <!-- Mockup 2 -->
        <div class="panel">
          <div class="img-box" style="height: 50mm;">
            <img src="{img_mockup_tumbler}" alt="Tumbler Termal">
          </div>
          <div style="margin-top: 2.5mm;">
            <span class="badge" style="background:#B6580B;">CENDERA MATA VIP</span>
            <div class="callout-title" style="margin-top: 1mm;">TUMBLER STAINLESS</div>
            <p style="font-size: 8.5px;">Double-wall stainless 304 finishing matte plum dengan grafir laser serat line-cut tinggi 80 mm.</p>
          </div>
        </div>

        <!-- Mockup 3 -->
        <div class="panel">
          <div class="img-box" style="height: 50mm;">
            <img src="{img_mockup_lanyard}" alt="Lanyard ID Card">
          </div>
          <div style="margin-top: 2.5mm;">
            <span class="badge" style="background:#5C186B;">ATRIBUT PANITIA</span>
            <div class="callout-title" style="margin-top: 1mm;">LANYARD &amp; ID CARD</div>
            <p style="font-size: 8.5px;">Pita satin kilap 20 mm Midnight Plum bolak-balik. Kartu PVC 0,8 mm laminasi dof standar ISO.</p>
          </div>
        </div>

        <!-- Mockup 4 -->
        <div class="panel">
          <div class="img-box" style="height: 50mm;">
            <img src="{img_mockup_totebag}" alt="Tote Bag & Pin">
          </div>
          <div style="margin-top: 2.5mm;">
            <span class="badge" style="background:#E09D17; color:#310603;">PAKET ALUMNI</span>
            <div class="callout-title" style="margin-top: 1mm;">TOTE BAG &amp; ENAMEL PIN</div>
            <p style="font-size: 8.5px;">Kanvas katun organik 14 oz natural white dengan pin logam sepuhan emas 24K die-struck.</p>
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
      <div class="header-meta">INTEGRITY &amp; BRAND COMPLIANCE</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="panel" style="border: 1.5px solid #EF4444; background: #260505;">
          <div class="panel-header" style="color: #FCA5A5; font-size: 12px;">❌ ENAM LARANGAN FATAL (DON'TS)</div>
          <div style="display: flex; flex-direction: column; gap: 2mm; margin-top: 1.5mm;">
            <div style="font-size: 10px;">
              <strong>1. Dilarang Menarik Proporsi (Stretch / Squash):</strong><br>
              Menarik lambang secara horizontal atau vertikal merusak keharmonisan geometris busur lingkaran.
            </div>
            <div style="font-size: 10px;">
              <strong>2. Dilarang Mengubah Arah Hadap / Memutar Lambang:</strong><br>
              Paruh rajawali dan akselerasi sayap wajib selalu menghadap ke arah kanan atas (masa depan).
            </div>
            <div style="font-size: 10px;">
              <strong>3. Dilarang Mengganti Urutan Gradasi Warna Faset:</strong><br>
              Seluruh faset emas wajib mematuhi sistem gradasi 8 warna resmi Master Palette.
            </div>
            <div style="font-size: 10px;">
              <strong>4. Dilarang Menambahkan Efek Bayangan Kasar (Heavy Shadow):</strong><br>
              Drop shadow hitam pekat yang tidak natural akan mengaburkan garis batas faset.
            </div>
            <div style="font-size: 10px;">
              <strong>5. Dilarang Menaruh di Atas Latar Tabrakan:</strong><br>
              Hindari menaruh logo warna di atas warna merah menyala, hijau stabilo, atau corak ramai.
            </div>
            <div style="font-size: 10px;">
              <strong>6. Dilarang Menggunakan Font Komikal / Tidak Resmi:</strong><br>
              Dilarang memakai font dekoratif sembarangan seperti Comic Sans, Papyrus, atau Brush Script.
            </div>
          </div>
        </div>

        <div class="panel" style="border: 1.5px solid #10B981; background: #042417;">
          <div class="panel-header" style="color: #6EE7B7; font-size: 12px;">✅ PANDUAN PENGGUNAAN BENAR (DO'S)</div>
          <div style="display: flex; flex-direction: column; gap: 2mm; margin-top: 1.5mm;">
            <div style="font-size: 10px;">
              <strong>1. Selalu Gunakan Berkas Vektor SVG untuk Cetak:</strong><br>
              Gunakan berkas di direktori <code>assets/svg/</code> untuk pencetakan spanduk, banner, atau kaos agar tidak pecah.
            </div>
            <div style="font-size: 10px;">
              <strong>2. Terapkan Monokrom Putih di Atas Foto Gelap:</strong><br>
              Gunakan varian <code>logo-monochrome-white.svg</code> bila diletakkan di atas dokumentasi foto kegiatan sekolah.
            </div>
            <div style="font-size: 10px;">
              <strong>3. Jaga Area Aman (Clear Space) Sebesar 1/4 Tinggi:</strong><br>
              Pastikan selalu ada ruang bernapas yang cukup di sekeliling lambang tanpa gangguan ornamen.
            </div>
            <div style="font-size: 10px;">
              <strong>4. Gunakan Font Plus Jakarta Sans &amp; Cinzel:</strong><br>
              Patuhi hierarki tipografi resmi almamater untuk menjaga konsistensi publikasi.
            </div>
            <div style="font-size: 10px;">
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
        <div class="header-tagline cinzel">BAB 13 • LEGALITAS &amp; PENGESAHAN</div>
        <div class="header-title">HAK CIPTA, STATUS LISENSI &amp; TANDA PENGESAHAN (COLOPHON)</div>
      </div>
      <div class="header-meta">LEGAL NOTICE &amp; SIGN-OFF</div>
    </div>

    <div class="content-area">
      <div class="grid-2" style="margin-bottom: 3.5mm;">
        <div class="panel">
          <div class="panel-header cinzel">PERNYATAAN HAK CIPTA EKSKLUSIF</div>
          <p style="text-align: justify; font-size: 10px;">
            Seluruh lambang, gambar vektor, skrip komputasi algoritma, tata letak lockup, dokumen pedoman identitas visual, serta materi pendukung Dies Natalis ke-44 ini dilindungi oleh Undang-Undang Hak Cipta Republik Indonesia (UU No. 28 Tahun 2014).
          </p>
          <div style="margin-top: 2.5mm; padding: 2.5mm; background: rgba(245, 197, 56, 0.08); border-left: 3px solid #F5C538; border-radius: 4px; font-size: 9.5px;">
            <strong style="color: #FFEAA0;">Status Kepemilikan &amp; Lisensi:</strong><br>
            <strong>PROPRIETARY / ALL RIGHTS RESERVED (LISENSI TERTUTUP EKSKLUSIF)</strong><br>
            Hak kekayaan intelektual sepenuhnya dimiliki secara bersama oleh <strong>SMA Negeri 1 Gedeg</strong> dan <strong>Ryan Ardian</strong>. Dilarang keras menyalin, memperbanyak, memperjualbelikan, atau memanfaatkan materi ini untuk kepentingan komersial pihak ketiga tanpa persetujuan tertulis resmi.
          </div>
        </div>

        <div class="panel darker">
          <div class="panel-header cinzel">ATRIBUSI KARYA &amp; SPESIFIKASI TEKNIS</div>
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
      <div class="panel" style="padding: 3.5mm; background: #1C0521;">
        <div style="display: flex; justify-content: space-around; text-align: center; font-size: 10px;">
          <div>
            <span style="color: #D4B8DE;">Mengetahui,</span><br>
            <strong style="color: #FFEAA0;">Kepala SMA Negeri 1 Gedeg</strong><br>
            <div style="height: 16mm;"></div>
            <strong style="text-decoration: underline; color: #FFFFFF;">...................................................</strong><br>
            <span style="font-size: 8.5px; color: #A891B0;">NIP. ...................................................</span>
          </div>

          <div>
            <span style="color: #D4B8DE;">Disusun Oleh,</span><br>
            <strong style="color: #FFEAA0;">Guru Pengampu / Desainer Lambang</strong><br>
            <div style="height: 16mm;"></div>
            <strong style="text-decoration: underline; color: #FFFFFF;">RYAN ARDIAN</strong><br>
            <span style="font-size: 8.5px; color: #F5C538;">SMA Negeri 1 Gedeg</span>
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
    print("=== BUILDING DIES NATALIS 44 BRAND GUIDELINES BOOK (ANTI-SLOP AUDITED) ===")
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
