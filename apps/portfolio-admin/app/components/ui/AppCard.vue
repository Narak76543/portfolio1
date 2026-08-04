<template>
  <div
    :class="[
      'bg-surface dark:bg-[#1C1C1E] rounded-card border border-border dark:border-white/8 shadow-sm dark:shadow-none transition-colors',
      padded ? 'p-6' : '',
    ]"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  padded?: boolean
}

withDefaults(defineProps<Props>(), {
  padded: true,
})
</script>
