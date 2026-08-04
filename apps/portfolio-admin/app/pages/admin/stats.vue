<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7] tracking-tight">Stat Cards Management</h1>
        <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-1">Manage metric counter cards displayed on the public About section</p>
      </div>
      <AppButton @click="openCreateModal">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Add Stat Card
      </AppButton>
    </div>

    <FormError :message="errorMessage" />

    <!-- Loading State -->
    <AppCard v-if="status === 'pending'" class="text-center py-16">
      <div class="animate-spin w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full mx-auto" />
      <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-3">Loading stat cards...</p>
    </AppCard>

    <!-- Error State -->
    <AppCard v-else-if="status === 'error'" class="text-center py-16">
      <p class="text-text-secondary dark:text-[#8E8E93] mb-4">Failed to load stat cards.</p>
      <AppButton variant="secondary" @click="refresh()">Retry Connection</AppButton>
    </AppCard>

    <!-- Table List -->
    <AppCard v-else padded class="space-y-4">
      <div class="overflow-hidden bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/8 rounded-card">
        <table class="w-full text-sm border-collapse">
          <thead>
            <tr class="border-b border-border dark:border-white/8 bg-background/60 dark:bg-white/3">
              <th class="text-left px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Stat Label</th>
              <th class="text-left px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Value</th>
              <th class="text-left px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Icon</th>
              <th class="text-center px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Display Order</th>
              <th class="text-right px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border dark:divide-white/8">
            <tr
              v-for="(item, index) in sortedStats"
              :key="item.id"
              class="hover:bg-background/60 dark:hover:bg-white/3 transition-colors"
            >
              <td class="px-5 py-4 font-semibold text-text-primary dark:text-[#F2F2F7]">
                {{ item.label }}
              </td>

              <td class="px-5 py-4 font-mono font-bold text-primary text-base">
                {{ item.value }}
              </td>

              <td class="px-5 py-4 text-xs font-mono text-text-secondary dark:text-[#8E8E93]">
                <span class="px-2 py-0.5 bg-primary/10 text-primary rounded-full">
                  {{ item.icon_name || 'default' }}
                </span>
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
                    :disabled="index === sortedStats.length - 1 || reordering"
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

        <div v-if="!sortedStats.length" class="text-center py-12 text-text-secondary dark:text-[#8E8E93] text-sm">
          No stat cards found. Click "Add Stat Card" to create one.
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
            {{ editingItem ? 'Edit Stat Card' : 'Add New Stat Card' }}
          </h3>
          <button type="button" class="text-text-secondary dark:text-[#8E8E93] hover:text-text-primary dark:hover:text-[#F2F2F7] transition-colors" @click="modalOpen = false">
            ✕
          </button>
        </div>

        <form @submit.prevent="handleSave" class="space-y-4">
          <AppInput
            id="stat-label"
            v-model="form.label"
            label="Stat Label"
            placeholder="e.g. Projects Built, GitHub Repos"
            required
          />

          <AppInput
            id="stat-value"
            v-model="form.value"
            label="Stat Value"
            placeholder="e.g. 8+, 49+, 2+"
            required
          />

          <AppInput
            id="stat-icon"
            v-model="form.icon_name"
            label="Icon Name"
            placeholder="folder, code, clock, git"
            hint="Options: folder, code, clock, git, star, trophy"
          />

          <AppInput
            id="stat-order"
            v-model="formOrderInput"
            label="Display Order"
            type="text"
            placeholder="0"
          />

          <div class="flex items-center justify-end gap-3 pt-3 border-t border-border dark:border-white/8">
            <AppButton variant="ghost" type="button" @click="modalOpen = false">Cancel</AppButton>
            <AppButton type="submit" :loading="saving">Save Card</AppButton>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { StatItem } from '~/types/stat'

definePageMeta({ layout: 'admin' })
useHead({ title: 'Stats — Admin' })

const {
  stats,
  status,
  refresh,
  createStat,
  updateStat,
  deleteStat,
  updateOrder,
} = useAdminStats()

const errorMessage = ref<string | null>(null)
const deletingId = ref<string | null>(null)
const reordering = ref(false)

const modalOpen = ref(false)
const editingItem = ref<StatItem | null>(null)
const saving = ref(false)

const form = reactive({
  label: '',
  value: '',
  icon_name: 'folder',
  display_order: 0,
})

const formOrderInput = computed({
  get: () => String(form.display_order),
  set: (val: string) => {
    form.display_order = parseInt(val, 10) || 0
  },
})

const sortedStats = computed(() => {
  if (!stats.value) return []
  return [...stats.value].sort((a, b) => a.display_order - b.display_order)
})

function openCreateModal() {
  editingItem.value = null
  form.label = ''
  form.value = ''
  form.icon_name = 'folder'
  form.display_order = sortedStats.value.length
  modalOpen.value = true
}

function openEditModal(item: StatItem) {
  editingItem.value = item
  form.label = item.label
  form.value = item.value
  form.icon_name = item.icon_name || 'folder'
  form.display_order = item.display_order
  modalOpen.value = true
}

async function handleSave() {
  if (!form.label.trim() || !form.value.trim()) return

  saving.value = true
  errorMessage.value = null

  try {
    if (editingItem.value) {
      await updateStat(editingItem.value.id, {
        label: form.label,
        value: form.value,
        icon_name: form.icon_name || null,
        display_order: form.display_order,
      })
    } else {
      await createStat({
        label: form.label,
        value: form.value,
        icon_name: form.icon_name || null,
        display_order: form.display_order,
      })
    }
    modalOpen.value = false
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to save stat card.'
  } finally {
    saving.value = false
  }
}

async function moveItem(index: number, direction: 'up' | 'down') {
  const targetIndex = direction === 'up' ? index - 1 : index + 1
  if (targetIndex < 0 || targetIndex >= sortedStats.value.length) return

  reordering.value = true
  const currentItem = sortedStats.value[index]
  const targetItem = sortedStats.value[targetIndex]

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
  if (!confirm('Are you sure you want to delete this stat card?')) return

  deletingId.value = id
  errorMessage.value = null

  try {
    await deleteStat(id)
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to delete stat card.'
  } finally {
    deletingId.value = null
  }
}
</script>
