<template>
  <component
    :is="to ? NuxtLink : 'button'"
    :to="to"
    :class="[
      'inline-flex items-center justify-center font-semibold rounded-full transition-all duration-200 cursor-pointer select-none',
      sizeClasses,
      variantClasses,
      { 'opacity-50 pointer-events-none': disabled || loading },
    ]"
    :disabled="disabled || loading"
    v-bind="$attrs"
  >
    <svg
      v-if="loading"
      class="animate-spin -ml-1 mr-2 h-4 w-4"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
    >
      <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
      <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
    </svg>
    <slot />
  </component>
</template>

<script setup lang="ts">
const NuxtLink = resolveComponent('NuxtLink')

interface Props {
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  to?: string
  disabled?: boolean
  loading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  to: undefined,
  disabled: false,
  loading: false,
})

const sizeClasses = computed(() => {
  const map = {
    sm: 'px-4 py-1.5 text-xs',
    md: 'px-6 py-2.5 text-sm',
    lg: 'px-9 py-3 text-base',
  }
  return map[props.size]
})

const variantClasses = computed(() => {
  const map = {
    primary:
      'bg-primary text-white hover:bg-primary-hover shadow-sm font-bold hover:-translate-y-0.5 active:translate-y-0',
    secondary:
      'bg-transparent text-primary border-2 border-primary hover:bg-primary/10 font-bold hover:-translate-y-0.5 active:translate-y-0',
    ghost:
      'text-text-secondary dark:text-[#8E8E93] hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/10 font-semibold',
    danger:
      'bg-red-50 text-red-600 hover:bg-red-100 dark:bg-red-950/40 dark:text-red-400 dark:hover:bg-red-900/50 dark:border dark:border-red-900/40 font-semibold',
  }
  return map[props.variant]
})
</script>
