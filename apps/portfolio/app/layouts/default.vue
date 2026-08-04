<template>
  <div class="min-h-screen flex flex-col font-sans bg-background dark:bg-black text-text-primary dark:text-[#F2F2F7] transition-colors duration-300">
    <!-- Desktop & Mobile Header -->
    <header class="sticky top-0 z-40 bg-surface/90 dark:bg-[#1C1C1E]/90 backdrop-blur-md border-b border-border/60 dark:border-white/8 transition-colors">
      <nav class="max-w-6xl mx-auto px-4 sm:px-6 py-3.5 flex items-center justify-between">
        <NuxtLink to="/" class="flex items-center gap-2">
          <img
            v-if="profile?.logo_type === 'image' && profile?.logo_image_url"
            :src="profile.logo_image_url"
            :alt="profile?.logo_text || 'SARAT NARAK'"
            class="h-8 md:h-9 w-auto object-contain"
          />
          <span
            v-else
            class="text-lg md:text-xl font-extrabold text-text-primary dark:text-[#F2F2F7] tracking-wider uppercase inline-flex items-center"
            :style="profile?.heading_font_name ? { fontFamily: `'${profile.heading_font_name}', 'Onest', sans-serif` } : {}"
          >
            <span>{{ firstWord }}</span>
            <span class="text-text-secondary dark:text-[#8E8E93] font-bold ml-1.5">{{ secondWord }}</span>
            <span class="w-1.5 h-1.5 rounded-full bg-primary ml-1" />
          </span>
        </NuxtLink>

        <!-- Desktop Nav Links -->
        <ul class="hidden md:flex items-center gap-1 text-sm font-medium text-text-secondary dark:text-[#8E8E93]">
          <li><a href="#about" class="px-3.5 py-1.5 rounded-full hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/8 transition-colors">About</a></li>
          <li><a href="#projects" class="px-3.5 py-1.5 rounded-full hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/8 transition-colors">Projects</a></li>
          <li><a href="#skills" class="px-3.5 py-1.5 rounded-full hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/8 transition-colors">Skills</a></li>
          <li><a href="#contact" class="px-3.5 py-1.5 rounded-full hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/8 transition-colors">Contact</a></li>
        </ul>

        <!-- Desktop Action Controls -->
        <div class="hidden md:flex items-center gap-3">
          <ThemeToggle />
          <AppButton to="#contact" size="sm">Contact Me</AppButton>
        </div>

        <!-- Mobile Controls -->
        <div class="md:hidden flex items-center gap-2">
          <ThemeToggle />
          <button
            class="p-2 rounded-full hover:bg-black/5 dark:hover:bg-white/8 text-text-secondary dark:text-[#8E8E93] transition-colors cursor-pointer"
            aria-label="Open Navigation Menu"
            @click="mobileMenuOpen = !mobileMenuOpen"
          >
            <Menu v-if="!mobileMenuOpen" class="w-5 h-5" :stroke-width="1.75" />
            <X v-else class="w-5 h-5" :stroke-width="1.75" />
          </button>
        </div>
      </nav>

      <!-- Mobile Dropdown Drawer -->
      <Transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="opacity-0 -translate-y-2"
        enter-to-class="opacity-100 translate-y-0"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="opacity-100 translate-y-0"
        leave-to-class="opacity-0 -translate-y-2"
      >
        <div v-if="mobileMenuOpen" class="md:hidden bg-surface dark:bg-[#1C1C1E] border-t border-border/60 dark:border-white/8 px-6 py-4 shadow-xl">
          <ul class="flex flex-col gap-3.5 text-sm font-semibold text-text-secondary dark:text-[#8E8E93]">
            <li><a href="#about" class="block py-1 hover:text-primary transition-colors" @click="mobileMenuOpen = false">About</a></li>
            <li><a href="#projects" class="block py-1 hover:text-primary transition-colors" @click="mobileMenuOpen = false">Projects</a></li>
            <li><a href="#skills" class="block py-1 hover:text-primary transition-colors" @click="mobileMenuOpen = false">Skills</a></li>
            <li><a href="#contact" class="block py-1 hover:text-primary transition-colors" @click="mobileMenuOpen = false">Contact</a></li>
            <li class="pt-2"><AppButton to="#contact" class="w-full justify-center" @click="mobileMenuOpen = false">Contact Me</AppButton></li>
          </ul>
        </div>
      </Transition>
    </header>

    <!-- Main Content -->
    <main class="flex-1 pb-24 md:pb-0">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-surface dark:bg-[#1C1C1E] border-t border-border/60 dark:border-white/8 py-8 mb-16 md:mb-0 transition-colors">
      <div class="max-w-6xl mx-auto px-6 text-center text-xs md:text-sm text-text-secondary dark:text-[#8E8E93]">
        <p>&copy; {{ new Date().getFullYear() }} {{ profile?.logo_text || 'SARAT NARAK' }}. Built with Nuxt, FastAPI &amp; Supabase.</p>
      </div>
    </footer>

    <!-- Mobile Floating One UI Quick Bottom Navigation Pill -->
    <nav class="md:hidden fixed bottom-4 inset-x-4 z-30 bg-surface/90 dark:bg-[#1C1C1E]/90 backdrop-blur-lg border border-border dark:border-white/10 rounded-full p-1.5 shadow-2xl flex items-center justify-around">
      <a
        href="#hero"
        class="flex flex-col items-center justify-center py-1.5 px-3 rounded-full text-[10px] font-medium text-text-secondary dark:text-[#8E8E93] hover:text-primary transition-colors"
      >
        <Home class="w-4 h-4 mb-0.5" :stroke-width="1.75" />
        <span>Home</span>
      </a>

      <a
        href="#about"
        class="flex flex-col items-center justify-center py-1.5 px-3 rounded-full text-[10px] font-medium text-text-secondary dark:text-[#8E8E93] hover:text-primary transition-colors"
      >
        <User class="w-4 h-4 mb-0.5" :stroke-width="1.75" />
        <span>About</span>
      </a>

      <a
        href="#projects"
        class="flex flex-col items-center justify-center py-1.5 px-3 rounded-full text-[10px] font-medium text-text-secondary dark:text-[#8E8E93] hover:text-primary transition-colors"
      >
        <FolderGit2 class="w-4 h-4 mb-0.5" :stroke-width="1.75" />
        <span>Projects</span>
      </a>

      <a
        href="#skills"
        class="flex flex-col items-center justify-center py-1.5 px-3 rounded-full text-[10px] font-medium text-text-secondary dark:text-[#8E8E93] hover:text-primary transition-colors"
      >
        <Layers class="w-4 h-4 mb-0.5" :stroke-width="1.75" />
        <span>Skills</span>
      </a>

      <a
        href="#contact"
        class="flex flex-col items-center justify-center py-1.5 px-3 rounded-full text-[10px] font-medium text-text-secondary dark:text-[#8E8E93] hover:text-primary transition-colors"
      >
        <Mail class="w-4 h-4 mb-0.5" :stroke-width="1.75" />
        <span>Contact</span>
      </a>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { Home, User, FolderGit2, Layers, Mail, Menu, X } from 'lucide-vue-next'

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
