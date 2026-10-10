# METODOLOGI TRACING & REKONSTRUKSI VEKTOR MASTER V6
## DIES NATALIS KE-44 SMA NEGERI 1 GEDEG

---

## 1. PENDAHULUAN & TUJUAN REKONSTRUKSI

Dokumen ini memuat penjelasan teknis dan metodologis mengenai proses digitalisasi, penarikan garis (*tracing*), pemurnian kurva geometris, hingga perampungan berkas vektor master **V6 Final** untuk lambang resmi **Dies Natalis ke-44 SMA Negeri 1 Gedeg**.

Tujuan utama dari rekonstruksi ini adalah mengonversi sketsa manual yang bersifat raster dan berpiksel menjadi vektor matematis beresolusi tak terbatas (*infinite resolution*). Hal ini memastikan lambang dapat dicetak pada berbagai media fisik (mulai dari lencana logam 30 mm hingga baliho panggung berukuran 10 meter) tanpa mengalami penurunan ketajaman grafis (*lossless scaling*).

---

## 2. BAHAN SUMBER & MASUKAN (*SOURCE INPUTS*)

Proses rekonstruksi bertumpu pada tiga berkas masukan primer yang disediakan oleh almamater:

1. **`raw draw.jpeg`**: Sketsa pensil grafit asli pada kertas gambar. Berkas ini merekam konsep visual orisinal figur kembar angka 44, arah hadap paruh burung rajawali, serta lingkaran pandu manual awal.
2. **`digital hand draw.PNG`**: Lukisan tangan digital raster berwarna (RGB 24-bit). Berkas ini menentukan batas siluet luar, sebaran bidang warna, dan arah pancaran gradasi api.
3. **`coolors.jpeg`**: Dokumen acuan palet warna resmi (*Master Chromatic Palette*) yang menetapkan nilai heksadesimal delapan warna standar almamater.

---

## 3. PERANGKAT & TEKNOLOGI (*TOOLS & STACK*)

Seluruh proses penarikan garis dan kalibrasi kurva dikerjakan secara komputasional (*algorithmic vectorization*) menggunakan bahasa pemrograman **Python 3.10+** dengan memanfaatkan pustaka grafis dan komputasi saintifik berikut:

| Nama Alat / Pustaka | Versi | Peran & Fungsi Teknis |
|---|---|---|
| **Python** | 3.10+ | Bahasa skrip utama untuk otomatisasi kalkulasi titik dan pembuatan berkas SVG. |
| **OpenCV (`cv2`)** | 4.8+ | Pengolahan citra digital: binerisasi adaptif, reduksi derau (*Gaussian blur*), dan deteksi kontur (*contour extraction*). |
| **NumPy** | 1.24+ | Operasi matriks koordinat $(x, y)$, perhitungan vektor tangen, dan normalisasi jarak antar-garis. |
| **SciPy (`scipy.interpolate`)** | 1.11+ | Penghalusan kurva *spline* dan penyesuaian parameter titik kontrol Bezier kubik (*cubic Bezier fitting*). |
| **svgwrite** | 1.4+ | Pustaka pembangun struktur XML SVG vektor murni berstandar W3C tanpa ketergantungan perangkat lunak bajakan. |
| **CairoSVG** | 2.7+ | Mesin perender (*rasterizer*) berbasis vektor untuk menghasilkan citra pratinjau PNG resolusi ultra-tinggi (2048x2048 piksel). |
| **Matplotlib** | 3.8+ | Visualisasi inspeksi kisi-kisi matematis (*geometric construction grid inspection*). |

---

## 4. TAHAPAN METODOLOGI PENGERJAAN (*TRACE PIPELINE*)

Proses pengolahan berlangsung melalui empat tahapan utama:

```
[raw draw.jpeg] & [digital hand draw.PNG]
                   │
                   ▼ (Tahap 1: Pengolahan Citra Digital)
      [Binerisasi Otsu & Deteksi Tepi Canny]
                   │
                   ▼ (Tahap 2: Ekstraksi Koordinat Kontur)
     [Sampling Titik Kontur & Penskalaan Kanvas 2048x2048]
                   │
                   ▼ (Tahap 3: Konstruksi Kurva Bezier Matematis)
       [Penyusunan Busur Lingkaran Konsentris V6]
                   │
                   ▼ (Tahap 4: Pembagian Faset & Pewarnaan)
       [Vektor Master V6 Final (SVG & PNG Ultra-HD)]
```

