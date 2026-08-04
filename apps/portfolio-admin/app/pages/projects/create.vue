<template>
  <div>
    <div class="mb-6">
      <NuxtLink to="/projects" class="text-sm text-text-secondary dark:text-[#8E8E93] hover:text-primary transition-colors font-medium">
        ← Back to Projects
      </NuxtLink>
      <h1 class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7] mt-2">Create Project</h1>
    </div>

    <AppCard>
      <ProjectForm
        submit-label="Create Project"
        :loading="loading"
        :error-message="errorMessage"
        @submit="handleCreate"
      />
    </AppCard>
  </div>
</template>

<script setup lang="ts">
import type { ProjectCreate } from '~/types/project'

definePageMeta({
  layout: 'admin',
})

useHead({ title: 'Create Project — Admin' })

const { createProject } = useAdminProjects()

const loading = ref(false)
const errorMessage = ref<string | null>(null)

async function handleCreate(data: ProjectCreate) {
  loading.value = true
  errorMessage.value = null

  try {
    await createProject(data)
    navigateTo('/projects')
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to create project.'
  } finally {
    loading.value = false
  }
}
</script>
