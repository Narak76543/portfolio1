<template>
  <form @submit.prevent="handleSubmit" class="space-y-6">
    <FormError :message="errorMessage" />

    <div class="grid md:grid-cols-2 gap-6">
      <AppInput
        id="project-title"
        v-model="form.title"
        label="Title"
        placeholder="My Awesome Project"
        required
      />
      <AppInput
        id="project-slug"
        v-model="form.slug"
        label="Slug"
        placeholder="my-awesome-project"
        required
        hint="URL-friendly identifier. Auto-generated from title if left empty."
      />
    </div>

    <AppInput
      id="project-short-description"
      v-model="form.short_description"
      label="Short Description"
      type="textarea"
      placeholder="A brief summary of the project..."
    />

    <AppInput
      id="project-full-description"
      v-model="form.full_description"
      label="Full Description"
      type="textarea"
      placeholder="Detailed description of the project, features, and technical details..."
    />

    <AppInput
      id="project-tech-stack"
      v-model="techStackInput"
      label="Tech Stack"
      placeholder="Nuxt, FastAPI, Supabase (comma-separated)"
      hint="Enter tags separated by commas."
    />

    <AppInput
      id="project-role"
      v-model="form.role"
      label="Your Role"
      placeholder="Solo developer, Lead frontend, etc."
    />

    <div class="grid md:grid-cols-2 gap-6">
      <AppInput
        id="project-github-url"
        v-model="form.github_url"
        label="GitHub URL"
        type="url"
        placeholder="https://github.com/user/repo"
      />
      <AppInput
        id="project-live-url"
        v-model="form.live_url"
        label="Live Demo URL"
        type="url"
        placeholder="https://myproject.com"
      />
    </div>

    <!-- Cover image upload -->
    <div class="mb-4">
      <label class="block text-sm font-semibold text-text-primary dark:text-[#F2F2F7] mb-1.5">Cover Image</label>
      <div class="flex items-center gap-4">
        <div
          class="w-24 h-24 bg-background dark:bg-[#1C1C1E] border-2 border-dashed border-border dark:border-white/10 rounded-card flex items-center justify-center overflow-hidden"
        >
          <img
            v-if="form.cover_image_url"
            :src="form.cover_image_url"
            alt="Cover"
            class="w-full h-full object-cover"
          />
          <ImageIcon v-else class="w-7 h-7 text-text-secondary dark:text-[#8E8E93]" :stroke-width="1.75" />
        </div>
        <div>
          <label
            for="cover-image-upload"
            class="inline-flex items-center px-4 py-2 bg-primary/10 text-primary border border-primary/20 rounded-full text-xs font-semibold hover:bg-primary/20 transition-colors cursor-pointer"
          >
            {{ uploadLoading ? 'Uploading...' : 'Choose Image' }}
          </label>
          <input
            id="cover-image-upload"
            type="file"
            accept="image/*"
            class="hidden"
            :disabled="uploadLoading"
            @change="handleImageUpload"
          />
          <p class="text-xs text-text-secondary dark:text-[#8E8E93] mt-1">PNG, JPG, or WebP. Max 5MB.</p>
        </div>
      </div>
    </div>

    <!-- Featured toggle & Order -->
    <div class="grid md:grid-cols-2 gap-6 items-center">
      <div class="flex items-center gap-3">
        <button
          type="button"
          :class="[
            'relative inline-flex h-6 w-11 items-center rounded-full transition-colors cursor-pointer',
            form.featured ? 'bg-primary' : 'bg-border dark:bg-white/20',
          ]"
          @click="form.featured = !form.featured"
        >
          <span
            :class="[
              'inline-block h-4 w-4 rounded-full bg-white transition-transform shadow-sm',
              form.featured ? 'translate-x-6' : 'translate-x-1',
            ]"
          />
        </button>
        <label class="text-sm font-medium text-text-primary dark:text-[#F2F2F7]">Featured Project</label>
      </div>

      <AppInput
        id="project-display-order"
        v-model="displayOrderInput"
        label="Display Order"
        type="text"
        placeholder="0"
      />
    </div>

    <!-- Submit -->
    <div class="flex items-center gap-3 pt-4">
      <AppButton type="submit" :loading="loading">
        {{ submitLabel }}
      </AppButton>
      <AppButton variant="ghost" to="/admin/projects">Cancel</AppButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import { Image as ImageIcon } from 'lucide-vue-next'
import type { ProjectCreate } from '~/types/project'

interface Props {
  initialData?: Partial<ProjectCreate>
  submitLabel?: string
  loading?: boolean
  errorMessage?: string | null
}

const props = withDefaults(defineProps<Props>(), {
  initialData: () => ({}),
  submitLabel: 'Save Project',
  loading: false,
  errorMessage: null,
})

const emit = defineEmits<{
  submit: [data: ProjectCreate]
}>()

const { uploadImage } = useAdminProjects()

const form = reactive<ProjectCreate>({
  title: props.initialData.title ?? '',
  slug: props.initialData.slug ?? '',
  short_description: props.initialData.short_description ?? '',
  full_description: props.initialData.full_description ?? '',
  tech_stack: props.initialData.tech_stack ?? [],
  role: props.initialData.role ?? '',
  github_url: props.initialData.github_url ?? '',
  live_url: props.initialData.live_url ?? '',
  cover_image_url: props.initialData.cover_image_url ?? '',
  featured: props.initialData.featured ?? false,
  display_order: props.initialData.display_order ?? 0,
})

const displayOrderInput = computed({
  get: () => String(form.display_order ?? 0),
  set: (val: string) => {
    form.display_order = parseInt(val, 10) || 0
  },
})

const techStackInput = computed({
  get: () => form.tech_stack.join(', '),
  set: (val: string) => {
    form.tech_stack = val
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean)
  },
})

const uploadLoading = ref(false)

// Auto-generate slug from title
watch(
  () => form.title,
  (title) => {
    if (!props.initialData.slug) {
      form.slug = title
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')
        .replace(/[\s_]+/g, '-')
        .replace(/-+/g, '-')
        .replace(/^-|-$/g, '')
    }
  },
)

async function handleImageUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  uploadLoading.value = true
  try {
    const url = await uploadImage(file)
    form.cover_image_url = url
  } catch {
    // Error handling is displayed via the parent's error state
  } finally {
    uploadLoading.value = false
  }
}

function handleSubmit() {
  emit('submit', { ...form })
}
</script>
