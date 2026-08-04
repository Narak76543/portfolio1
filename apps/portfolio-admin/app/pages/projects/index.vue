<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7]">Projects</h1>
        <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-1">Manage your portfolio projects</p>
      </div>
      <AppButton to="/projects/create">
        + Add Project
      </AppButton>
    </div>

    <FormError :message="errorMessage" />

    <!-- Loading state -->
    <AppCard v-if="status === 'pending'" class="text-center py-12">
      <div class="animate-spin w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full mx-auto" />
      <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-3">Loading projects...</p>
    </AppCard>

    <!-- Error state -->
    <AppCard v-else-if="status === 'error'" class="text-center py-12">
      <p class="text-text-secondary dark:text-[#8E8E93] mb-4">Failed to load projects.</p>
      <AppButton variant="secondary" @click="refresh()">Retry</AppButton>
    </AppCard>

    <!-- Project table -->
    <ProjectTable
      v-else
      :projects="projects ?? []"
      :deleting-id="deletingId"
      @delete="handleDelete"
    />
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
})

useHead({ title: 'Projects — Admin' })

const { projects, status, refresh, deleteProject } = useAdminProjects()

const deletingId = ref<string | null>(null)
const errorMessage = ref<string | null>(null)

async function handleDelete(id: string) {
  if (!confirm('Are you sure you want to delete this project?')) return

  deletingId.value = id
  errorMessage.value = null

  try {
    await deleteProject(id)
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to delete project.'
  } finally {
    deletingId.value = null
  }
}
</script>
