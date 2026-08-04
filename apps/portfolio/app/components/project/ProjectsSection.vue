<template>
  <section id="projects" class="scroll-mt-20 py-16 md:py-20 border-b border-border/40 dark:border-white/8 transition-colors duration-300">
    <div class="max-w-6xl mx-auto px-6">
      <SectionHeading tag="02. Portfolio Showcase" subtitle="Full-stack web applications, mobile apps, and developer toolkits.">
        Featured Projects
      </SectionHeading>

      <!-- Loading skeleton -->
      <div v-if="status === 'pending'" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
        <div v-for="i in 3" :key="i" class="bg-surface dark:bg-[#1C1C1E] rounded-card border border-border dark:border-white/8 overflow-hidden animate-pulse">
          <div class="h-52 bg-border dark:bg-white/8" />
          <div class="p-6 space-y-3">
            <div class="h-5 bg-border dark:bg-white/8 rounded-full w-3/4" />
            <div class="h-4 bg-border dark:bg-white/8 rounded-full w-full" />
            <div class="flex gap-2">
              <div class="h-6 bg-border dark:bg-white/8 rounded-full w-16" />
              <div class="h-6 bg-border dark:bg-white/8 rounded-full w-16" />
            </div>
          </div>
        </div>
      </div>

      <!-- Error state -->
      <AppCard v-else-if="status === 'error'" class="text-center py-16 max-w-xl mx-auto" interactive>
        <div class="w-12 h-12 bg-red-500/10 text-red-500 rounded-full flex items-center justify-center text-xl mx-auto mb-4">
          ⚠️
        </div>
        <h3 class="text-lg font-bold text-text-primary dark:text-[#F2F2F7] mb-2">Failed to load projects</h3>
        <p class="text-sm text-text-secondary dark:text-[#8E8E93] mb-6">Unable to connect to the backend server. Please try again.</p>
        <AppButton variant="secondary" @click="refresh()">
          Retry Connection
        </AppButton>
      </AppCard>

      <!-- Single Project Hero Centered Layout -->
      <div v-else-if="projects && projects.length === 1" class="max-w-3xl mx-auto mt-12">
        <ProjectCard :project="projects[0]" :index="1" />
      </div>

      <!-- Multi Project Grid -->
      <div v-else-if="projects && projects.length > 1" class="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mt-12">
        <ProjectCard
          v-for="(project, index) in projects"
          :key="project.id"
          :project="project"
          :index="index + 1"
        />
      </div>

      <!-- Empty state -->
      <AppCard v-else class="text-center py-16 max-w-xl mx-auto">
        <div class="w-12 h-12 bg-primary/10 text-primary rounded-full flex items-center justify-center text-xl mx-auto mb-4">
          📁
        </div>
        <h3 class="text-lg font-bold text-text-primary dark:text-[#F2F2F7] mb-2">No projects found</h3>
        <p class="text-sm text-text-secondary dark:text-[#8E8E93]">Projects added via the admin CMS will appear here automatically.</p>
      </AppCard>
    </div>
  </section>
</template>

<script setup lang="ts">
const { projects, status, refresh } = useProjects()
</script>
