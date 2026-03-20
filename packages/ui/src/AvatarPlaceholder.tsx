import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';

export const AvatarPlaceholder = ({ mood = 'thinking' }: { mood?: string }) => {
  const mountRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!mountRef.current) return;

    // Three.js setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });

    const size = 300;
    renderer.setSize(size, size);
    mountRef.current.appendChild(renderer.domElement);

    // Geometry: A more "conscious" shape
    const geometry = new THREE.IcosahedronGeometry(1.5, 4);
    const material = new THREE.MeshNormalMaterial({ wireframe: true });
    const sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);

    camera.position.z = 5;

    // Animation: React to mood
    const animate = () => {
      requestAnimationFrame(animate);

      const time = Date.now() * 0.001;

      if (mood === 'thinking') {
        sphere.rotation.x += 0.01;
        sphere.rotation.y += 0.01;
        sphere.scale.set(1 + Math.sin(time) * 0.1, 1 + Math.sin(time) * 0.1, 1 + Math.sin(time) * 0.1);
      } else if (mood === 'speaking') {
        sphere.rotation.y += 0.05;
        sphere.scale.set(1 + Math.cos(time * 2) * 0.3, 1 + Math.cos(time * 2) * 0.3, 1 + Math.cos(time * 2) * 0.3);
      } else {
        sphere.rotation.z += 0.005;
      }

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      if (mountRef.current) {
        mountRef.current.removeChild(renderer.domElement);
      }
    };
  }, [mood]);

  return (
    <div
      ref={mountRef}
      className="relative w-72 h-72 rounded-full overflow-hidden bg-slate-900/20 border border-slate-800 shadow-2xl flex items-center justify-center backdrop-blur-3xl group"
    >
      <div className="absolute inset-0 bg-aura/5 opacity-0 group-hover:opacity-100 transition-opacity duration-1000" />
      <div className="absolute bottom-6 px-4 py-1 rounded-full bg-slate-900/60 text-[10px] font-mono text-aura uppercase tracking-widest border border-aura/20">
        AI CEO v3.0 Status: {mood}
      </div>
    </div>
  );
};
