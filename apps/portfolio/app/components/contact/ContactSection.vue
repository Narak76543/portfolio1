<template>
  <section id="contact" class="scroll-mt-20 py-16 md:py-20 border-t border-border/40 dark:border-white/8 transition-colors duration-300">
    <div class="max-w-6xl mx-auto px-6">
      <!-- Section Heading -->
      <SectionHeading
        tag="04. Get In Touch"
        subtitle="I'm currently looking for junior or entry-level IT roles where I can contribute to real products and continue growing as a developer. Feel free to reach out anytime!"
      >
        LET'S CONNECT
      </SectionHeading>

      <!-- Contact / Social Cards Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-5 mt-10">
        <a
          v-for="item in activeLinks"
          :key="item.id"
          :href="item.url"
          target="_blank"
          rel="noopener noreferrer"
          class="group relative flex items-center justify-between p-5 rounded-card bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/8 hover:border-primary/40 dark:hover:border-primary/30 transition-all duration-200 shadow-sm dark:shadow-none hover:shadow-md hover:-translate-y-0.5"
        >
          <div class="flex items-center gap-4 min-w-0 pr-2">
            <!-- Icon Container -->
            <div class="w-11 h-11 bg-primary/10 rounded-full flex items-center justify-center text-primary flex-shrink-0">
              <component :is="getContactIcon(item.name)" class="w-5 h-5" :stroke-width="1.75" />
            </div>

            <!-- Content Details -->
            <div class="min-w-0 flex-1">
              <div class="text-xs font-bold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider mb-0.5">
                {{ item.name }}
              </div>
              <div class="text-sm md:text-base font-bold text-text-primary dark:text-[#F2F2F7] transition-colors truncate">
                {{ item.value }}
              </div>
            </div>
          </div>

          <!-- Arrow Link Icon -->
          <div class="w-8 h-8 rounded-full bg-primary/10 text-primary flex items-center justify-center flex-shrink-0 transition-all group-hover:bg-primary group-hover:text-white">
            <ArrowUpRight class="w-4 h-4 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" :stroke-width="2" />
          </div>
        </a>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Mail, Github, Linkedin, Send, Facebook, Globe, Link as LinkIcon, ArrowUpRight } from 'lucide-vue-next'

const { socialMedias } = useSocialMedia()

const fallbackLinks = [
  {
    id: 'email-fallback',
    name: 'Email',
    value: 'saratnarak85@gmail.com',
    url: 'mailto:saratnarak85@gmail.com',
    icon_url: null,
  },
  {
    id: 'github-fallback',
    name: 'GitHub',
    value: 'Narak76543',
    url: 'https://github.com/Narak76543',
    icon_url: null,
  },
  {
    id: 'linkedin-fallback',
    name: 'LinkedIn',
    value: 'narak-sarat',
    url: 'https://linkedin.com/in/narak-sarat',
    icon_url: null,
  },
  {
    id: 'telegram-fallback',
    name: 'Telegram',
    value: '@saratnarak',
    url: 'https://t.me/saratnarak',
    icon_url: null,
  },
]

const activeLinks = computed(() => {
  if (socialMedias.value && socialMedias.value.length > 0) {
    return socialMedias.value
  }
  return fallbackLinks
})

function getContactIcon(name: string) {
  const n = (name || '').toLowerCase()
  if (n.includes('email') || n.includes('mail')) return Mail
  if (n.includes('github')) return Github
  if (n.includes('linkedin')) return Linkedin
  if (n.includes('telegram')) return Send
  if (n.includes('facebook')) return Facebook
  if (n.includes('website') || n.includes('site')) return Globe
  return LinkIcon
}
</script>
