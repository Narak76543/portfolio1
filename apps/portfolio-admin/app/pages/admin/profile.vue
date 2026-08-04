<template>
  <div>
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7]">Profile Settings</h1>
      <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-1">Manage your public profile information</p>
    </div>

    <FormError :message="errorMessage" />
    <div v-if="successMessage" class="mb-6 p-4 bg-green-500/10 text-green-600 dark:text-green-400 rounded-card border border-green-500/20 text-sm font-medium">
      {{ successMessage }}
    </div>

    <!-- Loading state -->
    <AppCard v-if="status === 'pending'" class="text-center py-12">
      <div class="animate-spin w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full mx-auto" />
      <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-3">Loading profile...</p>
    </AppCard>

    <!-- Content -->
    <div v-else class="w-full space-y-6">
      <!-- Hero Heading & Pitch Settings -->
      <AppCard padded>
        <h2 class="text-lg font-bold text-text-primary dark:text-[#F2F2F7] mb-1">Hero Heading &amp; Pitch</h2>
        <p class="text-xs text-text-secondary dark:text-[#8E8E93] mb-4">Customize the primary name display (split into default and accent color words) and your hero pitch line.</p>

        <form @submit.prevent="handleSaveHero" class="space-y-4">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <AppInput
              id="hero-first-name"
              v-model="firstNameInput"
              label="First Name (Default Color)"
              placeholder="Sarat"
              required
            />

            <AppInput
              id="hero-last-name"
              v-model="lastNameInput"
              label="Last Name (Accent Blue)"
              placeholder="Narak"
              required
            />
          </div>

          <div>
            <label for="hero-pitch" class="block text-sm font-semibold text-text-primary dark:text-[#F2F2F7] mb-1">Hero Pitch Line</label>
            <textarea
              id="hero-pitch"
              v-model="heroPitchInput"
              rows="2"
              class="w-full px-4 py-2.5 rounded-2xl bg-background dark:bg-black border border-border dark:border-white/10 text-text-primary dark:text-[#F2F2F7] placeholder:text-text-secondary focus:outline-none focus:border-primary transition-colors text-sm font-medium"
              placeholder="I build backend APIs, mobile apps, and web dashboards..."
              required
            />
          </div>

          <!-- Live Preview Box -->
          <div class="p-4 rounded-2xl bg-background dark:bg-black border border-border dark:border-white/10 space-y-2">
            <p class="text-xs font-bold text-text-secondary dark:text-[#8E8E93] uppercase tracking-wider mb-2">Live Hero Heading Preview</p>
            <h1
              class="text-2xl md:text-4xl font-extrabold text-text-primary dark:text-[#F2F2F7] tracking-tight uppercase"
              :style="profile?.heading_font_name ? { fontFamily: `'${profile.heading_font_name}', 'Onest', sans-serif` } : {}"
            >
              {{ firstNameInput || 'SARAT' }} <span class="text-primary">{{ lastNameInput || 'NARAK' }}</span>
            </h1>
            <p class="text-xs md:text-sm text-text-secondary dark:text-[#8E8E93] font-medium">
              {{ heroPitchInput || 'I build backend APIs, mobile apps, and web dashboards — and this site is one of my projects too.' }}
            </p>
          </div>

          <div class="flex justify-end">
            <AppButton type="submit" :loading="savingHero">
              Save Hero Settings
            </AppButton>
          </div>
        </form>
      </AppCard>

      <!-- Navbar Brand Logo Settings -->
      <AppCard padded>
        <h2 class="text-lg font-bold text-text-primary dark:text-[#F2F2F7] mb-1">Header Brand Logo</h2>
        <p class="text-xs text-text-secondary dark:text-[#8E8E93] mb-4">Choose whether your header logo is rendered as customized text or an uploaded image logo.</p>

        <form @submit.prevent="handleSaveLogo" class="space-y-4">
          <!-- Logo Type Selector -->
          <div>
            <label class="block text-sm font-semibold text-text-primary dark:text-[#F2F2F7] mb-2">Logo Type</label>
            <div class="grid grid-cols-2 gap-3">
              <button
                type="button"
                class="px-4 py-2.5 rounded-full border text-sm font-semibold transition-all cursor-pointer flex items-center justify-center gap-2"
                :class="logoTypeInput === 'text' ? 'bg-primary/10 border-primary text-primary' : 'bg-surface dark:bg-[#1C1C1E] border-border dark:border-white/10 text-text-secondary dark:text-[#8E8E93]'"
                @click="logoTypeInput = 'text'"
              >
                <Type class="w-4 h-4" :stroke-width="1.75" />
                <span>Text Logo</span>
              </button>

              <button
                type="button"
                class="px-4 py-2.5 rounded-full border text-sm font-semibold transition-all cursor-pointer flex items-center justify-center gap-2"
                :class="logoTypeInput === 'image' ? 'bg-primary/10 border-primary text-primary' : 'bg-surface dark:bg-[#1C1C1E] border-border dark:border-white/10 text-text-secondary dark:text-[#8E8E93]'"
                @click="logoTypeInput = 'image'"
              >
                <ImageIcon class="w-4 h-4" :stroke-width="1.75" />
                <span>Image Logo</span>
              </button>
            </div>
          </div>

          <!-- Text Mode Input -->
          <div v-if="logoTypeInput === 'text'">
            <AppInput
              id="profile-logo-text"
              v-model="logoTextInput"
              label="Logo Text"
              placeholder="SARAT NARAK"
              required
            />
          </div>

          <!-- Image Mode Upload -->
          <div v-else class="space-y-3">
            <label class="block text-sm font-semibold text-text-primary dark:text-[#F2F2F7] mb-1">Logo Image File</label>
            <div class="flex items-center gap-4">
              <div class="h-12 px-4 bg-background dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-card flex items-center justify-center overflow-hidden">
                <img v-if="profile?.logo_image_url" :src="profile.logo_image_url" alt="Logo Preview" class="h-8 w-auto object-contain" />
                <span v-else class="text-xs text-text-secondary dark:text-[#8E8E93]">No Image Uploaded</span>
              </div>
              <div class="flex-1">
                <label
                  for="logo-file-input"
                  class="inline-flex items-center px-4 py-1.5 bg-primary/10 text-primary border border-primary/20 rounded-full text-xs font-semibold hover:bg-primary/20 transition-colors cursor-pointer"
                >
                  {{ uploadingLogo ? 'Uploading...' : 'Choose Logo Image (SVG/PNG)' }}
                </label>
                <input
                  id="logo-file-input"
                  type="file"
                  accept="image/svg+xml, image/png, image/jpeg, image/webp"
                  class="hidden"
                  :disabled="uploadingLogo"
                  @change="handleLogoUpload"
                />
              </div>
            </div>
          </div>

          <!-- Live Logo Preview Box -->
          <div>
            <label class="block text-xs font-semibold uppercase tracking-wider text-text-secondary dark:text-[#8E8E93] mb-2">Header Navbar Live Preview</label>
            <div class="p-4 bg-background dark:bg-black border border-border dark:border-white/10 rounded-card flex items-center justify-between">
              <div>
                <img v-if="logoTypeInput === 'image' && profile?.logo_image_url" :src="profile.logo_image_url" alt="Brand Logo" class="h-7 w-auto object-contain" />
                <span v-else class="text-lg font-bold text-primary tracking-tight">
                  {{ logoTextInput || 'SARAT NARAK' }}
                </span>
              </div>
              <div class="flex gap-4 text-xs text-text-secondary dark:text-[#8E8E93] font-medium">
                <span>Projects</span>
                <span>About</span>
                <span>Contact</span>
              </div>
            </div>
          </div>

          <div class="pt-2 flex justify-end">
            <AppButton type="submit" :loading="savingLogo">
              Save Logo Settings
            </AppButton>
          </div>
        </form>
      </AppCard>

      <!-- About Section Content Settings -->
      <AppCard padded>
        <h2 class="text-lg font-bold text-text-primary dark:text-[#F2F2F7] mb-1">About Section Content</h2>
        <p class="text-xs text-text-secondary dark:text-[#8E8E93] mb-4">Customize the section heading, subheading, and multi-paragraph biography displayed in the public About Me section.</p>

        <form @submit.prevent="handleSaveAbout" class="space-y-4">
          <AppInput
            id="about-heading"
            v-model="aboutHeadingInput"
            label="Section Eyebrow Heading"
            placeholder="ABOUT ME"
            required
          />

          <AppInput
            id="about-subheading"
            v-model="aboutSubheadingInput"
            label="Main Subheading"
            placeholder="PASSIONATE ABOUT BUILDING BACKENDS & MOBILE APPS"
            required
          />

          <div>
            <label for="about-bio" class="block text-sm font-semibold text-text-primary dark:text-[#F2F2F7] mb-1.5">
              Biography Paragraphs
            </label>
            <textarea
              id="about-bio"
              v-model="aboutBioInput"
              rows="6"
              class="w-full px-4 py-2.5 bg-background dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-card text-sm text-text-primary dark:text-[#F2F2F7] placeholder-text-secondary dark:placeholder-[#8E8E93] focus:outline-none focus:ring-2 focus:ring-primary/25 focus:border-primary transition-all"
              placeholder="Separate paragraphs using a blank line (double newline)..."
              required
            />
            <p class="text-xs text-text-secondary dark:text-[#8E8E93] mt-1">Separate paragraphs with a blank line (\n\n).</p>
          </div>

          <div class="pt-2 flex justify-end">
            <AppButton type="submit" :loading="savingAbout">
              Save About Section
            </AppButton>
          </div>
        </form>
      </AppCard>

      <!-- Custom Heading Font Settings -->
      <AppCard padded>
        <div class="flex items-center justify-between mb-1">
          <h2 class="text-lg font-bold text-text-primary dark:text-[#F2F2F7]">Heading Custom Font</h2>
          <div class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold" :class="profile?.heading_font_name ? 'bg-emerald-500/10 text-emerald-500 border border-emerald-500/20' : 'bg-primary/10 text-text-secondary dark:text-[#8E8E93]'">
            <span class="w-1.5 h-1.5 rounded-full" :class="profile?.heading_font_name ? 'bg-emerald-500' : 'bg-primary'" />
            <span>{{ profile?.heading_font_name ? `Custom: ${profile.heading_font_name}` : 'Default (Onest)' }}</span>
          </div>
        </div>
        <p class="text-xs text-text-secondary dark:text-[#8E8E93] mb-5">
          Upload a custom font file (.woff2, .woff, or .ttf) to apply strictly to your name and major heading text. Body text remains clean Onest font.
        </p>

        <form @submit.prevent="handleFontUpload" class="space-y-4">
          <!-- Font File Upload Input -->
          <div>
            <label class="block text-sm font-semibold text-text-primary dark:text-[#F2F2F7] mb-1.5">
              Custom Font File (.woff2, .woff, .ttf)
            </label>
            <div class="flex items-center gap-3">
              <label
                for="heading-font-file-input"
                class="inline-flex items-center gap-2 px-4 py-2 bg-primary/10 text-primary border border-primary/20 rounded-full text-xs font-bold hover:bg-primary/20 transition-colors cursor-pointer"
              >
                <UploadCloud class="w-4 h-4" :stroke-width="1.75" />
                <span>{{ selectedFontFile ? selectedFontFile.name : 'Choose Font File' }}</span>
              </label>
              <input
                id="heading-font-file-input"
                type="file"
                accept=".woff2, .woff, .ttf"
                class="hidden"
                :disabled="uploadingFont"
                @change="handleFontFileChange"
              />
              <span v-if="selectedFontFile" class="text-xs font-medium text-emerald-600 dark:text-emerald-400">
                Ready to upload ({{ (selectedFontFile.size / 1024).toFixed(1) }} KB)
              </span>
            </div>
          </div>

          <!-- Font Display Name Input -->
          <div>
            <AppInput
              id="font-display-name"
              v-model="fontFamilyNameInput"
              label="Font Family Display Name"
              placeholder="e.g. CustomHeadingFont"
              help-text="The CSS font-family name registered for your uploaded font."
            />
          </div>

          <!-- Live Font Preview Box -->
          <div>
            <label class="block text-xs font-semibold uppercase tracking-wider text-text-secondary dark:text-[#8E8E93] mb-2">
              Heading Font Live Preview
            </label>
            <div class="p-5 bg-background dark:bg-black border border-border dark:border-white/10 rounded-card space-y-2">
              <p class="text-xs text-text-secondary dark:text-[#8E8E93] font-mono">Font Family: {{ previewFontFamily }}</p>
              <h1
                class="text-3xl md:text-4xl font-extrabold text-text-primary dark:text-[#F2F2F7] tracking-tight uppercase transition-all"
                :style="{ fontFamily: previewFontFamily }"
              >
                {{ profile?.logo_text || 'SARAT NARAK' }}
              </h1>
              <p class="text-xs text-text-secondary dark:text-[#8E8E93] font-medium">
                The quick brown fox jumps over the lazy dog • 0123456789
              </p>
            </div>
          </div>

          <!-- Action Buttons -->
          <div class="pt-2 flex items-center justify-between gap-3 flex-wrap">
            <AppButton
              v-if="profile?.heading_font_url"
              type="button"
              variant="secondary"
              :loading="resettingFont"
              @click="handleResetFont"
            >
              <RotateCcw class="w-4 h-4 mr-1.5" :stroke-width="1.75" />
              Reset to Default (Onest)
            </AppButton>
            <div v-else />

            <AppButton type="submit" :loading="uploadingFont" :disabled="!selectedFontFile && !fontFamilyNameInputChanged">
              Save Custom Font
            </AppButton>
          </div>
        </form>
      </AppCard>

      <!-- Avatar Settings -->
      <AppCard padded>
        <h2 class="text-lg font-bold text-text-primary dark:text-[#F2F2F7] mb-4">Avatar</h2>
        
        <div class="flex items-center gap-8">
          <div class="w-32 h-32 rounded-card border border-border dark:border-white/10 bg-background dark:bg-black overflow-hidden flex-shrink-0 flex items-center justify-center">
            <img 
              v-if="profile?.avatar_url" 
              :src="profile.avatar_url" 
              alt="Avatar" 
              class="w-full h-full object-cover" 
            />
            <div v-else class="text-text-secondary dark:text-[#8E8E93]">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
          </div>

          <div class="flex-1 space-y-4">
            <p class="text-sm text-text-secondary dark:text-[#8E8E93]">
              Upload a new profile picture. Allowed formats: JPEG, PNG, WebP. Max size: 5MB.
            </p>
            
            <input
              type="file"
              accept="image/jpeg, image/png, image/webp"
              class="block w-full text-sm text-text-secondary dark:text-[#8E8E93] file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-primary/10 file:text-primary hover:file:bg-primary/20 cursor-pointer"
              @change="handleFileChange"
              :disabled="uploading"
            />
            
            <AppButton
              @click="handleUpload"
              :loading="uploading"
              :disabled="!selectedFile"
            >
              Upload Avatar
            </AppButton>
          </div>
        </div>
      </AppCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Type, Image as ImageIcon, UploadCloud, RotateCcw } from 'lucide-vue-next'

