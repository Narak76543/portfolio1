<template>
  <section id="about" class="scroll-mt-20 py-16 md:py-20 relative border-b border-border/40 dark:border-white/8 transition-colors duration-300">
    <div class="max-w-6xl mx-auto px-6">
      
      <!-- Eyebrow Badge & Subheading -->
      <div class="mb-10 md:mb-12">
        <div class="inline-flex items-center gap-2 bg-primary/10 border border-primary/20 text-primary px-4 py-1.5 rounded-full text-xs md:text-sm font-bold uppercase tracking-wider mb-4">
          <span class="w-2 h-2 bg-primary rounded-full animate-pulse" />
          <span>{{ profile?.about_heading || 'ABOUT ME' }}</span>
        </div>
        
        <h2 class="text-3xl md:text-5xl font-extrabold text-text-primary dark:text-[#F2F2F7] tracking-tight uppercase leading-tight max-w-3xl">
          {{ profile?.about_subheading || 'PASSIONATE ABOUT BUILDING BACKENDS & MOBILE APPS' }}
        </h2>
        <div class="w-16 h-1 bg-primary rounded-full mt-4" />
      </div>

      <!-- Main Layout: 2 Columns -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 lg:gap-16 items-start">
        
        <!-- Left Column: Biography Paragraphs -->
        <div class="space-y-4 text-base md:text-lg leading-relaxed text-text-secondary dark:text-[#8E8E93] font-medium">
          <p
            v-for="(paragraph, index) in bioParagraphs"
            :key="index"
            class="leading-relaxed"
          >
            {{ paragraph }}
          </p>

          <div class="pt-4">
            <AppButton to="#contact" variant="secondary" size="md">
              Let's Connect
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </AppButton>
          </div>
        </div>

        <!-- Right Column: 2x2 Dynamic Stats Grid -->
        <div class="grid grid-cols-2 gap-4 md:gap-5">
          <div
            v-for="stat in displayStats"
            :key="stat.id"
            class="bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/8 p-5 md:p-6 rounded-card shadow-sm dark:shadow-none hover:border-primary/40 dark:hover:border-primary/30 transition-all duration-200"
          >
            <div class="w-10 h-10 rounded-full bg-primary/10 text-primary flex items-center justify-center mb-3">
              <FolderGit2 v-if="stat.icon_name === 'folder'" class="w-5 h-5" :stroke-width="1.75" />
              <Code2 v-else-if="stat.icon_name === 'code'" class="w-5 h-5" :stroke-width="1.75" />
              <Clock v-else-if="stat.icon_name === 'clock'" class="w-5 h-5" :stroke-width="1.75" />
              <GitBranch v-else class="w-5 h-5" :stroke-width="1.75" />
            </div>
            
            <h3 class="text-3xl md:text-4xl font-extrabold text-text-primary dark:text-[#F2F2F7] tracking-tight mb-1 font-mono">
              {{ stat.value }}
            </h3>
            <p class="text-xs md:text-sm font-semibold text-text-secondary dark:text-[#8E8E93]">
              {{ stat.label }}
            </p>
          </div>
        </div>

      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { FolderGit2, Code2, Clock, GitBranch } from 'lucide-vue-next'

const { profile } = useProfile()
const { stats } = useStats()

const defaultBio = `I am an Information Technology student passionate about software engineering, backend architecture, and cross-platform mobile development.\n\nCurrently focusing on building scalable REST APIs with FastAPI, modern web UIs with Nuxt 3, and mobile experiences using Flutter. I love solving real-world problems through clean code and modern developer tooling.`

const bioParagraphs = computed(() => {
  const text = profile.value?.about_bio || defaultBio
  return text.split('\n\n').filter(p => p.trim().length > 0)
})

const defaultStats = [
  { id: '1', label: 'Projects Built', value: '8+', icon_name: 'folder', display_order: 0 },
  { id: '2', label: 'Technologies Mastered', value: '5+', icon_name: 'code', display_order: 1 },
  { id: '3', label: 'Years Learning', value: '2+', icon_name: 'clock', display_order: 2 },
  { id: '4', label: 'GitHub Repos', value: '49+', icon_name: 'git', display_order: 3 },
]

const displayStats = computed(() => {
  if (stats.value && stats.value.length > 0) {
    return [...stats.value].sort((a, b) => a.display_order - b.display_order)
  }
  return defaultStats
})
</script>
