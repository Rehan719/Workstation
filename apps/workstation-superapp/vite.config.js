import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react-swc'
import path from 'path'

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const apiTarget = env.VITE_API_BASE_URL || 'http://localhost:8000'

  return {
    plugins: [react()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, './src'),
        '@workstation/shared': path.resolve(__dirname, '../../packages/shared'),
        '@workstation/ui': path.resolve(__dirname, '../../packages/ui/src'),
        '@superapp': path.resolve(__dirname, './src'),
        'react-native': 'react-native-web',
      },
    },
    server: {
      proxy: {
        '/api': {
          target: apiTarget,
          changeOrigin: true,
          ws: true,
        }
      }
    },
    build: {
      // Chunking is left to Vite/Rollup's automatic strategy ON PURPOSE.
      // A previous custom manualChunks() (separating react-vendor / vendor / charts / motion) split
      // circularly-dependent modules across chunks, which produced a load-order temporal-dead-zone at
      // runtime ("Cannot access 'X' before initialization") — the production bundle failed to mount
      // React entirely (dev was fine because it doesn't chunk). Automatic chunking orders circular deps
      // correctly. Keep the warning limit generous since the SPA is large.
      chunkSizeWarningLimit: 1600,
    },
  }
})