definePageMeta({
  layout: 'admin',
})

useHead({ title: 'Profile — Admin' })

const { profile, status, refresh, uploadAvatar, uploadLogo, uploadFont, updateProfile } = useAdminProfile()

const firstNameInput = ref('Sarat')
const lastNameInput = ref('Narak')
const heroPitchInput = ref('')
const savingHero = ref(false)

const logoTypeInput = ref<'text' | 'image'>('text')
const logoTextInput = ref('')
const savingLogo = ref(false)
const uploadingLogo = ref(false)

const taglineInput = ref('')
const savingTagline = ref(false)

const aboutHeadingInput = ref('')
const aboutSubheadingInput = ref('')
const aboutBioInput = ref('')
const savingAbout = ref(false)

const selectedFontFile = ref<File | null>(null)
const fontFamilyNameInput = ref('')
const previewFontUrl = ref<string | null>(null)
const uploadingFont = ref(false)
const resettingFont = ref(false)

const selectedFile = ref<File | null>(null)
const uploading = ref(false)
const errorMessage = ref<string | null>(null)
const successMessage = ref<string | null>(null)

const fontFamilyNameInputChanged = computed(() => {
  return (
    !!profile.value?.heading_font_url &&
    fontFamilyNameInput.value.trim() !== (profile.value?.heading_font_name || '')
  )
})

