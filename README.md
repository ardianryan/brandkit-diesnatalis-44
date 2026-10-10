# Identitas Visual & Rekonstruksi Vektor Master V6
## Dies Natalis ke-44 SMA Negeri 1 Gedeg

Selamat datang di repositori resmi **Brand Identity & Rekonstruksi Vektor Dies Natalis ke-44 SMA Negeri 1 Gedeg** (Kabupaten Mojokerto, Jawa Timur). 

Repositori ini memuat seluruh berkas master lambang resmi beresolusi tinggi, dokumentasi metodologi penarikan garis (*vector tracing*), analisis geometris kurva Bezier, spesifikasi palet warna Coolors, dan pedoman penerapan identitas almamater.

---

## Daftar Isi
1. [Filosofi Lambang Resmi](#filosofi-lambang-resmi)
2. [Metodologi Tracing & Alat Komputasi](#metodologi-tracing--alat-komputasi)
3. [Riwayat Evolusi Perancangan (Sketsa ke V6)](#riwayat-evolusi-perancangan-sketsa-ke-v6)
4. [Sistem Palet Warna Resmi (Coolors Spec)](#sistem-palet-warna-resmi-coolors-spec)
5. [Struktur Repositori & Katalog Aset](#struktur-repositori--katalog-aset)
6. [Cara Menjalankan Skrip Generator Python](#cara-menjalankan-skrip-generator-python)
7. [Pedoman Penerapan & Cendera Mata](#pedoman-penerapan--cendera-mata)
8. [Hak Cipta & Lisensi Kepemilikan](#hak-cipta--lisensi-kepemilikan)

---

## Filosofi Lambang Resmi

Lambang Dies Natalis ke-44 SMA Negeri 1 Gedeg memadukan unsur tradisi almamater, ketegasan karakter, dan visi masa depan. Setiap lekukan garis kurva dibangun secara matematis untuk mencerminkan nilai luhur institusi:

```
          ▲ Puncak Visi Intelektual Rajawali
         / \
        /   \  Tatapan Tegas Visioner Masa Depan
       │  4  │ Sinergi Angka Kembar 44
        \   /  Lidah Api Abadi Berkobar
         \_/   Fondasi Karakter & Integritas SMAN 1 Gedeg
```

### 1. Sinergi Angka Kembar 44
Bentuk dasar lambang menyatukan dua figur angka empat yang saling bertaut dinamis. Figur kembar ini melambangkan keselarasan, persatuan civitas akademika, kedewasaan institusi selama 44 tahun dalam membina generasi bangsa, serta kebersamaan antargenerasi guru, karyawan, siswa, dan alumni.

### 2. Kepala dan Tatapan Tajam Rajawali
Pada bagian puncak lambang terpahat siluet kepala rajawali yang menatap tegas ke arah kanan atas. Simbol ini mengekspresikan kewibawaan almamater, ketajaman intelektual, keteguhan hati, dan keberanian civitas akademika dalam meraih prestasi tingkat nasional maupun global.

### 3. Lidah Api Abadi Berkobar
Lekukan yang mengalir dari dasar hingga puncak lambang melambangkan lidah api abadi. Api merepresentasikan semangat belajar yang tidak pernah padam, daya lenting (*resilience*) menghadapi tantangan zaman, kreativitas tanpa henti, dan energi kepemimpinan yang menerangi lingkungan sekitar.

### 4. Akselerasi Kurva Aerodinamis
Sayap luar dirancang dengan kelengkungan aerodinamis yang meluncur cepat ke arah kanan atas. Arah ini melambangkan orientasi masa depan, percepatan transformasi pendidikan, dan kemajuan yang berkesinambungan (*continuous advancement*).

### 5. Harmoni Tulang Punggung Medial (*Symmetrical Medial Spine*)
Pada pembaruan versi **V6 Master Final**, tulang punggung tengah (*medial spine*) disempurnakan dengan busur lingkaran konsentris simetris 100%. Harmoni garis ini menghasilkan dimensi visual trimatra (3D) yang anggun, kokoh, dan bebas dari distorsi sudut tajam.

---

## Metodologi Tracing & Alat Komputasi

Seluruh proses digitalisasi dan kalibrasi kurva dari sketsa pensil manual hingga vektor master V6 dikerjakan secara komputasional (*algorithmic vectorization*) menggunakan ekosistem **Python 3.10+**.

### Perangkat Lunak & Pustaka (*Tools & Libraries*):
* **OpenCV (`cv2`)**: Digunakan untuk pengolahan citra digital tahap awal, mencakup pemisahan latar belakang kertas (*Otsu thresholding*), perataan kontras (*CLAHE*), dan ekstraksi kontur piksel (`cv2.findContours`).
* **NumPy**: Digunakan untuk kalkulasi matriks koordinat $(x, y)$, perhitungan jarak euklides, dan normalisasi vektor tangen antartitik lengkung.
* **SciPy (`scipy.interpolate`)**: Digunakan untuk interpolasi *spline* dan penyesuaian parameter kurva Bezier kubik guna menjamin kontinuitas lengkungan (*$C^1$ smooth continuity*).
* **svgwrite**: Digunakan untuk menyusun sintaks XML SVG vektor murni berstandar W3C beresolusi tak terbatas (*lossless scaling*).
* **CairoSVG**: Digunakan untuk merender berkas SVG menjadi berkas raster cetak PNG ultra-tinggi (2048x2048 piksel) dengan transparansi alfa sempurna.
* **Matplotlib**: Digunakan untuk inspeksi kisi-kisi matematis (*geometric construction grid inspection*) pada busur rasio keemasan.

Dokumentasi matematis dan algoritma lengkap dapat dibaca pada [docs/METODOLOGI_TRACING_VEKTOR.md](docs/METODOLOGI_TRACING_VEKTOR.md).

---

## Riwayat Evolusi Perancangan (Sketsa ke V6)

Perancangan identitas visual ini melalui enam tahapan iterasi:

| Tahapan | Berkas Masukan / Hasil | Deskripsi Teknis |
| :--- | :--- | :--- |
| **01. Sketsa Pensil Awal** | `raw draw.jpeg` | Sketsa tangan pensil grafit asli di atas kertas gambar. Berisi proporsi dasar angka kembar 44, arah paruh rajawali, dan lingkaran pandu manual. |
| **02. Lukisan Tangan Digital** | `digital hand draw.PNG` | Pewarnaan tangan digital berbasis raster (RGB 24-bit). Menentukan sebaran gradasi api, kontras paruh, dan transisi ketebalan siluet. |
| **03. Vektor Kontur Awal (V1–V2)** | `archive/v1/`, `archive/v2/` | Ekstraksi kontur biner otomatis awal. Masih ditemukan sudut tajam bergerigi pada lengkungan ekor. |
| **04. Blueprint Geometris (V3)** | `archive/v3/` | Penerapan grid busur lingkaran rasio keemasan pada sayap dan kepala rajawali. |
| **05. Kalibrasi Line-Cut & Ekor (V4–V5)**| `archive/v4/`, `archive/v5/` | Penyetaraan celah antar-garis (*kerning gap*) dan perbaikan kelengkungan ujung ekor agar tidak kaku. |
| **06. Master Final V6** | `assets/` & `v6_detailing/` | **Penyempurnaan akhir**: Rekonstruksi total *medial spine* simetris 100%, 4 faset kedalaman 3D, dan standarisasi warna Coolors resmi. |

---

## Sistem Palet Warna Resmi (Coolors Spec)

Palet warna resmi dikalibrasi secara presisi mengacu pada dokumen `coolors.jpeg`:

| Nama Warna | Kode Hex | RGB | CMYK | Karakter & Peruntukan |
| :--- | :--- | :--- | :--- | :--- |
| **Obsidian Mahogany** | `#310603` | 49, 6, 3 | 48, 88, 76, 75 | Bayangan terdalam, batas siluet luar lambang, kontras monokrom pekat. |
| **Crimson Fire** | `#7D1B05` | 125, 27, 5 | 24, 96, 100, 27 | Pangkal lidah api berkobar, pembangun dimensi kedalaman. |
| **Bronze Shadow** | `#B6580B` | 182, 88, 11 | 18, 73, 100, 7 | Nada transisi hangat lekukan lipatan faset trimatra. |
| **Marigold Gold** | `#E09B17` | 224, 155, 23 | 9, 39, 99, 0 | Warna inti tubuh lambang dan sayap; memancarkan aura kemuliaan. |
| **Vivid Gold** | `#F5C538` | 245, 197, 56 | 3, 21, 84, 0 | Kilau keemasan medial spine dan aksentuasi garis dinamis utama. |
| **Champagne Gold** | `#F7D160` | 247, 209, 96 | 2, 16, 68, 0 | Sorotan cahaya puncak (*specular highlight*) pada permukaan lambang. |
| **Canary Glow** | `#FDF39D` | 253, 243, 157 | 1, 2, 44, 0 | Pendaran cahaya tertinggi, digunakan untuk gradasi aksen paruh dan api. |
| **Midnight Plum** | `#360538` | 54, 5, 56 | 72, 98, 38, 56 | Latar belakang beludru panggung gala dan cendera mata eksklusif. |

---

## Struktur Repositori & Katalog Aset

```text
diesnat44project/
├── raw draw.jpeg                         # Sketsa pensil asli di atas kertas
├── digital hand draw.PNG                 # Sketsa digital raster berwarna
├── coolors.jpeg                          # Dokumen palet warna resmi almamater
├── LICENSE                               # Dokumen lisensi kepemilikan tertutup (Proprietary)
├── README.md                             # Ringkasan utama repositori (berkas ini)
│
├── assets/                               # Kumpulan berkas ekspor master siap pakai
│   ├── svg/                              # Berkas vektor SVG resolusi tak terbatas
│   │   ├── logo-symbol-color.svg         # Simbol utama warna penuh (Master V6)
│   │   ├── logo-linecut-black.svg        # Garis kontur presisi (Line-cut)
│   │   ├── logo-horizontal-color.svg     # Susunan horizontal teks SMAN 1 Gedeg
│   │   ├── logo-vertical-color.svg       # Susunan vertikal (Format poster)
│   │   ├── logo-monochrome-black.svg     # Versi monokrom hitam pekat
│   │   ├── logo-monochrome-white.svg     # Versi monokrom putih bersih (Inverted)
│   │   └── logo-with-grid.svg            # Konstruksi kurva & lingkaran rasio emas
│   └── png/                              # Berkas raster PNG resolusi ultra-tinggi
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
│   ├── design-tokens.json                # Nilai token format JSON W3C
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
    ├── BRAND_GUIDELINES.md               # Buku pedoman tata cara penggunaan identitas
    └── METODOLOGI_TRACING_VEKTOR.md      # Metodologi teknis tracing & algoritma kurva
```

---

## Cara Menjalankan Skrip Generator Python

Untuk mereproduksi seluruh berkas SVG dan PNG master secara mandiri dari terminal:

```bash
# 1. Pasang pustaka dependensi Python
pip install opencv-python numpy scipy svgwrite cairosvg matplotlib

# 2. Jalankan skrip pembangun vektor master V6
python3 v6_detailing/scripts/generate_v6_master.py

# 3. Jalankan skrip verifikasi rendering dan ekspor PNG 2048px
python3 v6_detailing/scripts/render_and_verify_v6.py
```

---

## Pedoman Penerapan & Cendera Mata

Pedoman lengkap mengenai ukuran minimum (*minimum size*), zona bebas (*clear space*), aturan bordir kaos polo, sablon totebag, lencana pin enamel sepuh emas 24K, dan plakat akrilik dapat dipelajari secara rinci pada [docs/BRAND_GUIDELINES.md](docs/BRAND_GUIDELINES.md).

---

## Hak Cipta & Lisensi Kepemilikan

Seluruh karya cipta grafis, lambang, skrip komputasi, dan dokumentasi di dalam repositori ini dilindungi oleh undang-undang hak cipta Republik Indonesia.

Status lisensi adalah **PROPRIETARY / ALL RIGHTS RESERVED (LISENSI TERTUTUP MUTLAK)** milik:
* **SMA Negeri 1 Gedeg, Kabupaten Mojokerto**
* **Ardian Ryan**

Dilarang keras menyalin, memodifikasi, mendistribusikan, mempublikasikan ulang, atau menggunakan materi ini untuk kepentingan pihak ketiga tanpa izin tertulis resmi dari pemegang hak cipta. Teks hukum lengkap tercantum pada berkas [LICENSE](LICENSE).
