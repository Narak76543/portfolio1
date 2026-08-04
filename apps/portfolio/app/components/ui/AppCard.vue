<template>
  <div
    :class="[
      'bg-surface dark:bg-[#1C1C1E] rounded-card border border-border dark:border-white/8 shadow-sm dark:shadow-none transition-all duration-300',
      interactive ? 'hover:shadow-lg hover:-translate-y-1 cursor-pointer' : '',
      padded ? 'p-6 md:p-7' : '',
      $attrs.class,
    ]"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
interface Props {
  padded?: boolean
  interactive?: boolean
}

withDefaults(defineProps<Props>(), {
  padded: true,
  interactive: false,
})
</script>
