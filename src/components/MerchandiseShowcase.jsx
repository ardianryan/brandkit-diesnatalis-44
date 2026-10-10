import React, { useState } from 'react';
import { ShoppingBag, Award, Shirt, Tag, Check, ArrowUpRight, Sparkles, Box } from 'lucide-react';

const MERCH_ITEMS = [
  {
    id: 'lanyard',
    name: 'Lanyard & Kartu Identitas Panitia',
    category: 'Atribut Resmi Kegiatan',
    tag: 'Standar Kepanitiaan',
    icon: Tag,
    material: 'Pita Satin Polyester 20mm + Kartu PVC 0.8mm',
    colorSpec: 'Latar Midnight Plum (#360538) dengan Cetak Emas Sublimasi',
    size: 'Tali 90 x 2 cm • Kartu 8.5 x 5.4 cm (Standar ISO)',
    guideline: 'Wajib menggunakan varian logo horizontal atau lambang simbol dengan teks almamater di bawahnya. Finishing kait putar nikel dan stoper keselamatan hitam.',
    mockupType: 'lanyard'
  },
  {
    id: 'polo',
    name: 'Kaus Berkerah Resmi Panitia (Polo Shirt)',
    category: 'Seragam Civitas Akademika',
    tag: 'Bordir Komputer Presisi',
    icon: Shirt,
    material: 'Lacoste Cotton Pique 24s Lembut & Adem',
    colorSpec: 'Kain Hitam Pekat (Jet Black) atau Merah Marun Gelap (#310603)',
    size: 'Lebar Bordir Dada Kiri: 68 mm • Presisi 10.000 Stitches',
    guideline: 'Lambang utama dibordir pada dada kiri dengan benang rayon emas berkilau. Bagian lengan kanan memuat teks "SMA NEGERI 1 GEDEG".',
    mockupType: 'polo'
  },
  {
    id: 'totebag',
    name: 'Tas Jinjing Kanvas (Tote Bag)',
    category: 'Cendera Mata Ramah Lingkungan',
    tag: 'Sablon Plastisol Emas',
    icon: ShoppingBag,
    material: 'Kanvas Katun Organik 14 oz Tebal',
    colorSpec: 'Varian Natural Broken White & Obsidian Black',
    size: 'Dimensi 38 x 42 cm • Panjang Tali 60 cm',
    guideline: 'Pada kain krem gunakan varian monokrom hitam atau linecut. Pada kain hitam gunakan sablon plastisol emas metalik atau foil emas tahan cuci.',
    mockupType: 'totebag'
  },
  {
    id: 'pin',
    name: 'Lencana Logam Sepuhan Emas (Enamel Pin)',
    category: 'Cendera Mata Kehormatan',
    tag: 'Gold Electroplating 24K',
    icon: Award,
    material: 'Zinc Alloy Die-Struck + Lapisan Resin Kubah Jernih',
    colorSpec: 'Sepuhan Emas Polished Gold + Enamel Hitam Halus',
    size: 'Diameter 30 mm • Ketebalan 2.5 mm • Klip Kupu-Kupu Ganda',
    guideline: 'Diberikan sebagai cendera mata eksklusif tamu kehormatan, dewan guru, dan pengurus purna osis. Dilengkapi kartu latar beludru Midnight Plum.',
    mockupType: 'pin'
  },
  {
    id: 'plakat',
    name: 'Plakat Penghargaan Akrilik & Kayu',
    category: 'Kenang-Kenangan Resmi',
    tag: 'Laser Cut & Wood Mount',
    icon: Box,
    material: 'Akrilik Bening 10mm + Dudukan Kayu Jati Solid Pernis Dof',
    colorSpec: 'Grafir Putih Es + Lempengan Kuningan Emas Cermin',
    size: 'Tinggi 22 cm • Lebar 16 cm • Alas Kayu 18 x 7 cm',
    guideline: 'Lambang dipotong laser presisi mengikuti kontur sayap V6 atau digrafir pada permukaan akrilik dengan plat dasar kuningan bertuliskan apresiasi.',
    mockupType: 'plakat'
  }
];

