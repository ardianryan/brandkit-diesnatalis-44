import React, { useState } from 'react';
import { Download, FileCode, Image, Check, Sparkles, Filter, ExternalLink } from 'lucide-react';

const ASSET_ITEMS = [
  {
    name: 'Logo Symbol Color (Master)',
    filename: 'logo-symbol-color.svg',
    path: '/assets/svg/logo-symbol-color.svg',
    pngPath: '/assets/png/logo-symbol-color.png',
    type: 'svg',
    category: 'color',
    desc: 'Simbol utama warna penuh dengan gradasi emas dan kedalaman 3D facet.',
    badge: 'Master Utama'
  },
  {
    name: 'Logo Precision Line-Cut',
    filename: 'logo-linecut-black.svg',
    path: '/assets/svg/logo-linecut-black.svg',
    pngPath: '/assets/png/logo-linecut-black.png',
    type: 'svg',
    category: 'linecut',
    desc: 'Garis vektor kontur presisi dengan busur medial spine simetris circular.',
    badge: 'Presisi V6'
  },
  {
    name: 'Logo Horizontal Lockup',
    filename: 'logo-horizontal-color.svg',
    path: '/assets/svg/logo-horizontal-color.svg',
    pngPath: '/assets/png/logo-horizontal-color.png',
    type: 'svg',
    category: 'color',
    desc: 'Simbol berdampingan dengan tipografi resmi Cinzel "DIES NATALIS 44".',
    badge: 'Format Spanduk'
  },
  {
    name: 'Logo Vertical Lockup',
    filename: 'logo-vertical-color.svg',
    path: '/assets/svg/logo-vertical-color.svg',
    pngPath: '/assets/png/logo-vertical-color.png',
    type: 'svg',
    category: 'color',
    desc: 'Susunan vertikal simetris untuk materi poster, plakat, dan cover dokumen.',
    badge: 'Format Poster'
  },
  {
    name: 'Logo Monochrome Black',
    filename: 'logo-monochrome-black.svg',
    path: '/assets/svg/logo-monochrome-black.svg',
    pngPath: '/assets/png/logo-monochrome-black.png',
    type: 'svg',
    category: 'mono',
    desc: 'Versi monokrom hitam pekat untuk dokumen formal, cap stempel, dan kop surat.',
    badge: 'Monokrom Gelap'
  },
  {
    name: 'Logo Monochrome White (Inverted)',
    filename: 'logo-monochrome-white.svg',
    path: '/assets/svg/logo-monochrome-white.svg',
    pngPath: '/assets/png/logo-monochrome-white.png',
    type: 'svg',
    category: 'mono',
    desc: 'Versi monokrom putih bersih untuk penempatan di atas latar belakang gelap/foto.',
    badge: 'Monokrom Terang'
  },
  {
    name: 'Logo dengan Grid Geometris',
    filename: 'logo-with-grid.svg',
    path: '/assets/svg/logo-with-grid.svg',
    pngPath: '/assets/png/logo-with-grid.png',
    type: 'svg',
    category: 'linecut',
    desc: 'Garis pandu kurva rasio keemasan dan busur konstruksi matematis.',
    badge: 'Pedoman Geometri'
  },
  {
    name: 'Master Raster Ultra-HD (2048px)',
    filename: 'logo-color-2048.png',
    path: '/assets/png/logo-color-2048.png',
    pngPath: '/assets/png/logo-color-2048.png',
    type: 'png',
    category: 'color',
    desc: 'Berkas raster resolusi tinggi 2048x2048 px dengan transparansi alpha sempurna.',
    badge: '2048px Master'
  }
];

