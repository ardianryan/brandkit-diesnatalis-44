import React, { useState } from 'react';
import { History, ZoomIn, X, Check, ArrowRight, Sparkles, Layers, Sliders, ShieldCheck } from 'lucide-react';

const TIMELINE_STEPS = [
  {
    step: '01',
    title: 'Raw Pencil Hand Draw',
    subtitle: 'Sketsa Tangan Pensil Asli di Kertas',
    image: '/raw draw.jpeg',
    tag: 'Konseptualisasi Manual',
    date: 'Fase Eksplorasi Awal',
    description: 'Pencarian bentuk dasar figur kembar angka 44 yang berpadu dengan kepala burung rajawali. Dibuat menggunakan pensil grafit dengan bantuan lingkaran pandu geometris manual untuk menguji kelayakan proporsi.',
    specs: ['Media: Kertas & Pensil Grafit', 'Fokus: Anatomi Angka 44 & Karakter Paruh', 'Tantangan: Menentukan titik temu antar-lengkung']
  },
  {
    step: '02',
    title: 'Digital Raster Hand Draw',
    subtitle: 'Lukisan Tangan Digital Berwarna',
    image: '/digital hand draw.PNG',
    tag: 'Eksplorasi Kromatis & Siluet',
    date: 'Fase Desain Digital',
    description: 'Penerjemahan sketsa pensil ke media raster digital dengan pen tablet. Di tahap ini, gradasi warna api mulai dirumuskan—dari merah marun gelap hingga kuning menyala—serta mempertegas ketajaman tatapan mata elang.',
    specs: ['Format: Raster PNG 24-bit', 'Fokus: Penataan Gradasi Api & Arah Cahaya', 'Tantangan: Mempertahankan kedalaman 3D visual']
  },
  {
    step: '03',
    title: 'Vektorisasi & Kalibrasi (V1–V5)',
    subtitle: 'Konstruksi Kurva Bezier Matematis',
    image: '/assets/png/logo-with-grid.png',
    tag: 'Evolusi Geometri Vektor',
    date: 'Fase Iterasi Matematis',
    description: 'Transformasi dari raster menjadi vektor garis matematis murni. Melalui evaluasi mendalam pada versi V1 hingga V5 untuk mengatasi garis ekor yang kurang konsisten, merapikan jarak antar-garis linecut, dan menstabilkan busur kurva.',
    specs: ['Format: Vektor SVG + Grid Matematis', 'Fokus: Simetri Medial Spine & Busur Konsentris', 'Tantangan: Menghilangkan distorsi sudut tajam']
  },
  {
    step: '04',
    title: 'Master V6 Final Disempurnakan',
    subtitle: 'Standar Vektor Resmi Dies Natalis 44',
    image: '/assets/svg/logo-symbol-color.svg',
    tag: 'Penyempurnaan Akhir',
    date: 'Versi Resmi Almamater',
    description: 'Puncak penyempurnaan desain lambang dengan kurva lingkaran sempurna, tulang punggung tengah (medial spine) yang simetris 100%, sistem facet kedalaman 3D presisi tinggi, dan kompatibilitas penuh untuk cetak maupun digital.',
    specs: ['Format: SVG Master + PNG 2048px Ultra-HD', 'Fokus: Keharmonisan Garis Lengkung & PBR 3D', 'Status: Disahkan untuk Seluruh Media Resmi']
  }
];