export default function MerchandiseShowcase() {
  const [activeItem, setActiveItem] = useState(MERCH_ITEMS[0]);

  return (
    <section id="merchandise" className="py-20 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-500 text-xs font-bold uppercase tracking-wider mb-4">
            <ShoppingBag className="w-3.5 h-3.5" />
            Penerapan Identitas &amp; Cendera Mata
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-black title-primary tracking-tight mb-4">
            Aplikasi Resmi Cendera Mata <br />
            <span className="text-gold-gradient">Dies Natalis ke-44</span>
          </h2>
          <p className="text-themed-secondary text-sm sm:text-base leading-relaxed">
            Pedoman spesifikasi teknis dan visual untuk produksi atribut kepanitiaan, seragam resmi, tanda penghargaan, dan cendera mata tamu kehormatan.
          </p>
        </div>

        {/* Interactive Showcase Box */}
        <div className="card-themed p-6 sm:p-10 rounded-3xl border border-amber-500/20 mb-12 shadow-2xl">
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-center">
            {/* Visual Mockup Stage */}
            <div className="lg:col-span-6 bg-[var(--bg-secondary)] rounded-3xl border border-[var(--border-subtle)] p-8 flex flex-col items-center justify-center min-h-[380px] relative overflow-hidden group">
              {/* Decorative Glow */}
              <div className="absolute inset-0 bg-radial from-amber-500/10 via-transparent to-transparent pointer-events-none" />

              {/* Dynamic Product Visual representation */}
              <div className="relative z-10 w-full max-w-xs flex flex-col items-center">
                {activeItem.id === 'lanyard' && (
                  <div className="w-full flex flex-col items-center">
                    <div className="w-8 h-32 bg-gradient-to-b from-[#360538] via-[#7D1B05] to-[#E09B17] rounded-full shadow-lg flex items-center justify-center p-1 border border-amber-400/30 mb-2">
                      <div className="w-1 h-20 bg-amber-200/50 rounded-full" />
                    </div>
                    <div className="w-48 h-64 bg-[var(--bg-card)] rounded-2xl border-2 border-amber-400/40 p-4 shadow-2xl flex flex-col items-center justify-between">
                      <div className="w-full text-center border-b border-[var(--border-subtle)] pb-2">
                        <span className="text-[10px] font-black tracking-widest text-amber-500 block font-serif">SMAN 1 GEDEG</span>
                        <span className="text-[9px] text-themed-secondary">PANITIA DIES NATALIS 44</span>
                      </div>
                      <img src="/assets/svg/logo-symbol-color.svg" alt="Logo" className="w-20 h-20 object-contain drop-shadow-md" />
                      <div className="w-full bg-amber-400/15 rounded-lg p-2 text-center border border-amber-400/30">
                        <span className="text-xs font-bold text-amber-500 block">KARTU PESERTA RESMI</span>
                        <span className="text-[9px] text-themed-secondary font-mono">ID: DN44-SMAN1G-2024</span>
                      </div>
                    </div>
                  </div>
                )}

                {activeItem.id === 'polo' && (
                  <div className="w-56 h-64 bg-[var(--bg-card)] rounded-3xl border border-[var(--border-subtle)] p-6 flex flex-col items-center justify-between shadow-2xl relative">
                    <div className="w-24 h-8 bg-[var(--bg-secondary)] rounded-b-xl border-b border-x border-[var(--border-subtle)] flex items-center justify-center">
                      <div className="w-2 h-2 rounded-full bg-amber-500/40 mx-1" />
                      <div className="w-2 h-2 rounded-full bg-amber-500/40 mx-1" />
                    </div>
                    <div className="absolute top-16 left-8 flex items-center gap-2 bg-[var(--bg-secondary)] p-2 rounded-xl border border-amber-400/30 shadow-lg">
                      <img src="/assets/svg/logo-symbol-color.svg" alt="Embroidery Logo" className="w-12 h-12 object-contain" />
                    </div>
                    <span className="text-[10px] font-semibold text-themed-secondary text-center">Bordir Dada Kiri (68 mm)</span>
                  </div>
                )}

                {activeItem.id === 'totebag' && (
                  <div className="w-52 h-64 bg-[var(--bg-card)] rounded-2xl border border-amber-500/30 p-5 flex flex-col items-center justify-between shadow-2xl">
                    <div className="w-20 h-10 border-t-4 border-amber-500/40 rounded-t-full" />
                    <img src="/assets/svg/logo-symbol-color.svg" alt="Tote Bag Logo" className="w-28 h-28 object-contain filter drop-shadow-lg" />
                    <span className="font-serif text-[10px] tracking-widest text-amber-500 font-bold">DIES NATALIS 44</span>
                  </div>
                )}

                {activeItem.id === 'pin' && (
                  <div className="w-48 h-48 rounded-full bg-gradient-to-tr from-amber-600 via-amber-300 to-yellow-100 p-2 shadow-2xl shadow-amber-500/30 flex items-center justify-center">
                    <div className="w-full h-full rounded-full bg-[var(--bg-card)] flex items-center justify-center p-6 border-2 border-amber-400/60">
                      <img src="/assets/svg/logo-symbol-color.svg" alt="Pin Logo" className="w-full h-full object-contain filter drop-shadow" />
                    </div>
                  </div>
                )}

                {activeItem.id === 'plakat' && (
                  <div className="w-52 h-64 flex flex-col items-center justify-end">
                    <div className="w-40 h-48 bg-[var(--bg-card)] backdrop-blur-md rounded-t-2xl border-2 border-[var(--border-subtle)] p-4 flex flex-col items-center justify-between shadow-2xl">
                      <img src="/assets/svg/logo-symbol-color.svg" alt="Plakat Logo" className="w-20 h-20 object-contain" />
                      <div className="text-center w-full">
                        <span className="text-[10px] font-serif font-black text-amber-500 block">PENGHARGAAN RESMI</span>
                        <span className="text-[8px] text-themed-secondary">DIES NATALIS KE-44</span>
                      </div>
                    </div>
                    <div className="w-48 h-8 bg-amber-950 rounded-lg border border-amber-700/50 shadow-lg flex items-center justify-center">
                      <div className="w-36 h-3 bg-amber-400/20 rounded-xs" />
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Specifications Details */}
            <div className="lg:col-span-6 space-y-5">
              <div>
                <span className="px-3 py-1 rounded-full text-xs font-bold bg-amber-500/15 text-amber-500 border border-amber-500/30 inline-block mb-2">
                  {activeItem.tag}
                </span>
                <h3 className="font-serif text-2xl sm:text-3xl font-bold title-primary mb-2">
                  {activeItem.name}
                </h3>
                <p className="text-xs text-amber-500 font-semibold">
                  Kategori: {activeItem.category}
                </p>
              </div>

              <div className="space-y-3 bg-[var(--bg-secondary)] p-5 rounded-2xl border border-[var(--border-subtle)] text-xs sm:text-sm">
                <div>
                  <span className="text-themed-secondary text-xs block mb-0.5">Spesifikasi Material:</span>
                  <span className="title-primary font-medium">{activeItem.material}</span>
                </div>
                <div>
                  <span className="text-themed-secondary text-xs block mb-0.5">Pedoman Warna:</span>
                  <span className="text-amber-500 font-medium">{activeItem.colorSpec}</span>
                </div>
                <div>
                  <span className="text-themed-secondary text-xs block mb-0.5">Ukuran &amp; Dimensi Produksi:</span>
                  <span className="title-primary font-medium">{activeItem.size}</span>
                </div>
                <div className="pt-2 border-t border-[var(--border-subtle)]">
                  <span className="text-themed-secondary text-xs block mb-0.5">Petunjuk Standardisasi:</span>
                  <p className="text-themed-secondary text-xs leading-relaxed">{activeItem.guideline}</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Thumbnail Selector List */}
        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
          {MERCH_ITEMS.map((item) => {
            const Icon = item.icon;
            const isSelected = activeItem.id === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveItem(item)}
                className={`p-4 rounded-2xl border text-left transition-all ${
                  isSelected
                    ? 'bg-amber-400 text-slate-950 font-bold shadow-lg shadow-amber-500/20 border-amber-400 -translate-y-1'
                    : 'card-themed border-[var(--border-subtle)] text-themed-secondary hover:border-amber-400/40 hover:text-amber-500'
                }`}
              >
                <Icon className={`w-5 h-5 mb-2 ${isSelected ? 'text-slate-950' : 'text-amber-500'}`} />
                <h4 className="text-xs font-bold leading-tight mb-1">{item.name.split('(')[0]}</h4>
                <span className={`text-[10px] block ${isSelected ? 'text-slate-800' : 'text-themed-tertiary'}`}>
                  {item.tag}
                </span>
              </button>
            );
          })}
        </div>
      </div>
    </section>
  );
}
