<template>
  <div class="mb-10 text-left">
    <div
      v-if="tag"
      class="inline-flex items-center gap-2 bg-primary/10 text-primary px-4 py-1.5 rounded-full text-xs font-bold tracking-wide uppercase mb-4 border border-primary/20"
    >
      <span class="w-1.5 h-1.5 bg-primary rounded-full" />
      {{ tag }}
    </div>
    <h2 class="text-3xl md:text-4xl lg:text-5xl font-bold text-text-primary dark:text-[#F2F2F7] tracking-tight">
      <slot />
    </h2>
    <p v-if="subtitle" class="mt-3 text-base md:text-lg text-text-secondary dark:text-[#8E8E93] font-medium max-w-2xl leading-relaxed">
      {{ subtitle }}
    </p>
    <div class="mt-5 w-20 h-1.5 bg-primary rounded-full" />
  </div>
</template>

<script setup lang="ts">
interface Props {
  subtitle?: string
  tag?: string
}

withDefaults(defineProps<Props>(), {
  subtitle: undefined,
  tag: undefined,
})
</script>
