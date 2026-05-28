import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';

const HolographicForge: React.FC = () => {
    const mountRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (!mountRef.current) return;

        // 1. Scene Setup
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(75, mountRef.current.clientWidth / mountRef.current.clientHeight, 0.1, 1000);
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(mountRef.current.clientWidth, mountRef.current.clientHeight);
        mountRef.current.appendChild(renderer.domElement);

        // 2. Holographic Mesh (Article 1200)
        const geometry = new THREE.IcosahedronGeometry(1, 2);
        const material = new THREE.MeshBasicMaterial({
            color: 0x00ff00,
            wireframe: true,
            transparent: true,
            opacity: 0.5
        });
        const mesh = new THREE.Mesh(geometry, material);
        scene.add(mesh);

        // 3. Orbiting "Agents"
        const agents: THREE.Mesh[] = [];
        for (let i = 0; i < 5; i++) {
            const agentGeom = new THREE.SphereGeometry(0.1, 8, 8);
            const agentMat = new THREE.MeshBasicMaterial({ color: 0x00d4ff });
            const agent = new THREE.Mesh(agentGeom, agentMat);
            agent.position.set(Math.cos(i) * 2, Math.sin(i) * 2, 0);
            scene.add(agent);
            agents.push(agent);
        }

        camera.position.z = 5;

        // 4. Animation Loop
        const animate = () => {
            requestAnimationFrame(animate);
            mesh.rotation.x += 0.01;
            mesh.rotation.y += 0.01;

            agents.forEach((a, i) => {
                const t = Date.now() * 0.001 + i;
                a.position.x = Math.cos(t) * 1.5;
                a.position.y = Math.sin(t) * 1.5;
                a.position.z = Math.sin(t * 2) * 0.5;
            });

            renderer.render(scene, camera);
        };
        animate();

        return () => {
            if (mountRef.current) mountRef.current.removeChild(renderer.domElement);
        };
    }, []);

    return (
        <div style={{ padding: '20px', background: '#0a0a0a', color: '#fff', borderRadius: '12px', border: '1px solid #ff00ff' }}>
            <div style={{ marginBottom: '15px' }}>
                <h2 style={{ margin: 0, color: '#ff00ff', textShadow: '0 0 10px #ff00ff' }}>Holographic Agent Forge (L13)</h2>
                <p style={{ fontSize: '10px', color: '#888' }}>3D Immersive Swarm Composition Active</p>
            </div>
            <div ref={mountRef} style={{ width: '100%', height: '300px', background: '#000', borderRadius: '8px' }} />
            <div style={{ marginTop: '15px', display: 'flex', gap: '10px' }}>
                <button style={{ background: '#1a1a1a', color: '#ff00ff', border: '1px solid #ff00ff', padding: '5px 15px', borderRadius: '4px', cursor: 'pointer' }}>INFUSE QUALIA</button>
                <button style={{ background: '#ff00ff', color: '#fff', border: 'none', padding: '5px 15px', borderRadius: '4px', fontWeight: 'bold' }}>PROJECT SWARM</button>
            </div>
        </div>
    );
};

export default HolographicForge;
