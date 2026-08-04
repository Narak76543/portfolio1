<template>
  <button
    class="p-2 rounded-full text-text-secondary dark:text-[#8E8E93] hover:text-primary dark:hover:text-primary hover:bg-primary/10 dark:hover:bg-primary/10 transition-all duration-200"
    :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    @click="toggleTheme"
  >
    <svg v-if="isDark" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364-.707-.707M6.343 6.343l-.707-.707m12.728 0-.707.707M6.343 17.657l-.707.707M12 16a4 4 0 100-8 4 4 0 000 8z" />
    </svg>
    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z" />
    </svg>
  </button>
</template>

<script setup lang="ts">
const isDark = ref(false)

function applyTheme(value: boolean) {
  isDark.value = value
  document.documentElement.classList.toggle('dark', value)
}

function toggleTheme() {
  const value = !isDark.value
  applyTheme(value)
  localStorage.setItem('theme', value ? 'dark' : 'light')
}

onMounted(() => applyTheme(document.documentElement.classList.contains('dark')))
</script>
