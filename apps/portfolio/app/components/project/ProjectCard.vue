<template>
  <NuxtLink
    :to="`/projects/${project.slug}`"
    :class="[
      'group flex flex-col bg-surface dark:bg-[#1C1C1E] rounded-card border border-border dark:border-white/8 shadow-sm dark:shadow-none hover:shadow-xl hover:-translate-y-1.5 transition-all duration-300 overflow-hidden relative',
      project.featured ? 'ring-2 ring-primary/40 dark:ring-primary/30' : '',
    ]"
  >
    <!-- Top accent indicator -->
    <div
      :class="[
        'h-1.5 w-full',
        project.featured ? 'bg-primary' : 'bg-border dark:bg-white/8 group-hover:bg-primary/40 transition-colors',
      ]"
    />

    <!-- Cover banner header -->
    <div class="relative h-52 bg-[#101010] dark:bg-[#0a0a0a] overflow-hidden flex items-center justify-center p-6 text-white border-b border-white/8">
      <!-- Background subtle pattern -->
      <div class="absolute inset-0 bg-[radial-gradient(#1a1a1a_1px,transparent_1px)] [background-size:20px_20px] opacity-60" />
      
      <!-- Numbered Badge -->
      <div v-if="index" class="absolute top-4 left-4 z-20 text-3xl font-extrabold text-white/20 group-hover:text-white/50 transition-colors pointer-events-none select-none font-mono">
        {{ String(index).padStart(2, '0') }}
      </div>
      
      <img
        v-if="project.cover_image_url"
        :src="project.cover_image_url"
        :alt="project.title"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
      />
      
      <!-- Fallback icon banner -->
      <div v-else class="relative z-10 text-center flex flex-col items-center">
        <div class="w-14 h-14 bg-white/10 border border-white/20 rounded-full flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform duration-300">
          <component :is="fallbackInfo.iconComponent" class="w-7 h-7" :stroke-width="1.75" />
        </div>
        <div class="text-xs font-bold text-white/50 uppercase tracking-widest mt-3">
          {{ fallbackInfo.label }}
        </div>
      </div>

      <!-- Featured badge -->
      <div
        v-if="project.featured"
        class="absolute top-3.5 right-3.5 bg-primary text-white text-xs font-bold px-3.5 py-1.5 rounded-full shadow-md flex items-center gap-1.5"
      >
        <span class="w-1.5 h-1.5 bg-white rounded-full animate-ping" />
        Featured
      </div>
    </div>

    <!-- Content -->
    <div class="p-6 flex-1 flex flex-col justify-between space-y-4">
      <div>
        <h3 class="text-xl font-bold text-text-primary dark:text-[#F2F2F7] group-hover:text-primary transition-colors line-clamp-1 mb-2">
          {{ project.title }}
        </h3>
        <p v-if="project.short_description" class="text-sm text-text-secondary dark:text-[#8E8E93] leading-relaxed line-clamp-2">
          {{ project.short_description }}
        </p>
      </div>

      <!-- Tech stack tags -->
      <div v-if="project.tech_stack.length" class="flex flex-wrap gap-1.5 pt-2">
        <span
          v-for="tag in project.tech_stack.slice(0, 4)"
          :key="tag"
          class="bg-primary/8 dark:bg-primary/10 text-primary text-xs font-semibold px-3 py-1 rounded-full transition-colors border border-primary/20"
        >
          {{ tag }}
        </span>
        <span
          v-if="project.tech_stack.length > 4"
          class="text-xs text-text-secondary dark:text-[#8E8E93] font-semibold px-2 py-1"
        >
          +{{ project.tech_stack.length - 4 }}
        </span>
      </div>
    </div>
  </NuxtLink>
</template>

<script setup lang="ts">
import { LayoutDashboard, Server, Smartphone, Code2 } from 'lucide-vue-next'
import type { Project } from '~/types/project'

interface Props {
  project: Project
  index?: number
}

const props = defineProps<Props>()

const fallbackInfo = computed(() => {
  const stack = props.project.tech_stack.map((t) => t.toLowerCase())
  const title = props.project.title.toLowerCase()

  if (stack.some((t) => t.includes('nuxt') || t.includes('vue')) || title.includes('portfolio') || title.includes('sarat')) {
    return {
      iconComponent: LayoutDashboard,
      label: 'Nuxt 3 & Web Application',
    }
  }
  if (stack.some((t) => t.includes('fastapi') || t.includes('python'))) {
    return {
      iconComponent: Server,
      label: 'FastAPI Backend Architecture',
    }
  }
  if (stack.some((t) => t.includes('flutter') || t.includes('dart') || t.includes('sqlite')) || title.includes('driving') || title.includes('app')) {
    return {
      iconComponent: Smartphone,
      label: 'Flutter Mobile Experience',
    }
  }
  return {
    iconComponent: Code2,
    label: props.project.role || 'Full-Stack Software',
  }
})
</script>
