<template>
  <div class="min-h-screen bg-background dark:bg-black font-sans flex transition-colors duration-300">
    <!-- Sidebar -->
    <aside class="hidden md:flex flex-col w-64 bg-surface dark:bg-[#1C1C1E] border-r border-border dark:border-white/8 p-6 transition-colors">
      <div class="mb-8">
        <h1 class="text-lg font-extrabold text-text-primary dark:text-[#F2F2F7] tracking-wider uppercase inline-flex items-center">
          <span>SARAT</span>
          <span class="text-text-secondary dark:text-[#8E8E93] font-bold ml-1">NARAK</span>
          <span class="w-1.5 h-1.5 rounded-full bg-primary ml-1" />
        </h1>
        <p class="text-xs text-text-secondary dark:text-[#8E8E93] font-medium mt-0.5">Admin Management Panel</p>
      </div>

      <nav class="flex-1 space-y-1">
        <NuxtLink
          to="/admin/projects"
          class="group relative flex items-center justify-between w-full px-3.5 py-3 rounded-full text-sm transition-all duration-200 cursor-pointer select-none"
          active-class="bg-primary/10 dark:bg-primary/12 text-primary font-bold"
          inactive-class="text-text-secondary dark:text-[#8E8E93] hover:bg-black/5 dark:hover:bg-white/5 hover:text-text-primary dark:hover:text-[#F2F2F7] font-medium"
        >
          <div class="flex items-center gap-3">
            <FolderGit2 class="h-4 w-4 transition-colors group-[.router-link-active]:text-primary text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
            <span>Projects</span>
          </div>
          <span class="w-1.5 h-1.5 rounded-full bg-primary opacity-0 group-[.router-link-active]:opacity-100 transition-opacity duration-200" />
        </NuxtLink>

        <NuxtLink
          to="/admin/tech-stack"
          class="group relative flex items-center justify-between w-full px-3.5 py-3 rounded-full text-sm transition-all duration-200 cursor-pointer select-none"
          active-class="bg-primary/10 dark:bg-primary/12 text-primary font-bold"
          inactive-class="text-text-secondary dark:text-[#8E8E93] hover:bg-black/5 dark:hover:bg-white/5 hover:text-text-primary dark:hover:text-[#F2F2F7] font-medium"
        >
          <div class="flex items-center gap-3">
            <Cpu class="h-4 w-4 transition-colors group-[.router-link-active]:text-primary text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
            <span>Tech Stack</span>
          </div>
          <span class="w-1.5 h-1.5 rounded-full bg-primary opacity-0 group-[.router-link-active]:opacity-100 transition-opacity duration-200" />
        </NuxtLink>

        <NuxtLink
          to="/admin/skills"
          class="group relative flex items-center justify-between w-full px-3.5 py-3 rounded-full text-sm transition-all duration-200 cursor-pointer select-none"
          active-class="bg-primary/10 dark:bg-primary/12 text-primary font-bold"
          inactive-class="text-text-secondary dark:text-[#8E8E93] hover:bg-black/5 dark:hover:bg-white/5 hover:text-text-primary dark:hover:text-[#F2F2F7] font-medium"
        >
          <div class="flex items-center gap-3">
            <Layers class="h-4 w-4 transition-colors group-[.router-link-active]:text-primary text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
            <span>Skills</span>
          </div>
          <span class="w-1.5 h-1.5 rounded-full bg-primary opacity-0 group-[.router-link-active]:opacity-100 transition-opacity duration-200" />
        </NuxtLink>

        <NuxtLink
          to="/admin/stats"
          class="group relative flex items-center justify-between w-full px-3.5 py-3 rounded-full text-sm transition-all duration-200 cursor-pointer select-none"
          active-class="bg-primary/10 dark:bg-primary/12 text-primary font-bold"
          inactive-class="text-text-secondary dark:text-[#8E8E93] hover:bg-black/5 dark:hover:bg-white/5 hover:text-text-primary dark:hover:text-[#F2F2F7] font-medium"
        >
          <div class="flex items-center gap-3">
            <BarChart3 class="h-4 w-4 transition-colors group-[.router-link-active]:text-primary text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
            <span>Stats</span>
          </div>
          <span class="w-1.5 h-1.5 rounded-full bg-primary opacity-0 group-[.router-link-active]:opacity-100 transition-opacity duration-200" />
        </NuxtLink>

        <NuxtLink
          to="/admin/social-media"
          class="group relative flex items-center justify-between w-full px-3.5 py-3 rounded-full text-sm transition-all duration-200 cursor-pointer select-none"
          active-class="bg-primary/10 dark:bg-primary/12 text-primary font-bold"
          inactive-class="text-text-secondary dark:text-[#8E8E93] hover:bg-black/5 dark:hover:bg-white/5 hover:text-text-primary dark:hover:text-[#F2F2F7] font-medium"
        >
          <div class="flex items-center gap-3">
            <Share2 class="h-4 w-4 transition-colors group-[.router-link-active]:text-primary text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
            <span>Social Media</span>
          </div>
          <span class="w-1.5 h-1.5 rounded-full bg-primary opacity-0 group-[.router-link-active]:opacity-100 transition-opacity duration-200" />
        </NuxtLink>

        <NuxtLink
          to="/admin/devices"
          class="group relative flex items-center justify-between w-full px-3.5 py-3 rounded-full text-sm transition-all duration-200 cursor-pointer select-none"
          active-class="bg-primary/10 dark:bg-primary/12 text-primary font-bold"
          inactive-class="text-text-secondary dark:text-[#8E8E93] hover:bg-black/5 dark:hover:bg-white/5 hover:text-text-primary dark:hover:text-[#F2F2F7] font-medium"
        >
          <div class="flex items-center gap-3">
            <Smartphone class="h-4 w-4 transition-colors group-[.router-link-active]:text-primary text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
            <span>Devices</span>
          </div>
          <span class="w-1.5 h-1.5 rounded-full bg-primary opacity-0 group-[.router-link-active]:opacity-100 transition-opacity duration-200" />
        </NuxtLink>

        <NuxtLink
          to="/admin/profile"
          class="group relative flex items-center justify-between w-full px-3.5 py-3 rounded-full text-sm transition-all duration-200 cursor-pointer select-none"
          active-class="bg-primary/10 dark:bg-primary/12 text-primary font-bold"
          inactive-class="text-text-secondary dark:text-[#8E8E93] hover:bg-black/5 dark:hover:bg-white/5 hover:text-text-primary dark:hover:text-[#F2F2F7] font-medium"
        >
          <div class="flex items-center gap-3">
            <User class="h-4 w-4 transition-colors group-[.router-link-active]:text-primary text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
            <span>Profile</span>
          </div>
          <span class="w-1.5 h-1.5 rounded-full bg-primary opacity-0 group-[.router-link-active]:opacity-100 transition-opacity duration-200" />
        </NuxtLink>
      </nav>

      <!-- Sidebar Footer (Theme & Logout) -->
      <div class="pt-4 mt-auto border-t border-border dark:border-white/8">
        <div class="p-3 bg-background dark:bg-black border border-border dark:border-white/8 rounded-card space-y-2.5">
          <!-- Theme / Appearance item -->
          <div class="flex items-center justify-between px-1">
            <div class="flex items-center gap-2.5">
              <SunMoon class="h-4 w-4 text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
              <span class="text-xs font-semibold text-text-primary dark:text-[#F2F2F7]">Theme</span>
            </div>
            <ThemeToggle />
          </div>

          <div class="h-px bg-border dark:bg-white/8" />

          <!-- Logout Action button -->
          <button
            class="group flex items-center justify-between w-full px-2.5 py-2 rounded-full text-xs font-semibold text-text-secondary dark:text-[#8E8E93] hover:text-red-600 dark:hover:text-red-400 hover:bg-red-500/10 transition-all cursor-pointer select-none"
            @click="handleLogout"
          >
            <div class="flex items-center gap-2.5">
              <LogOut class="h-4 w-4 text-text-secondary dark:text-[#8E8E93] group-hover:text-red-600 dark:group-hover:text-red-400 transition-colors" :stroke-width="1.75" />
              <span>Sign Out</span>
            </div>
            <span class="text-[10px] uppercase font-bold text-text-secondary/60 dark:text-[#8E8E93]/60 group-hover:text-red-500/70 transition-colors">Exit</span>
          </button>
        </div>
      </div>
    </aside>

    <!-- Mobile header -->
    <div class="md:hidden fixed top-0 inset-x-0 z-50 bg-surface dark:bg-[#1C1C1E] border-b border-border dark:border-white/8 px-4 py-3 flex items-center justify-between transition-colors">
      <div>
        <h1 class="text-sm font-bold text-primary">{{ profile?.logo_text || 'SARAT NARAK' }}</h1>
        <p class="text-xs text-text-secondary dark:text-[#8E8E93]">Admin</p>
      </div>
      <div class="flex items-center gap-2">
        <ThemeToggle />
        <button
          class="p-2 rounded-full hover:bg-black/5 dark:hover:bg-white/8 transition-colors text-text-secondary dark:text-[#8E8E93] cursor-pointer"
          @click="handleLogout"
        >
          <LogOut class="h-4 w-4" :stroke-width="1.75" />
        </button>
      </div>
    </div>

    <!-- Main content -->
    <main class="flex-1 md:p-8 p-4 pt-16 md:pt-8 text-text-primary dark:text-[#F2F2F7] transition-colors">
      <slot />
    </main>
  </div>
</template>

<script setup lang="ts">
import { FolderGit2, Cpu, Layers, BarChart3, Share2, Smartphone, User, LogOut, SunMoon } from 'lucide-vue-next'

const { logout } = useAuth()
const { profile } = useAdminProfile()

async function handleLogout() {
  await logout()
  navigateTo('/login')
}
</script>
