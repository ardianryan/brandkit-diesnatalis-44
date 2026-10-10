import React, { useEffect, useRef, useState, useCallback } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
import { SVGLoader } from 'three/examples/jsm/loaders/SVGLoader.js';
import { RoomEnvironment } from 'three/examples/jsm/environments/RoomEnvironment.js';
import { Play, Pause, Layers, Eye, RefreshCw, Sparkles, ChevronRight, Compass } from 'lucide-react';

export const COMPONENT_DETAILS = {
  all: {
    id: 'all',
    title: 'Lambang Utuh Dies Natalis 44',
    badge: 'V6 Master Final',
    tag: 'Keutuhan & Harmoni Rasio Keemasan',
    description: 'Sinergi trimatra agung yang memadukan figur kembar angka 44, siluet kepala rajawali menatap masa depan, kobaran api semangat abadi, dan akselerasi sayap aerodinamis dalam busur kurva simetris murni.',
    color: '#F5C538',
    metric: '100% Simetris Medial Spine'
  },
  twin44: {
    id: 'twin44',
    title: 'Figur Kembar Angka 44',
    badge: 'Anatomi Almamater',
    tag: 'Kedewasaan & Ikatan Luhur',
    description: 'Dua figur angka 4 yang bertaut harmonis melambangkan 44 tahun perjalanan SMA Negeri 1 Gedeg dalam menggembleng generasi tangguh, berintegritas tinggi, dan senantiasa menjunjung nama baik almamater.',
    color: '#E09B17',
    metric: 'Proporsi Proporsional V6'
  },
  eagle: {
    id: 'eagle',
    title: 'Kepala & Tatapan Rajawali',
    badge: 'Visi Visioner',
    tag: 'Ketegasan & Keberanian',
    description: 'Siluet kepala rajawali perkasa yang menatap tajam ke kanan atas mencerminkan pandangan visioner, ketajaman intelektual, ketegasan prinsip moral, dan keberanian membela kebenaran.',
    color: '#FDF39D',
    metric: 'Puncak Kurva Superior'
  },
  flame: {
    id: 'flame',
    title: 'Lidah Api Abadi Berkobar',
    badge: 'Energi Juang',
    tag: 'Semangat Pantang Padam',
    description: 'Lidah api dinamis yang berkobar dari pangkal bawah menyimbolkan tekad belajar yang tak kunjung padam, daya lenting menghadapi rintangan zaman, dan gelora kreativitas siswa yang terus menyala.',
    color: '#B6580B',
    metric: 'Pangkal Kedalaman Dimensi'
  },
  acceleration: {
    id: 'acceleration',
    title: 'Akselerasi Sayap Aerodinamis',
    badge: 'Dinamika Prestasi',
    tag: 'Kecepatan & Modernitas',
    description: 'Lengkung sayap yang melesat aerodinamis menyimbolkan akselerasi prestasi akademik dan non-akademik, transformasi teknologi cerdas, serta kesiapan menyongsong era global.',
    color: '#7D1B05',
    metric: 'Sudut Aerodinamis Melesat'
  },
  spine: {
    id: 'spine',
    title: 'Harmoni Medial Spine Simetris',
    badge: 'Penyempurnaan Master V6',
    tag: 'Presisi Busur Lingkaran Konsentris',
    description: 'Penyempurnaan radikal pada versi V6 berupa tulang punggung medial spine yang 100% simetris dengan busur lingkaran murni, melenyapkan inkonsistensi sudut sketsa manual terdahulu.',
    color: '#F7D160',
    metric: 'Radius Busur 100% Presisi'
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
  const particlesRef = useRef(null);
  const mouseLightRef = useRef(null);

  const [isPlaying, setIsPlaying] = useState(true);
  const [isExploded, setIsExploded] = useState(false);
  const [isWireframe, setIsWireframe] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Normalized mouse coordinates for Meng To-style parallax
  const mousePos = useRef({ x: 0, y: 0, targetX: 0, targetY: 0 });

  // Initialize Three.js Scene
  useEffect(() => {
    if (!containerRef.current) return;

    const container = containerRef.current;
    const width = container.clientWidth;
    const height = container.clientHeight || 580;

    // 1. Scene
    const scene = new THREE.Scene();
    sceneRef.current = scene;

    // 2. Camera
    const camera = new THREE.PerspectiveCamera(42, width / height, 1, 3500);
    camera.position.set(0, 0, 520);
    cameraRef.current = camera;

    // 3. Renderer with ACES Filmic Tone Mapping
    const renderer = new THREE.WebGLRenderer({
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance'
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.4;
    renderer.shadowMap.enabled = true;
    renderer.shadowMap.type = THREE.PCFSoftShadowMap;
    rendererRef.current = renderer;

    // Studio Environment Reflections for Photorealistic PBR Gold
    const pmremGenerator = new THREE.PMREMGenerator(renderer);
    pmremGenerator.compileEquirectangularShader();
    scene.environment = pmremGenerator.fromScene(new RoomEnvironment(), 0.04).texture;

    container.appendChild(renderer.domElement);

    // 4. Controls
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    controls.autoRotate = isPlaying;
    controls.autoRotateSpeed = 1.4;
    controls.maxDistance = 1200;
    controls.minDistance = 220;
    controls.enablePan = false;
    controlsRef.current = controls;

    // 5. Cinematic Lighting Rig
    const ambientLight = new THREE.AmbientLight(0xfff5e6, 1.8);
    scene.add(ambientLight);

    const keyLight = new THREE.DirectionalLight(0xffeedd, 3.8);
    keyLight.position.set(350, 450, 550);
    scene.add(keyLight);

    const warmFill = new THREE.DirectionalLight(0xd48911, 2.6);
    warmFill.position.set(-400, -250, -300);
    scene.add(warmFill);

    const rimLight = new THREE.DirectionalLight(0xfff8e7, 3.2);
    rimLight.position.set(0, 550, -450);
    scene.add(rimLight);

    // Interactive Cursor Spotlight (Sylva light pool effect)
    const mouseLight = new THREE.PointLight(0xf5c538, 4.2, 1400);
    mouseLight.position.set(0, 0, 320);
    scene.add(mouseLight);
    mouseLightRef.current = mouseLight;

    // 6. Floating Golden Ember Particles (350 procedural particles)
    const particleCount = 350;
    const particleGeometry = new THREE.BufferGeometry();
    const particlePositions = new Float32Array(particleCount * 3);
    const particleScales = new Float32Array(particleCount);
    const particleSpeeds = new Float32Array(particleCount);

    for (let i = 0; i < particleCount; i++) {
      particlePositions[i * 3] = (Math.random() - 0.5) * 800;
      particlePositions[i * 3 + 1] = (Math.random() - 0.5) * 700;
      particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 600;
      particleScales[i] = Math.random() * 2.5 + 0.8;
      particleSpeeds[i] = Math.random() * 0.4 + 0.2;
    }

    particleGeometry.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));
    particleGeometry.setAttribute('scale', new THREE.BufferAttribute(particleScales, 1));

    // Particle Canvas Texture
    const particleCanvas = document.createElement('canvas');
    particleCanvas.width = 32;
    particleCanvas.height = 32;
    const pctx = particleCanvas.getContext('2d');
    const pGrad = pctx.createRadialGradient(16, 16, 0, 16, 16, 16);
    pGrad.addColorStop(0, 'rgba(253, 243, 157, 1)');
    pGrad.addColorStop(0.3, 'rgba(245, 197, 56, 0.7)');
    pGrad.addColorStop(1, 'rgba(182, 88, 11, 0)');
    pctx.fillStyle = pGrad;
    pctx.beginPath();
    pctx.arc(16, 16, 16, 0, Math.PI * 2);
    pctx.fill();

    const particleTexture = new THREE.CanvasTexture(particleCanvas);
    const particleMaterial = new THREE.PointsMaterial({
      size: 6,
      map: particleTexture,
      transparent: true,
      blending: THREE.AdditiveBlending,
      depthWrite: false,
      opacity: 0.75
    });

    const particles = new THREE.Points(particleGeometry, particleMaterial);
    scene.add(particles);
    particlesRef.current = { mesh: particles, speeds: particleSpeeds };

    // 7. Master Logo Layers Group
    const layersGroup = new THREE.Group();
    layersGroupRef.current = layersGroup;
    scene.add(layersGroup);

    // 8. SVGLoader for Master V6 SVG
    const svgLoader = new SVGLoader();
    svgLoader.load(
      '/assets/svg/logo-symbol-color.svg',
      (svgData) => {
        const paths = svgData.paths;
        const meshes = [];

        // Definition of the 4 harmonic facets from V6
        const facetSpecs = [
          { name: 'base', color: 0xB6580B, depth: 32, zOffset: 0, roughness: 0.28, metalness: 0.75, component: 'flame' },
          { name: 'marigold', color: 0xE09B17, depth: 38, zOffset: 8, roughness: 0.22, metalness: 0.80, component: 'twin44' },
          { name: 'vivid', color: 0xF5C538, depth: 44, zOffset: 16, roughness: 0.18, metalness: 0.85, component: 'spine' },
          { name: 'champagne', color: 0xFDF39D, depth: 48, zOffset: 24, roughness: 0.14, metalness: 0.88, component: 'eagle' }
        ];

        paths.forEach((path, index) => {
          const shapes = path.toShapes(true);
          const spec = facetSpecs[index % facetSpecs.length];

          shapes.forEach((shape) => {
            const extrudeSettings = {
              depth: spec.depth,
              bevelEnabled: true,
              bevelSegments: 5,
              steps: 1,
              bevelSize: 2.2,
              bevelThickness: 2.2
            };

            const geometry = new THREE.ExtrudeGeometry(shape, extrudeSettings);

            const material = new THREE.MeshStandardMaterial({
              color: spec.color,
              metalness: spec.metalness,
              roughness: spec.roughness,
              wireframe: false,
              emissive: 0x331a00,
              emissiveIntensity: 0.18,
              side: THREE.DoubleSide
            });

            const mesh = new THREE.Mesh(geometry, material);
            // Invert Y coordinate from standard SVG coordinates
            mesh.scale.set(0.24, -0.24, 0.24);
            mesh.position.z = spec.zOffset;
            mesh.castShadow = true;
            mesh.receiveShadow = true;
            mesh.userData = {
              defaultColor: spec.color,
              defaultZ: spec.zOffset,
              targetZ: spec.zOffset,
              component: spec.component,
              spec: spec
            };

            layersGroup.add(mesh);
            meshes.push(mesh);
          });
        });

        // Perfect Centering via Box3 on the entire composite group
        const box = new THREE.Box3().setFromObject(layersGroup);
        const center = new THREE.Vector3();
        box.getCenter(center);
        layersGroup.position.x = -center.x;
        layersGroup.position.y = -center.y;
        layersGroup.position.z = -center.z;

        meshesRef.current = meshes;
        setIsLoading(false);
      },
      undefined,
      (error) => {
        console.error('Error loading Master V6 SVG into Three.js:', error);
        setIsLoading(false);
      }
    );

    // 9. Pointer Parallax Listener (Sylva interaction model)
    const handlePointerMove = (e) => {
      const rect = container.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      const y = -(((e.clientY - rect.top) / rect.height) * 2 - 1);
      mousePos.current.targetX = x;
      mousePos.current.targetY = y;
    };

    container.addEventListener('pointermove', handlePointerMove);

    // 10. Animation Loop with Parallax & Particle Flow
    let animationFrameId;
    const clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const delta = clock.getDelta();

      // Smooth damping interpolation for mouse parallax
      mousePos.current.x = THREE.MathUtils.lerp(mousePos.current.x, mousePos.current.targetX, 0.05);
      mousePos.current.y = THREE.MathUtils.lerp(mousePos.current.y, mousePos.current.targetY, 0.05);

      // Move interactive spotlight according to cursor
      if (mouseLightRef.current) {
        mouseLightRef.current.position.x = mousePos.current.x * 250;
        mouseLightRef.current.position.y = mousePos.current.y * 220;
      }

      // Parallax camera tilt when not actively dragging
      if (controlsRef.current) {
        controlsRef.current.update();
      }

      // Animate floating embers
      if (particlesRef.current) {
        const positions = particlesRef.current.mesh.geometry.attributes.position.array;
        const speeds = particlesRef.current.speeds;
        for (let i = 0; i < particleCount; i++) {
          positions[i * 3 + 1] += speeds[i]; // Float upward
          // Recycle particles that move too high
          if (positions[i * 3 + 1] > 380) {
            positions[i * 3 + 1] = -380;
            positions[i * 3] = (Math.random() - 0.5) * 800;
          }
        }
        particlesRef.current.mesh.geometry.attributes.position.needsUpdate = true;
        particlesRef.current.mesh.rotation.y += 0.0012;
      }

      // Animate layer explosion smoothly
      meshesRef.current.forEach((mesh) => {
        mesh.position.z = THREE.MathUtils.lerp(mesh.position.z, mesh.userData.targetZ, 0.08);
      });

      renderer.render(scene, camera);
    };
    animate();

    // 11. Responsive Resize
    const handleResize = () => {
      if (!container || !rendererRef.current || !cameraRef.current) return;
      const newWidth = container.clientWidth;
      const newHeight = container.clientHeight || 580;
      cameraRef.current.aspect = newWidth / newHeight;
      cameraRef.current.updateProjectionMatrix();
      rendererRef.current.setSize(newWidth, newHeight);
    };

    window.addEventListener('resize', handleResize);
    const resizeObserver = new ResizeObserver(handleResize);
    resizeObserver.observe(container);

    return () => {
      window.removeEventListener('resize', handleResize);
      resizeObserver.disconnect();
      container.removeEventListener('pointermove', handlePointerMove);
      cancelAnimationFrame(animationFrameId);
      if (renderer.domElement && container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
      renderer.dispose();
    };
  }, []);

  // Sync Auto-Rotate
  useEffect(() => {
    if (controlsRef.current) {
      controlsRef.current.autoRotate = isPlaying;
    }
  }, [isPlaying]);

  // Handle Explode Layers
  useEffect(() => {
    meshesRef.current.forEach((mesh) => {
      if (isExploded) {
        mesh.userData.targetZ = mesh.userData.defaultZ * 3.2 + 25;
      } else {
        mesh.userData.targetZ = mesh.userData.defaultZ;
      }
    });
  }, [isExploded]);

  // Handle Wireframe Toggle
  useEffect(() => {
    meshesRef.current.forEach((mesh) => {
      if (mesh.material) {
        mesh.material.wireframe = isWireframe;
      }
    });
  }, [isWireframe]);

  // Highlight Active Component
  useEffect(() => {
    meshesRef.current.forEach((mesh) => {
      const isTarget = activeComponent === 'all' || mesh.userData.component === activeComponent;
      if (mesh.material) {
        if (isTarget) {
          mesh.material.color.setHex(mesh.userData.defaultColor);
          mesh.material.emissive.setHex(activeComponent === 'all' ? 0x331a00 : 0x663300);
          mesh.material.emissiveIntensity = activeComponent === 'all' ? 0.18 : 0.65;
          mesh.material.opacity = 1.0;
        } else {
          mesh.material.emissiveIntensity = 0.05;
          mesh.material.color.setHex(0x554433);
        }
      }
    });
  }, [activeComponent]);

  // Reset Camera View
  const handleResetCamera = useCallback(() => {
    if (cameraRef.current && controlsRef.current) {
      cameraRef.current.position.set(0, 0, 520);
      controlsRef.current.target.set(0, 0, 0);
      controlsRef.current.update();
      setIsExploded(false);
      setIsWireframe(false);
      setIsPlaying(true);
      if (onSelectComponent) onSelectComponent('all');
    }
  }, [onSelectComponent]);

  const activeDetail = COMPONENT_DETAILS[activeComponent] || COMPONENT_DETAILS.all;

  return (
    <div className="relative w-full rounded-3xl overflow-hidden glass-panel border border-[var(--border-card)] shadow-2xl">
      {/* Three.js Canvas Container */}
      <div
        ref={containerRef}
        className="w-full h-[520px] sm:h-[620px] lg:h-[680px] cursor-grab active:cursor-grabbing relative"
      >
        {/* Loading Indicator */}
        {isLoading && (
          <div className="absolute inset-0 z-20 flex flex-col items-center justify-center bg-[var(--bg-primary)]/80 backdrop-blur-md">
            <div className="w-12 h-12 rounded-full border-2 border-amber-400 border-t-transparent animate-spin mb-4" />
            <span className="font-serif text-sm font-bold tracking-widest text-amber-500 uppercase">
              Memuat Model Trimatra 3D V6...
            </span>
          </div>
        )}

        {/* Top Control Bar (Sylva Studio Capsule) */}
        <div className="absolute top-4 left-4 right-4 z-10 flex flex-wrap items-center justify-between gap-3 pointer-events-none">
          {/* Badge Studio */}
          <div className="pointer-events-auto inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full glass-dock border border-amber-500/30 shadow-lg">
            <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse" />
            <span className="text-[11px] font-mono font-bold tracking-wider uppercase text-amber-500 dark:text-amber-300">
              WEBGL 3D PBR STUDIO • 100% SIMETRIS V6
            </span>
          </div>

          {/* Action Pills */}
          <div className="pointer-events-auto flex items-center gap-2">
            <button
              onClick={() => setIsPlaying(!isPlaying)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold flex items-center gap-1.5 transition-all glass-dock border ${
                isPlaying
                  ? 'border-amber-400 text-amber-500 dark:text-amber-300'
                  : 'border-[var(--border-card)] text-themed-secondary hover:text-amber-500'
              }`}
              title="Putar Lambang Otomatis"
            >
              {isPlaying ? <Pause className="w-3.5 h-3.5" /> : <Play className="w-3.5 h-3.5" />}
              <span>{isPlaying ? 'Jeda Rotasi' : 'Putar 360°'}</span>
            </button>

            <button
              onClick={() => setIsExploded(!isExploded)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold flex items-center gap-1.5 transition-all glass-dock border ${
                isExploded
                  ? 'border-amber-400 text-amber-500 dark:text-amber-300 shadow-md shadow-amber-500/20'
                  : 'border-[var(--border-card)] text-themed-secondary hover:text-amber-500'
              }`}
              title="Pisahkan Layer Facet Trimatra"
            >
              <Layers className="w-3.5 h-3.5" />
              <span>{isExploded ? 'Satukan Layer' : 'Bedah Lapisan 3D'}</span>
            </button>

            <button
              onClick={() => setIsWireframe(!isWireframe)}
              className={`px-3 py-1.5 rounded-full text-xs font-semibold flex items-center gap-1.5 transition-all glass-dock border ${
                isWireframe
                  ? 'border-amber-400 text-amber-500 dark:text-amber-300'
                  : 'border-[var(--border-card)] text-themed-secondary hover:text-amber-500'
              }`}
              title="Mode Kerangka Vektor"
            >
              <Eye className="w-3.5 h-3.5" />
              <span>{isWireframe ? 'PBR Padat' : 'Wireframe'}</span>
            </button>

            <button
              onClick={handleResetCamera}
              className="p-2 rounded-full glass-dock border border-[var(--border-card)] text-themed-secondary hover:text-amber-500 hover:border-amber-400 transition-colors"
              title="Reset Sudut Pandang"
            >
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Floating Living Anatomy Inspection Card (Sylva-inspired Field Note) */}
        <div className="absolute bottom-5 left-4 right-4 sm:left-6 sm:right-auto sm:max-w-md z-10 pointer-events-auto">
          <div className="glass-panel p-5 rounded-2xl border border-amber-500/30 backdrop-blur-xl shadow-2xl">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[10px] font-mono font-bold uppercase tracking-widest text-amber-500 dark:text-amber-300 px-2 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/20">
                {activeDetail.badge}
              </span>
              <span className="text-[10px] font-mono text-themed-secondary">
                {activeDetail.metric}
              </span>
            </div>

            <h3 className="font-serif text-lg sm:text-xl font-bold title-primary mb-1">
              {activeDetail.title}
            </h3>

            <p className="text-xs text-themed-secondary leading-relaxed mb-3">
              {activeDetail.description}
            </p>

            {/* Component Quick Filter Strip */}
            <div className="flex flex-wrap items-center gap-1.5 pt-2 border-t border-[var(--border-subtle)]">
              <span className="text-[10px] text-themed-tertiary mr-1 font-semibold">Sorot Bagian:</span>
              {[
                { id: 'all', label: 'Utuh' },
                { id: 'twin44', label: 'Angka 44' },
                { id: 'eagle', label: 'Rajawali' },
                { id: 'flame', label: 'Api' },
                { id: 'acceleration', label: 'Sayap' },
                { id: 'spine', label: 'Spine V6' }
              ].map((item) => (
                <button
                  key={item.id}
                  onClick={() => onSelectComponent && onSelectComponent(item.id)}
                  className={`text-[10px] px-2.5 py-1 rounded-full font-semibold transition-all ${
                    activeComponent === item.id
                      ? 'bg-amber-500 text-slate-950 font-bold shadow-md'
                      : 'bg-[var(--bg-secondary)] text-themed-secondary hover:text-amber-500'
                  }`}
                >
                  {item.label}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Orbit Helper Prompt */}
        <div className="absolute bottom-4 right-4 z-10 hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full glass-dock text-[11px] text-themed-secondary border border-[var(--border-card)] pointer-events-none">
          <Compass className="w-3.5 h-3.5 text-amber-500 animate-spin" style={{ animationDuration: '8s' }} />
          <span>Klik &amp; seret untuk memutar 360° • Gulir untuk memperbesar</span>
        </div>
      </div>
    </div>
  );
}
