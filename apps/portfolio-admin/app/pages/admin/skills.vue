<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7] tracking-tight">Skills &amp; Expertise Management</h1>
        <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-1">Manage skill categories, Lucide icons, and bullet list items displayed on the public portfolio.</p>
      </div>
      <AppButton @click="openCreateModal">
        <Plus class="h-4 w-4 mr-1.5" :stroke-width="2" />
        Add Category
      </AppButton>
    </div>

    <FormError :message="errorMessage" />

    <!-- Success alert -->
    <div v-if="successMessage" class="p-4 rounded-card bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 text-sm font-semibold flex items-center justify-between">
      <span>{{ successMessage }}</span>
      <button @click="successMessage = null" class="text-emerald-500/70 hover:text-emerald-500">✕</button>
    </div>

    <!-- Loading State -->
    <AppCard v-if="status === 'pending'" class="text-center py-16">
      <div class="animate-spin w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full mx-auto" />
      <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-3">Loading skill categories...</p>
    </AppCard>

    <!-- Error State -->
    <AppCard v-else-if="status === 'error'" class="text-center py-16">
      <p class="text-text-secondary dark:text-[#8E8E93] mb-4">Failed to load skill categories.</p>
      <AppButton variant="secondary" @click="refresh()">Retry Connection</AppButton>
    </AppCard>

    <!-- Categories Grid -->
    <div v-else-if="sortedCategories.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <AppCard
        v-for="(cat, idx) in sortedCategories"
        :key="cat.id"
        padded
        class="flex flex-col justify-between space-y-4"
      >
        <div>
          <!-- Category Header -->
          <div class="flex items-center justify-between mb-4 pb-3 border-b border-border dark:border-white/8">
            <div class="flex items-center gap-3">
              <div class="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center text-primary flex-shrink-0">
                <component :is="resolveIcon(cat.icon_name)" class="w-5 h-5" :stroke-width="1.75" />
              </div>
              <div>
                <h3 class="text-base font-bold text-text-primary dark:text-[#F2F2F7]">{{ cat.name }}</h3>
                <span class="text-xs font-semibold text-text-secondary dark:text-[#8E8E93]">Icon: {{ cat.icon_name }}</span>
              </div>
            </div>
            <div class="inline-flex items-center gap-1 bg-primary/10 text-primary px-2.5 py-1 rounded-full text-xs font-bold">
              {{ cat.items.length }} {{ cat.items.length === 1 ? 'item' : 'items' }}
            </div>
          </div>

          <!-- Bullet Items -->
          <ul class="space-y-2">
            <li
              v-for="item in cat.items"
              :key="item"
              class="flex items-center gap-2.5 text-sm font-medium text-text-secondary dark:text-[#8E8E93]"
            >
              <span class="w-1.5 h-1.5 bg-primary rounded-full flex-shrink-0" />
              <span>{{ item }}</span>
            </li>
          </ul>
        </div>

        <!-- Action Controls -->
        <div class="pt-4 border-t border-border dark:border-white/8 flex items-center justify-between">
          <!-- Reorder Buttons -->
          <div class="flex items-center gap-1">
            <button
              type="button"
              class="p-1.5 rounded-full hover:bg-black/5 dark:hover:bg-white/5 text-text-secondary dark:text-[#8E8E93] disabled:opacity-30 cursor-pointer"
              :disabled="idx === 0 || reordering"
              @click="moveCategory(cat, -1)"
              title="Move Up"
            >
              <ArrowUp class="w-4 h-4" :stroke-width="2" />
            </button>
            <button
              type="button"
              class="p-1.5 rounded-full hover:bg-black/5 dark:hover:bg-white/5 text-text-secondary dark:text-[#8E8E93] disabled:opacity-30 cursor-pointer"
              :disabled="idx === sortedCategories.length - 1 || reordering"
              @click="moveCategory(cat, 1)"
              title="Move Down"
            >
              <ArrowDown class="w-4 h-4" :stroke-width="2" />
            </button>
          </div>

          <!-- Edit / Delete Buttons -->
          <div class="flex items-center gap-2">
            <AppButton size="sm" variant="secondary" @click="openEditModal(cat)">
              <Edit2 class="w-3.5 h-3.5 mr-1" :stroke-width="1.75" />
              Edit
            </AppButton>
            <AppButton size="sm" variant="outline" class="text-rose-500 border-rose-500/30 hover:bg-rose-500/10" @click="openDeleteDialog(cat)">
              <Trash2 class="w-3.5 h-3.5 mr-1" :stroke-width="1.75" />
              Delete
            </AppButton>
          </div>
        </div>
      </AppCard>
    </div>

    <!-- Empty State -->
    <AppCard v-else class="text-center py-16">
      <p class="text-text-secondary dark:text-[#8E8E93] mb-4">No skill categories found.</p>
      <AppButton @click="openCreateModal">Add First Category</AppButton>
    </AppCard>

    <!-- Create / Edit Modal -->
    <div v-if="showModal" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-2xl max-w-lg w-full max-h-[90vh] overflow-y-auto p-6 space-y-6 shadow-2xl">
        <div class="flex items-center justify-between">
          <h3 class="text-lg font-bold text-text-primary dark:text-[#F2F2F7]">
            {{ editingCategory ? 'Edit Skill Category' : 'Add New Skill Category' }}
          </h3>
          <button @click="closeModal" class="text-text-secondary dark:text-[#8E8E93] hover:text-text-primary dark:hover:text-[#F2F2F7]">✕</button>
        </div>

        <form @submit.prevent="handleSaveCategory" class="space-y-5">
          <!-- Category Name -->
          <AppInput
            id="category-name"
            v-model="formName"
            label="Category Name"
            placeholder="e.g. Backend Development"
            required
          />

          <!-- Icon Selector -->
          <div>
            <label class="block text-sm font-semibold text-text-primary dark:text-[#F2F2F7] mb-2">Lucide Icon</label>
            <div class="grid grid-cols-5 gap-2 mb-3">
              <button
                v-for="icon in presetIcons"
                :key="icon"
                type="button"
                class="p-2.5 rounded-2xl border flex flex-col items-center justify-center gap-1 transition-all cursor-pointer"
                :class="formIconName === icon ? 'bg-primary/10 border-primary text-primary font-bold' : 'bg-background dark:bg-black border-border dark:border-white/10 text-text-secondary hover:text-text-primary'"
                @click="formIconName = icon"
              >
                <component :is="resolveIcon(icon)" class="w-5 h-5" :stroke-width="1.75" />
                <span class="text-[10px] truncate max-w-full">{{ icon }}</span>
              </button>
            </div>
            <AppInput
              id="custom-icon-name"
              v-model="formIconName"
              label="Or Type Lucide Icon Name"
              placeholder="Server"
              required
            />
          </div>

          <!-- Bullet Items Editor -->
          <div>
            <label class="block text-sm font-semibold text-text-primary dark:text-[#F2F2F7] mb-1">
              Bullet Items ({{ formItems.length }})
            </label>
            <p class="text-xs text-text-secondary dark:text-[#8E8E93] mb-3">Add bullet points displayed inside this category card.</p>

            <!-- Input to add item -->
            <div class="flex items-center gap-2 mb-3">
              <AppInput
                id="new-item-input"
                v-model="newItemInput"
                placeholder="e.g. FastAPI (Python)"
                class="flex-1"
                @keyup.enter.prevent="addBulletItem"
              />
              <AppButton type="button" size="sm" variant="secondary" @click="addBulletItem">
                Add Item
              </AppButton>
            </div>

            <!-- Bullet List -->
            <div v-if="formItems.length > 0" class="space-y-2 max-h-48 overflow-y-auto pr-1">
              <div
                v-for="(item, idx) in formItems"
                :key="idx"
                class="flex items-center justify-between p-2.5 rounded-xl bg-background dark:bg-black border border-border dark:border-white/10 text-sm font-medium"
              >
                <span class="text-text-primary dark:text-[#F2F2F7] flex-1 truncate mr-2">• {{ item }}</span>
                <div class="flex items-center gap-1">
                  <button
                    type="button"
                    class="p-1 text-text-secondary hover:text-text-primary disabled:opacity-30"
                    :disabled="idx === 0"
                    @click="moveBulletItem(idx, -1)"
                  >
                    ▲
                  </button>
                  <button
                    type="button"
                    class="p-1 text-text-secondary hover:text-text-primary disabled:opacity-30"
                    :disabled="idx === formItems.length - 1"
                    @click="moveBulletItem(idx, 1)"
                  >
                    ▼
                  </button>
                  <button
                    type="button"
                    class="p-1 text-rose-500 hover:text-rose-600 ml-1"
                    @click="removeBulletItem(idx)"
                  >
                    ✕
                  </button>
                </div>
              </div>
            </div>
            <p v-else class="text-xs text-text-secondary italic">No bullet items added yet.</p>
          </div>

          <div class="flex justify-end gap-3 pt-3 border-t border-border dark:border-white/8">
            <AppButton type="button" variant="secondary" @click="closeModal">Cancel</AppButton>
            <AppButton type="submit" :loading="saving">
              {{ editingCategory ? 'Save Changes' : 'Create Category' }}
            </AppButton>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Dialog -->
    <div v-if="deletingCategory" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-2xl max-w-sm w-full p-6 space-y-4 shadow-2xl">
        <h3 class="text-lg font-bold text-text-primary dark:text-[#F2F2F7]">Delete Category?</h3>
        <p class="text-sm text-text-secondary dark:text-[#8E8E93]">
          Are you sure you want to delete <strong class="text-text-primary dark:text-[#F2F2F7]">{{ deletingCategory.name }}</strong>? This action cannot be undone.
        </p>
        <div class="flex justify-end gap-3 pt-2">
          <AppButton variant="secondary" @click="deletingCategory = null">Cancel</AppButton>
          <AppButton variant="outline" class="text-rose-500 border-rose-500/30 hover:bg-rose-500/10" :loading="deleting" @click="confirmDelete">
            Delete
          </AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Plus, Edit2, Trash2, ArrowUp, ArrowDown } from 'lucide-vue-next'
