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
      particleCount: 90,
      spread: 75,
      origin: { y: 0.6 },
      colors: ['#F5C538', '#E09B17', '#B6580B', '#FDF39D', '#F7D160']
    });
  };

  return (
    <div className="min-h-screen relative overflow-hidden flex flex-col justify-between">
      {/* Editorial Blueprint Grid Guides (Sylva-inspired architectural layout) */}
      <div className="blueprint-guides">
        <i style={{ left: '12%' }} />
        <i style={{ left: '38%' }} />
        <i style={{ left: '62%' }} />
        <i style={{ left: '88%' }} />
      </div>

      {/* Monumental Ghost Typography in background */}
      <div className="ghost-wordmark -top-10 -left-10 text-[18vw] opacity-40">
        44
      </div>

      {/* Ambient Radial Lighting Pools */}
      <div className="ambient-pool-gold top-0 right-[-10%] w-[600px] h-[600px]" />
      <div className="ambient-pool-flame top-[35%] left-[-15%] w-[700px] h-[700px]" />

      {/* Main Navigation */}
      <Navbar theme={theme} setTheme={setTheme} />

      {/* Hero Section */}
      <section className="relative pt-8 pb-12 sm:pt-14 sm:pb-16 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          {/* Official badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full card-themed border border-amber-500/30 backdrop-blur-md mb-6 shadow-xl">
            <span className="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping" />
            <span className="text-xs font-bold text-amber-500 tracking-wider uppercase font-mono">
              IDENTITAS RESMI • SMA NEGERI 1 GEDEG
            </span>
            <span className="text-[10px] bg-amber-500/20 text-amber-600 dark:text-amber-400 font-bold px-2 py-0.5 rounded-full border border-amber-400/40">
              V6 MASTER FINAL
            </span>
          </div>

          {/* Main Title */}
          <h1 className="font-serif text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight title-primary max-w-5xl mx-auto leading-[1.15] mb-5">
            DIES NATALIS KE-44 <br />
            <span className="text-gold-gradient">
              Kemuliaan Prestasi, Api Integritas
            </span>
          </h1>

          <p className="max-w-2xl mx-auto text-themed-secondary text-sm sm:text-base leading-relaxed mb-8">
            Dokumentasi komprehensif sistem identitas visual, filosofi lambang, evolusi perancangan dari sketsa pensil ke vektor master V6, dan pengalaman 3D trimatra interaktif resmi.
          </p>

          {/* Action Buttons */}
          <div className="flex flex-wrap items-center justify-center gap-3 mb-10">
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

          {/* Trust & Spec Pills */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 max-w-4xl mx-auto pt-6 border-t border-[var(--border-subtle)] text-xs">
            <div className="p-3 rounded-2xl card-themed">
              <span className="text-themed-secondary block mb-0.5 text-[11px]">Institusi Resmi</span>
              <strong className="title-primary font-bold">SMAN 1 Gedeg</strong>
            </div>
            <div className="p-3 rounded-2xl card-themed">
              <span className="text-themed-secondary block mb-0.5 text-[11px]">Presisi Medial Spine</span>
              <strong className="text-amber-500 font-bold">100% Simetris V6</strong>
            </div>
            <div className="p-3 rounded-2xl card-themed">
              <span className="text-themed-secondary block mb-0.5 text-[11px]">Sistem Warna</span>
              <strong className="title-primary font-bold">Coolors Gold Palette</strong>
            </div>
            <div className="p-3 rounded-2xl card-themed">
              <span className="text-themed-secondary block mb-0.5 text-[11px]">Status Hak Cipta</span>
              <strong className="text-red-500 font-bold">Proprietary Tertutup</strong>
            </div>
          </div>
        </div>
      </section>

      {/* 3D Visualizer Section */}
      <section id="visualizer-3d" className="py-8 sm:py-14 relative z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-8">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-500 text-xs font-bold uppercase tracking-wider mb-2">
              <Layers className="w-3.5 h-3.5" />
              Eksplorasi Trimatra 3D Interaktif
            </div>
            <h2 className="font-serif text-2xl sm:text-3xl lg:text-4xl font-black title-primary tracking-tight mb-2">
              Visualisasi 3D Lambang Master V6
            </h2>
            <p className="text-themed-secondary text-xs sm:text-sm leading-relaxed">
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