export default function AssetLibrarySection() {
  const [filter, setFilter] = useState('all');

  const filteredAssets = ASSET_ITEMS.filter((item) => {
    if (filter === 'all') return true;
    if (filter === 'svg') return item.type === 'svg';
    if (filter === 'png') return item.type === 'png';
    if (filter === 'color') return item.category === 'color';
    if (filter === 'linecut') return item.category === 'linecut';
    if (filter === 'mono') return item.category === 'mono';
    return true;
  });

  return (
    <section id="aset-unduh" className="py-20 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-500 text-xs font-bold uppercase tracking-wider mb-4">
            <FileCode className="w-3.5 h-3.5" />
            Pustaka Aset Vektor &amp; Raster
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-black title-primary tracking-tight mb-4">
            Berkas Master V6 Resolusi Tinggi <br />
            <span className="text-gold-gradient">Siap Pakai untuk Seluruh Media</span>
          </h2>
          <p className="text-themed-secondary text-sm sm:text-base leading-relaxed">
            Akses langsung ke seluruh berkas vektor SVG matematis dan raster PNG berkualitas ultra-tinggi untuk keperluan publikasi resmi SMA Negeri 1 Gedeg.
          </p>
        </div>

        {/* Filter Pills */}
        <div className="flex flex-wrap items-center justify-center gap-2 mb-10">
          {[
            { id: 'all', label: 'Semua Berkas Master' },
            { id: 'svg', label: 'Vektor SVG Murni' },
            { id: 'png', label: 'Raster PNG Ultra-HD' },
            { id: 'color', label: 'Warna Penuh (Color)' },
            { id: 'linecut', label: 'Line-Cut & Grid' },
            { id: 'mono', label: 'Monokrom' }
          ].map((btn) => (
            <button
              key={btn.id}
              onClick={() => setFilter(btn.id)}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                filter === btn.id
                  ? 'bg-amber-400 text-slate-950 shadow-lg shadow-amber-500/20 scale-105'
                  : 'card-themed border-[var(--border-subtle)] text-themed-secondary hover:text-amber-500 hover:border-amber-400/40'
              }`}
            >
              {btn.label}
            </button>
          ))}
        </div>

        {/* Assets Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {filteredAssets.map((asset) => {
            const isDarkBackgroundAsset = asset.filename.includes('white');

            return (
              <div
                key={asset.filename}
                className="group card-themed rounded-3xl p-5 border border-[var(--border-card)] hover:border-amber-400/50 transition-all duration-300 flex flex-col justify-between"
              >
                <div>
                  {/* Thumbnail stage */}
                  <div className={`aspect-square rounded-2xl mb-4 p-6 flex items-center justify-center relative overflow-hidden border border-[var(--border-subtle)] transition-transform group-hover:scale-[1.02] ${
                    isDarkBackgroundAsset ? 'bg-slate-900' : 'bg-[var(--bg-secondary)]'
                  }`}>
                    <img
                      src={asset.path}
                      alt={asset.name}
                      className="max-h-full max-w-full object-contain filter drop-shadow-md"
                    />
                    <span className="absolute top-3 left-3 text-[10px] font-bold px-2 py-0.5 rounded-md bg-[var(--bg-primary)] text-amber-500 border border-amber-500/30">
                      {asset.badge}
                    </span>
                  </div>

                  <h4 className="font-serif font-bold text-base title-primary group-hover:text-amber-500 transition-colors mb-1">
                    {asset.name}
                  </h4>
                  <p className="text-xs text-themed-secondary mb-4 leading-relaxed">
                    {asset.desc}
                  </p>
                </div>

                {/* Actions */}
                <div className="pt-4 border-t border-[var(--border-subtle)] space-y-2">
                  <a
                    href={asset.path}
                    download={asset.filename}
                    className="w-full py-2.5 rounded-xl text-xs font-bold bg-gradient-to-r from-amber-400 to-amber-500 hover:from-amber-300 hover:to-amber-400 text-slate-950 shadow-md transition-all flex items-center justify-center gap-1.5"
                  >
                    <Download className="w-3.5 h-3.5" />
                    <span>Unduh {asset.filename.toUpperCase().split('.').pop()}</span>
                  </a>

                  <a
                    href={asset.path}
                    target="_blank"
                    rel="noreferrer"
                    className="w-full py-1.5 rounded-lg text-[11px] font-semibold text-themed-secondary hover:text-amber-500 text-center block transition-colors"
                  >
                    Buka Berkas di Tab Baru
                  </a>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
