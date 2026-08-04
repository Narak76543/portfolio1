<template>
  <div class="min-h-screen bg-background dark:bg-black font-sans flex transition-colors duration-300">
    <!-- Desktop Sidebar -->
    <aside class="hidden md:flex flex-col w-64 bg-surface dark:bg-[#1C1C1E] border-r border-border dark:border-white/8 p-6 transition-colors flex-shrink-0">
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
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="group relative flex items-center justify-between w-full px-3.5 py-3 rounded-full text-sm transition-all duration-200 cursor-pointer select-none"
          active-class="bg-primary/10 dark:bg-primary/12 text-primary font-bold"
          inactive-class="text-text-secondary dark:text-[#8E8E93] hover:bg-black/5 dark:hover:bg-white/5 hover:text-text-primary dark:hover:text-[#F2F2F7] font-medium"
        >
          <div class="flex items-center gap-3">
            <component :is="item.icon" class="h-4 w-4 transition-colors group-[.router-link-active]:text-primary text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
            <span>{{ item.label }}</span>
          </div>
          <span class="w-1.5 h-1.5 rounded-full bg-primary opacity-0 group-[.router-link-active]:opacity-100 transition-opacity duration-200" />
        </NuxtLink>
      </nav>

      <!-- Sidebar Footer (Theme & Logout) -->
      <div class="pt-4 mt-auto border-t border-border dark:border-white/8">
        <div class="p-3 bg-background dark:bg-black border border-border dark:border-white/8 rounded-card space-y-2.5">
          <div class="flex items-center justify-between px-1">
            <div class="flex items-center gap-2.5">
              <SunMoon class="h-4 w-4 text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
              <span class="text-xs font-semibold text-text-primary dark:text-[#F2F2F7]">Theme</span>
            </div>
            <ThemeToggle />
          </div>

          <div class="h-px bg-border dark:bg-white/8" />

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

    <!-- Mobile Header -->
    <header class="md:hidden fixed top-0 inset-x-0 z-40 bg-surface/95 dark:bg-[#1C1C1E]/95 backdrop-blur-md border-b border-border dark:border-white/8 px-4 py-3 flex items-center justify-between transition-colors">
      <div class="flex items-center gap-3">
        <button
          class="p-2 rounded-full hover:bg-black/5 dark:hover:bg-white/8 text-text-primary dark:text-[#F2F2F7] transition-colors cursor-pointer"
          aria-label="Toggle Navigation Menu"
          @click="mobileMenuOpen = !mobileMenuOpen"
        >
          <Menu v-if="!mobileMenuOpen" class="w-5 h-5" :stroke-width="1.75" />
          <X v-else class="w-5 h-5" :stroke-width="1.75" />
        </button>
        <div>
          <h1 class="text-sm font-extrabold text-text-primary dark:text-[#F2F2F7] uppercase tracking-wider flex items-center gap-1">
            <span>SARAT</span>
            <span class="text-text-secondary dark:text-[#8E8E93]">NARAK</span>
            <span class="w-1.5 h-1.5 rounded-full bg-primary" />
          </h1>
          <p class="text-[10px] text-text-secondary dark:text-[#8E8E93] font-medium">Admin Panel</p>
        </div>
      </div>

      <div class="flex items-center gap-1.5">
        <ThemeToggle />
        <button
          class="p-2 rounded-full hover:bg-red-500/10 text-text-secondary hover:text-rose-500 dark:hover:text-rose-400 transition-colors cursor-pointer"
          title="Sign Out"
          @click="handleLogout"
        >
          <LogOut class="w-4 h-4" :stroke-width="1.75" />
        </button>
      </div>
    </header>

    <!-- Mobile Navigation Drawer Overlay & Content -->
    <Transition
      enter-active-class="transition duration-300 ease-out"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-200 ease-in"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="mobileMenuOpen"
        class="md:hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-sm"
        @click="mobileMenuOpen = false"
      />
    </Transition>

    <Transition
      enter-active-class="transition duration-300 ease-out transform"
      enter-from-class="-translate-x-full"
      enter-to-class="translate-x-0"
      leave-active-class="transition duration-200 ease-in transform"
      leave-from-class="translate-x-0"
      leave-to-class="-translate-x-full"
    >
      <aside
        v-if="mobileMenuOpen"
        class="md:hidden fixed inset-y-0 left-0 z-50 w-72 bg-surface dark:bg-[#1C1C1E] border-r border-border dark:border-white/8 p-5 flex flex-col justify-between shadow-2xl"
      >
        <div>
          <!-- Drawer Header -->
          <div class="flex items-center justify-between pb-4 mb-4 border-b border-border dark:border-white/8">
            <div>
              <h2 class="text-base font-extrabold text-text-primary dark:text-[#F2F2F7] tracking-wider uppercase inline-flex items-center gap-1">
                <span>SARAT</span>
                <span class="text-text-secondary dark:text-[#8E8E93]">NARAK</span>
                <span class="w-1.5 h-1.5 rounded-full bg-primary" />
              </h2>
              <p class="text-xs text-text-secondary dark:text-[#8E8E93]">Navigation</p>
            </div>
            <button
              class="p-2 rounded-full hover:bg-black/5 dark:hover:bg-white/8 text-text-secondary dark:text-[#8E8E93] cursor-pointer"
              @click="mobileMenuOpen = false"
            >
              <X class="w-5 h-5" :stroke-width="1.75" />
            </button>
          </div>

          <!-- Drawer Links -->
          <nav class="space-y-1.5">
            <NuxtLink
              v-for="item in navItems"
              :key="item.to"
              :to="item.to"
              class="group relative flex items-center justify-between w-full px-4 py-3 rounded-full text-sm font-semibold transition-all duration-200 cursor-pointer select-none"
              active-class="bg-primary/10 dark:bg-primary/15 text-primary font-bold"
              inactive-class="text-text-secondary dark:text-[#8E8E93] hover:bg-black/5 dark:hover:bg-white/5 hover:text-text-primary dark:hover:text-[#F2F2F7]"
              @click="mobileMenuOpen = false"
            >
              <div class="flex items-center gap-3.5">
                <component :is="item.icon" class="h-4 w-4 transition-colors group-[.router-link-active]:text-primary text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
                <span>{{ item.label }}</span>
              </div>
              <span class="w-2 h-2 rounded-full bg-primary opacity-0 group-[.router-link-active]:opacity-100 transition-opacity" />
            </NuxtLink>
          </nav>
        </div>

        <!-- Drawer Footer -->
        <div class="pt-4 border-t border-border dark:border-white/8 space-y-3">
          <div class="flex items-center justify-between px-3 py-2 bg-background dark:bg-black rounded-card border border-border dark:border-white/8">
            <div class="flex items-center gap-2 text-xs font-semibold text-text-primary dark:text-[#F2F2F7]">
              <SunMoon class="w-4 h-4 text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
              <span>Appearance</span>
            </div>
            <ThemeToggle />
          </div>

          <button
            class="flex items-center justify-center gap-2 w-full py-2.5 rounded-full bg-rose-500/10 hover:bg-rose-500/20 text-rose-500 text-xs font-bold transition-all cursor-pointer"
            @click="handleLogout"
          >
            <LogOut class="w-4 h-4" :stroke-width="1.75" />
            <span>Sign Out</span>
          </button>
        </div>
      </aside>
    </Transition>

    <!-- Main Content Body -->
    <main class="flex-1 w-full md:p-8 p-4 pt-20 pb-24 md:pb-8 text-text-primary dark:text-[#F2F2F7] transition-colors max-w-7xl mx-auto">
      <slot />
    </main>

    <!-- Mobile Floating One UI Quick Bottom Navigation Pill -->
    <nav class="md:hidden fixed bottom-4 inset-x-4 z-30 bg-surface/90 dark:bg-[#1C1C1E]/90 backdrop-blur-lg border border-border dark:border-white/10 rounded-full p-1.5 shadow-2xl flex items-center justify-around">
      <NuxtLink
        v-for="item in quickNavItems"
        :key="item.to"
        :to="item.to"
        class="flex flex-col items-center justify-center py-1.5 px-3 rounded-full text-[10px] font-medium transition-all"
        active-class="bg-primary text-white font-bold shadow-md"
        inactive-class="text-text-secondary dark:text-[#8E8E93] hover:text-text-primary"
      >
        <component :is="item.icon" class="w-4 h-4 mb-0.5" :stroke-width="1.75" />
        <span>{{ item.shortLabel }}</span>
      </NuxtLink>

      <button
        class="flex flex-col items-center justify-center py-1.5 px-3 rounded-full text-[10px] font-medium text-text-secondary dark:text-[#8E8E93] hover:text-text-primary cursor-pointer"
        @click="mobileMenuOpen = true"
      >
        <Menu class="w-4 h-4 mb-0.5" :stroke-width="1.75" />
        <span>More</span>
      </button>
    </nav>
  </div>
