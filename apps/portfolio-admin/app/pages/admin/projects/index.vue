<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7] tracking-tight">Projects</h1>
        <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-1">Manage your portfolio projects and showcase items</p>
      </div>
      <AppButton to="/admin/projects/create">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Add Project
      </AppButton>
    </div>

    <!-- Quick Stats Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
      <AppCard class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-full bg-primary/10 text-primary border border-primary/20 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
          </svg>
        </div>
        <div>
          <div class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7] font-mono">{{ projects?.length || 0 }}</div>
          <div class="text-xs font-semibold text-text-secondary dark:text-[#8E8E93]">Total Projects</div>
        </div>
      </AppCard>

      <AppCard class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-full bg-amber-500/10 text-amber-500 border border-amber-500/20 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z" />
          </svg>
        </div>
        <div>
          <div class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7] font-mono">{{ featuredCount }}</div>
          <div class="text-xs font-semibold text-text-secondary dark:text-[#8E8E93]">Featured Projects</div>
        </div>
      </AppCard>

      <AppCard class="flex items-center gap-4">
        <div class="w-12 h-12 rounded-full bg-primary/10 text-primary border border-primary/20 flex items-center justify-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
          </svg>
        </div>
        <div>
          <div class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7] font-mono">{{ totalTechTags }}</div>
          <div class="text-xs font-semibold text-text-secondary dark:text-[#8E8E93]">Unique Tech Tags</div>
        </div>
      </AppCard>
    </div>

    <!-- Search & Filter Controls -->
    <div class="flex flex-col sm:flex-row gap-3">
      <div class="relative flex-1">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 absolute left-4 top-3.5 text-text-secondary dark:text-[#8E8E93] pointer-events-none" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
        </svg>
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Search by title, slug, or tech stack..."
          class="w-full pl-11 pr-4 py-2.5 bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-card text-sm text-text-primary dark:text-[#F2F2F7] placeholder-text-secondary dark:placeholder-[#8E8E93] focus:outline-none focus:ring-2 focus:ring-primary/25 focus:border-primary transition-all"
        />
      </div>

      <select
        v-model="filterStatus"
        class="px-4 py-2.5 bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-card text-sm text-text-primary dark:text-[#F2F2F7] focus:outline-none focus:ring-2 focus:ring-primary/25 focus:border-primary transition-all"
      >
        <option value="all">All Projects</option>
        <option value="featured">Featured Only</option>
        <option value="standard">Standard Only</option>
      </select>
    </div>

    <FormError :message="errorMessage" />

    <!-- Loading state -->
    <AppCard v-if="status === 'pending'" class="text-center py-16">
      <div class="animate-spin w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full mx-auto" />
      <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-3">Loading projects...</p>
    </AppCard>

    <!-- Error state -->
    <AppCard v-else-if="status === 'error'" class="text-center py-16">
      <p class="text-text-secondary dark:text-[#8E8E93] mb-4">Failed to load projects from backend.</p>
      <AppButton variant="secondary" @click="refresh()">Retry Connection</AppButton>
    </AppCard>

    <!-- Project table -->
    <ProjectTable
      v-else
      :projects="filteredProjects"
      :deleting-id="deletingId"
      :reordering="reordering"
      @delete="handleDelete"
      @reorder="handleReorder"
    />
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'admin',
})

useHead({ title: 'Projects — Admin' })

const { projects, status, refresh, deleteProject, updateOrder } = useAdminProjects()

const deletingId = ref<string | null>(null)
const reordering = ref(false)
const errorMessage = ref<string | null>(null)
const searchQuery = ref('')
const filterStatus = ref<'all' | 'featured' | 'standard'>('all')

const featuredCount = computed(() => {
  return projects.value?.filter((p) => p.featured).length || 0
})

const totalTechTags = computed(() => {
  if (!projects.value) return 0
  const tags = new Set<string>()
  projects.value.forEach((p) => p.tech_stack?.forEach((t) => tags.add(t)))
  return tags.size
})

const filteredProjects = computed(() => {
  if (!projects.value) return []
  return projects.value.filter((p) => {
    // Search query
    const q = searchQuery.value.toLowerCase().trim()
    const matchesSearch =
      !q ||
      p.title.toLowerCase().includes(q) ||
      p.slug.toLowerCase().includes(q) ||
      p.tech_stack?.some((t) => t.toLowerCase().includes(q))

    // Filter status
    let matchesStatus = true
    if (filterStatus.value === 'featured') matchesStatus = p.featured
    if (filterStatus.value === 'standard') matchesStatus = !p.featured

    return matchesSearch && matchesStatus
  })
})

async function handleReorder(index: number, direction: 'up' | 'down') {
  const list = filteredProjects.value
  const targetIndex = direction === 'up' ? index - 1 : index + 1
  if (targetIndex < 0 || targetIndex >= list.length) return

  reordering.value = true
  const currentItem = list[index]
  const targetItem = list[targetIndex]

  try {
    await updateOrder(currentItem.id, targetItem.display_order)
    await updateOrder(targetItem.id, currentItem.display_order)
    await refresh()
  } catch {
    errorMessage.value = 'Failed to reorder projects.'
  } finally {
    reordering.value = false
  }
}

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
