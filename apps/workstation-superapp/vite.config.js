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
      // App ships as one large SPA; split rarely-changing vendor code into
      // separately-cacheable chunks so a code change doesn't re-download all deps.
      chunkSizeWarningLimit: 1200,
      rollupOptions: {
        output: {
          manualChunks(id) {
            if (!id.includes('node_modules')) return undefined
            if (/[\\/]node_modules[\\/](react|react-dom|react-router|react-router-dom|scheduler)[\\/]/.test(id)) return 'react-vendor'
            if (id.includes('lucide-react')) return 'icons'
            if (id.includes('recharts') || id.includes('d3-') || id.includes('victory')) return 'charts'
            if (id.includes('framer-motion')) return 'motion'
            if (id.includes('react-native-web')) return 'rn-web'
            return 'vendor'
          },
        },
      },
    },
  }
})
