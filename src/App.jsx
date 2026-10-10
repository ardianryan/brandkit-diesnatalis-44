import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { Sparkles, Download, Layers, ShieldCheck, Award, Palette, History, ShoppingBag, FolderDown } from 'lucide-react';
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
      particleCount: 90,
      spread: 75,
      origin: { y: 0.6 },
      colors: ['#F5C538', '#E09B17', '#B6580B', '#FDF39D', '#F7D160']
    });
  };

  return (
    <div className="min-h-screen relative overflow-hidden flex flex-col justify-between selection:bg-amber-400 selection:text-slate-950">
      {/* Ambient background glow pool */}
      <div className="hero-ambient-glow" />

      {/* Main Navigation */}
      <Navbar theme={theme} setTheme={setTheme} />

      {/* Hero Section — Luxury Brand Showcase */}
      <section className="relative pt-12 pb-16 sm:pt-20 sm:pb-24 z-10">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          
          {/* Institutional Badge Pill */}
          <div className="inline-flex items-center gap-2.5 px-4 py-2 rounded-full card-themed mb-8 shadow-md">
            <span className="w-2 h-2 rounded-full bg-amber-500 animate-ping" />
            <span className="text-xs font-bold tracking-widest uppercase text-amber-600 dark:text-amber-400 font-mono">
              IDENTITAS RESMI • SMA NEGERI 1 GEDEG
            </span>
            <span className="h-3.5 w-px bg-[var(--border-subtle)]" />
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-600 dark:text-amber-300 border border-amber-500/30">
              V6 MASTER FINAL
            </span>
          </div>

          {/* Monumental Headline */}
          <h1 className="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight title-primary max-w-5xl mx-auto leading-[1.1] mb-6">
            DIES NATALIS KE-44 <br />
            <span className="text-gold-gradient font-serif font-black block mt-2 text-3xl sm:text-5xl lg:text-6xl">
              Kemuliaan Prestasi, Api Integritas
            </span>
          </h1>

          {/* Subtitle */}
          <p className="max-w-2xl mx-auto text-themed-secondary text-sm sm:text-base lg:text-lg leading-relaxed mb-10">
            Dokumentasi komprehensif sistem identitas visual, filosofi lambang, evolusi perancangan dari sketsa pensil ke vektor master V6, dan visualisasi 3D trimatra interaktif resmi almamater.
          </p>

          {/* CTA Action Buttons */}
          <div className="flex flex-wrap items-center justify-center gap-3.5 mb-14">
            <a href="#visualizer-3d" className="btn-gold-primary">
              <Sparkles className="w-4 h-4" />
              <span>Eksplorasi Model 3D Interaktif</span>
            </a>
            <a href="#aset-unduh" className="btn-glass">
              <Download className="w-4 h-4 text-amber-500" />
              <span>Unduh Paket Vektor V6 Master</span>
            </a>
            <button onClick={triggerCelebration} className="btn-glass">
              🎉 Rayakan Dies Natalis 44
            </button>
          </div>

          {/* Trust & Metric Cards Dock */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 max-w-4xl mx-auto">
            <div className="p-4 rounded-2xl card-themed text-left">
              <span className="text-themed-secondary block mb-1 text-[11px] font-medium">Institusi Resmi</span>
              <strong className="title-primary font-bold text-sm block">SMAN 1 Gedeg</strong>
              <span className="text-[10px] text-amber-500 font-semibold block mt-1">Kab. Mojokerto</span>
            </div>

            <div className="p-4 rounded-2xl card-themed text-left">
              <span className="text-themed-secondary block mb-1 text-[11px] font-medium">Presisi Medial Spine</span>
              <strong className="text-amber-500 font-bold text-sm block">100% Simetris V6</strong>
              <span className="text-[10px] text-themed-secondary font-semibold block mt-1">Busur Konsentris Murni</span>
            </div>

            <div className="p-4 rounded-2xl card-themed text-left">
              <span className="text-themed-secondary block mb-1 text-[11px] font-medium">Sistem Kromatik</span>
              <strong className="title-primary font-bold text-sm block">Coolors Gold Palette</strong>
              <span className="text-[10px] text-amber-500 font-semibold block mt-1">8 Standar Warna Resmi</span>
            </div>

            <div className="p-4 rounded-2xl card-themed text-left">
              <span className="text-themed-secondary block mb-1 text-[11px] font-medium">Status Hak Cipta</span>
              <strong className="text-red-500 font-bold text-sm block">Proprietary Tertutup</strong>
              <span className="text-[10px] text-themed-secondary font-semibold block mt-1">All Rights Reserved</span>
            </div>
          </div>
        </div>
      </section>

      {/* 3D Visualizer Section */}
      <section id="visualizer-3d" className="py-16 sm:py-24 relative z-10 bg-[var(--bg-secondary)] border-y border-[var(--border-subtle)]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full card-themed text-amber-500 text-xs font-bold uppercase tracking-wider mb-3">
              <Layers className="w-3.5 h-3.5" />
              Eksplorasi Trimatra 3D Interaktif
            </div>
            <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-black title-primary tracking-tight mb-3">
              Visualisasi 3D Lambang Master V6
            </h2>
            <p className="text-themed-secondary text-sm sm:text-base leading-relaxed">
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
