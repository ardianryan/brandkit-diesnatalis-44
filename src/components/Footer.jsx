import React from 'react';
import { Shield, Sparkles, Heart, FileText, ExternalLink } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-white/10 bg-slate-950/90 pt-16 pb-12 text-slate-400 text-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 mb-12">
          {/* Brand Info */}
          <div className="md:col-span-5 space-y-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-600 to-amber-300 p-0.5">
                <div className="w-full h-full rounded-[10px] bg-slate-950 flex items-center justify-center p-1.5">
                  <img src="/assets/svg/logo-symbol-color.svg" alt="Dies Natalis 44" className="w-full h-full object-contain" />
                </div>
              </div>
              <div>
                <span className="font-serif font-black text-white text-base tracking-wider block">
                  DIES NATALIS KE-44
                </span>
                <span className="text-[11px] text-amber-400 font-semibold block">
                  SMA NEGERI 1 GEDEG, MOJOKERTO
                </span>
              </div>
            </div>
            <p className="text-slate-400 text-xs leading-relaxed max-w-sm">
              Sistem identitas visual dan pedoman desain resmi perayaan Dies Natalis ke-44. Dibangun dengan integritas kurva geometris presisi, filosofi keagungan rajawali, dan semangat api abadi.
            </p>
          </div>

          {/* Quick Links */}
          <div className="md:col-span-3 space-y-3">
            <h4 className="font-serif font-bold text-sm text-white tracking-wide">
              Navigasi Halaman
            </h4>
            <ul className="space-y-2 text-slate-400">
              <li><a href="#visualizer-3d" className="hover:text-amber-400 transition-colors">Visualizer 3D WebGL</a></li>
              <li><a href="#filosofi" className="hover:text-amber-400 transition-colors">Filosofi Lambang Resmi</a></li>
              <li><a href="#riwayat" className="hover:text-amber-400 transition-colors">Riwayat Pembuatan (Sketsa ke V6)</a></li>
              <li><a href="#palet-warna" className="hover:text-amber-400 transition-colors">Sistem Palet Warna</a></li>
              <li><a href="#merchandise" className="hover:text-amber-400 transition-colors">Aplikasi Cendera Mata</a></li>
              <li><a href="#aset-unduh" className="hover:text-amber-400 transition-colors">Pustaka Aset Master</a></li>
            </ul>
          </div>

          {/* Strict Proprietary License Notice */}
          <div className="md:col-span-4 space-y-3 bg-slate-900/60 p-5 rounded-2xl border border-red-500/20">
            <div className="flex items-center gap-2 text-red-400 font-bold text-xs uppercase tracking-wider">
              <Shield className="w-4 h-4" />
              <span>Lisensi Tertutup &amp; Hak Cipta Mutlak</span>
            </div>
            <p className="text-[11px] text-slate-300 leading-relaxed">
              Seluruh karya cipta grafis, lambang, kode sumber, dan dokumentasi ini dilindungi undang-undang. <strong>Dilarang keras menyalin, memodifikasi, mengedarkan, atau menggunakan materi ini tanpa izin tertulis resmi</strong> dari SMA Negeri 1 Gedeg dan Ardian Ryan.
            </p>
            <div className="pt-2 border-t border-white/5 flex items-center justify-between text-[10px] text-slate-400">
              <span>Status: Proprietary (Non-Open Source)</span>
              <a href="/LICENSE" className="text-amber-400 hover:underline flex items-center gap-1 font-semibold">
                <span>Baca LICENSE</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-8 border-t border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4 text-[11px]">
          <p>© 2024–2026 Ardian Ryan &amp; SMA Negeri 1 Gedeg. Seluruh Hak Dilindungi Undang-Undang.</p>
          <div className="flex items-center gap-2 text-slate-500">
            <span>Didesain dan dikembangkan secara presisi dengan Vite &amp; Three.js</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
