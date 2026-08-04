export function useQRAuth() {
  const config = useRuntimeConfig()
  const rawBaseUrl = config.public.apiBaseUrl || ''
  const baseUrl = (import.meta.client && window.location.hostname !== 'localhost')
    ? 'https://narak-portfolio-backend.fastapicloud.dev'
    : (rawBaseUrl || 'http://localhost:8000')
  const { getAuthHeader } = useAuth()

  async function startQR() {
    return await $fetch<{ id: string; approval_url: string; expires_at: string }>(
      `${baseUrl}/api/v1/qr-auth/start`,
      { method: 'POST' }
    )
  }

  async function checkStatus(id: string) {
    return await $fetch<{ id: string; status: 'pending' | 'approved' | 'expired'; access_token?: string; refresh_token?: string }>(
      `${baseUrl}/api/v1/qr-auth/status/${id}`
    )
  }

  async function approveQR(id: string, deviceSecret: string) {
    return await $fetch<{ message: string }>(
      `${baseUrl}/api/v1/qr-auth/approve/${id}`,
      {
        method: 'POST',
        body: { device_secret: deviceSecret },
      }
    )
  }

  async function registerDevice(deviceLabel: string = 'Samsung A05s') {
    return await $fetch<{ device_id: string; device_secret: string; device_label: string }>(
      `${baseUrl}/api/v1/qr-auth/register-device`,
      {
        method: 'POST',
        headers: getAuthHeader(),
        body: { device_label: deviceLabel },
      }
    )
  }

  async function listDevices() {
    return await $fetch<Array<{ id: string; device_label: string; created_at?: string; last_used_at?: string }>>(
      `${baseUrl}/api/v1/qr-auth/devices`,
      { headers: getAuthHeader() }
    )
  }

  async function revokeDevice(id: string) {
    return await $fetch(`${baseUrl}/api/v1/qr-auth/devices/${id}`, {
      method: 'DELETE',
      headers: getAuthHeader(),
    })
  }

  return {
    startQR,
    checkStatus,
    approveQR,
    registerDevice,
    listDevices,
    revokeDevice,
  }
}
