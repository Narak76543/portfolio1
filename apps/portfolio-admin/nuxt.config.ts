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
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL || 'https://narak-portfolio-backend.fastapicloud.dev',
      supabaseUrl: process.env.NUXT_PUBLIC_SUPABASE_URL || 'https://zcsgqdbqabksyyzstdtq.supabase.co',
      supabaseAnonKey: process.env.NUXT_PUBLIC_SUPABASE_ANON_KEY || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpjc2dxZGJxYWJrc3l5enN0ZHRxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODUyNTUxNzIsImV4cCI6MjEwMDgzMTE3Mn0.xTOu1gf7s8_6Z5LKOz1U7XG9-KTGE7sR__uC1TZ-9jQ',
      publicAppUrl: process.env.NUXT_PUBLIC_APP_URL || process.env.PUBLIC_APP_URL || 'https://portfolio1-portfolio-admin.vercel.app',
    },
  },

  app: {
    pageTransition: { name: 'page', mode: 'out-in' },
    layoutTransition: { name: 'layout', mode: 'out-in' },
    head: {
      script: [
        { innerHTML: "(function(){var t=localStorage.getItem('theme');document.documentElement.classList.toggle('dark',t?t==='dark':matchMedia('(prefers-color-scheme: dark)').matches)})()" },
      ],
      title: 'Admin — SARAT NARAK',
      link: [
        { rel: 'icon', type: 'image/x-icon', href: '/admin-favicon.ico' },
        { rel: 'icon', type: 'image/png', sizes: '32x32', href: '/admin-favicon-32x32.png' },
        { rel: 'icon', type: 'image/png', sizes: '16x16', href: '/admin-favicon-16x16.png' },
        { rel: 'apple-touch-icon', sizes: '180x180', href: '/admin-apple-touch-icon.png' },
        { rel: 'manifest', href: '/site.webmanifest' },
      ],
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      ],
    },
  },
})