import * as LucideIcons from 'lucide-vue-next'
import type { SkillCategory } from '~/types/skillCategory'

definePageMeta({
  layout: 'admin',
})

useHead({ title: 'Skills — Admin' })

const { categories, status, refresh, createCategory, updateCategory, deleteCategory } = useAdminSkillCategories()

const presetIcons = ['Server', 'LayoutGrid', 'Smartphone', 'Database', 'Code', 'Terminal', 'Cpu', 'Layers', 'Globe', 'Shield']

const sortedCategories = computed(() => {
  if (!categories.value) return []
  return [...categories.value].sort((a, b) => a.display_order - b.display_order)
})

const showModal = ref(false)
const editingCategory = ref<SkillCategory | null>(null)
const deletingCategory = ref<SkillCategory | null>(null)

const formName = ref('')
const formIconName = ref('Server')
const formItems = ref<string[]>([])
const newItemInput = ref('')

const saving = ref(false)
const deleting = ref(false)
const reordering = ref(false)
const errorMessage = ref<string | null>(null)
const successMessage = ref<string | null>(null)

function resolveIcon(name: string) {
  const icon = (LucideIcons as Record<string, any>)[name]
  if (icon) return icon
  if (name === 'LayoutGrid') return LucideIcons.LayoutGrid || LucideIcons.LayoutDashboard
  return LucideIcons.Folder
}

