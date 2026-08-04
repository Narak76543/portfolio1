<template>
  <div class="min-h-screen flex items-center justify-center bg-background dark:bg-black px-4 transition-colors">
    <div class="w-full max-w-md space-y-6">
      <!-- Header -->
      <div class="text-center">
        <h1 class="text-2xl font-extrabold text-text-primary dark:text-[#F2F2F7] tracking-wider uppercase inline-flex items-center">
          <span>SARAT</span>
          <span class="text-text-secondary dark:text-[#8E8E93] font-bold ml-1.5">NARAK</span>
          <span class="w-1.5 h-1.5 rounded-full bg-primary ml-1" />
        </h1>
        <p class="text-xs text-text-secondary dark:text-[#8E8E93] font-medium mt-1">Admin Panel Security</p>
      </div>

      <AppCard padded class="space-y-5">
        <!-- Auth Mode Selector Pills (If Hosted) -->
        <div v-if="isHosted" class="grid grid-cols-2 gap-2 p-1 bg-background dark:bg-black rounded-full border border-border dark:border-white/10">
          <button
            type="button"
            class="py-2 px-3 rounded-full text-xs font-bold transition-all cursor-pointer flex items-center justify-center gap-2"
            :class="mode === 'password' ? 'bg-surface dark:bg-[#1C1C1E] text-primary shadow-sm border border-border dark:border-white/10' : 'text-text-secondary hover:text-text-primary'"
            @click="switchMode('password')"
          >
            <KeyRound class="w-4 h-4" :stroke-width="1.75" />
            <span>Password</span>
          </button>

          <button
            type="button"
            class="py-2 px-3 rounded-full text-xs font-bold transition-all cursor-pointer flex items-center justify-center gap-2"
            :class="mode === 'qr' ? 'bg-surface dark:bg-[#1C1C1E] text-primary shadow-sm border border-border dark:border-white/10' : 'text-text-secondary hover:text-text-primary'"
            @click="switchMode('qr')"
          >
            <QrCode class="w-4 h-4" :stroke-width="1.75" />
            <span>QR Code Login</span>
          </button>
        </div>

        <FormError :message="errorMessage" />

        <!-- 1. Password Mode (Always available, default in local dev) -->
        <form v-if="mode === 'password'" @submit.prevent="handlePasswordLogin" class="space-y-4">
          <AppInput
            id="login-email"
            v-model="email"
            label="Email"
            type="email"
            placeholder="admin@example.com"
            required
            :disabled="loading"
          />

          <AppInput
            id="login-password"
            v-model="password"
            label="Password"
            type="password"
            placeholder="••••••••"
            required
            :disabled="loading"
          />

          <AppButton type="submit" :loading="loading" class="w-full">
            Sign In with Password
          </AppButton>

          <!-- Local Dev Badge Note -->
          <div v-if="!isHosted" class="pt-2 text-center">
            <div class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/10 text-[11px] font-medium text-text-secondary dark:text-[#8E8E93]">
              <QrCode class="w-3.5 h-3.5 text-primary" :stroke-width="1.75" />
              <span>QR Code Login available once hosted (set PUBLIC_APP_URL)</span>
            </div>
          </div>
        </form>

        <!-- 2. QR Code Mode (Only available when hosted with PUBLIC_APP_URL) -->
        <div v-else-if="isHosted && mode === 'qr'" class="text-center space-y-4 py-2">
          <div v-if="qrLoading" class="py-12 space-y-3">
            <div class="animate-spin w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full mx-auto" />
            <p class="text-xs text-text-secondary">Generating secure QR code...</p>
          </div>

          <div v-else-if="qrDataUrl" class="space-y-4">
            <!-- QR Canvas Wrapper -->
            <div class="relative w-56 h-56 mx-auto p-3 bg-white rounded-2xl shadow-md border-2 border-primary/30 flex items-center justify-center">
              <img :src="qrDataUrl" alt="Scan QR Code" class="w-full h-full object-contain" />
              <!-- Status overlay if expired -->
              <div v-if="qrExpired" class="absolute inset-0 bg-black/80 rounded-2xl backdrop-blur-sm flex flex-col items-center justify-center p-4 text-white space-y-2">
                <span class="text-xs font-bold uppercase tracking-wider text-rose-400">QR Code Expired</span>
                <AppButton size="sm" @click="fetchNewQR">Refresh QR Code</AppButton>
              </div>
            </div>

            <!-- Countdown Timer & Instructions -->
            <div class="space-y-1">
              <div class="inline-flex items-center gap-2 bg-primary/10 border border-primary/20 text-primary px-3 py-1 rounded-full text-xs font-bold">
                <span class="w-2 h-2 rounded-full bg-primary animate-pulse" />
                <span>Scan with phone camera to log in</span>
              </div>
              <p class="text-xs text-text-secondary dark:text-[#8E8E93] font-medium pt-1">
                Auto-refreshes in <span class="font-bold text-text-primary dark:text-[#F2F2F7]">{{ timeLeftSeconds }}s</span>
              </p>
            </div>
          </div>
        </div>
      </AppCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { QrCode, KeyRound } from 'lucide-vue-next'
import QRCode from 'qrcode'

definePageMeta({
  layout: 'default',
})

useHead({ title: 'Admin Login' })

const config = useRuntimeConfig()
const { login, setSessionToken } = useAuth()
const { startQR, checkStatus } = useQRAuth()

const isHosted = computed(() => {
  const url = config.public.publicAppUrl
  return !!url && typeof url === 'string' && url.trim() !== ''
})

const mode = ref<'password' | 'qr'>('password')
const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMessage = ref<string | null>(null)

// QR State
const currentRequestId = ref<string | null>(null)
const qrDataUrl = ref<string | null>(null)
const qrLoading = ref(false)
const qrExpired = ref(false)
const timeLeftSeconds = ref(90)

let pollTimer: NodeJS.Timeout | null = null
let countdownTimer: NodeJS.Timeout | null = null

function switchMode(newMode: 'password' | 'qr') {
  if (newMode === 'qr' && !isHosted.value) return
  mode.value = newMode
  errorMessage.value = null
  if (newMode === 'qr') {
    fetchNewQR()
  } else {
    stopPolling()
  }
}

async function fetchNewQR() {
  qrLoading.value = true
  qrExpired.value = false
  errorMessage.value = null
  stopPolling()

  try {
    const res = await startQR()
    currentRequestId.value = res.id
    
    // Generate QR Image Data URL
    qrDataUrl.value = await QRCode.toDataURL(res.approval_url, {
      margin: 1,
      width: 240,
      color: {
        dark: '#0381FE',
        light: '#FFFFFF',
      },
    })

    timeLeftSeconds.value = 90
    startCountdown()
    startPolling()
  } catch (err: any) {
    console.error('QR Generation Error:', err)
    const detail = err?.data?.detail || err?.statusMessage || err?.message || String(err)
    errorMessage.value = `Failed to generate QR code: ${detail}`
  } finally {
    qrLoading.value = false
  }
}

function startCountdown() {
  if (countdownTimer) clearInterval(countdownTimer)
  countdownTimer = setInterval(() => {
    if (timeLeftSeconds.value > 0) {
      timeLeftSeconds.value -= 1
    } else {
      qrExpired.value = true
      stopPolling()
    }
  }, 1000)
}

function startPolling() {
  if (pollTimer) clearInterval(pollTimer)
  pollTimer = setInterval(async () => {
    if (!currentRequestId.value || qrExpired.value) return

    try {
      const res = await checkStatus(currentRequestId.value)
      if (res.status === 'approved' && res.access_token) {
        stopPolling()
        await setSessionToken(res.access_token)
        navigateTo('/admin/projects')
      } else if (res.status === 'expired') {
        qrExpired.value = true
        stopPolling()
      }
    } catch (err) {
      // Ignore transient network poll error
    }
  }, 1500)
}

function stopPolling() {
  if (pollTimer) {
    clearInterval(pollTimer)
    pollTimer = null
  }
  if (countdownTimer) {
    clearInterval(countdownTimer)
    countdownTimer = null
  }
}

async function handlePasswordLogin() {
  loading.value = true
  errorMessage.value = null

  try {
    await login(email.value, password.value)
    navigateTo('/admin/projects')
  } catch (err: unknown) {
    const error = err as { data?: { detail?: string }; message?: string }
    errorMessage.value = error.data?.detail || error.message || 'Login failed. Please check your credentials.'
  } finally {
    loading.value = false
  }
}

onUnmounted(() => {
  stopPolling()
})
</script>