const previewFontFamily = computed(() => {
  if (fontFamilyNameInput.value.trim()) return fontFamilyNameInput.value.trim()
  if (profile.value?.heading_font_name) return profile.value.heading_font_name
  return 'Onest, sans-serif'
})

useHead(() => {
  const url = previewFontUrl.value || profile.value?.heading_font_url
  const name = previewFontFamily.value
  if (!url || !name || name.includes('Onest')) return {}
  return {
    style: [
      {
        id: 'admin-heading-font-preview',
        innerHTML: `@font-face { font-family: '${name}'; src: url('${url}'); font-display: swap; }`,
      },
    ],
  }
})

watch(
  () => profile.value,
  (p) => {
    if (p) {
      if (p.first_name) firstNameInput.value = p.first_name
      if (p.last_name) lastNameInput.value = p.last_name
      if (p.hero_pitch) heroPitchInput.value = p.hero_pitch
      if (p.logo_type) logoTypeInput.value = p.logo_type as 'text' | 'image'
      if (p.logo_text) logoTextInput.value = p.logo_text
      if (p.tagline) taglineInput.value = p.tagline
      if (p.about_heading) aboutHeadingInput.value = p.about_heading
      if (p.about_subheading) aboutSubheadingInput.value = p.about_subheading
      if (p.about_bio) aboutBioInput.value = p.about_bio
      if (p.heading_font_name) fontFamilyNameInput.value = p.heading_font_name
    }
  },
  { immediate: true },
)

