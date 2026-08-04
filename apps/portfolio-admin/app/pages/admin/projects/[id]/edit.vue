<template>
  <div class="max-w-4xl mx-auto space-y-6">
    <div>
      <NuxtLink to="/admin/projects" class="inline-flex items-center text-sm font-medium text-text-secondary dark:text-[#8E8E93] hover:text-primary transition-colors">
        ← Back to Projects
      </NuxtLink>
      <h1 class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7] tracking-tight mt-2">Edit Project</h1>
      <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-1">Update details for project {{ project?.title || '' }}</p>
    </div>

    <!-- Loading state -->
    <AppCard v-if="pageLoading" class="text-center py-16">
      <div class="animate-spin w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full mx-auto" />
      <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-3">Loading project details...</p>
    </AppCard>

    <!-- Error state -->
    <AppCard v-else-if="pageError" class="text-center py-16">
      <p class="text-text-secondary dark:text-[#8E8E93] mb-4">{{ pageError }}</p>
      <AppButton variant="secondary" to="/admin/projects">Back to Projects</AppButton>
    </AppCard>

    <!-- Edit form -->
    <AppCard v-else-if="project" padded>
      <ProjectForm
        :initial-data="project"
        submit-label="Update Project"
        :loading="saving"
        :error-message="saveError"
        @submit="handleUpdate"
      />
    </AppCard>
  </div>
</template>

<script setup lang="ts">
import type { Project, ProjectCreate, ProjectUpdate } from '~/types/project'

definePageMeta({
  layout: 'admin',
})

useHead({ title: 'Edit Project — Admin' })

const route = useRoute()
const projectId = route.params.id as string

const { getProject, updateProject } = useAdminProjects()

const project = ref<Project | null>(null)
const pageLoading = ref(true)
const pageError = ref<string | null>(null)
const saving = ref(false)
const saveError = ref<string | null>(null)

// Load project data
onMounted(async () => {
  try {
    project.value = await getProject(projectId)
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    pageError.value = error.data?.detail || error.message || 'Project not found.'
  } finally {
    pageLoading.value = false
  }
})

async function handleUpdate(data: ProjectCreate) {
  saving.value = true
  saveError.value = null

  try {
    const updateData: ProjectUpdate = { ...data }
    await updateProject(projectId, updateData)
    navigateTo('/admin/projects')
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    saveError.value = error.data?.detail || error.message || 'Failed to update project.'
  } finally {
    saving.value = false
  }
}
</script>
