import React from 'react';
import { Sparkles, Shield, Flame, Compass, Eye, CheckCircle2, ChevronRight } from 'lucide-react';

const PHILOSOPHY_ITEMS = [
  {
    id: 'twin44',
    title: 'Sinergi Angka Kembar 44',
    tag: 'Fondasi Sejarah & Kebersamaan',
    icon: Shield,
    color: '#E09B17',
    summary: 'Dua figur angka empat yang saling menopang dan menyatu erat dalam alur dinamis.',
    points: [
      'Menandai usia ke-44 tahun perjalanan penuh dedikasi SMA Negeri 1 Gedeg dalam melahirkan generasi berprestasi.',
      'Melambangkan keharmonisan antargenerasi pendidik, tenaga kependidikan, siswa, dan ikatan alumni.',
      'Keteguhan institusi yang kokoh berakar pada nilai-nilai integritas, budi pekerti luhur, dan disiplin tinggi.'
    ]
  },
  {
    id: 'eagle',
    title: 'Kepala & Tatapan Rajawali',
    tag: 'Wibawa & Ketajaman Intelektual',
    icon: Eye,
    color: '#FDF39D',
    summary: 'Siluet paruh dan kepala rajawali yang menatap tajam ke arah kanan atas (masa depan).',
    points: [
      'Mencerminkan keberanian moral dan kejernihan berpikir dalam mengambil keputusan strategis.',
      'Ketajaman visi untuk membaca peluang zaman di tengah era disrupsi sains dan teknologi global.',
      'Kewibawaan almamater yang disegani karena karya nyata, prestasi akademik, dan kemuliaan akhlak.'
    ]
  },
  {
    id: 'flame',
    title: 'Lidah Api Abadi Berkobar',
    tag: 'Daya Juang Pantang Padam',
    icon: Flame,
    color: '#B6580B',
    summary: 'Lekukan sulur api dinamis yang menjulang tinggi memancarkan energi kehangatan dan semangat.',
    points: [
      'Gairah belajar dan haus akan ilmu pengetahuan yang senantiasa menyala dalam dada civitas akademika.',
      'Daya lenting (resiliensi) tinggi dalam menghadapi rintangan tanpa pernah menyerah.',
      'Energi kebaikan yang menular untuk menghangatkan, membimbing, dan mencerahkan lingkungan masyarakat.'
    ]
  },
  {
    id: 'acceleration',
    title: 'Momentum Melesat & Sayap Aerodinamis',
    tag: 'Akselerasi Prestasi & Inovasi',
    icon: Compass,
    color: '#7D1B05',
    summary: 'Sayap luar dengan kelengkungan aerodinamis yang meluncur cepat ke kuadran kanan atas.',
    points: [
      'Simbol orientasi masa depan, menolak stagnasi, dan terus bergerak maju secara berkesinambungan.',
      'Akselerasi transformasi pembelajaran modern berbasis riset dan kecakapan abad ke-21.',
      'Kecepatan beradaptasi dengan tetap menjaga orisinalitas akar budaya luhur bangsa Indonesia.'
    ]
  },
  {
    id: 'spine',
    title: 'Harmoni Symmetrical Medial Spine',
    tag: 'Keunggulan Presisi Geometri V6',
    icon: Sparkles,
    color: '#F7D160',
    summary: 'Tulang punggung simetris berbusur lingkaran sempurna hasil penyempurnaan master V6.',
    points: [
      'Menghadirkan kedalaman trimatra (3D) yang seimbang tanpa ketidakselarasan lengkungan antar-vektor.',
      'Dibangun dengan rasio presisi konsentris yang menjamin keanggunan bentuk pada berbagai skala.',
      'Bebas dari distorsi dan penumpukan garis tajam, menghasilkan cetakan fisik yang sangat rapi.'
    ]
  }
];

export default function PhilosophySection({ activeComponent, onSelectComponent }) {
  return (
    <section id="filosofi" className="py-20 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-xs font-bold uppercase tracking-wider mb-4">
            <Sparkles className="w-3.5 h-3.5" />
            Makna Filosofis Lambang Resmi
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-black title-primary tracking-tight mb-4">
            Anatomi Karakter &amp; Nilai Luhur <br />
            <span className="text-gold-gradient">SMA Negeri 1 Gedeg</span>
          </h2>
          <p className="text-themed-secondary text-sm sm:text-base leading-relaxed">
            Setiap garis kurva, busur lingkaran, dan transisi keemasan pada lambang Dies Natalis ke-44 bukan sekadar estetika visual belaka, melainkan manifestasi dari cita-cita luhur dan jiwa kepemimpinan almamater.
          </p>
        </div>

        {/* Philosophy Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {PHILOSOPHY_ITEMS.map((item) => {
            const Icon = item.icon;
            const isSelected = activeComponent === item.id;

            return (
              <div
                key={item.id}
                onClick={() => onSelectComponent(item.id)}
                className={`group relative rounded-3xl p-6 sm:p-8 cursor-pointer transition-all duration-300 card-themed border ${
                  isSelected
                    ? 'border-amber-500 ring-2 ring-amber-400/40 shadow-2xl shadow-amber-500/20 -translate-y-1'
                    : 'hover:border-amber-500/40 hover:-translate-y-1'
                }`}
              >
                {/* Top Badge & Icon */}
                <div className="flex items-center justify-between mb-6">
                  <div
                    className="w-12 h-12 rounded-2xl flex items-center justify-center transition-transform group-hover:scale-110 shadow-lg"
                    style={{
                      background: `linear-gradient(135deg, ${item.color}33, ${item.color}11)`,
                      border: `1px solid ${item.color}66`
                    }}
                  >
                    <Icon className="w-6 h-6" style={{ color: item.color }} />
                  </div>
                  <span
                    className="text-[10px] font-bold uppercase tracking-wider px-3 py-1 rounded-full"
                    style={{
                      backgroundColor: `${item.color}18`,
                      color: item.color,
                      border: `1px solid ${item.color}40`
                    }}
                  >
                    {item.tag}
                  </span>
                </div>

                {/* Card Title & Summary */}
                <h3 className="font-serif text-xl font-bold title-primary mb-2 group-hover:text-amber-500 transition-colors">
                  {item.title}
                </h3>
                <p className="text-xs sm:text-sm text-themed-secondary mb-6 leading-relaxed">
                  {item.summary}
                </p>

                {/* Detailed Key Points */}
                <div className="space-y-2.5 pt-4 border-t border-[var(--border-subtle)]">
                  {item.points.map((pt, idx) => (
                    <div key={idx} className="flex items-start gap-2.5 text-xs text-themed-secondary">
                      <CheckCircle2 className="w-3.5 h-3.5 mt-0.5 text-amber-500 shrink-0" />
                      <span className="leading-snug">{pt}</span>
                    </div>
                  ))}
                </div>

                {/* 3D Sync Call-to-action */}
                <div className="mt-6 pt-4 border-t border-[var(--border-subtle)] flex items-center justify-between text-xs font-semibold text-amber-500 group-hover:text-amber-600 dark:group-hover:text-amber-400">
                  <span className="flex items-center gap-1.5">
                    {isSelected ? '✓ Sedang Disorot di Model 3D' : 'Sorot Komponen di 3D'}
                  </span>
                  <ChevronRight className="w-4 h-4 transition-transform group-hover:translate-x-1" />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