async function handleSaveHero() {
  errorMessage.value = null
  successMessage.value = null
  savingHero.value = true

  try {
    await updateProfile({
      first_name: firstNameInput.value.trim(),
      last_name: lastNameInput.value.trim(),
      hero_pitch: heroPitchInput.value.trim(),
    })
    await refresh()
    successMessage.value = 'Hero heading and pitch saved successfully.'
  } catch (err: any) {
    errorMessage.value = err.data?.detail || err.message || 'Failed to save Hero settings.'
  } finally {
    savingHero.value = false
  }
}

function handleFontFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    selectedFontFile.value = file
    previewFontUrl.value = URL.createObjectURL(file)
    if (!fontFamilyNameInput.value.trim()) {
      const nameWithoutExt = file.name.substring(0, file.name.lastIndexOf('.')) || file.name
      fontFamilyNameInput.value = nameWithoutExt.replace(/[-_]/g, ' ')
    }
  }
}

async function handleFontUpload() {
  uploadingFont.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    if (selectedFontFile.value) {
      await uploadFont(selectedFontFile.value, fontFamilyNameInput.value.trim() || undefined)
      successMessage.value = 'Heading font file uploaded and applied successfully.'
      selectedFontFile.value = null
    } else if (fontFamilyNameInputChanged.value) {
      await updateProfile({
        heading_font_name: fontFamilyNameInput.value.trim(),
      })
      successMessage.value = 'Heading font display name updated successfully.'
    }
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to update heading font.'
  } finally {
    uploadingFont.value = false
  }
}

