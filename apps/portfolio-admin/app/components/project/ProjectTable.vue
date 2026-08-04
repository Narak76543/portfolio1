<template>
  <div class="overflow-hidden bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/8 rounded-card shadow-sm dark:shadow-none transition-colors">
    <table class="w-full text-sm border-collapse">
      <thead>
        <tr class="border-b border-border dark:border-white/8 bg-background/60 dark:bg-white/3">
          <th class="text-left px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Project</th>
          <th class="text-left px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider hidden md:table-cell">Slug</th>
          <th class="text-left px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider hidden lg:table-cell">Tech Stack</th>
          <th class="text-center px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Status</th>
          <th class="text-center px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Order</th>
          <th class="text-right px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Actions</th>
        </tr>
      </thead>
      <tbody class="divide-y divide-border dark:divide-white/8">
        <tr
          v-for="(project, index) in projects"
          :key="project.id"
          class="hover:bg-background/60 dark:hover:bg-white/3 transition-colors"
        >
          <td class="px-5 py-4">
            <div class="flex items-center gap-3.5">
              <div class="w-11 h-11 bg-background dark:bg-black border border-border dark:border-white/10 rounded-full flex-shrink-0 overflow-hidden flex items-center justify-center">
                <img
                  v-if="project.cover_image_url"
                  :src="project.cover_image_url"
                  :alt="project.title"
                  class="w-full h-full object-cover"
                />
                <svg v-else xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-text-secondary dark:text-[#8E8E93]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
              </div>
              <div>
                <div class="font-semibold text-text-primary dark:text-[#F2F2F7] flex items-center gap-2">
                  {{ project.title }}
                </div>
                <div class="text-xs text-text-secondary dark:text-[#8E8E93] md:hidden mt-0.5 font-mono">{{ project.slug }}</div>
              </div>
            </div>
          </td>
          <td class="px-5 py-4 text-text-secondary dark:text-[#8E8E93] hidden md:table-cell">
            <code class="bg-primary/8 dark:bg-primary/10 text-primary border border-primary/20 px-2 py-1 rounded-full text-xs font-mono">
              {{ project.slug }}
            </code>
          </td>
          <td class="px-5 py-4 hidden lg:table-cell">
            <div class="flex flex-wrap gap-1.5">
              <span
                v-for="tag in project.tech_stack.slice(0, 3)"
                :key="tag"
                class="bg-primary/8 dark:bg-primary/10 text-primary border border-primary/20 text-xs px-2.5 py-0.5 rounded-full font-semibold"
              >
                {{ tag }}
              </span>
              <span v-if="project.tech_stack.length > 3" class="text-xs font-medium text-text-secondary dark:text-[#8E8E93] self-center">
                +{{ project.tech_stack.length - 3 }}
              </span>
            </div>
          </td>
          <td class="px-5 py-4 text-center">
            <span
              v-if="project.featured"
              class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-primary text-white shadow-sm"
            >
              <span class="w-1 h-1 bg-white rounded-full animate-ping" />
              Featured
            </span>
            <span
              v-else
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium text-text-secondary dark:text-[#8E8E93] bg-background dark:bg-black border border-border dark:border-white/8"
            >
              Standard
            </span>
          </td>
          <td class="px-5 py-4 text-center">
            <div class="inline-flex items-center gap-1.5">
              <button
                type="button"
                class="p-1 rounded-full text-text-secondary dark:text-[#8E8E93] hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/8 transition-colors disabled:opacity-30 cursor-pointer text-xs"
                :disabled="index === 0 || reordering"
                @click="$emit('reorder', index, 'up')"
                title="Move Up"
              >
                ▲
              </button>
              <span class="font-mono text-xs font-semibold px-2.5 py-0.5 bg-primary/10 text-primary rounded-full">
                {{ project.display_order }}
              </span>
              <button
                type="button"
                class="p-1 rounded-full text-text-secondary dark:text-[#8E8E93] hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/8 transition-colors disabled:opacity-30 cursor-pointer text-xs"
                :disabled="index === projects.length - 1 || reordering"
                @click="$emit('reorder', index, 'down')"
                title="Move Down"
              >
                ▼
              </button>
            </div>
          </td>
          <td class="px-5 py-4">
            <div class="flex items-center justify-end gap-2">
              <AppButton variant="ghost" size="sm" :to="`/admin/projects/${project.id}/edit`">
                Edit
              </AppButton>
              <AppButton
                variant="danger"
                size="sm"
                :loading="deletingId === project.id"
                @click="$emit('delete', project.id)"
              >
                Delete
              </AppButton>
            </div>
          </td>
        </tr>
      </tbody>
    </table>

    <div v-if="!projects.length" class="text-center py-16 text-text-secondary dark:text-[#8E8E93] text-sm">
      <div class="w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-3 text-primary">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
      </div>
      <p class="font-semibold text-text-primary dark:text-[#F2F2F7]">No projects found</p>
      <p class="text-xs text-text-secondary dark:text-[#8E8E93] mt-1">Get started by adding your first portfolio project.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Project } from '~/types/project'

interface Props {
  projects: Project[]
  deletingId?: string | null
  reordering?: boolean
}

withDefaults(defineProps<Props>(), {
  deletingId: null,
  reordering: false,
})

defineEmits<{
  delete: [id: string]
  reorder: [index: number, direction: 'up' | 'down']
}>()
</script>
