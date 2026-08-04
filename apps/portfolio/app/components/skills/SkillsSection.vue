<template>
  <section id="skills" class="scroll-mt-20 py-16 md:py-20 border-b border-border/40 dark:border-white/8 transition-colors duration-300">
    <div class="max-w-6xl mx-auto px-6">
      <SectionHeading tag="03. Technical Toolkit">
        Skills &amp; Expertise
      </SectionHeading>

      <!-- Skeleton loading -->
      <div v-if="status === 'pending'" class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 md:gap-8 mt-12">
        <div v-for="i in 4" :key="i" class="bg-surface dark:bg-[#1C1C1E] rounded-card border border-border dark:border-white/8 p-6 space-y-4 animate-pulse">
          <div class="flex items-center gap-3">
            <div class="w-11 h-11 bg-border dark:bg-white/8 rounded-full" />
            <div class="h-5 bg-border dark:bg-white/8 rounded-full w-24" />
          </div>
          <div class="space-y-2 pt-2">
            <div class="h-4 bg-border dark:bg-white/8 rounded-full w-3/4" />
            <div class="h-4 bg-border dark:bg-white/8 rounded-full w-2/3" />
            <div class="h-4 bg-border dark:bg-white/8 rounded-full w-1/2" />
          </div>
        </div>
      </div>

      <div v-else class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6 md:gap-8 mt-12">
        <AppCard
          v-for="category in categories"
          :key="category.id"
          interactive
          class="flex flex-col justify-between"
        >
          <div>
            <div class="flex items-center gap-3.5 mb-6">
              <div class="w-11 h-11 bg-primary/10 rounded-full flex items-center justify-center text-primary shadow-sm">
                <component :is="resolveIcon(category.icon_name)" class="w-5 h-5" :stroke-width="1.75" />
              </div>
              <h3 class="text-base font-bold text-text-primary dark:text-[#F2F2F7]">{{ category.name }}</h3>
            </div>
            <ul class="space-y-3">
              <li
                v-for="item in category.items"
                :key="item"
                class="flex items-center gap-2.5 text-sm font-semibold text-text-secondary dark:text-[#8E8E93]"
              >
                <span class="w-1.5 h-1.5 bg-primary rounded-full flex-shrink-0" />
                {{ item }}
              </li>
            </ul>
          </div>
        </AppCard>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import * as LucideIcons from 'lucide-vue-next'

const { categories, status } = useSkillCategories()

function resolveIcon(name: string) {
  const icon = (LucideIcons as Record<string, any>)[name]
  if (icon) return icon
  if (name === 'LayoutGrid') return LucideIcons.LayoutGrid || LucideIcons.LayoutDashboard
  return LucideIcons.Folder
}
</script>
