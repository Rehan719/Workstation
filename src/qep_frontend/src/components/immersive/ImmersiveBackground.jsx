import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, Stars, Text } from '@react-three/drei';

const GeometricCore = ({ color }) => {
  const mesh = useRef();
  useFrame((state) => {
    mesh.current.rotation.x = state.clock.getElapsedTime() * 0.2;
    mesh.current.rotation.y = state.clock.getElapsedTime() * 0.3;
  });

  return (
    <mesh ref={mesh}>
      <octahedronGeometry args={[2, 0]} />
      <meshStandardMaterial color={color} wireframe />
    </mesh>
  );
};

const ImmersiveBackground = ({ domain }) => {
  const themes = {
    religion: '#f59e0b',
    education: '#10b981',
    science: '#06b6d4',
    law: '#facc15',
    business: '#ec4899'
  };

  const color = themes[domain] || '#4f46e5';

  return (
    <div className="absolute inset-0 z-[-1] bg-slate-950 overflow-hidden">
      <Canvas camera={{ position: [0, 0, 5] }}>
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />
        <Float speed={2} rotationIntensity={1} floatIntensity={1}>
           <GeometricCore color={color} />
        </Float>
      </Canvas>
    </div>
  );
};

export default ImmersiveBackground;
