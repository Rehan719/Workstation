# Zero-Cost Infrastructure Strategy (v2.0)

## 1. Cloud Hosting
*   **Vercel / Render:** Free tier for React/Next.js frontend.
*   **Supabase / PlanetScale:** Free tier for PostgreSQL/Metadata.
*   **Upstash:** Free tier for Redis (Caching).

## 2. Intelligence & Generation
*   **Hugging Face Inference API:** Free tier for quantized models.
*   **Groq / DeepSeek:** Free API credits (where available).
*   **Local Processing:** Offloading inference to client-side (Transformers.js) for PWA features.

## 3. Quantum Simulation
*   **Qiskit Aer:** Local classical simulation (Python).
*   **Cirq Simulator:** Local simulation.
*   **IBM Quantum:** Limited free-tier jobs for valid academic/research.

## 4. Resource Optimization
*   **Aggressive Caching:** AI Dispatcher caches common generation results.
*   **Throttling:** Stricter rate limits for Free Tier (Article 238).
