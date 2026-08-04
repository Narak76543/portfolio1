<template>
  <div class="min-h-screen flex items-center justify-center bg-background dark:bg-black px-4 transition-colors">
    <div class="w-full max-w-sm text-center space-y-6">
      <!-- Header -->
      <div>
        <h1 class="text-2xl font-extrabold text-text-primary dark:text-[#F2F2F7] tracking-wider uppercase inline-flex items-center">
          <span>SARAT</span>
          <span class="text-text-secondary dark:text-[#8E8E93] font-bold ml-1.5">NARAK</span>
          <span class="w-1.5 h-1.5 rounded-full bg-primary ml-1" />
        </h1>
        <p class="text-xs text-text-secondary dark:text-[#8E8E93] font-medium mt-1">Admin Device Login Approval</p>
      </div>

      <AppCard padded class="space-y-4">
        <!-- 1. Loading State -->
        <div v-if="loading" class="py-8 space-y-3">
          <div class="animate-spin w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full mx-auto" />
          <p class="text-sm font-semibold text-text-primary dark:text-[#F2F2F7]">Verifying trusted device &amp; approving login...</p>
        </div>

        <!-- 2. Success State -->
        <div v-else-if="success" class="py-6 space-y-4">
          <div class="w-16 h-16 bg-emerald-500/10 text-emerald-500 rounded-full flex items-center justify-center mx-auto border border-emerald-500/20">
            <CheckCircle2 class="w-8 h-8" :stroke-width="2" />
          </div>
          <div>
            <h2 class="text-lg font-bold text-text-primary dark:text-[#F2F2F7]">Login Approved!</h2>
            <p class="text-xs text-text-secondary dark:text-[#8E8E93] font-medium mt-1">
              Your desktop browser has been logged in automatically. You can close this tab.
            </p>
          </div>
        </div>

        <!-- 3. Untrusted Device Error -->
        <div v-else-if="notTrusted" class="py-6 space-y-4">
          <div class="w-16 h-16 bg-amber-500/10 text-amber-500 rounded-full flex items-center justify-center mx-auto border border-amber-500/20">
            <ShieldAlert class="w-8 h-8" :stroke-width="2" />
          </div>
          <div>
            <h2 class="text-base font-bold text-text-primary dark:text-[#F2F2F7]">Device Not Trusted</h2>
            <p class="text-xs text-text-secondary dark:text-[#8E8E93] font-medium mt-2 leading-relaxed">
              This device hasn't been registered for QR login yet. Log in to <strong class="text-text-primary dark:text-[#F2F2F7]">/admin</strong> once on this phone using your password, then click <strong class="text-primary">"Trust this device for QR login"</strong>.
            </p>
          </div>
          <AppButton to="/login" size="sm" class="w-full">
            Log In on Phone First
          </AppButton>
        </div>

        <!-- 4. General Error -->
        <div v-else class="py-6 space-y-4">
          <div class="w-16 h-16 bg-rose-500/10 text-rose-500 rounded-full flex items-center justify-center mx-auto border border-rose-500/20">
            <AlertCircle class="w-8 h-8" :stroke-width="2" />
          </div>
          <div>
            <h2 class="text-base font-bold text-text-primary dark:text-[#F2F2F7]">Approval Failed</h2>
            <p class="text-xs text-rose-500 font-medium mt-1">{{ errorMessage }}</p>
          </div>
        </div>
      </AppCard>
    </div>
  </div>
</template>

<script setup lang="ts">
import { CheckCircle2, ShieldAlert, AlertCircle } from 'lucide-vue-next'

definePageMeta({
  layout: 'default',
})

useHead({ title: 'Approve QR Login' })

const route = useRoute()
const requestId = computed(() => route.params.id as string)

const { approveQR } = useQRAuth()

const loading = ref(true)
const success = ref(false)
const notTrusted = ref(false)
const errorMessage = ref<string | null>(null)

async function autoApprove() {
  loading.value = true
  success.value = false
  notTrusted.value = false
  errorMessage.value = null

  if (!import.meta.client) return

  const deviceSecret = localStorage.getItem('trusted_device_secret')
  if (!deviceSecret) {
    loading.value = false
    notTrusted.value = true
    return
  }

  try {
    await approveQR(requestId.value, deviceSecret)
    success.value = true
  } catch (err: any) {
    errorMessage.value = err.data?.detail || err.message || 'Failed to approve QR login request. The code may have expired.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  autoApprove()
})
</script>