function openCreateModal() {
  editingCategory.value = null
  formName.value = ''
  formIconName.value = 'Server'
  formItems.value = []
  newItemInput.value = ''
  showModal.value = true
}

function openEditModal(cat: SkillCategory) {
  editingCategory.value = cat
  formName.value = cat.name
  formIconName.value = cat.icon_name
  formItems.value = [...(cat.items || [])]
  newItemInput.value = ''
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  editingCategory.value = null
}

function addBulletItem() {
  const val = newItemInput.value.trim()
  if (!val) return
  formItems.value.push(val)
  newItemInput.value = ''
}

function removeBulletItem(idx: number) {
  formItems.value.splice(idx, 1)
}

function moveBulletItem(idx: number, delta: number) {
  const targetIdx = idx + delta
  if (targetIdx < 0 || targetIdx >= formItems.value.length) return
  const temp = formItems.value[idx]
  formItems.value[idx] = formItems.value[targetIdx]
  formItems.value[targetIdx] = temp
}

async function handleSaveCategory() {
  errorMessage.value = null
  successMessage.value = null
  saving.value = true

  try {
    if (editingCategory.value) {
      await updateCategory(editingCategory.value.id, {
        name: formName.value.trim(),
        icon_name: formIconName.value.trim(),
        items: formItems.value,
      })
      successMessage.value = 'Skill category updated successfully.'
    } else {
      const nextOrder = (sortedCategories.value.length > 0 ? Math.max(...sortedCategories.value.map(c => c.display_order)) : 0) + 1
      await createCategory({
        name: formName.value.trim(),
        icon_name: formIconName.value.trim(),
        items: formItems.value,
        display_order: nextOrder,
      })
      successMessage.value = 'Skill category created successfully.'
    }
    closeModal()
    await refresh()
  } catch (err: any) {
    errorMessage.value = err.data?.detail || err.message || 'Failed to save skill category.'
  } finally {
    saving.value = false
  }
}

function openDeleteDialog(cat: SkillCategory) {
  deletingCategory.value = cat
}

async function confirmDelete() {
  if (!deletingCategory.value) return
  errorMessage.value = null
  deleting.value = true
  try {
    await deleteCategory(deletingCategory.value.id)
    successMessage.value = `Skill category "${deletingCategory.value.name}" deleted.`
    deletingCategory.value = null
    await refresh()
  } catch (err: any) {
    errorMessage.value = err.data?.detail || err.message || 'Failed to delete category.'
  } finally {
    deleting.value = false
  }
}

async function moveCategory(cat: SkillCategory, delta: number) {
  const currentIdx = sortedCategories.value.findIndex(c => c.id === cat.id)
  const targetIdx = currentIdx + delta
  if (targetIdx < 0 || targetIdx >= sortedCategories.value.length) return

  const targetCat = sortedCategories.value[targetIdx]
  reordering.value = true

  try {
    await Promise.all([
      updateCategory(cat.id, { display_order: targetCat.display_order }),
      updateCategory(targetCat.id, { display_order: cat.display_order }),
    ])
    await refresh()
  } catch (err: any) {
    errorMessage.value = 'Failed to reorder categories.'
  } finally {
    reordering.value = false
  }
}
</script>
