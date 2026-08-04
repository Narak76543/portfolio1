<template>
  <div v-if="message" class="bg-red-500/8 dark:bg-red-900/20 border border-red-500/20 dark:border-red-700/30 text-red-600 dark:text-red-400 px-4 py-3 rounded-card text-sm flex items-start gap-3" role="alert">
    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 flex-shrink-0 mt-0.5 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
    </svg>
    <span>{{ message }}</span>
  </div>
</template>

<script setup lang="ts">
interface Props {
  message: string | null | undefined
}

defineProps<Props>()
</script>
