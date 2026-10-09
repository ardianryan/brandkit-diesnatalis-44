import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { SVGLoader } from 'three/examples/jsm/loaders/SVGLoader.js';
import { RotateCw, Maximize2, Minimize2, Eye, Box, Sparkles, Layers, RefreshCw, Compass } from 'lucide-react';

const COMPONENT_DETAILS = {
  all: {
    title: "Lambang Utuh Dies Natalis 44 (V6 Master)",
    subtitle: "Sinergi Keutuhan, Kejayaan, & Visi Futuristik",
    description: "Komposisi trimatra utuh menyatukan figur kembar angka 44, siluet rajawali, lidah api abadi, dan sayap aerodinamis dalam harmoni rasio keemasan yang presisi.",
    color: "#F5C538",
    badge: "Master V6 Final"
  },
  twin44: {
    title: "Figur Kembar Angka 44",
    subtitle: "Persatuan & Kedewasaan Institusi",
    description: "Dua figur angka 4 yang saling bertaut dinamis melambangkan 44 tahun perjalanan sejarah SMA Negeri 1 Gedeg dalam mendidik insan berkarakter unggul dan mempererat ikatan antargenerasi.",
    color: "#E09B17",
    badge: "Identitas Utama"
  },
  eagle: {
    title: "Kepala & Tatapan Rajawali",
    subtitle: "Kewibawaan & Visi Visioner Masa Depan",
    description: "Siluet kepala burung rajawali yang menatap tajam ke arah kanan atas melambangkan keberanian, ketajaman intelektual, ketegasan prinsip, dan integritas moral tanpa kompromi.",
    color: "#FDF39D",
    badge: "Orientasi Puncak"
  },
  flame: {
    title: "Lidah Api Abadi Berkobar",
    subtitle: "Semangat Juang Pantang Padam",
    description: "Aliran kurva bergelombang yang membubung dari dasar mencerminkan api semangat belajar abadi, kreativitas tanpa batas, serta daya lenting tinggi dalam menghadapi tantangan zaman.",
    color: "#B6580B",
    badge: "Energi Abadi"
  },
  acceleration: {
    title: "Akselerasi Sayap Aerodinamis",
    subtitle: "Kecepatan Inovasi & Transformasi",
    description: "Lengkungan aerodinamis sayap yang melesat melambangkan akselerasi prestasi siswa, adaptasi teknologi modern, dan dorongan tak terhentikan menuju masa depan gemilang.",
    color: "#7D1B05",
    badge: "Dinamika Melesat"
  },
  spine: {
    title: "Harmoni Medial Spine Simetris (Keunggulan V6)",
    subtitle: "Presisi Busur Lingkaran Konsentris",
    description: "Tulang punggung tengah yang disempurnakan pada versi V6 dengan busur lingkaran simetris murni. Menghadirkan kedalaman visual 3D yang elegan, bersih, dan bebas distorsi sudut.",
    color: "#F7D160",
    badge: "Keunggulan Detailing V6"
  }
};