### Tahap 1: Pra-pengolahan Citra (*Image Preprocessing*)
1. Citra raster masukan dibaca melalui modul `cv2.imread()`.
2. Penerapan filter perataan kontras adaptif (*Contrast Limited Adaptive Histogram Equalization* / CLAHE) untuk memisahkan garis siluet dari artefak latar belakang kertas.
3. Penerapan ambang batas binerisasi Otsu (*Otsu's thresholding*) guna menghasilkan masker biner hitam-putih murni berukuran $2048 \times 2048$ piksel.

### Tahap 2: Ekstraksi Kontur & Dekomposisi Titik
1. Modul `cv2.findContours()` dengan parameter `RETR_TREE` dan `CHAIN_APPROX_NONE` dijalankan untuk memperoleh seluruh titik batas siluet luar dan lubang faset bagian dalam.
2. Titik-titik koordinat mentah disaring menggunakan algoritma *Douglas-Peucker* (`cv2.approxPolyDP()`) untuk mengeliminasi titik redundan yang berjarak kurang dari 1,5 piksel tanpa mengubah bentuk dasar.

### Tahap 3: Konstruksi Kurva Bezier Kubik & Harmonisasi Busur Konsentris
1. Koordinat poligon hasil ekstraksi diubah menjadi perintah kurva Bezier kubik (`C x1 y1, x2 y2, x y` pada sintaks SVG).
2. Setiap titik pertemuan kurva (*tangent anchor point*) dihitung vektor gradiennya sehingga perpindahan antarlengkung berlangsung secara kontinu tanpa sudut patah tajam (*smooth $C^1$ continuity*).
3. Penerapan perhitungan busur lingkaran konsentris murni (*circular tangent arcs*) pada tulang punggung tengah (*medial spine*) untuk menjamin keselarasan simetri 100%.

### Tahap 4: Struktur Faset Trimatra (*Layered 3D Faceting*) & Gradasi Warna
1. Jalur vektor dipilah menjadi empat lapisan faset yang tumpang-tindih (*overlapping hierarchical layers*):
   - **Lapisan 1: Dasar Kontur & Api Berkobar (`facet-base`)**: Siluet terluar bergradasi perunggu tembaga (`#B6580B` ke `#F5C538`).
   - **Lapisan 2: Tubuh Angka Kembar 44 (`facet-marigold`)**: Tubuh utama berwarna kuning marigold (`#E09B17`).
   - **Lapisan 3: Tulang Punggung Simetris (`facet-vivid`)**: Garis akselerasi tengah berwarna emas terang (`#F5C538`).
   - **Lapisan 4: Siluet Kepala & Paruh Rajawali (`facet-champagne`)**: Puncak kilau berwarna sampanye cerah (`#F7D160` dan `#FDF39D`).
2. Seluruh warna dipetakan secara presisi ke acuan Coolors resmi almamater.

---

## 5. RIWAYAT ITERASI & EVALUASI VERSI (V1 HINGGA V6)

Penyempurnaan lambang tidak diselesaikan dalam satu kali proses, melainkan melalui enam fase pengujian mutu (*quality audit*):

### Versi 1 (V1 — *Initial Contour Trace*)
* **Karakteristik**: Penarikan kontur otomatis langsung dari citra raster.
* **Kelemahan Terdeteksi**: Garis tepi masih kasar, bergerigi (*pixelated artifacts*), dan sudut lengkungan belum simetris.

### Versi 2 (V2 — *Bezier Smoothing*)
* **Karakteristik**: Penerapan penghalusan Bezier kubik awal pada seluruh jalur luar.
* **Kelemahan Terdeteksi**: Bentuk sayap kanan dan kepala burung rajawali mulai terbentuk, tetapi ketebalan garis faset masih timpang.

### Versi 3 (V3 — *Circular Arc Guidelines*)
* **Karakteristik**: Pemanfaatan lingkaran bantu matematis untuk merapikan lengkungan utama.
* **Kelemahan Terdeteksi**: Bagian kepala dan badan sudah proporsional, tetapi ujung ekor dan jarak antar-garis linecut masih mengalami distorsi sudut tajam.

### Versi 4 (V4 — *Linecut Spacing Calibration*)
* **Karakteristik**: Kalibrasi jarak celah antar-garis (*kerning gap*) pada varian garis kontur.
* **Kelemahan Terdeteksi**: Hasil cetak monokrom membaik, tetapi lengkungan pada ekor masih kurang melingkar (*not circular*) dan terkesan kaku.

### Versi 5 (V5 — *Tail Sweep Revision*)
* **Karakteristik**: Perbaikan sudut sapuan ekor dan penyelarasan tangen luar.
* **Kelemahan Terdeteksi**: Masih ditemukan inkonsistensi kelengkungan pada bagian pertemuan *medial spine* tengah.

### Versi 6 (V6 — *Master Final Detailing*) 🌟
* **Penyempurnaan yang Diterapkan**:
  1. **Rekonstruksi Total Medial Spine**: Tulang punggung tengah dimodelkan ulang menggunakan busur lingkaran simetris murni (*pure concentric arcs*), melenyapkan ketidakkonsistenan sudut manual.
  2. **Harmonisasi Faset 3D**: Pemotongan masker faset (*clip-path*) ditata ulang secara konsentris sehingga menghasilkan kedalaman trimatra yang bersih dan elegan.
  3. **Verifikasi Skala**: Lambang diuji pada ukuran mikro 16 piksel dan cetak makro 2048 piksel dengan hasil ketajaman 100% sempurna.
  4. **Penetapan Status**: Ditetapkan sebagai **Versi Tunggal Resmi (*Single Source of Truth*)** perayaan Dies Natalis ke-44 SMA Negeri 1 Gedeg.

---

## 6. STRUKTUR DIREKTORI & BERKAS HASIL

Seluruh berkas produksi master tersimpan secara rapi dalam struktur repositori berikut:

```text
diesnat44project/
├── raw draw.jpeg                         # Sketsa pensil asli di atas kertas
├── digital hand draw.PNG                 # Sketsa digital raster berwarna
├── coolors.jpeg                          # Dokumen palet warna resmi almamater
├── LICENSE                               # Dokumen lisensi tertutup (Proprietary)
├── README.md                             # Ringkasan utama repositori
│
├── assets/                               # Kumpulan berkas ekspor master siap pakai
│   ├── svg/                              # Vektor SVG matematis murni
│   │   ├── logo-symbol-color.svg         # Lambang utama warna penuh (Master V6)
│   │   ├── logo-linecut-black.svg        # Garis kontur presisi (Line-cut)
│   │   ├── logo-horizontal-color.svg     # Susunan horizontal teks SMAN 1 Gedeg
│   │   ├── logo-vertical-color.svg       # Susunan vertikal (Format poster)
│   │   ├── logo-monochrome-black.svg     # Versi monokrom hitam pekat
│   │   ├── logo-monochrome-white.svg     # Versi monokrom putih bersih (Inverted)
│   │   └── logo-with-grid.svg            # Konstruksi kurva & lingkaran rasio emas
│   └── png/                              # Raster PNG resolusi ultra-tinggi
│       ├── logo-symbol-color.png         # Raster 1024x1024 px transparansi alfa
│       ├── logo-color-2048.png           # Raster 2048x2048 px resolusi cetak
│       └── logo-with-grid.png            # Visualisasi cetak grid konstruksi
│
├── v6_detailing/                         # Sumber kode dan skrip generator V6
│   └── scripts/
│       ├── generate_v6_master.py         # Skrip Python pembangun seluruh aset SVG V6
│       └── render_and_verify_v6.py       # Skrip penguji rendering & ekspor PNG
│
├── tokens/                               # Spesifikasi token desain resmi
│   ├── design-tokens.json                # Nilai token format JSON
│   └── design-tokens.css                 # Variabel CSS warna & tipografi
│
├── archive/                              # Arsip riwayat pembuatan versi terdahulu
│   ├── v1_initial_trace/                 # Berkas arsip versi 1
│   ├── v2_refined/                       # Berkas arsip versi 2
│   ├── v3_revisi/                        # Berkas arsip versi 3
│   ├── v4_revisi/                        # Berkas arsip versi 4
│   └── v5_revisi/                        # Berkas arsip versi 5
│
└── docs/                                 # Dokumentasi komprehensif
    ├── BRAND_GUIDELINES.md               # Pedoman tata cara penggunaan identitas
    └── METODOLOGI_TRACING_VEKTOR.md      # Dokumen metodologi tracing (berkas ini)
```

---

## 7. CARA MENJALANKAN ULANG SKRIP GENERATOR

Bagi pengembang atau tim teknis yang ingin mereproduksi seluruh berkas vektor master secara mandiri dari baris perintah (*terminal*):

```bash
# 1. Pastikan dependensi Python terpasang
pip install opencv-python numpy scipy svgwrite cairosvg matplotlib

# 2. Jalankan skrip pembangun master V6
python3 v6_detailing/scripts/generate_v6_master.py

# 3. Jalankan skrip verifikasi dan pembuatan PNG
python3 v6_detailing/scripts/render_and_verify_v6.py
```

Skrip akan secara otomatis memvalidasi koordinat kurva Bezier dan mengekspor seluruh varian berkas SVG dan PNG ke dalam direktori `assets/` dan `v6_detailing/`.
