<template>
  <div class="space-y-6 w-full">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7] tracking-tight">Social Media & Contact Links</h1>
        <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-1">Manage public social media channels and contact handles in the Get In Touch section</p>
      </div>
      <AppButton @click="openCreateModal">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
        </svg>
        Add Social Link
      </AppButton>
    </div>

    <FormError :message="errorMessage" />

    <!-- Loading State -->
    <AppCard v-if="status === 'pending'" class="text-center py-16">
      <div class="animate-spin w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full mx-auto" />
      <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-3">Loading social media links...</p>
    </AppCard>

    <!-- Error State -->
    <AppCard v-else-if="status === 'error'" class="text-center py-16">
      <p class="text-text-secondary dark:text-[#8E8E93] mb-4">Failed to load social media links.</p>
      <AppButton variant="secondary" @click="refresh()">Retry Connection</AppButton>
    </AppCard>

    <!-- Table List -->
    <AppCard v-else padded class="space-y-4">
      <div class="overflow-hidden bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/8 rounded-card">
        <table class="w-full text-sm border-collapse">
          <thead>
            <tr class="border-b border-border dark:border-white/8 bg-background/60 dark:bg-white/3">
              <th class="text-left px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Platform & Icon</th>
              <th class="text-left px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Display Handle / Text</th>
              <th class="text-left px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Target URL</th>
              <th class="text-center px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Display Order</th>
              <th class="text-right px-5 py-3.5 text-xs font-semibold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-border dark:divide-white/8">
            <tr
              v-for="(item, index) in sortedSocials"
              :key="item.id"
              class="hover:bg-background/60 dark:hover:bg-white/3 transition-colors"
            >
              <td class="px-5 py-4">
                <div class="flex items-center gap-3.5">
                  <div class="w-9 h-9 bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-full flex items-center justify-center p-2 shadow-sm flex-shrink-0">
                    <img v-if="item.icon_url" :src="item.icon_url" :alt="item.name" class="w-full h-full object-contain" />
                    <LinkIcon v-else class="w-4 h-4 text-primary" :stroke-width="1.75" />
                  </div>
                  <span class="font-bold text-text-primary dark:text-[#F2F2F7]">{{ item.name }}</span>
                </div>
              </td>

              <td class="px-5 py-4 font-medium text-text-primary dark:text-[#F2F2F7]">
                {{ item.value }}
              </td>

              <td class="px-5 py-4 font-mono text-xs text-primary max-w-xs truncate">
                <a :href="item.url" target="_blank" rel="noopener noreferrer" class="hover:underline">
                  {{ item.url }}
                </a>
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
                    :disabled="index === sortedSocials.length - 1 || reordering"
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

        <div v-if="!sortedSocials.length" class="text-center py-12 text-text-secondary dark:text-[#8E8E93] text-sm">
          No social media links found. Click "Add Social Link" to create one.
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
            {{ editingItem ? 'Edit Social Link' : 'Add New Social Link' }}
          </h3>
          <button type="button" class="text-text-secondary dark:text-[#8E8E93] hover:text-text-primary dark:hover:text-[#F2F2F7] transition-colors" @click="modalOpen = false">
            ✕
          </button>
        </div>

        <form @submit.prevent="handleSave" class="space-y-4">
          <AppInput
            id="social-name"
            v-model="form.name"
            label="Platform Name"
            placeholder="e.g. GitHub, LinkedIn, Telegram, Email"
            required
          />

          <AppInput
            id="social-value"
            v-model="form.value"
            label="Display Handle / Value"
            placeholder="e.g. saratnarak85@gmail.com, Narak76543"
            required
          />

          <AppInput
            id="social-url"
            v-model="form.url"
            label="Target URL"
            placeholder="e.g. https://github.com/Narak76543 or mailto:..."
            required
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
                  for="social-icon-upload"
                  class="inline-flex items-center px-4 py-1.5 bg-primary/10 text-primary border border-primary/20 rounded-full text-xs font-semibold hover:bg-primary/20 transition-colors cursor-pointer"
                >
                  {{ uploading ? 'Uploading...' : 'Choose SVG/PNG' }}
                </label>
                <input
                  id="social-icon-upload"
                  type="file"
                  accept="image/svg+xml, image/png, image/jpeg, image/webp"
                  class="hidden"
                  :disabled="uploading"
                  @change="handleFileUpload"
                />
                <p class="text-xs text-text-secondary dark:text-[#8E8E93] mt-1">Official SVG brand icon recommended.</p>
              </div>
            </div>
          </div>

          <AppInput
            id="social-order"
            v-model="formOrderInput"
            label="Display Order"
            type="text"
            placeholder="0"
          />

          <div class="flex items-center justify-end gap-3 pt-3 border-t border-border dark:border-white/8">
            <AppButton variant="ghost" type="button" @click="modalOpen = false">Cancel</AppButton>
            <AppButton type="submit" :loading="saving">Save Link</AppButton>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Link as LinkIcon } from 'lucide-vue-next'
import type { SocialMediaItem } from '~/types/socialMedia'

definePageMeta({ layout: 'admin' })
useHead({ title: 'Social Media — Admin' })

const {
  socialMedias,
  status,
  refresh,
  createSocialMedia,
  updateSocialMedia,
  deleteSocialMedia,
  uploadIcon,
  updateOrder,
} = useAdminSocialMedia()

const errorMessage = ref<string | null>(null)
const deletingId = ref<string | null>(null)
const reordering = ref(false)

const modalOpen = ref(false)
const editingItem = ref<SocialMediaItem | null>(null)
const uploading = ref(false)
const saving = ref(false)

const form = reactive({
  name: '',
  value: '',
  url: '',
  icon_url: '',
  display_order: 0,
})

const formOrderInput = computed({
  get: () => String(form.display_order),
  set: (val: string) => {
    form.display_order = parseInt(val, 10) || 0
  },
})

const sortedSocials = computed(() => {
  if (!socialMedias.value) return []
  return [...socialMedias.value].sort((a, b) => a.display_order - b.display_order)
})

function openCreateModal() {
  editingItem.value = null
  form.name = ''
  form.value = ''
  form.url = ''
  form.icon_url = ''
  form.display_order = sortedSocials.value.length
  modalOpen.value = true
}

function openEditModal(item: SocialMediaItem) {
  editingItem.value = item
  form.name = item.name
  form.value = item.value
  form.url = item.url
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
  if (!form.name.trim() || !form.value.trim() || !form.url.trim()) return

  saving.value = true
  errorMessage.value = null

  try {
    if (editingItem.value) {
      await updateSocialMedia(editingItem.value.id, {
        name: form.name,
        value: form.value,
        url: form.url,
        icon_url: form.icon_url || null,
        display_order: form.display_order,
      })
    } else {
      await createSocialMedia({
        name: form.name,
        value: form.value,
        url: form.url,
        icon_url: form.icon_url || null,
        display_order: form.display_order,
      })
    }
    modalOpen.value = false
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to save social link.'
  } finally {
    saving.value = false
  }
}

async function moveItem(index: number, direction: 'up' | 'down') {
  const targetIndex = direction === 'up' ? index - 1 : index + 1
  if (targetIndex < 0 || targetIndex >= sortedSocials.value.length) return

  reordering.value = true
  const currentItem = sortedSocials.value[index]
  const targetItem = sortedSocials.value[targetIndex]

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
  if (!confirm('Are you sure you want to delete this social media link?')) return

  deletingId.value = id
  errorMessage.value = null

  try {
    await deleteSocialMedia(id)
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to delete social link.'
  } finally {
    deletingId.value = null
  }
}
</script>