export default function Logo3DViewer({ activeComponent = 'all', onSelectComponent }) {
  const containerRef = useRef(null);
  const rendererRef = useRef(null);
  const sceneRef = useRef(null);
  const cameraRef = useRef(null);
  const controlsRef = useRef(null);
  const layersGroupRef = useRef(null);
  const meshesRef = useRef([]);

  const [autoRotate, setAutoRotate] = useState(true);
  const [isExploded, setIsExploded] = useState(false);
  const [isWireframe, setIsWireframe] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Initialize Three.js Scene
  useEffect(() => {
    if (!containerRef.current) return;

    const width = containerRef.current.clientWidth;
    const height = containerRef.current.clientHeight || 560;

    // 1. Scene
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    // 2. Camera
    const camera = new THREE.PerspectiveCamera(45, width / height, 1, 3000);
    camera.position.set(0, 0, 750);
    cameraRef.current = camera;

    // 3. Renderer
    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFShadowMap;
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.25;
    rendererRef.current = renderer;

    containerRef.current.appendChild(renderer.domElement);

    // 4. OrbitControls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.autoRotate = autoRotate;
    controls.autoRotateSpeed = 1.8;
    controls.maxDistance = 1400;
    controls.minDistance = 300;
    controlsRef.current = controls;

    // 5. Lighting Setup (Cinematic Gold Studio)
    const ambientLight = new THREE.AmbientLight(0xfff5e6, 1.2);
    scene.add(ambientLight);

    const dirLight1 = new THREE.DirectionalLight(0xffeedd, 3.5);
    dirLight1.position.set(400, 500, 600);
    dirLight1.castShadow = true;
    scene.add(dirLight1);

    const dirLight2 = new THREE.DirectionalLight(0xd48911, 2.0);
    dirLight2.position.set(-500, -300, -400);
    scene.add(dirLight2);

    const rimLight = new THREE.DirectionalLight(0xffffff, 2.5);
    rimLight.position.set(0, 600, -500);
    scene.add(rimLight);

    const pointLight = new THREE.PointLight(0xf5c538, 3.0, 1000);
    pointLight.position.set(0, 0, 350);
    scene.add(pointLight);

    // 6. Master Logo Layers Group
    const layersGroup = new THREE.Group();
    layersGroupRef.current = layersGroup;
    scene.add(layersGroup);

    // 7. Load Master V6 SVG and Extrude into 3D Geometry
    const svgLoader = new SVGLoader();
    svgLoader.load(
      '/assets/svg/logo-symbol-color.svg',
      (svgData) => {
        const paths = svgData.paths;
        const meshes = [];

        // Color & Depth definitions for the 4 facets of V6
        const layerSpecs = [
          { name: 'base', color: 0xB6580B, depth: 32, zOffset: 0, roughness: 0.28, metalness: 0.88, component: 'acceleration' },
          { name: 'marigold', color: 0xE09B17, depth: 38, zOffset: 6, roughness: 0.22, metalness: 0.90, component: 'twin44' },
          { name: 'vivid', color: 0xF5C538, depth: 44, zOffset: 12, roughness: 0.18, metalness: 0.92, component: 'spine' },
          { name: 'champagne', color: 0xFDF39D, depth: 48, zOffset: 18, roughness: 0.14, metalness: 0.94, component: 'eagle' }
        ];

        paths.forEach((path, index) => {
          const shapes = path.toShapes(true);
          const spec = layerSpecs[index % layerSpecs.length];

          shapes.forEach((shape) => {
            const extrudeSettings = {
              depth: spec.depth,
              bevelEnabled: true,
              bevelSegments: 4,
              steps: 2,
              bevelSize: 2.5,
              bevelThickness: 2.5
            };

            const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);
            geometry.center();

            const material = new THREE.MeshStandardMaterial({
              color: spec.color,
              metalness: spec.metalness,
              roughness: spec.roughness,
              wireframe: false,
              emissive: 0x000000,
              emissiveIntensity: 0.0
            });

            const mesh = new THREE.Mesh(geometry, material);
            mesh.scale.set(0.32, -0.32, 0.32); // Invert Y from SVG coords
            mesh.position.z = spec.zOffset;
            mesh.castShadow = true;
            mesh.receiveShadow = true;
            mesh.userData = {
              defaultColor: spec.color,
              defaultZ: spec.zOffset,
              component: spec.component,
              spec: spec
            };

            layersGroup.add(mesh);
            meshes.push(mesh);
          });
        });

        meshesRef.current = meshes;
        setIsLoading(false);
      },
      undefined,
      (error) => {
        console.error('Error loading SVG for Three.js:', error);
        setIsLoading(false);
      }
    );

    // 8. Animation Loop
    let animationFrameId;
    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      if (controlsRef.current) {
        controlsRef.current.update();
      }
      renderer.render(scene, camera);
    };
    animate();

    // 9. Resize Handling
    const handleResize = () => {
      if (!containerRef.current || !rendererRef.current || !cameraRef.current) return;
      const newWidth = containerRef.current.clientWidth;
      const newHeight = containerRef.current.clientHeight || 560;
      cameraRef.current.aspect = newWidth / newHeight;
      cameraRef.current.updateProjectionMatrix();
      rendererRef.current.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
      if (renderer.domElement && containerRef.current) {
        containerRef.current.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  // Update Auto-Rotate
  useEffect(() => {
    if (controlsRef.current) {
      controlsRef.current.autoRotate = autoRotate;
    }
  }, [autoRotate]);

  // Update Wireframe
  useEffect(() => {
    meshesRef.current.forEach((mesh) => {
      if (mesh.material) {
        mesh.material.wireframe = isWireframe;
      }
    });
  }, [isWireframe]);

  // Update Exploded View (Layer separation along Z axis)
  useEffect(() => {
    meshesRef.current.forEach((mesh) => {
      const defaultZ = mesh.userData.defaultZ || 0;
      if (isExploded) {
        // Expand along Z axis smoothly
        mesh.position.z = defaultZ * 4.5 + 40;
      } else {
        mesh.position.z = defaultZ;
      }
    });
  }, [isExploded]);

  // Update Component Highlighting & Emissive Glow
  useEffect(() => {
    meshesRef.current.forEach((mesh) => {
      const comp = mesh.userData.component;
      if (!mesh.material) return;

      if (activeComponent === 'all') {
        mesh.material.color.setHex(mesh.userData.defaultColor);
        mesh.material.emissive.setHex(0x000000);
        mesh.material.emissiveIntensity = 0.0;
        mesh.material.opacity = 1.0;
        mesh.material.transparent = false;
      } else if (activeComponent === comp) {
        // Active component highlighted with brilliant glowing effect
        mesh.material.color.setHex(0xFFE082);
        mesh.material.emissive.setHex(0xE09B17);
        mesh.material.emissiveIntensity = 0.55;
        mesh.material.opacity = 1.0;
        mesh.material.transparent = false;
      } else {
        // Other components dimmed softly
        mesh.material.color.setHex(mesh.userData.defaultColor);
        mesh.material.emissive.setHex(0x000000);
        mesh.material.emissiveIntensity = 0.0;
        mesh.material.opacity = 0.45;
        mesh.material.transparent = true;
      }
    });
  }, [activeComponent]);

  const resetCamera = () => {
    if (cameraRef.current && controlsRef.current) {
      cameraRef.current.position.set(0, 0, 750);
      controlsRef.current.target.set(0, 0, 0);
      controlsRef.current.update();
    }
  };

  const currentDetails = COMPONENT_DETAILS[activeComponent] || COMPONENT_DETAILS.all;

  return (
    <div className="relative w-full rounded-3xl overflow-hidden glass-panel border border-amber-500/20 shadow-2xl">
      {/* Top 3D Canvas Header & Badges */}
      <div className="absolute top-4 left-4 right-4 z-20 flex flex-wrap items-center justify-between gap-3 pointer-events-none">
        <div className="pointer-events-auto bg-slate-900/85 backdrop-blur-md px-4 py-2 rounded-2xl border border-white/10 flex items-center gap-3 shadow-lg">
          <div className="w-3 h-3 rounded-full bg-amber-400 animate-pulse" />
          <div>
            <span className="text-xs font-bold uppercase tracking-wider text-amber-400 block">
              WebGL 3D Studio
            </span>
            <span className="text-sm font-semibold text-white">
              PBR Metallic Gold Extrusion
            </span>
          </div>
        </div>

        {/* View Controls Toolbar */}
        <div className="pointer-events-auto flex items-center gap-2 bg-slate-900/85 backdrop-blur-md p-1.5 rounded-2xl border border-white/10 shadow-lg">
          <button
            onClick={() => setAutoRotate(!autoRotate)}
            title={autoRotate ? "Jeda Rotasi Otomatis" : "Mulai Rotasi Otomatis"}
            className={`p-2 rounded-xl text-xs flex items-center gap-1.5 transition-all ${
              autoRotate ? 'bg-amber-400 text-slate-950 font-bold' : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
          >
            <RotateCw className={`w-3.5 h-3.5 ${autoRotate ? 'animate-spin' : ''}`} style={{ animationDuration: '6s' }} />
            <span className="hidden sm:inline">Rotasi</span>
          </button>

          <button
            onClick={() => setIsExploded(!isExploded)}
            title="Tampilan Meledak / Pemisahan Layer (Exploded View)"
            className={`p-2 rounded-xl text-xs flex items-center gap-1.5 transition-all ${
              isExploded ? 'bg-amber-400 text-slate-950 font-bold' : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
          >
            <Layers className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Pisah Layer</span>
          </button>

          <button
            onClick={() => setIsWireframe(!isWireframe)}
            title="Tampilkan Jaring Geometri (Wireframe Mode)"
            className={`p-2 rounded-xl text-xs flex items-center gap-1.5 transition-all ${
              isWireframe ? 'bg-amber-400 text-slate-950 font-bold' : 'text-slate-300 hover:text-white hover:bg-slate-800'
            }`}
          >
            <Box className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">Wireframe</span>
          </button>

          <button
            onClick={resetCamera}
            title="Atur Ulang Sudut Kamera"
            className="p-2 rounded-xl text-xs text-slate-300 hover:text-white hover:bg-slate-800 transition-all"
          >
            <RefreshCw className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>

      {/* Main 3D WebGL Canvas */}
      <div 
        ref={containerRef} 
        className="w-full h-[520px] sm:h-[600px] cursor-grab active:cursor-grabbing relative bg-gradient-to-b from-slate-950/60 via-slate-900/30 to-slate-950/80"
      >
        {isLoading && (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-slate-950/90 z-30">
            <div className="w-12 h-12 border-4 border-amber-400 border-t-transparent rounded-full animate-spin mb-4" />
            <p className="text-amber-400 font-semibold tracking-wider text-sm">
              Membangun Geometri 3D Vektor Master V6...
            </p>
          </div>
        )}

        {/* Floating Hint */}
        <div className="absolute bottom-4 left-4 z-10 pointer-events-none hidden sm:flex items-center gap-2 bg-slate-950/70 backdrop-blur-md px-3 py-1.5 rounded-xl border border-white/10 text-[11px] text-slate-400">
          <Compass className="w-3.5 h-3.5 text-amber-400" />
          <span>Klik & seret untuk memutar 360° • Gulir untuk memperbesar/memperkecil</span>
        </div>
      </div>

      {/* Bottom Component Selector Pills */}
      <div className="p-4 sm:p-6 bg-slate-950/90 border-t border-white/10">
        <div className="flex items-center justify-between mb-3">
          <span className="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5" />
            Sorot Anatomi Filosofis Lambang:
          </span>
          <span className="text-xs text-slate-400">Pilih komponen untuk fokus trimatra</span>
        </div>

        <div className="flex flex-wrap gap-2">
          {Object.entries(COMPONENT_DETAILS).map(([key, item]) => {
            const isActive = activeComponent === key;
            return (
              <button
                key={key}
                onClick={() => onSelectComponent ? onSelectComponent(key) : null}
                className={`px-3.5 py-2 rounded-xl text-xs font-semibold transition-all flex items-center gap-2 ${
                  isActive
                    ? 'bg-gradient-to-r from-amber-400 to-amber-500 text-slate-950 font-bold shadow-lg shadow-amber-500/25 scale-[1.02]'
                    : 'bg-slate-900/90 text-slate-300 hover:text-white hover:bg-slate-800/90 border border-white/5'
                }`}
              >
                <div
                  className="w-2 h-2 rounded-full"
                  style={{ backgroundColor: item.color }}
                />
                {item.title.split('(')[0]}
              </button>
            );
          })}
        </div>

        {/* Dynamic Philosophy Explanation Panel */}
        <div className="mt-4 p-4 rounded-2xl bg-slate-900/80 border border-amber-500/20 transition-all">
          <div className="flex flex-wrap items-center justify-between gap-2 mb-1.5">
            <h4 className="font-serif font-bold text-base text-amber-300 flex items-center gap-2">
              {currentDetails.title}
            </h4>
            <span className="px-2.5 py-0.5 text-[11px] font-bold rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30">
              {currentDetails.badge}
            </span>
          </div>
          <p className="text-xs font-semibold text-amber-400/90 mb-2">
            {currentDetails.subtitle}
          </p>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            {currentDetails.description}
          </p>
        </div>
      </div>
    </div>
  );
}
