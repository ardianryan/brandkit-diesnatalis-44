import React, { useState } from 'react';
import { Palette, Copy, Check, Sparkles, Sliders, Layers } from 'lucide-react';

const PALETTE_DATA = [
  {
    name: 'Obsidian Mahogany',
    hex: '#310603',
    rgb: 'rgb(49, 6, 3)',
    cmyk: 'C:48 M:88 Y:76 K:75',
    category: 'Deep Shadow & Boundary',
    role: 'Bayangan terdalam, batas kontras monokrom gelap, dan garis penegas siluet.',
    contrastDark: 'Rendah (Latar Gelap)',
    contrastLight: 'AAA (Sangat Kontras di Putih)'
  },
  {
    name: 'Crimson Fire',
    hex: '#7D1B05',
    rgb: 'rgb(125, 27, 5)',
    cmyk: 'C:24 M:96 Y:100 K:27',
    category: 'Core Flame Depth',
    role: 'Pangkal lidah api berkobar, pembangun dimensi kedalaman dan aura keberanian.',
    contrastDark: 'AA (Di Latar Gelap)',
    contrastLight: 'AAA (Di Latar Terang)'
  },
  {
    name: 'Bronze Shadow',
    hex: '#B6580B',
    rgb: 'rgb(182, 88, 11)',
    cmyk: 'C:18 M:73 Y:100 K:7',
    category: 'Warm Transition Bronze',
    role: 'Nada transisi hangat antara bayangan tembaga dan keemasan utama tubuh lambang.',
    contrastDark: 'AAA (Di Latar Gelap)',
    contrastLight: 'AA (Di Latar Terang)'
  },
  {
    name: 'Marigold Gold',
    hex: '#E09B17',
    rgb: 'rgb(224, 155, 23)',
    cmyk: 'C:9 M:39 Y:99 K:0',
    category: 'Primary Brand Body',
    role: 'Warna inti tubuh angka 44 dan bulu rajawali; memancarkan aura kemuliaan almamater.',
    contrastDark: 'AAA (Di Latar Gelap)',
    contrastLight: 'AA (Di Latar Terang)'
  },
  {
    name: 'Vivid Gold',
    hex: '#F5C538',
    rgb: 'rgb(245, 197, 56)',
    cmyk: 'C:3 M:21 Y:84 K:0',
    category: 'Medial Spine & Brilliance',
    role: 'Kilau keemasan tulang punggung (medial spine) dan aksentuasi garis dinamis utama.',
    contrastDark: 'AAA (Sangat Kontras)',
    contrastLight: 'Aksen Garis / Teks Gelap'
  },
  {
    name: 'Champagne Gold',
    hex: '#F7D160',
    rgb: 'rgb(247, 209, 96)',
    cmyk: 'C:2 M:16 Y:68 K:0',
    category: 'Specular Highlight',
    role: 'Sorotan pantulan cahaya puncak pada lengkung 3D dan paruh rajawali.',
    contrastDark: 'AAA (Di Latar Gelap)',
    contrastLight: 'Sebagai Latar / Aksen Lembut'
  },
  {
    name: 'Canary Glow',
    hex: '#FDF39D',
    rgb: 'rgb(253, 243, 157)',
    cmyk: 'C:1 M:2 Y:44 K:0',
    category: 'Pinnacle Luminescence',
    role: 'Pendaran cahaya tertinggi pada gradasi emas, efek pendar api, dan sorotan tatapan mata.',
    contrastDark: 'AAA (Sangat Terang)',
    contrastLight: 'Latar Belakang Halus'
  },
  {
    name: 'Midnight Plum',
    hex: '#360538',
    rgb: 'rgb(54, 5, 56)',
    cmyk: 'C:72 M:98 Y:38 K:56',
    category: 'Contrast Velvet Field',
    role: 'Latar belakang premium panggung, kain beludru cendera mata, dan media berkarakter elegan.',
    contrastDark: 'Latar Lapis Dalam',
    contrastLight: 'AAA (Sangat Kontras di Putih)'
  }
];

