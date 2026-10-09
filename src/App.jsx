import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { Sparkles, Download, Layers, Shield, ChevronDown, Check, ArrowRight } from 'lucide-react';
import Navbar from './components/Navbar';
import Logo3DViewer from './components/Logo3DViewer';
import PhilosophySection from './components/PhilosophySection';
import EvolutionTimeline from './components/EvolutionTimeline';
import ColorPaletteSection from './components/ColorPaletteSection';
import MerchandiseShowcase from './components/MerchandiseShowcase';
import AssetLibrarySection from './components/AssetLibrarySection';
import Footer from './components/Footer';

export default function App() {
  // Theme state: 'dark' | 'light' | 'system' (Default by system)
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('dn44_theme') || 'system';
  });

  // Active highlighted component in 3D viewer & philosophy
  const [activeComponent, setActiveComponent] = useState('all');

  // Apply Theme & System Preferences Listener
  useEffect(() => {
    const root = document.documentElement;

    const applyTheme = (t) => {
      let effectiveTheme = t;
      if (t === 'system') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        effectiveTheme = prefersDark ? 'dark' : 'light';
      }
      root.setAttribute('data-theme', effectiveTheme);
    };

    applyTheme(theme);
    localStorage.setItem('dn44_theme', theme);

    if (theme === 'system') {
      const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
      const handleMediaChange = () => applyTheme('system');
      mediaQuery.addEventListener('change', handleMediaChange);
      return () => mediaQuery.removeEventListener('change', handleMediaChange);
    }
  }, [theme]);

  // Trigger festive golden confetti
  const triggerCelebration = () => {
    confetti({
      particleCount: 80,
      spread: 70,
      origin: { y: 0.6 },
      colors: ['#F5C538', '#E09B17', '#B6580B', '#FDF39D', '#F7D160']
    });
  };

  return (
    <div className="min-h-screen relative overflow-hidden flex flex-col justify-between">
      {/* Ambient background gradients */}
      <div className="ambient-glow-top" />
      <div className="ambient-glow-center" />

      {/* Main Navigation */}
      <Navbar theme={theme} setTheme={setTheme} />

      {/* Hero Section */}
      <section className="relative pt-12 pb-20 sm:pt-20 sm:pb-28 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          {/* Official badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-slate-900/80 border border-amber-500/30 backdrop-blur-md mb-8 shadow-xl">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping" />
            <span className="text-xs font-bold text-amber-300 tracking-wider uppercase font-mono">
              IDENTITAS RESMI • SMA NEGERI 1 GEDEG
            </span>
            <span className="text-[10px] bg-amber-500/20 text-amber-300 font-bold px-2 py-0.5 rounded-full border border-amber-400/40">
              V6 MASTER FINAL
            </span>
          </div>

          {/* Main Title */}
          <h1 className="font-serif text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight text-white max-w-5xl mx-auto leading-[1.1] mb-6">
            DIES NATALIS KE-44 <br />
            <span className="text-gold-gradient">
              Kemuliaan Prestasi, Api Integritas
            </span>
          </h1>

          <p className="max-w-2xl mx-auto text-slate-300 text-sm sm:text-lg leading-relaxed mb-10">
            Dokumentasi komprehensif sistem identitas visual, filosofi lambang, evolusi perancangan dari sketsa pensil ke vektor master V6, dan pengalaman 3D trimatra interaktif resmi.
          </p>

          {/* Action Buttons */}
          <div className="flex flex-wrap items-center justify-center gap-4 mb-14">
            <a href="#visualizer-3d" className="btn-gold">
              <Sparkles className="w-4 h-4" />
              <span>Eksplorasi Model 3D Interaktif</span>
            </a>
            <a href="#aset-unduh" className="btn-secondary">
              <Download className="w-4 h-4 text-amber-400" />
              <span>Unduh Paket Vektor V6 Master</span>
            </a>
            <button onClick={triggerCelebration} className="btn-secondary">
              🎉 Rayakan Dies Natalis 44
            </button>
          </div>

          {/* Trust & Spec Pills */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-4xl mx-auto pt-8 border-t border-white/10 text-xs">
            <div className="p-3 rounded-2xl bg-slate-900/50 border border-white/5">
              <span className="text-slate-400 block mb-0.5">Institusi Resmi</span>
              <strong className="text-white font-bold">SMAN 1 Gedeg</strong>
            </div>
            <div className="p-3 rounded-2xl bg-slate-900/50 border border-white/5">
              <span className="text-slate-400 block mb-0.5">Presisi Medial Spine</span>
              <strong className="text-amber-400 font-bold">100% Simetris V6</strong>
            </div>
            <div className="p-3 rounded-2xl bg-slate-900/50 border border-white/5">
              <span className="text-slate-400 block mb-0.5">Sistem Warna</span>
              <strong className="text-white font-bold">Coolors Gold Palette</strong>
            </div>
            <div className="p-3 rounded-2xl bg-slate-900/50 border border-white/5">
              <span className="text-slate-400 block mb-0.5">Status Hak Cipta</span>
              <strong className="text-red-400 font-bold">Proprietary Tertutup</strong>
            </div>
          </div>
        </div>
      </section>

      {/* 3D Visualizer Section */}
      <section id="visualizer-3d" className="py-12 sm:py-20 relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold uppercase tracking-wider mb-3">
              <Layers className="w-3.5 h-3.5" />
              Eksplorasi Trimatra 3D Interaktif
            </div>
            <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-black text-white tracking-tight mb-3">
              Visualisasi 3D Lambang Master V6
            </h2>
            <p className="text-slate-400 text-sm sm:text-base leading-relaxed">
              Putar 360°, perbesar, pisahkan layer 3D, atau pilih komponen filosofis untuk melihat sorotan interaktif secara langsung.
            </p>
          </div>

          <Logo3DViewer
            activeComponent={activeComponent}
            onSelectComponent={(comp) => setActiveComponent(comp)}
          />
        </div>
      </section>

      {/* Philosophy Section with 3D link */}
      <PhilosophySection
        activeComponent={activeComponent}
        onSelectComponent={(comp) => {
          setActiveComponent(comp);
          const el = document.getElementById('visualizer-3d');
          if (el) el.scrollIntoView({ behavior: 'smooth' });
        }}
      />

      {/* Evolution Timeline: Raw Hand Draw -> Digital -> V6 */}
      <EvolutionTimeline />

      {/* Color Palette (Official Coolors Spec) */}
      <ColorPaletteSection />

      {/* Merchandise & Guidelines */}
      <MerchandiseShowcase />

      {/* Master Assets Library */}
      <AssetLibrarySection />

      {/* Footer */}
      <Footer />
    </div>
  );
}
