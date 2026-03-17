import { useState, useEffect } from 'react';
import * as LocalAuthentication from 'expo-local-authentication';

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
    if (!isCompatible || !isEnrolled) return true; // Fallback for simulators

    const result = await LocalAuthentication.authenticateAsync({
      promptMessage: 'Sovereign Handshake Required',
      fallbackLabel: 'Enter PIN',
    });

    return result.success;
  };

  return { authenticate, isCompatible, isEnrolled };
};
