import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'

export default defineConfig({
    plugins: [vue()],

    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },

    server: {
        port: 5173,
        host: true,
    },

    build: {
        // ✅ Code splitting strategy
        rollupOptions: {
            output: {
                manualChunks: {
                    // Vendor chunks
                    'vue-vendor': ['vue', 'vue-router', 'pinia'],
                    'ui-vendor': ['vue-toastification', 'vue-loading-overlay'],
                    'form-vendor': ['vee-validate', 'yup'],

                    // Heavy libraries - lazy load these
                    'canvas-libs': ['konva', 'vue-konva',],
                    'utils': ['axios', 'dayjs', 'dompurify', 'marked'],
                },

                // Better file naming
                chunkFileNames: 'assets/js/[name]-[hash].js',
                entryFileNames: 'assets/js/[name]-[hash].js',
                assetFileNames: (assetInfo) => {
                    const info = assetInfo.name.split('.')
                    const ext = info[info.length - 1]
                    if (/\.(png|jpe?g|svg|gif|tiff|bmp|ico)$/i.test(assetInfo.name)) {
                        return `assets/images/[name]-[hash].${ext}`
                    }
                    if (/\.(woff2?|eot|ttf|otf)$/i.test(assetInfo.name)) {
                        return `assets/fonts/[name]-[hash].${ext}`
                    }
                    return `assets/[ext]/[name]-[hash].${ext}`
                }
            }
        },

        // ✅ Build optimization
        minify: 'terser',
        terserOptions: {
            compress: {
                drop_console: true, // Remove console.log in production
                drop_debugger: true,
                pure_funcs: ['console.log', 'console.info'],
            },
            format: {
                comments: false, // Remove comments
            }
        },

        // ✅ Chunk size limits
        chunkSizeWarningLimit: 1000, // 1MB warning

        // ✅ Source maps only for production debugging
        sourcemap: false,

        // ✅ CSS code splitting
        cssCodeSplit: true,

        // ✅ Asset inlining threshold (4kb)
        assetsInlineLimit: 4096,

        // ✅ Target modern browsers
        target: 'esnext',
    },

    // ✅ Dependency optimization
    optimizeDeps: {
        include: [
            'vue',
            'vue-router',
            'pinia',
            'axios',
            'dayjs',
        ],
        exclude: [
            'konva',
        ]
    },

    // ✅ Preview server config
    preview: {
        port: 4173,
        strictPort: true,
    }
})