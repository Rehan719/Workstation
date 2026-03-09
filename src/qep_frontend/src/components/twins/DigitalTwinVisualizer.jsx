import React, { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial, Text } from '@react-three/drei';

const DigitalTwinVisualizer = ({ twinData }) => {
  const meshRef = useRef();

  useFrame((state) => {
    const t = state.clock.getElapsedTime();
    if (meshRef.current) {
      meshRef.current.rotation.x = Math.cos(t / 4) / 8;
      meshRef.current.rotation.y = Math.sin(t / 4) / 8;
      meshRef.current.position.y = (1 + Math.sin(t / 1.5)) / 10;
    }
  });

  return (
    <group>
      <Sphere ref={meshRef} args={[1, 64, 64]} position={[0, 0, 0]}>
        <MeshDistortMaterial
          color="#f59e0b"
          speed={2}
          distort={0.4}
          radius={1}
        />
        <Text
          position={[0, 1.5, 0]}
          fontSize={0.2}
          color="white"
          font="/fonts/Inter-Bold.woff"
        >
          {twinData?.name || 'Digital Twin Active'}
        </Text>
      </Sphere>

      {/* Simulation Data Nodes */}
      <mesh position={[2, 0, 0]}>
        <boxGeometry args={[0.2, 0.2, 0.2]} />
        <meshStandardMaterial color="#3b82f6" emissive="#3b82f6" />
      </mesh>
    </group>
  );
};

export default DigitalTwinVisualizer;
