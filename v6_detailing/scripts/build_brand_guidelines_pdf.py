#!/usr/bin/env python3
"""
build_brand_guidelines_pdf.py
Buku Pedoman Identitas Visual Dies Natalis ke-44 SMAN 1 Gedeg (1982—2026).
Tema: AVERSA.

Pembaruan Tipografi & Pedoman Font Lengkap:
1. Tema ditulis ringkas dan tegas: "AVERSA" (tanpa imbuhan "TEMA BESAR:").
2. Pedoman Komprehensif Tipografi:
   - Karakteristik dan peruntukan 3 keluarga huruf resmi (Plus Jakarta Sans, Cinzel, Playfair Display).
   - Pedoman pasangan huruf (font pairing: formal, media sosial, dan pentas seni).
   - Aturan format huruf (kapital penuh/ALL CAPS, spasi antarhuruf/tracking, dan jarak antarbaris/leading).
   - Larangan penggunaan jenis huruf sembarangan.
3. Direktori Berkas Font Asli (.ttf dan .otf) di repositori:
   - Tersedia di folder assets/fonts/ siap unduh langsung di GitHub.
4. Kepatuhan 100% EYD Edisi Kelima (Kemendikdasmen RI).
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
        print(f"Peringatan: Berkas gambar tidak ditemukan: {p}")
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
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@600;700&display=swap" rel="stylesheet">
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
      color: #F8F3FA;
      background: #09020C;
      font-size: 13.5px;
      line-height: 1.55;
    }}
    .cinzel {{
      font-family: 'Cinzel', Georgia, serif;
    }}
    .playfair {{
      font-family: 'Playfair Display', Georgia, serif;
    }}
    .mono {{
      font-family: 'JetBrains Mono', monospace;
    }}
    
    /* Wadah Halaman */
    .page {{
      width: 297mm;
      height: 210mm;
      position: relative;
      overflow: hidden;
      page-break-after: always;
      display: flex;
      flex-direction: column;
      background: #110314;
      padding: 13mm 18mm;
    }}
    
    /* Header Atas */
    .page-header {{
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      border-bottom: 2px solid rgba(245, 197, 56, 0.4);
      padding-bottom: 3mm;
      margin-bottom: 5mm;
    }}
    .header-tagline {{
      font-size: 11px;
      letter-spacing: 2px;
      color: #E09D17;
      font-weight: 800;
      text-transform: uppercase;
    }}
    .header-title {{
      font-size: 22px;
      font-weight: 800;
      color: #FFFFFF;
      letter-spacing: 0.2px;
      line-height: 1.2;
    }}
    .header-meta {{
      text-align: right;
      font-size: 10.5px;
      color: #D4B8DE;
      letter-spacing: 1px;
      font-weight: 700;
    }}
    
    /* Footer Bawah */
    .page-footer {{
      position: absolute;
      bottom: 6mm;
      left: 18mm;
      right: 18mm;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid rgba(255, 255, 255, 0.12);
      padding-top: 2.5mm;
      font-size: 9.5px;
      color: #9C89A3;
    }}
    .page-num {{
      font-weight: 900;
      color: #F5C538;
      font-size: 11px;
      letter-spacing: 1px;
    }}
    
    /* Grid & Tata Letak */
    .content-area {{
      flex: 1;
      display: flex;
      flex-direction: column;
    }}
    .grid-2 {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 5.5mm;
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
      gap: 4.5mm;
      height: 100%;
    }}
    
    /* Panel Konten */
    .panel {{
      background: #18041D;
      border: 1px solid rgba(245, 197, 56, 0.25);
      border-radius: 8px;
      padding: 4.5mm 5mm;
      display: flex;
      flex-direction: column;
    }}
    .panel.darker {{
      background: #0E0211;
      border-color: rgba(255, 255, 255, 0.1);
    }}
    .panel.highlight {{
      background: #24052C;
      border-color: #F5C538;
    }}
    .panel-header {{
      font-size: 14px;
      font-weight: 800;
      color: #FFEAA0;
      margin-bottom: 2.5mm;
      display: flex;
      align-items: center;
      justify-content: space-between;
      letter-spacing: 0.5px;
    }}
    
    /* Label & Lencana */
    .badge {{
      display: inline-block;
      padding: 2.5px 8px;
      border-radius: 4px;
      font-size: 9.5px;
      font-weight: 800;
      letter-spacing: 0.8px;
      background: #3B0C46;
      color: #FFEAA0;
      border: 1px solid #F5C538;
      text-transform: uppercase;
    }}
    
    /* Tipografi Dasar */
    h1, h2, h3, h4 {{
      color: #FFFFFF;
    }}
    p {{
      color: #E6D7EB;
      margin-bottom: 2.5mm;
      font-size: 13px;
      line-height: 1.5;
    }}
    strong {{
      color: #FFFFFF;
    }}
    
    /* Kotak Pratinjau Gambar */
    .img-box {{
      background: #09010C;
      border: 1px solid rgba(255, 255, 255, 0.1);
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
      background: #FAF8F5;
      border-color: #E2DBD0;
    }}
    
    /* Baris Bernomor */
    .callout-row {{
      display: flex;
      gap: 12px;
      margin-bottom: 3mm;
      align-items: flex-start;
    }}
    .callout-idx {{
      font-family: 'Cinzel', serif;
      font-size: 18px;
      font-weight: 900;
      color: #F5C538;
      min-width: 28px;
      line-height: 1;
    }}
    .callout-body {{
      flex: 1;
    }}
    .callout-title {{
      font-size: 13.5px;
      font-weight: 800;
      color: #FFEAA0;
      margin-bottom: 1mm;
    }}
    .callout-desc {{
      font-size: 12.5px;
      color: #D6C2DC;
      margin: 0;
      line-height: 1.45;
    }}
    
    /* Tabel */
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 11.5px;
      margin-top: 1.5mm;
    }}
    th {{
      background: #2E0B37;
      color: #FFEAA0;
      text-align: left;
      padding: 5px 8px;
      font-weight: 800;
      letter-spacing: 0.3px;
      border-bottom: 2px solid #F5C538;
      font-size: 11.5px;
    }}
    td {{
      padding: 4.5px 8px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      color: #E1D1E7;
    }}
    tr:nth-child(even) td {{
      background: rgba(255, 255, 255, 0.02);
    }}
    
    /* Halaman Sampul */
    .cover-page {{
      background: radial-gradient(circle at 50% 45%, #2D052F 0%, #160218 55%, #080009 100%);
      padding: 16mm 20mm;
      justify-content: space-between;
      align-items: center;
      text-align: center;
    }}
    .cover-badge {{
      display: inline-block;
      padding: 3mm 9mm;
      border-radius: 20px;
      background: rgba(245, 197, 56, 0.12);
      border: 1.5px solid #F5C538;
      color: #FFEAA0;
      font-size: 12px;
      font-weight: 800;
      letter-spacing: 3px;
      margin-bottom: 3.5mm;
    }}
    .cover-title {{
      font-size: 32px;
      font-weight: 900;
      letter-spacing: 1px;
      color: #FFFFFF;
      text-transform: uppercase;
      line-height: 1.25;
      margin-bottom: 2.5mm;
    }}
    .cover-subtitle {{
      font-size: 18px;
      font-weight: 700;
      color: #F7D160;
      letter-spacing: 2px;
      margin-bottom: 4mm;
    }}
    .cover-theme {{
      font-size: 28px;
      font-weight: 900;
      color: #FFFFFF;
      letter-spacing: 8px;
    }}
    .cover-footer {{
      border-top: 1.5px solid rgba(245, 197, 56, 0.4);
      padding-top: 4.5mm;
      width: 100%;
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: #CBB4D2;
    }}
  </style>
</head>
<body>

  <!-- ==================== HALAMAN 1: SAMPUL RESMI ==================== -->
  <div class="page cover-page">
    <div style="width: 100%; text-align: center;">
      <div class="cover-badge cinzel">PEDOMAN RESMI</div>
      <div class="cover-title">PEDOMAN IDENTITAS VISUAL</div>
      <div class="cover-subtitle cinzel">DIES NATALIS KE-44 SMAN 1 GEDEG (1982—2026)</div>
      <div class="cover-theme playfair">AVERSA</div>
    </div>
    
    <div style="margin: 4mm 0;">
      <img src="{img_logo_color}" style="width: 68mm; height: auto; filter: drop-shadow(0 14px 32px rgba(245, 197, 56, 0.35));" alt="Lambang Dies Natalis 44">
    </div>

    <div class="cover-footer">
      <div>
        <strong style="color: #F7D160; font-size: 12px;">SMA NEGERI 1 GEDEG</strong><br>
        Kecamatan Gedeg, Kabupaten Mojokerto, Jawa Timur
      </div>
      <div style="text-align: center;">
        <span class="cinzel" style="color: #FFFFFF; font-weight: 800; letter-spacing: 1.5px;">KARYA KOLABORATIF SISWA DAN GURU</span><br>
        Tim Kreatif Dies Natalis ke-44 SMAN 1 Gedeg
      </div>
      <div style="text-align: right;">
        <strong style="color: #F5C538; font-size: 12px;">EDISI RESMI</strong><br>
        Identitas Visual dan Media Publikasi
      </div>
    </div>
  </div>


  <!-- ==================== HALAMAN 2: PENDAHULUAN & LANDASAN ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 1 • PENDAHULUAN</div>
        <div class="header-title">44 TAHUN PENGABDIAN DAN TUJUAN PEDOMAN</div>
      </div>
      <div class="header-meta">SMAN 1 GEDEG • 1982—2026</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="panel">
          <div class="panel-header cinzel">PERJALANAN 44 TAHUN ALMAMATER</div>
          <p style="text-align: justify; margin-bottom: 3.5mm;">
            Didirikan pada tahun <strong>1982</strong> di Kabupaten Mojokerto, SMA Negeri 1 Gedeg telah melangkah selama 44 tahun mengabdi mencerdaskan kehidupan bangsa. Peringatan Dies Natalis ke-44 pada tahun <strong>2026</strong> menjadi momentum kematangan almamater dalam memadukan keteguhan budi pekerti dengan semangat prestasi modern.
          </p>
          <p style="text-align: justify; margin-bottom: 4mm;">
            Buku pedoman ini disusun sebagai pegangan kerja visual agar seluruh panitia, perancang grafis, dan mitra kerja menghasilkan media publikasi yang selaras, rapi, dan berwibawa.
          </p>
          <div style="margin-top: auto; padding: 3.5mm; background: rgba(0,0,0,0.35); border-left: 3.5px solid #E09D17; border-radius: 4px;">
            <strong style="color: #FFEAA0; font-size: 13.5px;">Nilai Luhur SMAN 1 Gedeg:</strong><br>
            <span style="font-size: 12.5px; color: #E5D5EB;">Religius, Berbudi Luhur, Unggul Intelektual, Peduli Lingkungan, dan Berwawasan Global.</span>
          </div>
        </div>

        <div class="panel darker">
          <div class="panel-header cinzel">3 FOKUS UTAMA PEDOMAN</div>
          
          <div class="callout-row">
            <div class="callout-idx">01</div>
            <div class="callout-body">
              <div class="callout-title">KONSISTENSI VISUAL</div>
              <p class="callout-desc">Menjaga keseragaman bentuk, rona keemasan, dan proporsi lambang di seluruh media publikasi, spanduk, pakaian seragam, dan cendera mata.</p>
            </div>
          </div>

          <div class="callout-row">
            <div class="callout-idx">02</div>
            <div class="callout-body">
              <div class="callout-title">PENCEGAHAN KESALAHAN DESAIN</div>
              <p class="callout-desc">Menghindari lambang terdistorsi (gepeng atau ditarik paksa), terpotong, atau bertabrakan dengan warna latar yang tidak serasi.</p>
            </div>
          </div>

          <div class="callout-row">
            <div class="callout-idx">03</div>
            <div class="callout-body">
              <div class="callout-title">KEMUDAHAN PELAKSANAAN TEKNIS</div>
              <p class="callout-desc">Menyediakan format berkas siap pakai: vektor SVG untuk percetakan besar, bordir, dan sablon, serta PNG berkualitas tinggi untuk media digital.</p>
            </div>
          </div>

          <div style="margin-top: auto; padding: 2.5mm; background: rgba(245, 197, 56, 0.1); border-radius: 4px; text-align: center; border: 1px dashed rgba(245, 197, 56, 0.4);">
            <span style="font-size: 11px; color: #F7D160; font-weight: 800;">PEDOMAN RESMI IDENTITAS VISUAL DIES NATALIS KE-44</span>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 02</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 3: INTEGRASI FILOSOFI (LAMBANG 44 & AVERSA) ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 2 • INTEGRASI FILOSOFI</div>
        <div class="header-title">KESATUAN FILOSOFI: LAMBANG 44 DAN AVERSA</div>
      </div>
      <div class="header-meta">RAGA DAN JIWA IDENTITAS</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <!-- Visual Lockup Gabungan -->
        <div class="panel darker" style="align-items: center; justify-content: space-between; padding: 3.5mm;">
          <div style="width: 100%; text-align: center; margin-bottom: 2mm;">
            <span class="badge" style="background:#5C186B;">KOLABORASI DUA SIMBOL UTAMA</span>
          </div>
          <div class="img-box" style="width: 100%; height: 95mm; background: transparent; border: none;">
            <img src="{img_aversa_combo}" style="max-height: 90mm;" alt="Integrasi Lambang 44 dan Aversa">
          </div>
          <div style="font-size: 11.5px; color: #F7D160; text-align: center; font-weight: 800; letter-spacing: 0.5px;">
            KESATUAN TUNGGAL IDENTITAS VISUAL DIES NATALIS KE-44
          </div>
        </div>

        <!-- Narasi Integrasi Filosofis -->
        <div class="panel" style="justify-content: space-between;">
          <div>
            <div class="panel-header cinzel">SATU KESATUAN: RAGA DAN RUH</div>
            <p style="text-align: justify; margin-bottom: 3mm;">
              Identitas Dies Natalis ke-44 SMA Negeri 1 Gedeg diperkenalkan sebagai <strong>satu kesatuan utuh</strong> yang memadukan wujud lambang angka 44 dengan doktrin <strong>AVERSA</strong>:
            </p>

            <div class="callout-row" style="margin-bottom: 2.5mm;">
              <div class="callout-idx">A</div>
              <div class="callout-body">
                <div class="callout-title">LAMBANG 44 SEBAGAI RAGA IDENTITAS</div>
                <p class="callout-desc">Menjadi simbol ragawi almamater yang merepresentasikan tonggak sejarah 44 tahun perjalanan sekolah, keteguhan tradisi, ketajaman visi elang rajawali, dan sayap akselerasi prestasi.</p>
              </div>
            </div>

            <div class="callout-row" style="margin-bottom: 2.5mm;">
              <div class="callout-idx">B</div>
              <div class="callout-body">
                <div class="callout-title">AVERSA SEBAGAI RUH DAN GERAKAN</div>
                <p class="callout-desc">Menjadi jiwa pendorong dan landasan sikap seluruh warga sekolah: doktrin untuk terus berkembang, memiliki visi yang jelas, membangun solidaritas, dan berani mewujudkan perubahan.</p>
              </div>
            </div>

            <div class="callout-row">
              <div class="callout-idx">★</div>
              <div class="callout-body">
                <div class="callout-title">PESAN TUNGGAL KEJAYAAN</div>
                <p class="callout-desc">Keduanya bersenyawa melahirkan narasi utama: <em>"44 Tahun Mengobarkan Api Prestasi, Melesat Bersama Semangat AVERSA."</em></p>
              </div>
            </div>
          </div>

          <div style="padding: 2.5mm; background: rgba(245, 197, 56, 0.08); border-radius: 4px; border-left: 3px solid #F5C538; font-size: 11px; color: #E5D5EB;">
            Pada bab-bab selanjutnya, rincian anatomi bentuk lambang 44 dan pilar AVERSA diuraikan secara tersendiri untuk memudahkan penerapan teknis.
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 03</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 4: RINCIAN ANATOMI LAMBANG 44 ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 3 • ANATOMI LAMBANG</div>
        <div class="header-title">RINCIAN MAKNA DAN ANATOMI LAMBANG 44</div>
      </div>
      <div class="header-meta">ANATOMI LAMBANG</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="panel darker" style="align-items: center; justify-content: center; padding: 3mm;">
          <div class="img-box" style="width: 100%; height: 115mm; background: transparent; border: none;">
            <img src="{img_logo_color}" style="max-height: 105mm;" alt="Anatomi Lambang 44">
          </div>
          <div style="font-size: 11.5px; color: #F7D160; text-align: center; margin-top: 1mm; font-weight: 800;">
            LAMBANG RESMI DIES NATALIS KE-44 SMAN 1 GEDEG
          </div>
        </div>

        <div class="panel" style="justify-content: space-between;">
          <div>
            <div class="panel-header cinzel">4 ELEMEN ANATOMIS UTAMA</div>
            
            <div class="callout-row">
              <div class="callout-idx">1</div>
              <div class="callout-body">
                <div class="callout-title">FIGUR KEMBAR ANGKA 44</div>
                <p class="callout-desc">Menandai usia ke-44 tahun almamater. Angka 4 pertama berdiri kokoh sebagai fondasi tradisi dan sejarah; angka 4 kedua melesat maju sebagai pilar inovasi masa depan.</p>
              </div>
            </div>

            <div class="callout-row">
              <div class="callout-idx">2</div>
              <div class="callout-body">
                <div class="callout-title">TATAPAN BURUNG RAJAWALI</div>
                <p class="callout-desc">Siluet kepala rajawali menatap mantap ke arah kanan atas, menyimbolkan pandangan visioner, ketajaman intelektual, dan keberanian civitas akademika dalam melangkah maju.</p>
              </div>
            </div>

            <div class="callout-row">
              <div class="callout-idx">3</div>
              <div class="callout-body">
                <div class="callout-title">KOBARAN LIDAH API ABADI</div>
                <p class="callout-desc">Tiga sulur api yang menyala melambangkan semangat belajar yang pantang padam, ketangguhan menghadapi tantangan, dan daya cipta yang senantiasa memberi manfaat.</p>
              </div>
            </div>

            <div class="callout-row">
              <div class="callout-idx">4</div>
              <div class="callout-body">
                <div class="callout-title">SAYAP MELESAT AERODINAMIS</div>
                <p class="callout-desc">Sapuan sayap melengkung ke atas mencerminkan percepatan prestasi sekolah serta tekad teguh untuk terus terbang tinggi meraih cita-cita mulia.</p>
              </div>
            </div>
          </div>

          <div style="padding: 2.5mm; background: rgba(245, 197, 56, 0.08); border-radius: 4px; border-left: 3px solid #F5C538; font-size: 11px; color: #E5D5EB;">
            Garis tengah simetris menyatukan seluruh elemen dalam keserasian bentuk yang bersih, anggun, dan berwibawa.
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 04</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 5: EMPAT PILAR AVERSA ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 4 • AVERSA</div>
        <div class="header-title">LOGOTIPE RESMI DAN 4 PILAR AVERSA</div>
      </div>
      <div class="header-meta">DOKTRIN GERAKAN</div>
    </div>

    <div class="content-area">
      <!-- Wordmark Box -->
      <div class="panel" style="margin-bottom: 4mm; padding: 3.5mm; align-items: center; background: #1C0521;">
        <div class="img-box" style="width: 100%; height: 38mm; background: transparent; border: none;">
          <img src="{img_aversa_wordmark}" style="max-height: 35mm;" alt="Logotipe Aversa">
        </div>
        <div style="font-size: 11.5px; color: #F7D160; margin-top: 1mm; font-weight: 800; letter-spacing: 1.5px;">
          LOGOTIPE RESMI AVERSA (BERAKAR DARI SKETSA TIPOGRAFI TANGAN SISWA)
        </div>
      </div>

      <!-- 4 Pillars Grid -->
      <div class="grid-4" style="flex: 1;">
        <div class="panel" style="border-top: 4px solid #E09D17;">
          <div class="callout-idx" style="font-size: 20px;">01</div>
          <div class="callout-title" style="font-size: 13px; margin-top: 1mm;">SEMANGAT TERUS BERKEMBANG</div>
          <p style="font-size: 12px; text-align: justify; margin-top: 2mm;">
            Dorongan internal untuk pantang berpuas diri, tekun mengasah potensi diri, memperluas wawasan keilmuan, dan adaptif terhadap kemajuan zaman.
          </p>
        </div>

        <div class="panel" style="border-top: 4px solid #F5C538;">
          <div class="callout-idx" style="font-size: 20px;">02</div>
          <div class="callout-title" style="font-size: 13px; margin-top: 1mm;">MEMILIKI VISI YANG JELAS</div>
          <p style="font-size: 12px; text-align: justify; margin-top: 2mm;">
            Arah langkah masa depan yang terencana dan terukur, berfokus pada capaian prestasi dan akhlak luhur, selaras dengan tatapan tajam burung rajawali.
          </p>
        </div>

        <div class="panel" style="border-top: 4px solid #F7D160;">
          <div class="callout-idx" style="font-size: 20px;">03</div>
          <div class="callout-title" style="font-size: 13px; margin-top: 1mm;">MEMBANGUN SOLIDARITAS</div>
          <p style="font-size: 12px; text-align: justify; margin-top: 2mm;">
            Rasa persaudaraan yang erat dan saling menopang antarsiswa, guru, tenaga kependidikan, serta alumni demi kemajuan bersama almamater.
          </p>
        </div>

        <div class="panel" style="border-top: 4px solid #FDF39D;">
          <div class="callout-idx" style="font-size: 20px;">04</div>
          <div class="callout-title" style="font-size: 13px; margin-top: 1mm;">BERANI MEWUJUDKAN PERUBAHAN</div>
          <p style="font-size: 12px; text-align: justify; margin-top: 2mm;">
            Keberanian melangkah melalui tindakan nyata dan karya yang berdaya guna, bukan sekadar berhenti pada tataran gagasan atau wacana.
          </p>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 05</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 6: 4 VARIAN LOGO RESMI ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 5 • VARIAN LAMBANG</div>
        <div class="header-title">4 VARIAN PENGGUNAAN LAMBANG RESMI</div>
      </div>
      <div class="header-meta">FORMAT PENGGUNAAN</div>
    </div>

    <div class="content-area">
      <div class="grid-4" style="height: 100%;">
        <!-- Varian 1 -->
        <div class="panel">
          <div class="img-box" style="height: 52mm; background: #0E0211;">
            <img src="{img_logo_color}" alt="Lambang Berwarna">
          </div>
          <div style="margin-top: 3mm;">
            <span class="badge" style="background:#B6580B;">LAMBANG BERWARNA (UTAMA)</span>
            <div class="callout-title" style="margin-top: 1.5mm;">WARNA EMAS PENUH</div>
            <p style="font-size: 11.5px;">Varian utama dengan warna emas lengkap. Digunakan untuk spanduk panggung, banner web, media sosial, dan buku kenangan.</p>
          </div>
        </div>

        <!-- Varian 2 -->
        <div class="panel">
          <div class="img-box light" style="height: 52mm;">
            <img src="{img_logo_linecut}" alt="Lambang Garis">
          </div>
          <div style="margin-top: 3mm;">
            <span class="badge" style="background:#334155;">LAMBANG GARIS (LINE-ART)</span>
            <div class="callout-title" style="margin-top: 1.5mm; color:#FFEAA0;">SATU WARNA TEGAS</div>
            <p style="font-size: 11.5px;">Garis kontur hitam tegas untuk sablon satu warna, stempel dinas, bordir seragam, dan grafir laser tumbler.</p>
          </div>
        </div>

        <!-- Varian 3 -->
        <div class="panel">
          <div class="img-box" style="height: 52mm; background: #000000;">
            <img src="{img_logo_mono_white}" alt="Lambang Monokrom Putih">
          </div>
          <div style="margin-top: 3mm;">
            <span class="badge" style="background:#4A1255;">LAMBANG PUTIH (MONOKROM)</span>
            <div class="callout-title" style="margin-top: 1.5mm;">KONTRAS TINGGI</div>
            <p style="font-size: 11.5px;">Siluet putih bersih untuk ditempatkan di atas latar belakang foto kegiatan, video bumper, dan kain berwarna gelap.</p>
          </div>
        </div>

        <!-- Varian 4 -->
        <div class="panel">
          <div class="img-box light" style="height: 52mm;">
            <img src="{img_logo_grid}" alt="Kisi Proporsi">
          </div>
          <div style="margin-top: 3mm;">
            <span class="badge" style="background:#1E3A8A;">KISI PROPORSI</span>
            <div class="callout-title" style="margin-top: 1.5mm; color:#FFEAA0;">PANDUAN KESEIMBANGAN</div>
            <p style="font-size: 11.5px;">Pedoman konstruksi dan rasio kelengkungan agar lambang selalu proporsional dan tidak mengalami perubahan bentuk.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 06</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 7: SUSUNAN LOGO (LOCKUP) ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 6 • TATA LETAK</div>
        <div class="header-title">SUSUNAN LAMBANG DAN IDENTITAS SEKOLAH</div>
      </div>
      <div class="header-meta">PILIHAN TATA LETAK</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="panel">
          <div class="panel-header cinzel">1. SUSUNAN DENGAN IDENTITAS SEKOLAH</div>
          <div class="img-box" style="height: 44mm; margin-bottom: 2mm; background: #130418;">
            <img src="{img_logo_horizontal}" style="max-height: 38mm;" alt="Susunan Horizontal">
          </div>
          <p style="font-size: 12px; margin-bottom: 3mm;">
            <strong>Susunan Horizontal:</strong> Lambang di sebelah kiri dan nama sekolah di kanan. Sangat tepat untuk spanduk jalan, kop surat dinas, header website, dan media memanjang.
          </p>
          <div class="img-box" style="height: 42mm; background: #130418;">
            <img src="{img_logo_vertical}" style="max-height: 38mm;" alt="Susunan Vertikal">
          </div>
          <p style="font-size: 12px; margin-top: 2.5mm;">
            <strong>Susunan Vertikal:</strong> Lambang di atas dan nama sekolah di bawah. Sangat tepat untuk sampul proposal, poster tegak, plakat, dan baliho gerbang sekolah.
          </p>
        </div>

        <div class="panel">
          <div class="panel-header cinzel">2. SUSUNAN BERSAMA TEMA AVERSA</div>
          <div class="img-box" style="height: 44mm; margin-bottom: 2mm; background: #130418;">
            <img src="{img_aversa_horizontal}" style="max-height: 38mm;" alt="Aversa Horizontal">
          </div>
          <p style="font-size: 12px; margin-bottom: 3mm;">
            <strong>Susunan Tema Horizontal:</strong> Tulisan tema AVERSA berdampingan dengan identitas sekolah. Cocok untuk backdrop pentas seni dan promosi media sosial.
          </p>
          <div class="img-box" style="height: 42mm; background: #130418;">
            <img src="{img_aversa_combo}" style="max-height: 38mm;" alt="Susunan Lengkap">
          </div>
          <p style="font-size: 12px; margin-top: 2.5mm;">
            <strong>Susunan Lengkap:</strong> Penggabungan lambang rajawali 44, tulisan AVERSA, dan identitas SMAN 1 Gedeg untuk keperluan publikasi akbar sekolah.
          </p>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 07</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 8: SISTEM PALET WARNA RESMI ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 7 • PALET WARNA</div>
        <div class="header-title">SPESIFIKASI 8 WARNA RESMI ALMAMATER</div>
      </div>
      <div class="header-meta">KODE WARNA RESMI</div>
    </div>

    <div class="content-area">
      <div class="panel darker" style="padding: 2mm; margin-bottom: 3.5mm;">
        <div class="img-box" style="height: 56mm; background: transparent; border: none;">
          <img src="{img_palette_guide}" style="max-height: 55mm; width: 100%; object-fit: contain;" alt="Panduan Palet Warna">
        </div>
      </div>

      <div class="panel" style="flex: 1; padding: 3mm;">
        <div class="panel-header cinzel" style="font-size: 13px;">KODE WARNA RESMI UNTUK PERANCANG GRAFIS DAN PERCETAKAN</div>
        <table>
          <thead>
            <tr>
              <th style="width: 28px;">No</th>
              <th>Nama Warna</th>
              <th>Kode HEX</th>
              <th>RGB (Layar)</th>
              <th>CMYK (Cetak)</th>
              <th>Penerapan dalam Desain</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>1</strong></td>
              <td><strong>Obsidian Mahogany</strong></td>
              <td><code class="mono" style="color:#FFEAA0; font-size:12.5px; font-weight:bold;">#310603</code></td>
              <td>49, 6, 3</td>
              <td>48, 88, 76, 75</td>
              <td>Garis batas luar terdalam, bayangan kontras, teks gelap</td>
            </tr>
            <tr>
              <td><strong>2</strong></td>
              <td><strong>Deep Crimson Rust</strong></td>
              <td><code class="mono" style="color:#FFEAA0; font-size:12.5px; font-weight:bold;">#7D1B05</code></td>
              <td>125, 27, 5</td>
              <td>24, 96, 100, 27</td>
              <td>Pangkal lidah api berkobar, bayangan gradasi hangat</td>
            </tr>
            <tr>
              <td><strong>3</strong></td>
              <td><strong>Rich Amber Bronze</strong></td>
              <td><code class="mono" style="color:#FFEAA0; font-size:12.5px; font-weight:bold;">#B6580B</code></td>
              <td>182, 88, 11</td>
              <td>18, 73, 100, 7</td>
              <td>Lekukan lipatan pita dan transisi warna keemasan</td>
            </tr>
            <tr>
              <td><strong>4</strong></td>
              <td><strong>Marigold Warm Gold</strong></td>
              <td><code class="mono" style="color:#FFEAA0; font-size:12.5px; font-weight:bold;">#E09D17</code></td>
              <td>224, 157, 23</td>
              <td>9, 39, 99, 0</td>
              <td>Warna tubuh utama angka 44 dan sayap rajawali</td>
            </tr>
            <tr>
              <td><strong>5</strong></td>
              <td><strong>Vivid Royal Gold</strong></td>
              <td><code class="mono" style="color:#FFEAA0; font-size:12.5px; font-weight:bold;">#F5C538</code></td>
              <td>245, 197, 56</td>
              <td>3, 21, 84, 0</td>
              <td>Garis tengah lambang dan aksen kilau cahaya utama</td>
            </tr>
            <tr>
              <td><strong>6</strong></td>
              <td><strong>Champagne Highlight</strong></td>
              <td><code class="mono" style="color:#FFEAA0; font-size:12.5px; font-weight:bold;">#F7D160</code></td>
              <td>247, 209, 96</td>
              <td>2, 16, 68, 0</td>
              <td>Kilau cahaya terang, paruh rajawali, ujung bulu sayap</td>
            </tr>
            <tr>
              <td><strong>7</strong></td>
              <td><strong>Pale Canary Vanilla</strong></td>
              <td><code class="mono" style="color:#FFEAA0; font-size:12.5px; font-weight:bold;">#FDF39D</code></td>
              <td>253, 243, 157</td>
              <td>1, 2, 44, 0</td>
              <td>Kilau bintang stardust dan pantulan mata rajawali</td>
            </tr>
            <tr>
              <td><strong>8</strong></td>
              <td><strong>Midnight Imperial Plum</strong></td>
              <td><code class="mono" style="color:#FFEAA0; font-size:12.5px; font-weight:bold;">#360538</code></td>
              <td>54, 5, 56</td>
              <td>72, 98, 38, 56</td>
              <td>Latar panggung gala, sampul dokumen mewah, kaos panitia</td>
            </tr>
            <tr>
              <td colspan="6" style="background: rgba(245, 197, 56, 0.12); color: #FFEAA0; font-weight: bold; font-size: 11px;">
                ★ Warna Aksen Pendukung: Mint Pastel (<code class="mono">#A0D9CA</code>) • Pink Lembut (<code class="mono">#F5B8CB</code>) • Vanilla Custard (<code class="mono">#FFF5D6</code>)
              </td>
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


  <!-- ==================== HALAMAN 9: KARAKTERISTIK 3 HURUF RESMI ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 8 • TIPOGRAFI BAGIAN 1</div>
        <div class="header-title">3 KELUARGA HURUF RESMI ALMAMATER</div>
      </div>
      <div class="header-meta">KARAKTER &amp; PERUNTUKAN</div>
    </div>

    <div class="content-area">
      <div class="grid-3" style="margin-bottom: 3.5mm;">
        <!-- Font 1: Plus Jakarta Sans -->
        <div class="panel" style="border-top: 4px solid #F5C538;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="badge" style="background:#047857;">HURUF UTAMA INSTITUSI</span>
            <span class="mono" style="font-size:10px; color:#FFEAA0;">.TTF &bull; .OTF</span>
          </div>
          <div class="callout-title" style="margin-top: 2.5mm; font-size: 16px;">Plus Jakarta Sans</div>
          <p style="font-size: 11.5px; color: #E5D2EC;">Huruf sans-serif modern berdaya baca tinggi untuk surat dinas, proposal kegiatan, publikasi Instagram, materi presentasi, dan teks website sekolah.</p>
          <div style="margin-top: auto; padding: 2.5mm; background: rgba(0,0,0,0.35); border-radius: 4px; font-size: 11px;">
            <strong>ExtraBold (800)</strong>: Tajuk Utama Spanduk &amp; Poster<br>
            <strong>SemiBold (600)</strong>: Sub-judul &amp; Kategori Lomba<br>
            <strong>Regular (400)</strong>: Isi Paragraf Surat &amp; Deskripsi
          </div>
        </div>

        <!-- Font 2: Cinzel -->
        <div class="panel" style="border-top: 4px solid #E09D17;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="badge" style="background:#5C186B;">SEREMONIAL &amp; KEHORMATAN</span>
            <span class="mono" style="font-size:10px; color:#FFEAA0;">.TTF</span>
          </div>
          <div class="callout-title cinzel" style="margin-top: 2.5mm; font-size: 16px; color:#FFEAA0;">Cinzel</div>
          <p style="font-size: 11.5px; color: #E5D2EC;">Huruf serif prasasti klasik berwibawa tinggi untuk menegaskan sejarah akademik 44 tahun SMAN 1 Gedeg pada media kehormatan almamater.</p>
          <div style="margin-top: auto; padding: 2.5mm; background: rgba(0,0,0,0.35); border-radius: 4px; font-size: 11px;">
            <strong>Format Wajib:</strong> Seluruhnya Huruf Kapital (ALL CAPS)<br>
            <strong>Spasi Antarhuruf:</strong> Wajib renggang (tracking +100 s.d. +200)<br>
            <strong>Penerapan:</strong> Piagam, Tiket Emas, Sertifikat, Plakat
          </div>
        </div>

        <!-- Font 3: Playfair Display / Aversa -->
        <div class="panel" style="border-top: 4px solid #F7D160;">
          <div style="display:flex; justify-content:space-between; align-items:center;">
            <span class="badge" style="background:#B6580B;">PENTAS SENI &amp; TEMA</span>
            <span class="mono" style="font-size:10px; color:#FFEAA0;">.TTF</span>
          </div>
          <div class="callout-title playfair" style="margin-top: 2.5mm; font-size: 16px; color:#FFEAA0;">Playfair / AVERSA</div>
          <p style="font-size: 11.5px; color: #E5D2EC;">Huruf bergaya panggung teatrikal dengan kontras garis anggun untuk tajuk pementasan seni kreatif siswa bertema AVERSA.</p>
          <div style="margin-top: auto; padding: 2.5mm; background: rgba(0,0,0,0.35); border-radius: 4px; font-size: 11px;">
            <strong>Karakteristik:</strong> Artistik, Ceria, Dinamis, Berkesan<br>
            <strong>Peran:</strong> Tajuk Pentas Seni &amp; Judul Banner Panggung<br>
            <strong>Larangan:</strong> Tidak digunakan untuk naskah surat dinas
          </div>
        </div>
      </div>

      <!-- Tabel Hierarki Teks -->
      <div class="panel" style="flex: 1; padding: 3mm;">
        <div class="panel-header cinzel" style="font-size: 13px;">PEDOMAN SKALA DAN UKURAN HURUF YANG DIANJURKAN</div>
        <table>
          <thead>
            <tr>
              <th>Kegunaan Teks</th>
              <th>Ukuran di Layar/Medsos</th>
              <th>Ukuran di Media Cetak</th>
              <th>Keluarga Huruf &amp; Bobot</th>
              <th>Contoh Media Penerapan</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Judul Utama Panggung</strong></td>
              <td><code>56px – 72px</code></td>
              <td><code>36pt – 48pt</code></td>
              <td>Plus Jakarta Sans / Playfair (Bold)</td>
              <td>Spanduk Panggung Akbar, Baliho Gerbang Depan</td>
            </tr>
            <tr>
              <td><strong>Judul Poster Acara</strong></td>
              <td><code>40px – 48px</code></td>
              <td><code>26pt – 30pt</code></td>
              <td>Plus Jakarta Sans (ExtraBold 800)</td>
              <td>Poster Perlombaan, Pengumuman Acara Puncak</td>
            </tr>
            <tr>
              <td><strong>Sub-Judul &amp; Kategori</strong></td>
              <td><code>28px – 32px</code></td>
              <td><code>18pt – 22pt</code></td>
              <td>Plus Jakarta Sans (SemiBold 600)</td>
              <td>Kategori Lomba Siswa, Jadwal Pelaksanaan</td>
            </tr>
            <tr>
              <td><strong>Keterangan Waktu &amp; Lokasi</strong></td>
              <td><code>20px – 24px</code></td>
              <td><code>14pt – 16pt</code></td>
              <td>Plus Jakarta Sans (Medium 500)</td>
              <td>Waktu Acara, Lokasi Panggung, Syarat Pendaftaran</td>
            </tr>
            <tr>
              <td><strong>Isi Teks Paragraf</strong></td>
              <td><code>14px – 16px</code></td>
              <td><code>10pt – 11pt</code></td>
              <td>Plus Jakarta Sans (Regular 400)</td>
              <td>Surat Edaran, Proposal Sponsor, Narasi Berita</td>
            </tr>
            <tr>
              <td><strong>Teks Piagam &amp; Lencana</strong></td>
              <td><code>18px – 28px</code></td>
              <td><code>12pt – 18pt</code></td>
              <td>Cinzel (Bold 700 / ALL CAPS)</td>
              <td>Tiket Emas, Nama Almamater, Piagam Kejuaraan</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 09</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 10: ATURAN TIPOGRAFI, PASANGAN HURUF & UNDUHAN ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 9 • TIPOGRAFI BAGIAN 2</div>
        <div class="header-title">PEDOMAN PENERAPAN, PASANGAN HURUF &amp; UNDUHAN BERKAS</div>
      </div>
      <div class="header-meta">PANDUAN &amp; UNDUHAN FONT</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <!-- Kolom Kiri: Pasangan Huruf & Aturan Spasi -->
        <div class="panel">
          <div class="panel-header cinzel">1. PASANGAN HURUF RESMI (FONT PAIRING)</div>
          
          <div class="callout-row" style="margin-bottom: 2mm;">
            <div class="callout-idx">A</div>
            <div class="callout-body">
              <div class="callout-title">DOKUMEN RESMI &amp; PIAGAM KEHORMATAN</div>
              <p class="callout-desc">
                <strong>Judul / Tajuk:</strong> Cinzel (Bold, ALL CAPS, spasi renggang).<br>
                <strong>Isi / Keterangan:</strong> Plus Jakarta Sans (Regular / Medium).
              </p>
            </div>
          </div>

          <div class="callout-row" style="margin-bottom: 2mm;">
            <div class="callout-idx">B</div>
            <div class="callout-body">
              <div class="callout-title">MEDIA SOSIAL &amp; POSTER UMUM</div>
              <p class="callout-desc">
                <strong>Judul Utama:</strong> Plus Jakarta Sans (ExtraBold 800).<br>
                <strong>Subjudul:</strong> Plus Jakarta Sans (SemiBold 600).<br>
                <strong>Isi Paragraf:</strong> Plus Jakarta Sans (Regular 400).
              </p>
            </div>
          </div>

          <div class="callout-row" style="margin-bottom: 2mm;">
            <div class="callout-idx">C</div>
            <div class="callout-body">
              <div class="callout-title">PENTAS SENI &amp; FESTIVAL AVERSA</div>
              <p class="callout-desc">
                <strong>Tajuk Panggung:</strong> Playfair Display / Kaligrafi AVERSA.<br>
                <strong>Keterangan Waktu &amp; Bintang Tamu:</strong> Plus Jakarta Sans (SemiBold).
              </p>
            </div>
          </div>

          <div style="margin-top: auto; padding: 2.5mm; background: rgba(245,197,56,0.08); border-left: 3px solid #F5C538; font-size: 11.5px; border-radius: 4px;">
            <strong>Aturan Spasi (Leading):</strong> Jarak antarbaris teks paragraf wajib 1,4 hingga 1,6 kali ukuran huruf agar mata pembaca tidak cepat lelah.
          </div>
        </div>

        <!-- Kolom Kanan: Aturan Ketat & Unduhan Berkas -->
        <div class="panel darker">
          <div class="panel-header cinzel">2. ATURAN PENGGUNAAN &amp; LOKASI UNDUHAN FONT</div>

          <div style="display:flex; flex-direction:column; gap:2mm; margin-bottom: 3mm;">
            <div style="background: rgba(239,68,68,0.12); padding: 2.5mm; border-left: 3px solid #EF4444; border-radius: 4px; font-size: 11.5px;">
              <strong style="color:#FFAAAA;">❌ Hal yang Dilarang:</strong><br>
              &bull; Dilarang menarik huruf secara paksa (distorsi/gepeng).<br>
              &bull; Dilarang mengganti jenis huruf dengan font kasual sembarangan.<br>
              &bull; Dilarang memberi efek bayangan hitam tebal yang merusak keterbacaan.
            </div>

            <div style="background: rgba(16,185,129,0.12); padding: 2.5mm; border-left: 3px solid #10B981; border-radius: 4px; font-size: 11.5px;">
              <strong style="color:#A7F3D0;">✅ Hal yang Wajib:</strong><br>
              &bull; Menggunakan jenis huruf resmi yang telah disediakan di repositori.<br>
              &bull; Huruf Cinzel wajib berjarak renggang (tracking +100 s.d. +200).
            </div>
          </div>

          <div style="margin-top: auto; background: rgba(0,0,0,0.4); padding: 3mm; border: 1px dashed rgba(245,197,56,0.4); border-radius: 6px;">
            <strong style="color: #FFEAA0; font-size: 12px;">📁 Direktori Unduhan Font Siap Pasang (.ttf &amp; .otf):</strong>
            <p style="font-size: 11px; margin: 1.5mm 0 2mm 0; color: #D6BDDF;">
              Seluruh berkas font asli telah disediakan langsung di repositori proyek agar panitia dan desainer tinggal mengunduh dan memasangnya:
            </p>
            <div style="display: flex; flex-direction: column; gap: 1.5mm; font-size: 11px;">
              <div><code class="mono" style="color:#F7D160;">assets/fonts/plus-jakarta-sans/</code> &rarr; Format TTF &amp; OTF</div>
              <div><code class="mono" style="color:#F7D160;">assets/fonts/cinzel/</code> &rarr; Format TTF &amp; Variable TTF</div>
              <div><code class="mono" style="color:#F7D160;">assets/fonts/playfair-display/</code> &rarr; Format Variable TTF</div>
            </div>
            <div style="font-size: 10px; color: #A895AD; margin-top: 2mm;">
              Lisensi: SIL Open Font License (OFL) &bull; Bebas &amp; legal untuk seluruh media sekolah.
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 10</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 11: AREA AMAN & UKURAN MINIMAL ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 10 • ATURAN PENGGUNAAN</div>
        <div class="header-title">AREA AMAN BEBAS GANGGUAN DAN UKURAN MINIMAL</div>
      </div>
      <div class="header-meta">BATAS RUANG DAN UKURAN</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="panel">
          <div class="panel-header cinzel">1. AREA AMAN BEBAS GANGGUAN (CLEAR SPACE)</div>
          <div class="img-box darker" style="height: 56mm; margin-bottom: 3mm; border: 2px dashed #F5C538;">
            <div style="position: relative; width: 55mm; height: 46mm; display: flex; justify-content: center; align-items: center;">
              <img src="{img_logo_color}" style="max-height: 40mm;" alt="Area Aman Lambang">
              <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; border: 1.5px dashed rgba(245,197,56,0.7); pointer-events: none;"></div>
            </div>
          </div>
          <p style="text-align: justify; font-size: 12.5px;">
            Area aman adalah batas ruang kosong di sekeliling lambang yang tidak boleh dimasuki oleh teks, logo sponsor lain, foto, maupun garis tepi potong cetakan.
          </p>
          <div style="margin-top: auto; padding: 3mm; background: rgba(245, 197, 56, 0.1); border-radius: 4px; font-size: 12px;">
            <strong style="color: #FFEAA0;">Ketentuan Area Aman:</strong><br>
            Beri jarak ruang bebas sebesar <strong>1/4 tinggi lambang</strong> di sekeliling sisi atas, kanan, bawah, dan kiri lambang agar tampil jelas dan tidak terhimpit.
          </div>
        </div>

        <div class="panel darker">
          <div class="panel-header cinzel">2. UKURAN MINIMAL LAMBANG</div>
          <p style="text-align: justify; font-size: 12.5px; margin-bottom: 3.5mm;">
            Agar paruh rajawali, angka 44, dan kobaran api tetap terlihat jelas dan tidak buram, hindari mengecilkan lambang melebihi batas berikut:
          </p>

          <div style="display: flex; gap: 4mm; margin-bottom: 3.5mm;">
            <div class="panel" style="flex: 1; padding: 3.5mm; text-align: center; align-items: center;">
              <img src="{img_logo_color}" style="height: 36px; width: auto; margin-bottom: 2mm;" alt="Min Digital">
              <strong style="color: #F5C538; font-size: 12.5px;">MEDIA DIGITAL</strong>
              <span style="font-size: 11.5px; color: #D6BDDF;">Tinggi Min: <strong>32 Piksel</strong><br>(Contoh: Ikon Medsos / Web)</span>
            </div>

            <div class="panel light" style="flex: 1; padding: 3.5mm; text-align: center; align-items: center;">
              <img src="{img_logo_linecut}" style="height: 42px; width: auto; margin-bottom: 2mm;" alt="Min Print">
              <strong style="color: #310603; font-size: 12.5px;">MEDIA CETAK</strong>
              <span style="font-size: 11.5px; color: #444444;">Tinggi Min: <strong>15 Milimeter</strong><br>(Contoh: Lencana Pin Baju)</span>
            </div>
          </div>

          <div style="margin-top: auto; padding: 3mm; background: rgba(0,0,0,0.4); border-left: 3.5px solid #F5C538; border-radius: 4px; font-size: 11.5px;">
            <strong>Tips Cetak Ukuran Kecil:</strong><br>
            Jika mencetak di bawah 25 mm atau membuat grafir tumbler, gunakan berkas lambang versi garis (<code>logo-linecut-black.svg</code>) agar detailnya tetap rapi dan tidak meluber.
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 11</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 12: ELEMEN GRAFIS PENDUKUNG ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 11 • ELEMEN PENDUKUNG</div>
        <div class="header-title">8 ELEMEN GRAFIS PENDUKUNG RESMI</div>
      </div>
      <div class="header-meta">ELEMEN GRAFIS</div>
    </div>

    <div class="content-area">
      <div class="grid-4" style="height: 100%;">
        <!-- Item 1: Ticket -->
        <div class="panel" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_ticket}" alt="Golden Ticket">
          </div>
          <div style="margin-top: 2.5mm;">
            <strong style="color: #FFEAA0; font-size: 12px;">TIKET EMAS KLASIK</strong>
            <p style="font-size: 11px; margin-top: 1mm;">Lencana tiket emas dengan bingkai ukiran untuk undangan khusus dan kupon acara.</p>
          </div>
        </div>

        <!-- Item 2: Magic Hat -->
        <div class="panel" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_hat}" alt="Top Hat">
          </div>
          <div style="margin-top: 2.5mm;">
            <strong style="color: #FFEAA0; font-size: 12px;">TOPI PESULAP UNGU</strong>
            <p style="font-size: 11px; margin-top: 1mm;">Topi pesulap ungu dengan pita emas untuk ornamen pentas seni dan karnaval.</p>
          </div>
        </div>

        <!-- Item 3: Lollipop -->
        <div class="panel" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_lollipop}" alt="Swirl Lollipop">
          </div>
          <div style="margin-top: 2.5mm;">
            <strong style="color: #FFEAA0; font-size: 12px;">PERMEN SPIRAL PASTEL</strong>
            <p style="font-size: 11px; margin-top: 1mm;">Lolipop spiral toska mint, pink ceria, dan vanilla untuk materi promosi bazar siswa.</p>
          </div>
        </div>

        <!-- Item 4: Golden Cane -->
        <div class="panel" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_cane}" alt="Golden Cane">
          </div>
          <div style="margin-top: 2.5mm;">
            <strong style="color: #FFEAA0; font-size: 12px;">TONGKAT PESULAP EMAS</strong>
            <p style="font-size: 11px; margin-top: 1mm;">Tongkat kayu mahoni dengan kenop bola emas untuk aksen dekorasi panggung.</p>
          </div>
        </div>

        <!-- Item 5: Bonbon Pink -->
        <div class="panel" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_bonbon}" alt="Wrapped Bonbon">
          </div>
          <div style="margin-top: 2.5mm;">
            <strong style="color: #FFEAA0; font-size: 12px;">PERMEN BONBON PINK</strong>
            <p style="font-size: 11px; margin-top: 1mm;">Permen bungkus satin warna pink ceria dengan ikatan pita emas yang manis.</p>
          </div>
        </div>

        <!-- Item 6: Rose -->
        <div class="panel" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_rose}" alt="Confectionery Rose">
          </div>
          <div style="margin-top: 2.5mm;">
            <strong style="color: #FFEAA0; font-size: 12px;">BUNGA MAWAR GULA</strong>
            <p style="font-size: 11px; margin-top: 1mm;">Mawar merah anggur dan daun toska untuk dekorasi ucapan selamat dan apresiasi.</p>
          </div>
        </div>

        <!-- Item 7: Glasses -->
        <div class="panel" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_glasses}" alt="Whimsical Glasses">
          </div>
          <div style="margin-top: 2.5mm;">
            <strong style="color: #FFEAA0; font-size: 12px;">KACAMATA UNIK KUNINGAN</strong>
            <p style="font-size: 11px; margin-top: 1mm;">Bingkai bundar kuningan emas dengan lensa kilau untuk elemen desain ekspresif.</p>
          </div>
        </div>

        <!-- Item 8: Stardust -->
        <div class="panel" style="padding: 3mm;">
          <div class="img-box" style="height: 38mm;">
            <img src="{img_stardust}" alt="Stardust Stars">
          </div>
          <div style="margin-top: 2.5mm;">
            <strong style="color: #FFEAA0; font-size: 12px;">BINTANG KILAU EMAS</strong>
            <p style="font-size: 11px; margin-top: 1mm;">Gugusan bintang empat sudut berkilau untuk taburan kilauan di poster dan media sosial.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 12</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 13: LATAR BELAKANG RESMI ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 12 • LATAR BELAKANG</div>
        <div class="header-title">PILIHAN LATAR MEDIA SOSIAL DAN PANGGUNG</div>
      </div>
      <div class="header-meta">FEED (1:1) DAN STORY (9:16)</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="panel">
          <div class="panel-header cinzel">1. LATAR KINCIR TOSKA DAN KREM (CERIA)</div>
          <div class="img-box darker" style="height: 62mm; margin-bottom: 3mm;">
            <img src="{img_bg_pinwheel}" style="max-height: 58mm;" alt="Latar Kincir Toska">
          </div>
          <p style="font-size: 12.5px; text-align: justify;">
            <strong>Suasana Visual:</strong> Nuansa keceriaan kincir spiral toska mint pastel dan krem vanilla yang lembut, ramah, dan bersahabat.
          </p>
          <div style="margin-top: auto; padding: 2.5mm; background: rgba(0,0,0,0.35); border-radius: 4px; font-size: 11.5px;">
            <strong>Penggunaan:</strong> Postingan media sosial tentang perlombaan, info bazar kuliner siswa, dan kartu ucapan Dies Natalis bertema ceria.
          </div>
        </div>

        <div class="panel darker">
          <div class="panel-header cinzel">2. LATAR UNGU BELUDRU DAN BINTANG EMAS (MEGAH)</div>
          <div class="img-box darker" style="height: 62mm; margin-bottom: 3mm;">
            <img src="{img_bg_velvet}" style="max-height: 58mm;" alt="Latar Ungu Beludru">
          </div>
          <p style="font-size: 12.5px; text-align: justify;">
            <strong>Suasana Visual:</strong> Nuansa panggung akbar ungu beludru malam dengan lengkungan taburan debu bintang emas yang megah dan berwibawa.
          </p>
          <div style="margin-top: auto; padding: 2.5mm; background: rgba(0,0,0,0.35); border-radius: 4px; font-size: 11.5px;">
            <strong>Penggunaan:</strong> Acara malam puncak inagurasi, backdrop panggung pentas seni akbar, sampul proposal sponsor resmi, dan piagam kehormatan.
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 13</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 14: APLIKASI CENDERA MATA ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 13 • CENDERA MATA</div>
        <div class="header-title">PENERAPAN IDENTITAS PADA CENDERA MATA RESMI</div>
      </div>
      <div class="header-meta">CONTOH PRODUK</div>
    </div>

    <div class="content-area">
      <div class="grid-4" style="height: 100%;">
        <!-- Mockup 1 -->
        <div class="panel">
          <div class="img-box" style="height: 52mm;">
            <img src="{img_mockup_polo}" alt="Kaos Polo">
          </div>
          <div style="margin-top: 3mm;">
            <span class="badge" style="background:#4A1255;">SERAGAM PANITIA</span>
            <div class="callout-title" style="margin-top: 1.5mm;">KAOS POLO DAN T-SHIRT</div>
            <p style="font-size: 11px;">Bordir komputer benang emas diameter 65 mm di dada kiri. Bahan kain polo katun hitam yang sejuk dan nyaman dipakai.</p>
          </div>
        </div>

        <!-- Mockup 2 -->
        <div class="panel">
          <div class="img-box" style="height: 52mm;">
            <img src="{img_mockup_tumbler}" alt="Tumbler Termal">
          </div>
          <div style="margin-top: 3mm;">
            <span class="badge" style="background:#B6580B;">CENDERA MATA VIP</span>
            <div class="callout-title" style="margin-top: 1.5mm;">TUMBLER STAINLESS</div>
            <p style="font-size: 11px;">Botol minum stainless warna hitam dof dengan grafir laser lambang satu warna setinggi 80 mm yang awet dan tahan cuci.</p>
          </div>
        </div>

        <!-- Mockup 3 -->
        <div class="panel">
          <div class="img-box" style="height: 52mm;">
            <img src="{img_mockup_lanyard}" alt="Lanyard Tanda Pengenal">
          </div>
          <div style="margin-top: 3mm;">
            <span class="badge" style="background:#5C186B;">ATRIBUT PANITIA</span>
            <div class="callout-title" style="margin-top: 1.5mm;">LANYARD DAN TANDA PENGENAL</div>
            <p style="font-size: 11px;">Tali pita satin ungu halus lebar 20 mm tulisan emas bolak-balik. Kartu tanda pengenal PVC tebal laminasi dof.</p>
          </div>
        </div>

        <!-- Mockup 4 -->
        <div class="panel">
          <div class="img-box" style="height: 52mm;">
            <img src="{img_mockup_totebag}" alt="Tas Kanvas dan Pin">
          </div>
          <div style="margin-top: 3mm;">
            <span class="badge" style="background:#E09D17; color:#310603;">PAKET ALUMNI</span>
            <div class="callout-title" style="margin-top: 1.5mm;">TAS KANVAS DAN PIN LOGAM</div>
            <p style="font-size: 11px;">Tas kain kanvas putih tebal sablon emas tahan cuci, dilengkapi pin lencana logam kuningan sepuh emas.</p>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 14</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 15: PANDUAN KETEPATAN (DO'S & DON'TS) ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 14 • KEPATUHAN DESAIN</div>
        <div class="header-title">PANDUAN KETEPATAN DAN LARANGAN PENGGUNAAN</div>
      </div>
      <div class="header-meta">ATURAN PENGGUNAAN</div>
    </div>

    <div class="content-area">
      <div class="grid-2">
        <div class="panel" style="border: 2px solid #EF4444; background: #260505;">
          <div class="panel-header" style="color: #FCA5A5; font-size: 15px;">❌ 5 HAL YANG DILARANG (DON'TS)</div>
          <div style="display: flex; flex-direction: column; gap: 3.5mm; margin-top: 2mm;">
            <div style="font-size: 12.5px;">
              <strong style="color:#FFAAAA;">1. Menarik Lambang Hingga Gepeng (Distorsi):</strong><br>
              Dilarang menarik lambang hanya pada satu sisi (horizontal atau vertikal) yang membuat proporsi lambang rusak.
            </div>
            <div style="font-size: 12.5px;">
              <strong style="color:#FFAAAA;">2. Memutar Arah Hadap Lambang:</strong><br>
              Paruh rajawali dan sayap wajib selalu menghadap ke kanan atas (arah kemajuan). Dilarang diputar miring atau dibalik ke kiri.
            </div>
            <div style="font-size: 12.5px;">
              <strong style="color:#FFAAAA;">3. Mengubah Rona Warna Sembarangan:</strong><br>
              Dilarang mengganti warna lambang dengan warna neon lain (seperti biru muda, hijau terang, atau oranye menyala).
            </div>
            <div style="font-size: 12.5px;">
              <strong style="color:#FFAAAA;">4. Menempatkan di Atas Latar yang Terlalu Ramai:</strong><br>
              Hindari menaruh lambang emas langsung di atas foto yang ramai tanpa lapisan bayangan atau latar kontras.
            </div>
            <div style="font-size: 12.5px;">
              <strong style="color:#FFAAAA;">5. Menggunakan Jenis Huruf Sembarangan:</strong><br>
              Dilarang memakai font dekoratif sembarangan yang tidak sesuai dengan karakter almamater sekolah.
            </div>
          </div>
        </div>

        <div class="panel" style="border: 2px solid #10B981; background: #042417;">
          <div class="panel-header" style="color: #6EE7B7; font-size: 15px;">✅ 5 CARA PENGGUNAAN YANG BENAR (DO'S)</div>
          <div style="display: flex; flex-direction: column; gap: 3.5mm; margin-top: 2mm;">
            <div style="font-size: 12.5px;">
              <strong style="color:#A7F3D0;">1. Gunakan Berkas Vektor SVG untuk Cetak:</strong><br>
              Selalu kirimkan berkas dari folder <code>assets/svg/</code> ke pihak percetakan agar hasil cetak spanduk tajam dan tidak pecah.
            </div>
            <div style="font-size: 12.5px;">
              <strong style="color:#A7F3D0;">2. Gunakan Versi Putih di Latar Gelap atau Foto:</strong><br>
              Pakai berkas lambang putih (<code>logo-monochrome-white.png</code>) jika harus ditaruh di atas foto dokumentasi kegiatan sekolah.
            </div>
            <div style="font-size: 12.5px;">
              <strong style="color:#A7F3D0;">3. Berikan Jarak Ruang Bebas yang Cukup:</strong><br>
              Pastikan ada ruang kosong di sekeliling lambang agar lambang tetap terlihat rapi dan tidak berdesakan dengan tulisan lain.
            </div>
            <div style="font-size: 12.5px;">
              <strong style="color:#A7F3D0;">4. Terapkan Jenis Huruf Resmi Sekolah:</strong><br>
              Gunakan jenis huruf Plus Jakarta Sans dan Cinzel agar seluruh materi publikasi sekolah serasi dan profesional.
            </div>
            <div style="font-size: 12.5px;">
              <strong style="color:#A7F3D0;">5. Manfaatkan Latar Resmi yang Disediakan:</strong><br>
              Gunakan template latar yang telah disiapkan (kincir toska atau ungu malam) untuk kebutuhan postingan media sosial.
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 15</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 16: TIM KREATIF & ATRIBUSI KARYA SENI ==================== -->
  <div class="page">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 15 • ATRIBUSI KARYA</div>
        <div class="header-title">TIM KREATIF DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      </div>
      <div class="header-meta">KOLABORASI SISWA DAN GURU</div>
    </div>

    <div class="content-area">
      <div style="margin-bottom: 3.5mm; background: rgba(245, 197, 56, 0.08); border-left: 3.5px solid #F5C538; padding: 2.5mm 3.5mm; border-radius: 4px;">
        <span style="font-size: 12.5px; color: #FFEAA0; font-weight: 700;">
          Karya Kolaboratif: Lahir dari sinergi kreatif antara sketsa tangan pensil siswa, pewarnaan digital, dan digitalisasi grafis resmi.
        </span>
      </div>

      <!-- 5 Member Cards Grid -->
      <div style="display: grid; grid-template-columns: 1.15fr 1fr; gap: 4mm; flex: 1;">
        <!-- Left Column -->
        <div style="display: flex; flex-direction: column; gap: 3mm;">
          <!-- 1. Ryan Ardian -->
          <div class="panel" style="border-left: 4px solid #F5C538; padding: 3mm 3.5mm;">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <strong style="color: #FFFFFF; font-size: 13.5px;">Ryan Ardian</strong>
              <span class="badge" style="background:#5C186B;">Guru SMAN 1 Gedeg</span>
            </div>
            <div style="color: #F7D160; font-size: 11px; font-weight: 800; margin-top: 0.5mm;">Pengarah Artistik dan Digitalisasi Vektor</div>
            <p style="font-size: 11.5px; color: #E5D5EB; margin: 1mm 0 0 0; line-height: 1.4;">
              Penggagas inisiatif proyek, pengarah konsep visual, penataan sistem brand kit, rekonstruksi kurva vektor resmi, penyempurnaan keseimbangan bentuk, dan standardisasi seluruh berkas siap pakai.
            </p>
          </div>

          <!-- 2. Putri Nur Azizah -->
          <div class="panel" style="border-left: 4px solid #E09D17; padding: 3mm 3.5mm;">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <strong style="color: #FFFFFF; font-size: 13.5px;">Putri Nur Azizah</strong>
              <span class="badge" style="background:#B6580B;">Angkatan '42 (Kelas XII 6)</span>
            </div>
            <div style="color: #F7D160; font-size: 11px; font-weight: 800; margin-top: 0.5mm;">Konseptor dan Ilustrator Sketsa Pensil</div>
            <p style="font-size: 11.5px; color: #E5D5EB; margin: 1mm 0 0 0; line-height: 1.4;">
              Kreator sketsa tangan asli di atas kertas grafit. Merumuskan ide dasar figur elang rajawali, proporsi angka kembar 44, kobaran api, dan bentuk dasar lambang utama yang menjadi jiwa dari identitas ini.
            </p>
          </div>

          <!-- 3. Naysila Zahra Alsabella -->
          <div class="panel" style="border-left: 4px solid #FDF39D; padding: 3mm 3.5mm;">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <strong style="color: #FFFFFF; font-size: 13.5px;">Naysila Zahra Alsabella</strong>
              <span class="badge" style="background:#3B0C46;">Angkatan '43 (Kelas XI 1)</span>
            </div>
            <div style="color: #F7D160; font-size: 11px; font-weight: 800; margin-top: 0.5mm;">Desainer Tipografi AVERSA</div>
            <p style="font-size: 11.5px; color: #E5D5EB; margin: 1mm 0 0 0; line-height: 1.4;">
              Perancang tulisan tangan AVERSA. Menggubah seni tipografi huruf gelembung cair yang luwes, ekspresif, dan ceria yang menjadi identitas tema pementasan seni siswa.
            </p>
          </div>
        </div>

        <!-- Right Column -->
        <div style="display: flex; flex-direction: column; gap: 3mm;">
          <!-- 4. Culvar Zamiiryaser Setyaji -->
          <div class="panel" style="border-left: 4px solid #7D1B05; padding: 3mm 3.5mm;">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <strong style="color: #FFFFFF; font-size: 13.5px;">Culvar Zamiiryaser Setyaji</strong>
              <span class="badge" style="background:#7D1B05;">Angkatan '42 (Kelas XI 4)</span>
            </div>
            <div style="color: #F7D160; font-size: 11px; font-weight: 800; margin-top: 0.5mm;">Pewarnaan dan Pencahayaan Digital</div>
            <p style="font-size: 11.5px; color: #E5D5EB; margin: 1mm 0 0 0; line-height: 1.4;">
              Seniman pewarnaan digital. Menerjemahkan garis sketsa manual menjadi lukisan digital penuh rona, mengembangkan sebaran gradasi lidah api, dan eksplorasi pencahayaan awal.
            </p>
          </div>

          <!-- 5. Farel Indra Febrihansen -->
          <div class="panel" style="border-left: 4px solid #7D1B05; padding: 3mm 3.5mm;">
            <div style="display: flex; justify-content: space-between; align-items: baseline;">
              <strong style="color: #FFFFFF; font-size: 13.5px;">Farel Indra Febrihansen</strong>
              <span class="badge" style="background:#7D1B05;">Angkatan '42 (Kelas XI 4)</span>
            </div>
            <div style="color: #F7D160; font-size: 11px; font-weight: 800; margin-top: 0.5mm;">Pewarnaan dan Pencahayaan Digital</div>
            <p style="font-size: 11.5px; color: #E5D5EB; margin: 1mm 0 0 0; line-height: 1.4;">
              Seniman pewarnaan digital. Berkolaborasi mengembangkan efek pendaran cahaya keemasan hangat, kontras rona, dan memberikan kedalaman visual pada karya sketsa.
            </p>
          </div>

          <!-- Catatan Kebersamaan -->
          <div class="panel darker" style="margin-top: auto; padding: 2.5mm 3.5mm; border: 1px dashed rgba(245, 197, 56, 0.4);">
            <strong style="color: #FFEAA0; font-size: 11.5px;">Alur Kolaborasi Karya:</strong>
            <div style="font-size: 11px; color: #D6BDDF; margin-top: 1mm; line-height: 1.45;">
              Sketsa tangan pensil (Putri &amp; Naysila) → Olah rona &amp; pencahayaan digital (Culvar &amp; Farel) → Digitalisasi vektor dan brand kit resmi (Ryan Ardian).
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 16</div>
    </div>
  </div>


  <!-- ==================== HALAMAN 17: PANDUAN PENGGUNAAN & UNDUHAN BERKAS ==================== -->
  <div class="page" style="justify-content: space-between;">
    <div class="page-header">
      <div>
        <div class="header-tagline cinzel">BAB 16 • PANDUAN BERKAS</div>
        <div class="header-title">PANDUAN PRAKTIS UNDUHAN DAN FORMAT BERKAS</div>
      </div>
      <div class="header-meta">PANDUAN BERKAS</div>
    </div>

    <div class="content-area">
      <div class="grid-2" style="margin-bottom: 4mm;">
        <!-- Left: Quick Asset Directory -->
        <div class="panel">
          <div class="panel-header cinzel">LOKASI FOLDER BERKAS SIAP PAKAI</div>
          <p style="font-size: 12.5px; margin-bottom: 2.5mm;">
            Semua berkas desain resmi tersimpan rapi di dalam repositori untuk langsung digunakan oleh panitia dan siswa:
          </p>
          <div style="display: flex; flex-direction: column; gap: 2mm; font-size: 11.5px;">
            <div style="background: rgba(0,0,0,0.3); padding: 2mm; border-left: 3.5px solid #F5C538; border-radius: 4px;">
              <strong style="color:#FFEAA0;">Folder Berkas Vektor Cetak (SVG):</strong><br>
              <code class="mono" style="color:#F7D160; font-size:11px;">assets/svg/</code> &bull; Untuk spanduk panggung akbar, sablon, bordir, dan laser.
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 2mm; border-left: 3.5px solid #E09D17; border-radius: 4px;">
              <strong style="color:#FFEAA0;">Folder Gambar Transparan (PNG Ultra-HD):</strong><br>
              <code class="mono" style="color:#F7D160; font-size:11px;">assets/png/</code> &bull; Untuk Canva, PowerPoint, poster Instagram, dan video.
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 2mm; border-left: 3.5px solid #10B981; border-radius: 4px;">
              <strong style="color:#FFEAA0;">Folder Berkas Font Resmi (.TTF &amp; .OTF):</strong><br>
              <code class="mono" style="color:#F7D160; font-size:11px;">assets/fonts/</code> &bull; Berkas font asli Plus Jakarta Sans, Cinzel, &amp; Playfair Display.
            </div>
            <div style="background: rgba(0,0,0,0.3); padding: 2mm; border-left: 3.5px solid #FDF39D; border-radius: 4px;">
              <strong style="color:#FFEAA0;">Folder Elemen Pendukung dan Latar:</strong><br>
              <code class="mono" style="color:#F7D160; font-size:11px;">assets/brandkit_elements/</code> &bull; 8 ornamen modular dan preset latar feed/story.
            </div>
          </div>
        </div>

        <!-- Right: Practical Cheat Sheet Table -->
        <div class="panel darker">
          <div class="panel-header cinzel">PILIHAN FORMAT SESUAI KEBUTUHAN</div>
          <table>
            <thead>
              <tr>
                <th>Kebutuhan Desain</th>
                <th>Format Rekomendasi</th>
                <th>Lokasi Berkas</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><strong>Spanduk Panggung / Baliho</strong></td>
                <td><span class="badge" style="background:#1E3A8A;">SVG (Vektor)</span></td>
                <td><code>assets/svg/logo-color-2048.svg</code></td>
              </tr>
              <tr>
                <td><strong>Postingan Instagram / Feed</strong></td>
                <td><span class="badge" style="background:#047857;">PNG (Transparan)</span></td>
                <td><code>assets/png/logo-color-2048.png</code></td>
              </tr>
              <tr>
                <td><strong>Story, Reels, Video Bumper</strong></td>
                <td><span class="badge" style="background:#047857;">PNG (Putih)</span></td>
                <td><code>assets/png/logo-monochrome-white.png</code></td>
              </tr>
              <tr>
                <td><strong>Bordir Kaos / Sablon Seragam</strong></td>
                <td><span class="badge" style="background:#1E3A8A;">SVG (Garis)</span></td>
                <td><code>assets/svg/logo-linecut-black.svg</code></td>
              </tr>
              <tr>
                <td><strong>Grafir Laser Tumbler Botol</strong></td>
                <td><span class="badge" style="background:#1E3A8A;">SVG (Garis)</span></td>
                <td><code>assets/svg/logo-linecut-black.svg</code></td>
              </tr>
              <tr>
                <td><strong>Ketik Naskah / Canva / Corel</strong></td>
                <td><span class="badge" style="background:#10B981;">TTF / OTF</span></td>
                <td><code>assets/fonts/</code> (Pasang font resmi)</td>
              </tr>
            </tbody>
          </table>

          <div style="margin-top: auto; padding: 2.5mm; background: rgba(245, 197, 56, 0.08); border-radius: 4px; font-size: 11px;">
            <strong style="color: #FFEAA0;">Penyelenggara dan Almamater:</strong><br>
            Panitia Dies Natalis ke-44 • <strong>SMA Negeri 1 Gedeg</strong><br>
            Kecamatan Gedeg, Kabupaten Mojokerto, Jawa Timur (1982—2026).
          </div>
        </div>
      </div>

      <!-- Quick Helpful Bar -->
      <div class="panel highlight" style="padding: 3mm 4mm; flex-direction: row; justify-content: space-between; align-items: center;">
        <div>
          <strong style="color: #FFFFFF; font-size: 13px;">Butuh Bantuan Teknis Terkait Berkas Desain atau Font?</strong><br>
          <span style="font-size: 11.5px; color: #E5D5EB;">Hubungi Tim Kreatif Desain dan Multimedia Panitia Dies Natalis ke-44 SMAN 1 Gedeg.</span>
        </div>
        <div class="badge" style="background:#F5C538; color:#1C0521; font-size:11px; padding:3px 10px; font-weight:900;">
          DIES NATALIS 44 • AVERSA
        </div>
      </div>
    </div>

    <div class="page-footer">
      <div>BUKU PEDOMAN IDENTITAS VISUAL • DIES NATALIS KE-44 SMAN 1 GEDEG</div>
      <div class="page-num">HALAMAN 17 (SELESAI)</div>
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
    print("=== MEMBANGUN BUKU PEDOMAN IDENTITAS VISUAL DIES NATALIS KE-44 (EDISI TIPOGRAFI LENGKAP & FONT DOWNLOAD) ===")
    html_content = build_html()
    HTML_OUT.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT.write_text(html_content, encoding="utf-8")
    print(f"Berkas HTML Tersimpan: {HTML_OUT}")

    render_html_to_pdf(HTML_OUT, PDF_OUT)

    if PDF_OUT.exists():
        size_mb = PDF_OUT.stat().st_size / (1024 * 1024)
        print(f"Berkas PDF Siap: {PDF_OUT} ({size_mb:.2f} MB)")

if __name__ == "__main__":
    main()