</template>

<script setup lang="ts">
import {
  FolderGit2,
  Cpu,
  Layers,
  BarChart3,
  Share2,
  Smartphone,
  User,
  LogOut,
  SunMoon,
  Menu,
  X,
} from 'lucide-vue-next'

const mobileMenuOpen = ref(false)
const { logout } = useAuth()

const navItems = [
  { to: '/admin/projects', label: 'Projects', icon: FolderGit2 },
  { to: '/admin/tech-stack', label: 'Tech Stack', icon: Cpu },
  { to: '/admin/skills', label: 'Skills', icon: Layers },
  { to: '/admin/stats', label: 'Stats', icon: BarChart3 },
  { to: '/admin/social-media', label: 'Social Media', icon: Share2 },
  { to: '/admin/devices', label: 'Devices', icon: Smartphone },
  { to: '/admin/profile', label: 'Profile', icon: User },
]

const quickNavItems = [
  { to: '/admin/projects', shortLabel: 'Projects', icon: FolderGit2 },
  { to: '/admin/skills', shortLabel: 'Skills', icon: Layers },
  { to: '/admin/devices', shortLabel: 'Devices', icon: Smartphone },
  { to: '/admin/profile', shortLabel: 'Profile', icon: User },
]

async function handleLogout() {
  await logout()
  navigateTo('/login')
}
</script>