export default function ColorPaletteSection() {
  const [copiedHex, setCopiedHex] = useState(null);

  const handleCopy = (hex) => {
    navigator.clipboard.writeText(hex);
    setCopiedHex(hex);
    setTimeout(() => setCopiedHex(null), 2200);
  };

  return (
    <section id="palet-warna" className="py-20 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold uppercase tracking-wider mb-4">
            <Palette className="w-3.5 h-3.5" />
            Spesifikasi Palet Warna Resmi
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight mb-4">
            Harmoni Kromatik Emas &amp; Api <br />
            <span className="text-gold-gradient">Pedoman Resmi Coolors</span>
          </h2>
          <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
            Delapan nilai warna terpilih yang dikalibrasi secara presisi dari dokumen palet resmi. Membangun gradasi keemasan fotorealistis dan kontras visual yang kuat untuk media digital maupun cetak.
          </p>
        </div>

        {/* Master Color Strip Banner */}
        <div className="glass-panel p-4 rounded-3xl border border-white/10 mb-12 shadow-2xl">
          <div className="h-16 sm:h-20 w-full rounded-2xl overflow-hidden flex shadow-inner">
            {PALETTE_DATA.map((color) => (
              <div
                key={color.hex}
                onClick={() => handleCopy(color.hex)}
                className="h-full flex-1 group relative cursor-pointer transition-all duration-300 hover:flex-[1.8] flex items-center justify-center"
                style={{ backgroundColor: color.hex }}
                title={`Salin ${color.name} (${color.hex})`}
              >
                <span className="opacity-0 group-hover:opacity-100 bg-slate-950/90 text-white text-[10px] font-bold px-2 py-1 rounded-md shadow-lg transition-opacity duration-200">
                  {color.hex}
                </span>
              </div>
            ))}
          </div>
          <div className="mt-3 flex items-center justify-between text-xs text-slate-400 px-2">
            <span>Spektrum Lengkap Coolors Palette Spec</span>
            <span className="text-amber-400 font-semibold">Klik warna pada pita untuk menyalin kode Hex</span>
          </div>
        </div>

        {/* Individual Color Cards Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {PALETTE_DATA.map((color) => {
            const isCopied = copiedHex === color.hex;
            const isDark = ['#310603', '#7D1B05', '#360538'].includes(color.hex);

            return (
              <div
                key={color.hex}
                className="group glass-panel rounded-3xl overflow-hidden border border-white/10 hover:border-amber-400/40 transition-all duration-300 hover:-translate-y-1 flex flex-col justify-between"
              >
                {/* Top Swatch */}
                <div
                  className="h-32 sm:h-36 relative p-4 flex flex-col justify-between cursor-pointer"
                  style={{ backgroundColor: color.hex }}
                  onClick={() => handleCopy(color.hex)}
                >
                  <div className="flex items-center justify-between">
                    <span
                      className={`text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md ${
                        isDark ? 'bg-white/15 text-white' : 'bg-black/20 text-slate-900'
                      }`}
                    >
                      {color.category}
                    </span>
                    <button
                      className={`p-1.5 rounded-lg transition-transform hover:scale-110 ${
                        isDark ? 'bg-white/15 text-white' : 'bg-black/20 text-slate-900'
                      }`}
                      title="Salin Kode Hex"
                    >
                      {isCopied ? <Check className="w-3.5 h-3.5 text-green-400" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                  </div>

                  <div>
                    <span
                      className={`font-serif font-black text-xl tracking-wider block ${
                        isDark ? 'text-white' : 'text-slate-950'
                      }`}
                    >
                      {color.hex}
                    </span>
                    <span
                      className={`text-xs font-semibold block ${
                        isDark ? 'text-slate-300' : 'text-slate-800'
                      }`}
                    >
                      {color.name}
                    </span>
                  </div>
                </div>

                {/* Details Body */}
                <div className="p-5 flex-1 flex flex-col justify-between bg-slate-900/80">
                  <p className="text-xs text-slate-300 leading-relaxed mb-4">
                    {color.role}
                  </p>

                  <div className="space-y-2 pt-3 border-t border-white/5 text-[11px] font-mono text-slate-400">
                    <div className="flex items-center justify-between">
                      <span className="text-slate-500">RGB:</span>
                      <span className="text-slate-300 font-semibold">{color.rgb}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-slate-500">CMYK:</span>
                      <span className="text-slate-300 font-semibold">{color.cmyk}</span>
                    </div>
                  </div>

                  <button
                    onClick={() => handleCopy(color.hex)}
                    className="mt-4 w-full py-2 rounded-xl text-xs font-bold bg-slate-800 hover:bg-amber-400 hover:text-slate-950 text-slate-300 transition-colors flex items-center justify-center gap-1.5"
                  >
                    {isCopied ? (
                      <>
                        <Check className="w-3.5 h-3.5 text-green-400" />
                        <span>Tersalin ke Papan Klip!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="w-3.5 h-3.5" />
                        <span>Salin Kode Warna</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
