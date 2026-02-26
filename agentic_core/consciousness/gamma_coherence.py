import numpy as np
import logging
from scipy.fft import fft, ifft, fftfreq

logger = logging.getLogger(__name__)

def morlet_wavelet(f0, fs, n_cycles=6.0):
    """
    Complex Morlet wavelet for a specific target frequency.
    f0: target frequency (Hz)
    fs: sampling frequency (Hz)
    n_cycles: trade-off between time and frequency resolution (default 6.0)
    """
    # Time length of wavelet: enough to cover the Gaussian envelope
    # Sigma in time domain = n_cycles / (2 * pi * f0)
    sigma_t = n_cycles / (2 * np.pi * f0)
    t = np.arange(-5 * sigma_t, 5 * sigma_t, 1/fs)

    # Complex Morlet formula
    # normalization factor A = 1 / (sigma_t * sqrt(pi)) ^ 0.5
    norm_constant = 1 / (sigma_t * np.sqrt(np.pi))**0.5
    wavelet = norm_constant * np.exp(2j * np.pi * f0 * t) * np.exp(-t**2 / (2 * sigma_t**2))
    return wavelet

class GammaCoherenceMonitor:
    """
    ARTICLE DB: Gamma-Band Coherence (40±5 Hz).
    Implements Phase Locking Value (PLV) monitoring using custom fCWT logic.
    Target: ≥4 cycles (≥100 ms).
    """
    def __init__(self, target_freq: float = 40.0, fs: float = 1000.0):
        self.target_freq = target_freq
        self.fs = fs
        self.threshold = 0.8
        self.consecutive_integrated = 0
        self.wavelet = morlet_wavelet(target_freq, fs)

    def calculate_coherence(self, signal_a: np.ndarray, signal_b: np.ndarray) -> float:
        """
        Calculates Phase Locking Value (PLV) between two signals using fCWT-optimized Morlet convolution.
        """
        # Perform FFT-based convolution for fCWT behavior
        # Length for FFT
        n = len(signal_a) + len(self.wavelet) - 1
        n_fft = 2**int(np.ceil(np.log2(n))) # Next power of 2 for speed

        # Frequency domain convolution
        fft_wavelet = fft(self.wavelet, n_fft)

        # Signal A
        cwt_a = ifft(fft(signal_a, n_fft) * fft_wavelet)
        # Signal B
        cwt_b = ifft(fft(signal_b, n_fft) * fft_wavelet)

        # Trim to original signal size (centered)
        start = (len(self.wavelet) - 1) // 2
        cwt_a = cwt_a[start:start+len(signal_a)]
        cwt_b = cwt_b[start:start+len(signal_b)]

        # Extract phase
        phase_a = np.angle(cwt_a)
        phase_b = np.angle(cwt_b)

        # PLV = | (1/N) * sum( exp(i * (phi_a - phi_b)) ) |
        phase_diff = phase_a - phase_b
        plv = np.abs(np.mean(np.exp(1j * phase_diff)))

        if plv >= self.threshold:
            self.consecutive_integrated += 1
        else:
            self.consecutive_integrated = 0

        return float(plv)

    def is_consciously_integrated(self) -> bool:
        """Requirement: ≥4 cycles (approx 100ms at 40Hz)."""
        return self.consecutive_integrated >= 4