async function handleResetFont() {
  resettingFont.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    await updateProfile({
      heading_font_url: null,
      heading_font_name: null,
    })
    fontFamilyNameInput.value = ''
    selectedFontFile.value = null
    previewFontUrl.value = null
    successMessage.value = 'Reverted to default Onest font.'
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to reset heading font.'
  } finally {
    resettingFont.value = false
  }
}

async function handleSaveLogo() {
  savingLogo.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    await updateProfile({
      logo_type: logoTypeInput.value,
      logo_text: logoTextInput.value.trim(),
    })
    successMessage.value = 'Logo settings updated successfully.'
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to update logo settings.'
  } finally {
    savingLogo.value = false
  }
}

async function handleLogoUpload(event: Event) {
  const input = event.target as HTMLInputElement
  const file = input.files?.[0]
  if (!file) return

  uploadingLogo.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    await uploadLogo(file)
    logoTypeInput.value = 'image'
    successMessage.value = 'Logo image uploaded successfully.'
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to upload logo image.'
  } finally {
    uploadingLogo.value = false
  }
}

async function handleSaveTagline() {
  if (!taglineInput.value.trim()) return

  savingTagline.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    await updateProfile({ tagline: taglineInput.value.trim() })
    successMessage.value = 'Tagline updated successfully.'
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to update tagline.'
  } finally {
    savingTagline.value = false
  }
}

async function handleSaveAbout() {
  savingAbout.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    await updateProfile({
      about_heading: aboutHeadingInput.value.trim(),
      about_subheading: aboutSubheadingInput.value.trim(),
      about_bio: aboutBioInput.value.trim(),
    })
    successMessage.value = 'About section content updated successfully.'
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to update About section.'
  } finally {
    savingAbout.value = false
  }
}

function handleFileChange(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0]
    errorMessage.value = null
    successMessage.value = null
  }
}

async function handleUpload() {
  if (!selectedFile.value) return

  uploading.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    await uploadAvatar(selectedFile.value)
    successMessage.value = 'Avatar uploaded successfully.'
    selectedFile.value = null
    // Reset file input
    const fileInput = document.querySelector('input[type="file"]') as HTMLInputElement
    if (fileInput) fileInput.value = ''
    await refresh()
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Failed to upload avatar.'
  } finally {
    uploading.value = false
  }
}
</script>
