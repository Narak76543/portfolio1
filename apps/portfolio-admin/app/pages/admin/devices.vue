<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div>
        <h1 class="text-2xl font-bold text-text-primary dark:text-[#F2F2F7] tracking-tight">Trusted Devices (QR Login)</h1>
        <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-1">Manage devices registered to approve QR code logins without entering a password.</p>
      </div>
      <AppButton v-if="!thisDeviceIsTrusted" @click="handleTrustThisDevice" :loading="registering">
        <Smartphone class="h-4 w-4 mr-1.5" :stroke-width="1.75" />
        Trust This Device (Samsung A05s)
      </AppButton>
    </div>

    <FormError :message="errorMessage" />

    <!-- Success Banner -->
    <div v-if="successMessage" class="p-4 rounded-card bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 text-sm font-semibold flex items-center justify-between">
      <span>{{ successMessage }}</span>
      <button @click="successMessage = null" class="text-emerald-500/70 hover:text-emerald-500">✕</button>
    </div>

    <!-- Hosting Environment Banner -->
    <div v-if="!isHosted" class="p-4 rounded-card bg-primary/10 border border-primary/20 text-primary text-xs font-semibold flex items-center gap-2">
      <Smartphone class="w-4 h-4 flex-shrink-0" :stroke-width="1.75" />
      <span>QR login and phone device registration will become active once deployed with a public URL (PUBLIC_APP_URL). Password login remains active in local dev.</span>
    </div>

    <!-- Trust Status Banner for current device -->
    <AppCard padded class="flex items-center justify-between gap-4">
      <div class="flex items-center gap-3.5">
        <div class="w-10 h-10 rounded-full flex items-center justify-center" :class="thisDeviceIsTrusted ? 'bg-emerald-500/10 text-emerald-500' : 'bg-amber-500/10 text-amber-500'">
          <ShieldCheck v-if="thisDeviceIsTrusted" class="w-5 h-5" :stroke-width="1.75" />
          <Smartphone v-else class="w-5 h-5" :stroke-width="1.75" />
        </div>
        <div>
          <h3 class="text-sm font-bold text-text-primary dark:text-[#F2F2F7]">
            Current Device Status: {{ thisDeviceIsTrusted ? 'Trusted for QR Login' : 'Not Trusted' }}
          </h3>
          <p class="text-xs text-text-secondary dark:text-[#8E8E93] mt-0.5">
            {{ thisDeviceIsTrusted ? 'This browser holds a secret key allowing it to approve login QR codes.' : 'Register this phone to enable passwordless QR login.' }}
          </p>
        </div>
      </div>

      <AppButton v-if="!thisDeviceIsTrusted" size="sm" @click="handleTrustThisDevice" :loading="registering">
        Trust Device
      </AppButton>
    </AppCard>

    <!-- Loading State -->
    <AppCard v-if="loading" class="text-center py-16">
      <div class="animate-spin w-8 h-8 border-2 border-primary/20 border-t-primary rounded-full mx-auto" />
      <p class="text-sm text-text-secondary dark:text-[#8E8E93] mt-3">Loading trusted devices...</p>
    </AppCard>

    <!-- Devices List -->
    <AppCard v-else-if="devices.length > 0" padded class="space-y-4">
      <h2 class="text-base font-bold text-text-primary dark:text-[#F2F2F7]">Registered Trusted Devices</h2>

      <div class="divide-y divide-border dark:divide-white/8">
        <div
          v-for="device in devices"
          :key="device.id"
          class="py-4 flex items-center justify-between gap-4"
        >
          <div class="flex items-center gap-4">
            <div class="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center text-primary flex-shrink-0">
              <Smartphone class="w-5 h-5" :stroke-width="1.75" />
            </div>
            <div>
              <div class="font-bold text-text-primary dark:text-[#F2F2F7] flex items-center gap-2">
                <span>{{ device.device_label }}</span>
                <span v-if="isCurrentDevice(device)" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-500 border border-emerald-500/20 uppercase">This Phone</span>
              </div>
              <div class="text-xs text-text-secondary dark:text-[#8E8E93] mt-0.5 flex items-center gap-3">
                <span>Registered: {{ formatDate(device.created_at) }}</span>
                <span>•</span>
                <span>Last Used: {{ formatDate(device.last_used_at) || 'Never' }}</span>
              </div>
            </div>
          </div>

          <AppButton size="sm" variant="outline" class="text-rose-500 border-rose-500/30 hover:bg-rose-500/10" @click="openRevokeModal(device)">
            <Trash2 class="w-3.5 h-3.5 mr-1" :stroke-width="1.75" />
            Revoke Access
          </AppButton>
        </div>
      </div>
    </AppCard>

    <!-- Empty State -->
    <AppCard v-else class="text-center py-16">
      <p class="text-text-secondary dark:text-[#8E8E93] mb-4">No trusted devices registered yet.</p>
      <AppButton @click="handleTrustThisDevice" :loading="registering">Trust This Device (Samsung A05s)</AppButton>
    </AppCard>

    <!-- Revoke Confirmation Dialog -->
    <div v-if="revokingDevice" class="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
      <div class="bg-surface dark:bg-[#1C1C1E] border border-border dark:border-white/10 rounded-2xl max-w-sm w-full p-6 space-y-4 shadow-2xl">
        <h3 class="text-lg font-bold text-text-primary dark:text-[#F2F2F7]">Revoke Device Access?</h3>
        <p class="text-sm text-text-secondary dark:text-[#8E8E93]">
          Are you sure you want to revoke <strong class="text-text-primary dark:text-[#F2F2F7]">{{ revokingDevice.device_label }}</strong>? This device will no longer be able to approve QR logins.
        </p>
        <div class="flex justify-end gap-3 pt-2">
          <AppButton variant="secondary" @click="revokingDevice = null">Cancel</AppButton>
          <AppButton variant="outline" class="text-rose-500 border-rose-500/30 hover:bg-rose-500/10" :loading="revoking" @click="confirmRevoke">
            Revoke Access
          </AppButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Smartphone, ShieldCheck, Trash2 } from 'lucide-vue-next'

