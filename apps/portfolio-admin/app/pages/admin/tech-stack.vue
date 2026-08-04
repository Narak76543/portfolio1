<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7] tracking-tight">Tech Stack Management</h1>
        <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-1">Manage brand logos and tech stack items displayed on the public Hero section</p>
      </div>
      <AppButton @click="openCreateModal">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Add Tech Item
      </AppButton>
    </div>

    <FormError :message="errorMessage" />

    <!-- Loading State -->
    <AppCard v-if="status === 'pending'" class="text-center py-16">
      <div class="animate-spin w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full mx-auto" />
      <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-3">Loading tech stack items...</p>
    </AppCard>

    <!-- Error State -->
    <AppCard v-else-if="status === 'error'" class="text-center py-16">
      <p class="text-text-secondary dark:text-[#8E8E93] mb-4">Failed to load tech stack items.</p>
      <AppButton variant="secondary" @click="refresh()">Retry Connection</AppButton>
    </AppCard>

    <!-- Table List -->
    <AppCard v-else padded class="space-y-4">
      <div class="overflow-hidden bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/8 rounded-card">
        <table class="w-full text-sm border-collapse">
          <thead>
            <tr class="border-b border-border dark:border-white/8 bg-background/60 dark:bg-white/3">
              <th class="text-left px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Icon & Name</th>
              <th class="text-center px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Display Order</th>
              <th class="text-right px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border dark:divide-white/8">
            <tr
              v-for="(item, index) in sortedTechStacks"
              :key="item.id"
              class="hover:bg-background/60 dark:hover:bg-white/3 transition-colors"
            >
              <td class="px-5 py-4">
                <div class="flex items-center gap-4">
                  <div class="w-10 h-10 bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-full flex items-center justify-center p-2 shadow-sm flex-shrink-0">
                    <img v-if="item.icon_url" :src="item.icon_url" :alt="item.name" class="w-full h-full object-contain" />
                    <span v-else class="text-xs text-primary/50">⚡</span>
                  </div>
                  <div>
                    <div class="font-semibold text-text-primary dark:text-[#F2F2F7]">{{ item.name }}</div>
                    <div class="text-xs text-text-secondary dark:text-[#8E8E93] font-mono mt-0.5">{{ item.icon_url ? 'Official Brand Icon' : 'No Icon' }}</div>
                  </div>
                </div>
              </td>

              <td class="px-5 py-4 text-center">
                <div class="inline-flex items-center gap-2">
                  <button
                    type="button"
                    class="p-1 rounded-full text-text-secondary dark:text-[#8E8E93] hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/8 transition-colors disabled:opacity-30 cursor-pointer"
                    :disabled="index === 0 || reordering"
                    @click="moveItem(index, 'up')"
                    title="Move Up"
                  >
                    ▲
                  </button>
                  <span class="font-mono text-xs font-semibold px-2.5 py-0.5 bg-primary/10 text-primary rounded-full">
                    {{ item.display_order }}
                  </span>
                  <button
                    type="button"
                    class="p-1 rounded-full text-text-secondary dark:text-[#8E8E93] hover:text-text-primary dark:hover:text-[#F2F2F7] hover:bg-black/5 dark:hover:bg-white/8 transition-colors disabled:opacity-30 cursor-pointer"
                    :disabled="index === sortedTechStacks.length - 1 || reordering"
                    @click="moveItem(index, 'down')"
                    title="Move Down"
                  >
                    ▼
                  </button>
                </div>
              </td>

              <td class="px-5 py-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  <AppButton variant="ghost" size="sm" @click="openEditModal(item)">
                    Edit
                  </AppButton>
                  <AppButton
                    variant="danger"
                    size="sm"
                    :loading="deletingId === item.id"
                    @click="handleDelete(item.id)"
                  >
                    Delete
                  </AppButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="!sortedTechStacks.length" class="text-center py-12 text-text-secondary dark:text-[#8E8E93] text-sm">
          No tech stack items found. Click "Add Tech Item" to create one.
        </div>
      </div>
    </AppCard>

    <!-- Modal Form (Create / Edit) -->
    <div
      v-if="modalOpen"
      class="fixed inset-0 z-50 bg-text-primary/50 dark:bg-black/70 backdrop-blur-sm flex items-center justify-center p-4"
    >
      <div class="bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-card max-w-md w-full p-6 shadow-2xl space-y-5">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-bold text-text-primary dark:text-[#F2F2F7]">
            {{ editingItem ? 'Edit Tech Item' : 'Add New Tech Item' }}
          </h3>
          <button type="button" class="text-text-secondary dark:text-[#8E8E93] hover:text-text-primary dark:hover:text-[#F2F2F7] transition-colors" @click="modalOpen = false">
            ✕
          </button>
        </div>

        <form @submit.prevent="handleSave" class="space-y-4">
          <AppInput
            id="tech-name"
            v-model="form.name"
            label="Technology Name"
            placeholder="e.g. FastAPI, Nuxt.js, Docker"
            required
          />

          <AppInput
            id="tech-order"
            v-model="formOrderInput"
            label="Display Order"
            type="text"
            placeholder="0"
            hint="Numerical order. Lower numbers render first."
          />

          <!-- Icon Upload -->
          <div>
            <label class="block text-sm font-semibold text-text-primary dark:text-[#F2F2F7] mb-1.5">Brand Icon (SVG/PNG)</label>
            <div class="flex items-center gap-4">
              <div class="w-12 h-12 bg-background dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-card flex items-center justify-center p-2 overflow-hidden">
                <img v-if="form.icon_url" :src="form.icon_url" alt="Preview" class="w-full h-full object-contain" />
                <span v-else class="text-xs text-text-secondary dark:text-[#8E8E93]">Preview</span>
              </div>
              <div class="flex-1">
                <label
                  for="icon-file-upload"
                  class="inline-flex items-center px-4 py-1.5 bg-primary/10 text-primary border border-primary/20 rounded-full text-xs font-semibold hover:bg-primary/20 transition-colors cursor-pointer"
                >
                  {{ uploading ? 'Uploading...' : 'Choose SVG/PNG' }}
                </label>
                <input
                  id="icon-file-upload"
                  type="file"
                  accept="image/svg+xml, image/png, image/jpeg, image/webp"
                  class="hidden"
                  :disabled="uploading"
                  @change="handleFileUpload"
                />
                <p class="text-xs text-text-secondary dark:text-[#8E8E93] mt-1">Official SVG brand logo recommended.</p>
              </div>
            </div>
          </div>

          <div class="flex items-center justify-end gap-3 pt-3 border-t border-border dark:border-white/8">
            <AppButton variant="ghost" type="button" @click="modalOpen = false">Cancel</AppButton>
            <AppButton type="submit" :loading="saving">Save Item</AppButton>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { TechStackItem } from '~/types/techStack'

definePageMeta({ layout: 'admin' })
useHead({ title: 'Tech Stack — Admin' })

const {
  techStacks,
  status,
  refresh,
  createTechStack,
  updateTechStack,
  deleteTechStack,
  uploadIcon,
  updateOrder,
} = useAdminTechStack()

const errorMessage = ref<string | null>(null)
const deletingId = ref<string | null>(null)
const reordering = ref(false)

// Modal state
const modalOpen = ref(false)
const editingItem = ref<TechStackItem | null>(null)
const uploading = ref(false)
const saving = ref(false)

const form = reactive({
  name: '',
  icon_url: '',
  display_order: 0,
})

const formOrderInput = computed({
  get: () => String(form.display_order),
  set: (val: string) => {
    form.display_order = parseInt(val, 10) || 0
  },
})

const sortedTechStacks = computed(() => {
  if (!techStacks.value) return []
  return [...techStacks.value].sort((a, b) => a.display_order - b.display_order)
})

function openCreateModal() {
  editingItem.value = null
  form.name = ''
  form.icon_url = ''
  form.display_order = sortedTechStacks.value.length
  modalOpen.value = true
}

function openEditModal(item: TechStackItem) {
  editingItem.value = item
  form.name = item.name
  form.icon_url = item.icon_url || ''
  form.display_order = item.display_order
  modalOpen.value = true
}

async function handleFileUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  uploading.value = true
  try {
    const url = await uploadIcon(file)
    form.icon_url = url
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to upload icon.'
  } finally {
    uploading.value = false
  }
}

