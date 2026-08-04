<template>
  <div class="min-h-screen flex flex-col font-sans bg-background dark:bg-black text-text-primary dark:text-[#F2F2F7] transition-colors duration-300">
    <header class="sticky top-0 z-50 bg-surface/90 dark:bg-[#1C1C1E]/90 backdrop-blur-md border-b border-border/60 dark:border-white/8 transition-colors">
      <nav class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <NuxtLink to="/" class="flex items-center gap-2">
          <img
            v-if="profile?.logo_type === 'image' && profile?.logo_image_url"
            :src="profile.logo_image_url"
            :alt="profile?.logo_text || 'SARAT NARAK'"
            class="h-8 md:h-9 w-auto object-contain"
          />
          <span
            v-else
            class="text-xl font-extrabold text-text-primary dark:text-[#F2F2F7] tracking-wider uppercase inline-flex items-center"
            :style="profile?.heading_font_name ? { fontFamily: `'${profile.heading_font_name}', 'Onest', sans-serif` } : {}"
          >
            <span>{{ firstWord }}</span>
            <span class="text-text-secondary dark:text-[#8E8E93] font-bold ml-1.5">{{ secondWord }}</span>
            <span class="w-1.5 h-1.5 rounded-full bg-primary ml-1" />
          </span>
        </NuxtLink>
        <ul class="hidden md:flex items-center gap-1 text-sm font-medium text-text-secondary dark:text-[#8E8E93]">
          <li><a href="#about" class="px-3 py-1.5 rounded-full hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/8 transition-colors">About</a></li>
          <li><a href="#projects" class="px-3 py-1.5 rounded-full hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/8 transition-colors">Projects</a></li>
          <li><a href="#skills" class="px-3 py-1.5 rounded-full hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/8 transition-colors">Skills</a></li>
          <li><a href="#contact" class="px-3 py-1.5 rounded-full hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/8 transition-colors">Contact</a></li>
        </ul>
        <div class="hidden md:flex items-center gap-4">
          <ThemeToggle />
          <AppButton to="#contact" size="sm">Contact Me</AppButton>
        </div>
        <div class="md:hidden flex items-center gap-2">
          <ThemeToggle />
          <button
            id="mobile-menu-toggle"
            class="p-2 rounded-full hover:bg-black/5 dark:hover:bg-white/8 transition-colors"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-text-secondary dark:text-[#8E8E93]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </nav>
      <!-- Mobile menu -->
      <div v-if="mobileMenuOpen" class="md:hidden bg-surface dark:bg-[#1C1C1E] border-t border-border/60 dark:border-white/8 px-6 py-4">
        <ul class="flex flex-col gap-4 text-sm font-medium text-text-secondary dark:text-[#8E8E93]">
          <li><a href="#about" class="hover:text-primary transition-colors" @click="mobileMenuOpen = false">About</a></li>
          <li><a href="#projects" class="hover:text-primary transition-colors" @click="mobileMenuOpen = false">Projects</a></li>
          <li><a href="#skills" class="hover:text-primary transition-colors" @click="mobileMenuOpen = false">Skills</a></li>
          <li><a href="#contact" class="hover:text-primary transition-colors" @click="mobileMenuOpen = false">Contact</a></li>
          <li class="pt-2"><AppButton to="#contact" class="w-full justify-center" @click="mobileMenuOpen = false">Contact Me</AppButton></li>
        </ul>
      </div>
    </header>

    <main class="flex-1">
      <slot />
    </main>

    <footer class="bg-surface dark:bg-[#1C1C1E] border-t border-border/60 dark:border-white/8 py-8 transition-colors">
      <div class="max-w-6xl mx-auto px-6 text-center text-sm text-text-secondary dark:text-[#8E8E93]">
        <p>&copy; {{ new Date().getFullYear() }} {{ profile?.logo_text || 'SARAT NARAK' }}. Built with Nuxt, FastAPI &amp; Supabase.</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
const mobileMenuOpen = ref(false)
const { profile } = useProfile()

const logoText = computed(() => profile.value?.logo_text || 'SARAT NARAK')
const firstWord = computed(() => logoText.value.split(' ')[0] || 'SARAT')
const secondWord = computed(() => logoText.value.split(' ').slice(1).join(' ') || 'NARAK')

useHead(() => {
  const fontUrl = profile.value?.heading_font_url
  const fontName = profile.value?.heading_font_name
  if (!fontUrl || !fontName) return {}
  return {
    style: [
      {
        id: 'heading-custom-font',
        innerHTML: `@font-face { font-family: '${fontName}'; src: url('${fontUrl}') format('woff2'), url('${fontUrl}'); font-display: swap; }`,
      },
    ],
  }
})
</script>
