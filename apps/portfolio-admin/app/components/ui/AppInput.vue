<template>
  <div class="mb-4">
    <label :for="id" class="block text-sm font-semibold text-text-primary dark:text-[#F2F2F7] mb-1.5">
      {{ label }}
      <span v-if="required" class="text-red-400">*</span>
    </label>

    <textarea
      v-if="type === 'textarea'"
      :id="id"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      rows="4"
      class="w-full px-4 py-2.5 bg-background dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-card text-sm text-text-primary dark:text-[#F2F2F7] placeholder-text-secondary dark:placeholder-[#8E8E93] focus:outline-none focus:ring-2 focus:ring-primary/25 focus:border-primary transition-all disabled:opacity-50"
      @input="$emit('update:modelValue', ($event.target as HTMLTextAreaElement).value)"
    />

    <input
      v-else
      :id="id"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :required="required"
      :disabled="disabled"
      class="w-full px-4 py-2.5 bg-background dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-card text-sm text-text-primary dark:text-[#F2F2F7] placeholder-text-secondary dark:placeholder-[#8E8E93] focus:outline-none focus:ring-2 focus:ring-primary/25 focus:border-primary transition-all disabled:opacity-50"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
    />

    <p v-if="hint" class="mt-1 text-xs text-text-secondary dark:text-[#8E8E93]">{{ hint }}</p>
  </div>
</template>

<script setup lang="ts">
interface Props {
  id: string
  label: string
  modelValue: string
  type?: 'text' | 'email' | 'password' | 'url' | 'textarea'
  placeholder?: string
  required?: boolean
  disabled?: boolean
  hint?: string
}

withDefaults(defineProps<Props>(), {
  type: 'text',
  placeholder: '',
  required: false,
  disabled: false,
  hint: undefined,
})

defineEmits<{
  'update:modelValue': [value: string]
}>()
</script>
