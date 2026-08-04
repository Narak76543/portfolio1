/**
 * Auth composable — handles login, logout, token storage, and session check.
 * Uses Nuxt's useCookie and useState for SSR and hydration safety.
 */

interface AuthState {
  accessToken: string | null
  email: string | null
  userId: string | null
}

export function useAuth() {
  const config = useRuntimeConfig()
  const rawBaseUrl = config.public.apiBaseUrl || ''
  const baseUrl = (import.meta.client && window.location.hostname !== 'localhost')
    ? 'https://narak-portfolio-backend.fastapicloud.dev'
    : (rawBaseUrl || 'http://localhost:8000')

  const tokenCookie = useCookie<string | null>('admin_token', {
    maxAge: 60 * 60 * 24 * 7, // 7 days
    sameSite: 'lax',
    secure: process.env.NODE_ENV === 'production',
  })
  const emailCookie = useCookie<string | null>('admin_email', { maxAge: 60 * 60 * 24 * 7 })
  const userIdCookie = useCookie<string | null>('admin_user_id', { maxAge: 60 * 60 * 24 * 7 })

  const authState = useState<AuthState>('auth-state', () => ({
    accessToken: tokenCookie.value || null,
    email: emailCookie.value || null,
    userId: userIdCookie.value || null,
  }))

  const isAuthenticated = computed(() => !!authState.value.accessToken || !!tokenCookie.value)

  /** Initialize auth state from cookies or localStorage fallback. */
  function initAuth() {
    const token = tokenCookie.value || (import.meta.client ? localStorage.getItem('admin_token') : null)
    const email = emailCookie.value || (import.meta.client ? localStorage.getItem('admin_email') : null)
    const userId = userIdCookie.value || (import.meta.client ? localStorage.getItem('admin_user_id') : null)

    if (token) {
      authState.value.accessToken = token
      authState.value.email = email
      authState.value.userId = userId

      // Sync cookies if missing
      if (!tokenCookie.value) tokenCookie.value = token
      if (email && !emailCookie.value) emailCookie.value = email
      if (userId && !userIdCookie.value) userIdCookie.value = userId
    }
  }

  // Ensure initial sync
  initAuth()

  /** Get the Authorization header value. */
  function getAuthHeader(): Record<string, string> {
    initAuth()
    const token = authState.value.accessToken || tokenCookie.value || (import.meta.client ? localStorage.getItem('admin_token') : null)
    if (!token) return {}
    return { Authorization: `Bearer ${token}` }
  }

  /** Verify session token with backend GET /api/v1/auth/me */
  async function checkAuth(): Promise<boolean> {
    initAuth()
    const token = authState.value.accessToken || tokenCookie.value
    if (!token) return false

    try {
      const user = await $fetch<{ id: string; email: string }>(`${baseUrl}/api/v1/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      authState.value.email = user.email
      authState.value.userId = user.id
      emailCookie.value = user.email
      userIdCookie.value = user.id
      return true
    } catch {
      await logout()
      return false
    }
  }

  /** Log in with email and password. */
  async function login(email: string, password: string) {
    const response = await $fetch<{
      access_token: string
      user_id: string
      email: string
    }>(`${baseUrl}/api/v1/auth/login`, {
      method: 'POST',
      body: { email, password },
    })

    authState.value.accessToken = response.access_token
    authState.value.email = response.email
    authState.value.userId = response.user_id

    tokenCookie.value = response.access_token
    emailCookie.value = response.email
    userIdCookie.value = response.user_id

    if (import.meta.client) {
      localStorage.setItem('admin_token', response.access_token)
      localStorage.setItem('admin_email', response.email)
      localStorage.setItem('admin_user_id', response.user_id)
    }
  }

  /** Set session token directly (e.g. from QR Auth login approval). */
  async function setSessionToken(accessToken: string) {
    authState.value.accessToken = accessToken
    tokenCookie.value = accessToken

    if (import.meta.client) {
      localStorage.setItem('admin_token', accessToken)
    }

    await checkAuth()
  }

  /** Clear auth state and remove stored token. */
  async function logout() {
    authState.value.accessToken = null
    authState.value.email = null
    authState.value.userId = null

    tokenCookie.value = null
    emailCookie.value = null
    userIdCookie.value = null

    if (import.meta.client) {
      localStorage.removeItem('admin_token')
      localStorage.removeItem('admin_email')
      localStorage.removeItem('admin_user_id')
    }
  }

  return {
    authState,
    isAuthenticated,
    initAuth,
    checkAuth,
    login,
    setSessionToken,
    logout,
    getAuthHeader,
  }
}
