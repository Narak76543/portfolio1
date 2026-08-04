// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from '@tailwindcss/vite'

export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  experimental: {
    appManifest: false,
  },

  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],

  modules: ['@nuxt/fonts'],

  fonts: {
    families: [
      { name: 'Onest', provider: 'google', weights: [400, 500, 600, 700] },
    ],
  },

  css: ['~/assets/css/main.css'],

  vite: {
    plugins: [tailwindcss()],
    server: {
      hmr: {
        overlay: false,
      },
    },
  },

  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
      supabaseUrl: process.env.NUXT_PUBLIC_SUPABASE_URL || '',
      supabaseAnonKey: process.env.NUXT_PUBLIC_SUPABASE_ANON_KEY || '',
    },
  },

  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
    layoutTransition: { name: 'layout', mode: 'out-in' },
    head: {
      script: [
        { innerHTML: "(function(){var t=localStorage.getItem('theme');document.documentElement.classList.toggle('dark',t?t==='dark':matchMedia('(prefers-color-scheme: dark)').matches)})()" },
      ],
      title: 'SARAT NARAK — IT Student & Full-Stack Developer',
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/favicon-32x32.png' },
        { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/favicon-16x16.png' },
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/apple-touch-icon.png' },
        { rel: 'manifest', href: '/site.webmanifest' },
      ],
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        {
          name: 'description',
          content:
            "I'm an IT student who builds full-stack applications — from mobile apps to backend APIs — and this portfolio itself is one of my projects.",
        },
      ],
    },
  },
})