definePageMeta({
  layout: 'admin',
})

useHead({ title: 'Trusted Devices — Admin' })

const config = useRuntimeConfig()
const isHosted = computed(() => {
  const url = config.public.publicAppUrl
  return !!url && typeof url === 'string' && url.trim() !== ''
})

const { listDevices, registerDevice, revokeDevice } = useQRAuth()

const devices = ref<Array<{ id: string; device_label: string; created_at?: string; last_used_at?: string }>>([])
const loading = ref(true)
const registering = ref(false)
const revoking = ref(false)
const revokingDevice = ref<any | null>(null)

const errorMessage = ref<string | null>(null)
const successMessage = ref<string | null>(null)
const thisDeviceIsTrusted = ref(false)

function checkLocalTrust() {
  if (import.meta.client) {
    thisDeviceIsTrusted.value = !!localStorage.getItem('trusted_device_secret')
  }
}

async function fetchDevices() {
  loading.value = true
  errorMessage.value = null
  try {
    devices.value = await listDevices()
  } catch (err: any) {
    errorMessage.value = 'Failed to load trusted devices.'
  } finally {
    loading.value = false
  }
}

async function handleTrustThisDevice() {
  registering.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    const res = await registerDevice('Samsung A05s')
    if (import.meta.client) {
      localStorage.setItem('trusted_device_secret', res.device_secret)
      localStorage.setItem('trusted_device_id', res.device_id)
    }
    thisDeviceIsTrusted.value = true
    successMessage.value = `This device (${res.device_label}) is now trusted for QR login!`
    await fetchDevices()
  } catch (err: any) {
    if (err.status === 401 || err.statusCode === 401 || err.data?.error_code === 'TOKEN_MISSING' || err.data?.error_code === 'AUTH_FAILED') {
      errorMessage.value = 'Session expired. Please sign out (top right icon) and sign in with password again to refresh your session.'
    } else {
      errorMessage.value = err.data?.detail || err.statusMessage || err.message || 'Failed to register device.'
    }
  } finally {
    registering.value = false
  }
}

function openRevokeModal(device: any) {
  revokingDevice.value = device
}

async function confirmRevoke() {
  if (!revokingDevice.value) return
  revoking.value = true
  errorMessage.value = null

  try {
    await revokeDevice(revokingDevice.value.id)
    if (import.meta.client && localStorage.getItem('trusted_device_id') === revokingDevice.value.id) {
      localStorage.removeItem('trusted_device_secret')
      localStorage.removeItem('trusted_device_id')
      thisDeviceIsTrusted.value = false
    }
    successMessage.value = `Device "${revokingDevice.value.device_label}" revoked successfully.`
    revokingDevice.value = null
    await fetchDevices()
  } catch (err: any) {
    errorMessage.value = err.data?.detail || err.message || 'Failed to revoke device.'
  } finally {
    revoking.value = false
  }
}

function isCurrentDevice(device: any) {
  if (!import.meta.client) return false
  return localStorage.getItem('trusted_device_id') === device.id
}

function formatDate(isoStr?: string) {
  if (!isoStr) return ''
  return new Date(isoStr).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
}

onMounted(() => {
  checkLocalTrust()
  fetchDevices()
})
</script>
