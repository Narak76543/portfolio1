<template>
  <section id="hero" class="scroll-mt-20 relative overflow-hidden border-b border-border/40 dark:border-white/8 transition-colors duration-300">

    <div class="relative max-w-6xl mx-auto px-6 pt-8 md:pt-12 lg:pt-14 pb-16 md:pb-20 lg:pb-24 grid grid-cols-1 lg:grid-cols-2 gap-6 lg:gap-8 items-center">
      
      <!-- Left Column: Content -->
      <div class="flex-1 max-w-3xl text-center lg:text-left">
        <!-- Badge pill -->
        <div class="inline-flex items-center gap-2 bg-primary/10 border border-primary/20 text-primary px-4 py-1.5 rounded-full text-xs md:text-sm font-bold uppercase tracking-wider mb-4 animate-fade-in-up">
          <span class="w-2 h-2 bg-primary rounded-full animate-pulse" />
          <span>{{ profile?.tagline || 'IT Student • Full-Stack Developer' }}</span>
        </div>

        <!-- Title -->
        <h1
          class="text-4xl md:text-6xl lg:text-7xl font-extrabold text-text-primary dark:text-[#F2F2F7] tracking-tight leading-[1.08] mb-3 animate-fade-in-up delay-100 uppercase"
          :style="profile?.heading_font_name ? { fontFamily: `'${profile.heading_font_name}', 'Onest', sans-serif` } : {}"
        >
          {{ profile?.first_name || 'SARAT' }} <span class="text-primary">{{ profile?.last_name || 'NARAK' }}</span>
        </h1>

        <!-- Tagline -->
        <p class="text-base md:text-lg text-text-secondary dark:text-[#8E8E93] font-medium leading-relaxed mb-5 max-w-2xl mx-auto lg:mx-0 animate-fade-in-up delay-200">
          {{ profile?.hero_pitch || 'I build backend APIs, mobile apps, and web dashboards — and this site is one of my projects too.' }}
        </p>

        <!-- Tech Stack -->
        <div class="animate-fade-in-up delay-300 mb-6">
          <div class="flex items-center justify-center lg:justify-start gap-3 flex-wrap">
            <div
              v-for="item in techStacks"
              :key="item.id"
              class="group relative p-2.5 bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-full shadow-sm hover:border-primary/50 dark:hover:border-primary/40 hover:scale-110 hover:-translate-y-0.5 transition-all duration-200 cursor-pointer"
            >
              <img
                v-if="item.icon_url"
                :src="item.icon_url"
                :alt="item.name"
                class="w-5 h-5 object-contain"
              />
              <span v-else class="text-xs font-bold text-primary">
                {{ item.name.substring(0, 2) }}
              </span>

              <!-- Hover Tooltip -->
              <div class="absolute -top-9 left-1/2 -translate-x-1/2 px-2.5 py-1 bg-text-primary dark:bg-[#1C1C1E] text-white dark:text-[#F2F2F7] text-[11px] font-semibold rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none whitespace-nowrap shadow-md z-20 border border-white/10">
                {{ item.name }}
                <div class="absolute top-full left-1/2 -translate-x-1/2 border-4 border-transparent border-t-text-primary dark:border-t-[#1C1C1E]" />
              </div>
            </div>
          </div>
        </div>

        <!-- CTAs -->
        <div class="flex flex-wrap items-center justify-center lg:justify-start gap-3.5 animate-fade-in-up delay-400">
          <AppButton size="md" to="#projects">
            <span>View Projects</span>
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </AppButton>
          <AppButton variant="secondary" size="md" to="#contact">
            Contact Me
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
            </svg>
          </AppButton>
        </div>
      </div>

      <!-- Right Column: Image -->
      <div class="flex-1 w-full max-w-md mx-auto lg:mx-0 relative animate-fade-in-up flex justify-center lg:justify-end">
        <div class="relative w-64 md:w-80 flex items-center justify-center">
          <!-- Ambient glow -->
          <div class="absolute -inset-3 md:-inset-6 bg-primary/15 dark:bg-primary/8 rounded-full blur-3xl pointer-events-none opacity-60 dark:opacity-50" />
          
          <!-- Cutout profile image -->
          <img 
            v-if="profile?.avatar_url"
            :src="profile.avatar_url" 
            alt="Sarat Narak"
            class="relative z-10 w-full h-auto object-contain pointer-events-none drop-shadow-xl"
            @error="(e) => (e.target as HTMLImageElement).src = 'https://ui-avatars.com/api/?name=Sarat+Narak&size=512&background=transparent'"
          />
          <!-- Fallback placeholder -->
          <div v-else class="relative z-10 w-56 h-56 flex items-center justify-center text-primary/40">
             <svg xmlns="http://www.w3.org/2000/svg" class="h-28 w-28" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup lang="ts">
const { profile } = useProfile()
const { techStacks } = useTechStack()
</script>