export default function EvolutionTimeline() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [activeTab, setActiveTab] = useState(0);

  return (
    <section id="riwayat" className="py-20 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold uppercase tracking-wider mb-4">
            <History className="w-3.5 h-3.5" />
            Riwayat Pembuatan Lambang
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-black title-primary tracking-tight mb-4">
            Dari Goresan Tangan Pensil <br />
            <span className="text-gold-gradient">Hingga Presisi Vektor V6 Master</span>
          </h2>
          <p className="text-themed-secondary text-sm sm:text-base leading-relaxed">
            Perjalanan perancangan identitas visual Dies Natalis ke-44 mendokumentasikan setiap fase evolusi estetika—mulai dari sketsa pensil mentah, lukisan digital pertama, hingga kalibrasi vektor geometris tingkat lanjut.
          </p>
        </div>

        {/* Interactive Comparison Preview Box */}
        <div className="card-themed p-6 sm:p-8 rounded-3xl border border-amber-500/20 mb-16 shadow-2xl">
          <div className="flex flex-wrap items-center justify-between gap-4 mb-6 pb-6 border-b border-[var(--border-subtle)]">
            <div>
              <span className="text-xs font-bold text-amber-500 dark:text-amber-400 uppercase tracking-wider block mb-1">
                Navigasi Tahapan Perancangan
              </span>
              <h3 className="font-serif text-xl sm:text-2xl font-bold title-primary">
                {TIMELINE_STEPS[activeTab].title} — {TIMELINE_STEPS[activeTab].subtitle}
              </h3>
            </div>
            
            {/* Tab Switcher */}
            <div className="flex flex-wrap gap-2 card-themed p-1.5 rounded-2xl border border-[var(--border-subtle)]">
              {TIMELINE_STEPS.map((s, idx) => (
                <button
                  key={s.step}
                  onClick={() => setActiveTab(idx)}
                  className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                    activeTab === idx
                      ? 'bg-amber-400 text-slate-950 shadow-md'
                      : 'text-themed-secondary hover:text-[var(--text-primary)]'
                  }`}
                >
                  Tahap {s.step}
                </button>
              ))}
            </div>
          </div>

          {/* Active Tab Spotlight */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            {/* Visual Preview */}
            <div className="lg:col-span-7 relative group rounded-2xl overflow-hidden card-themed aspect-video flex items-center justify-center p-4">
              <img
                src={TIMELINE_STEPS[activeTab].image}
                alt={TIMELINE_STEPS[activeTab].title}
                className="max-h-full max-w-full object-contain rounded-lg transition-transform duration-500 group-hover:scale-105"
              />
              <button
                onClick={() => setSelectedImage(TIMELINE_STEPS[activeTab])}
                className="absolute inset-0 bg-slate-950/40 opacity-0 group-hover:opacity-100 flex items-center justify-center gap-2 text-white font-semibold text-xs backdrop-blur-xs transition-opacity duration-300"
              >
                <ZoomIn className="w-5 h-5 text-amber-400" />
                <span>Klik untuk Memperbesar Resolusi Penuh</span>
              </button>
            </div>

            {/* Explanation & Technical Specs */}
            <div className="lg:col-span-5 space-y-4">
              <span className="px-3 py-1 rounded-full text-xs font-bold bg-amber-500/15 text-amber-600 dark:text-amber-400 border border-amber-500/30 inline-block">
                {TIMELINE_STEPS[activeTab].tag}
              </span>
              <p className="text-sm text-themed-secondary leading-relaxed">
                {TIMELINE_STEPS[activeTab].description}
              </p>
              
              <div className="card-themed rounded-2xl p-4 border border-[var(--border-subtle)] space-y-2">
                <span className="text-[11px] font-bold uppercase tracking-wider text-amber-500 dark:text-amber-400 block mb-2">
                  Spesifikasi Teknis Tahapan:
                </span>
                {TIMELINE_STEPS[activeTab].specs.map((item, i) => (
                  <div key={i} className="flex items-center gap-2 text-xs text-themed-secondary">
                    <Check className="w-3.5 h-3.5 text-amber-500 shrink-0" />
                    <span>{item}</span>
                  </div>
                ))}
              </div>

              <div className="pt-2 flex items-center justify-between text-xs text-themed-secondary">
                <span>Status Proses: Terarsip Aman</span>
                <button
                  onClick={() => setActiveTab((prev) => (prev + 1) % TIMELINE_STEPS.length)}
                  className="text-amber-500 hover:text-amber-600 dark:hover:text-amber-300 font-bold flex items-center gap-1"
                >
                  <span>Tahap Selanjutnya</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* 4 Cards Overview Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {TIMELINE_STEPS.map((item, index) => (
            <div
              key={item.step}
              onClick={() => setActiveTab(index)}
              className={`group card-themed rounded-3xl p-5 border cursor-pointer transition-all duration-300 flex flex-col justify-between ${
                activeTab === index
                  ? 'border-amber-500 ring-2 ring-amber-400/30'
                  : 'hover:border-amber-500/40'
              }`}
            >
              <div>
                <div className="relative aspect-video rounded-2xl overflow-hidden card-themed mb-4 flex items-center justify-center p-2">
                  <img
                    src={item.image}
                    alt={item.title}
                    className="max-h-full max-w-full object-contain group-hover:scale-105 transition-transform duration-300"
                  />
                  <span className="absolute top-2 left-2 text-[10px] font-black px-2 py-0.5 rounded-md bg-slate-950/80 text-amber-400 border border-amber-500/30 font-serif">
                    TAHAP {item.step}
                  </span>
                </div>

                <h4 className="font-serif font-bold text-base title-primary group-hover:text-amber-500 transition-colors mb-1">
                  {item.title}
                </h4>
                <p className="text-xs text-themed-secondary mb-3 leading-snug">
                  {item.subtitle}
                </p>
              </div>

              <div className="pt-3 border-t border-[var(--border-subtle)] flex items-center justify-between text-[11px] font-semibold text-amber-500">
                <span>{item.tag}</span>
                <ArrowRight className="w-3.5 h-3.5 group-hover:translate-x-1 transition-transform" />
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Lightbox Zoom Modal */}
      {selectedImage && (
        <div className="fixed inset-0 z-50 bg-slate-950/95 backdrop-blur-md flex items-center justify-center p-4">
          <div className="relative max-w-5xl w-full max-h-[90vh] flex flex-col items-center">
            <button
              onClick={() => setSelectedImage(null)}
              className="absolute -top-12 right-0 p-2 text-slate-400 hover:text-white bg-slate-900 rounded-full border border-white/10 transition-colors"
            >
              <X className="w-6 h-6" />
            </button>

            <div className="w-full bg-slate-900/60 rounded-3xl border border-white/10 p-4 flex items-center justify-center overflow-hidden">
              <img
                src={selectedImage.image}
                alt={selectedImage.title}
                className="max-h-[75vh] max-w-full object-contain rounded-2xl"
              />
            </div>

            <div className="mt-4 text-center">
              <h3 className="font-serif text-lg font-bold text-white">
                {selectedImage.title} — {selectedImage.subtitle}
              </h3>
              <p className="text-xs text-slate-400 mt-1">
                {selectedImage.description}
              </p>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
