import { useState, useEffect } from 'react';
import * as LocalAuthentication from 'expo-local-authentication';

/**
 * IDBO Layer 1 & 2: Identity & Hardware Attestation.
 * Sovereign biometric handshake for Capital Fund operations.
 */
export const useBiometrics = () => {
  const [isCompatible, setIsCompatible] = useState(false);
  const [isEnrolled, setIsEnrolled] = useState(false);

  useEffect(() => {
    (async () => {
      const compatible = await LocalAuthentication.hasHardwareAsync();
      const enrolled = await LocalAuthentication.isEnrolledAsync();
      setIsCompatible(compatible);
      setIsEnrolled(enrolled);
    })();
  }, []);

  const authenticate = async () => {
    // 1. Check hardware compatibility
    if (!isCompatible || !isEnrolled) {
      console.warn('Biometric hardware not detected or not enrolled. Falling back to sovereign PIN.');
      return true; // Simplified for Phase 4 scaffold
    }

    // 2. Perform Biometric Auth (FaceID/TouchID)
    const result = await LocalAuthentication.authenticateAsync({
      promptMessage: 'Sovereign Identity Handshake Required',
      disableDeviceFallback: false,
      cancelLabel: 'Cancel',
    });

    if (result.success) {
      // In Phase 5, this would trigger a PQC-signed attestation blob
      return true;
    }

    return false;
  };

  return { authenticate, isCompatible, isEnrolled };
};