async function handleSave() {
  if (!form.name.trim()) return

  saving.value = true
  errorMessage.value = null

  try {
    if (editingItem.value) {
      await updateTechStack(editingItem.value.id, {
        name: form.name,
        icon_url: form.icon_url || null,
        display_order: form.display_order,
      })
    } else {
      await createTechStack({
        name: form.name,
        icon_url: form.icon_url || null,
        display_order: form.display_order,
      })
    }
    modalOpen.value = false
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to save item.'
  } finally {
    saving.value = false
  }
}

async function moveItem(index: number, direction: 'up' | 'down') {
  const targetIndex = direction === 'up' ? index - 1 : index + 1
  if (targetIndex < 0 || targetIndex >= sortedTechStacks.value.length) return

  reordering.value = true
  const currentItem = sortedTechStacks.value[index]
  const targetItem = sortedTechStacks.value[targetIndex]

  try {
    await updateOrder(currentItem.id, targetItem.display_order)
    await updateOrder(targetItem.id, currentItem.display_order)
    await refresh()
  } catch {
    errorMessage.value = 'Failed to reorder items.'
  } finally {
    reordering.value = false
  }
}

async function handleDelete(id: string) {
  if (!confirm('Are you sure you want to delete this tech stack item?')) return

  deletingId.value = id
  errorMessage.value = null

  try {
    await deleteTechStack(id)
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to delete item.'
  } finally {
    deletingId.value = null
  }
}
</script>
