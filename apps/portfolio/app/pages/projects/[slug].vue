<template>
  <div class="py-12 md:py-20 bg-background dark:bg-black min-h-screen text-text-primary dark:text-[#F2F2F7] transition-colors">
    <div class="max-w-4xl mx-auto px-6">
      <!-- Back link -->
      <NuxtLink to="/#projects" class="inline-flex items-center gap-2 text-sm text-text-secondary dark:text-[#8E8E93] hover:text-primary transition-colors mb-8 group font-semibold">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 group-hover:-translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Back to Projects
      </NuxtLink>

      <!-- Loading state -->
      <div v-if="status === 'pending'" class="space-y-6 animate-pulse">
        <div class="h-8 bg-border dark:bg-white/8 rounded-full w-1/2" />
        <div class="h-64 bg-border dark:bg-white/8 rounded-card" />
        <div class="space-y-3">
          <div class="h-4 bg-border dark:bg-white/8 rounded-full w-full" />
          <div class="h-4 bg-border dark:bg-white/8 rounded-full w-3/4" />
        </div>
      </div>

      <!-- Error state -->
      <AppCard v-else-if="status === 'error'" class="text-center py-12">
        <p class="text-text-secondary dark:text-[#8E8E93] mb-4">Project not found or failed to load.</p>
        <AppButton variant="secondary" to="/#projects">Back to Projects</AppButton>
      </AppCard>

      <!-- Project detail -->
      <article v-else-if="project">
        <!-- Header -->
        <div class="mb-8">
          <div class="flex items-center gap-3 mb-4">
            <span
              v-if="project.featured"
              class="bg-primary text-white text-xs font-bold px-3.5 py-1.5 rounded-full shadow-sm inline-flex items-center gap-1.5"
            >
              <Star class="w-3.5 h-3.5 fill-white" />
              Featured Project
            </span>
          </div>
          <h1 class="text-3xl md:text-5xl font-extrabold text-text-primary dark:text-[#F2F2F7] mb-3 tracking-tight">
            {{ project.title }}
          </h1>
          <p v-if="project.short_description" class="text-lg text-text-secondary dark:text-[#8E8E93] font-medium">
            {{ project.short_description }}
          </p>
        </div>

        <!-- Cover image -->
        <div v-if="project.cover_image_url" class="mb-8 rounded-card overflow-hidden border border-border dark:border-white/10 shadow-md">
          <img
            :src="project.cover_image_url"
            :alt="project.title"
            class="w-full h-auto object-cover"
          />
        </div>

        <!-- Meta info -->
        <div class="grid sm:grid-cols-2 gap-4 mb-8">
          <AppCard v-if="project.role">
            <div class="text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wide mb-1">My Role</div>
            <div class="text-sm font-bold text-text-primary dark:text-[#F2F2F7]">{{ project.role }}</div>
          </AppCard>
          <AppCard v-if="project.tech_stack.length">
            <div class="text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wide mb-2">Tech Stack</div>
            <div class="flex flex-wrap gap-1.5">
              <span
                v-for="tag in project.tech_stack"
                :key="tag"
                class="bg-primary/8 dark:bg-primary/10 text-primary border border-primary/20 text-xs font-semibold px-3 py-1 rounded-full"
              >
                {{ tag }}
              </span>
            </div>
          </AppCard>
        </div>

        <!-- Links -->
        <div v-if="project.github_url || project.live_url" class="flex flex-wrap gap-3 mb-10">
          <AppButton v-if="project.github_url" variant="secondary" :to="project.github_url">
            <Github class="w-4 h-4 mr-2" :stroke-width="1.75" />
            GitHub
          </AppButton>
          <AppButton v-if="project.live_url" :to="project.live_url">
            <Globe class="w-4 h-4 mr-2" :stroke-width="1.75" />
            Live Demo
          </AppButton>
        </div>

        <!-- Full description -->
        <div v-if="project.full_description" class="prose dark:prose-invert max-w-none">
          <div class="text-text-primary dark:text-[#F2F2F7] leading-relaxed whitespace-pre-line text-base font-medium">
            {{ project.full_description }}
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Github, Globe, Star } from 'lucide-vue-next'

const route = useRoute()
const slug = computed(() => route.params.slug as string)

const { project, status } = useProject(slug)

useHead({
  title: computed(() =>
    project.value
      ? `${project.value.title} — SARAT NARAK`
      : 'Project — SARAT NARAK'
  ),
})
</script>
