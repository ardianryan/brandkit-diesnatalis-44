import React from 'react';
import { Sun, Moon, Laptop, Sparkles, ShieldAlert, Layers } from 'lucide-react';

export default function Navbar({ theme, setTheme }) {
  return (
    <header className="sticky top-0 z-50 glass-nav transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between">
        {/* Brand identity badge */}
        <div className="flex items-center gap-4">
          <div className="relative group cursor-pointer" onClick={() => window.scrollTo({ top: 0, behavior: 'smooth' })}>
            <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-amber-600 via-amber-400 to-yellow-200 p-[2px] shadow-lg shadow-amber-500/20 group-hover:scale-105 transition-transform duration-300">
              <div className="w-full h-full rounded-[10px] bg-[var(--bg-primary)] flex items-center justify-center p-1.5">
                <img 
                  src="/assets/svg/logo-symbol-color.svg" 
                  alt="Dies Natalis 44" 
                  className="w-full h-full object-contain filter drop-shadow" 
                />
              </div>
            </div>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-serif font-black tracking-wider text-lg text-gold-gradient">
                DIES NATALIS 44
              </span>
              <span className="px-2 py-0.5 text-[10px] font-bold tracking-widest uppercase rounded-full bg-amber-500/15 text-amber-500 border border-amber-500/30">
                MASTER V6
              </span>
            </div>
            <p className="text-xs text-themed-secondary font-medium">
              SMA Negeri 1 Gedeg • Brand Identity &amp; 3D Interactive System
            </p>
          </div>
        </div>

        {/* Navigation links */}
        <nav className="hidden lg:flex items-center gap-6 text-sm font-semibold text-themed-secondary">
          <a href="#visualizer-3d" className="hover:text-amber-500 transition-colors">Visualizer 3D</a>
          <a href="#filosofi" className="hover:text-amber-500 transition-colors">Filosofi Lambang</a>
          <a href="#riwayat" className="hover:text-amber-500 transition-colors">Riwayat Pembuatan</a>
          <a href="#palet-warna" className="hover:text-amber-500 transition-colors">Palet Warna</a>
          <a href="#merchandise" className="hover:text-amber-500 transition-colors">Cendera Mata</a>
          <a href="#aset-unduh" className="hover:text-amber-500 transition-colors">Aset Master</a>
        </nav>

        {/* Right Action: Theme Switcher & Status */}
        <div className="flex items-center gap-3">
          {/* Light/Dark/System Theme Selector */}
          <div className="flex items-center gap-1 bg-[var(--bg-secondary)] p-1 rounded-xl border border-[var(--border-subtle)] shadow-inner">
            <button
              onClick={() => setTheme('light')}
              title="Mode Terang (Light Mode)"
              className={`px-2.5 py-1.5 rounded-lg text-xs flex items-center gap-1.5 whitespace-nowrap transition-all ${
                theme === 'light'
                  ? 'bg-amber-400 text-slate-950 font-bold shadow-md'
                  : 'text-themed-secondary hover:text-amber-500'
              }`}
            >
              <Sun className="w-3.5 h-3.5" />
              <span className="text-[11px]">Terang</span>
            </button>
            <button
              onClick={() => setTheme('dark')}
              title="Mode Gelap (Dark Mode)"
              className={`px-2.5 py-1.5 rounded-lg text-xs flex items-center gap-1.5 whitespace-nowrap transition-all ${
                theme === 'dark'
                  ? 'bg-amber-400 text-slate-950 font-bold shadow-md'
                  : 'text-themed-secondary hover:text-amber-500'
              }`}
            >
              <Moon className="w-3.5 h-3.5" />
              <span className="text-[11px]">Gelap</span>
            </button>
            <button
              onClick={() => setTheme('system')}
              title="Sistem Otomatis (Default by System)"
              className={`px-2.5 py-1.5 rounded-lg text-xs flex items-center gap-1.5 whitespace-nowrap transition-all ${
                theme === 'system'
                  ? 'bg-amber-400 text-slate-950 font-bold shadow-md'
                  : 'text-themed-secondary hover:text-amber-500'
              }`}
            >
              <Laptop className="w-3.5 h-3.5" />
              <span className="text-[11px]">Sistem</span>
            </button>
          </div>

          <a
            href="https://github.com/ardianryan/brandkit-diesnatalis-44"
            target="_blank"
            rel="noreferrer"
            title="Repositori GitHub Resmi"
            className="hidden sm:flex items-center justify-center w-9 h-9 rounded-xl bg-[var(--bg-secondary)] hover:bg-[var(--bg-card)] border border-[var(--border-subtle)] text-themed-secondary hover:text-amber-500 transition-all hover:scale-105"
          >
            <svg className="w-4 h-4 fill-current" viewBox="0 0 24 24">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z" />
            </svg>
          </a>
        </div>
      </div>
    </header>
  );
}
