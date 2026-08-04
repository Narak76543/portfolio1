/**
 * Auth middleware — guards protected admin routes using backend auth check.
 * Publicly allows /login and /qr-approve/* routes.
 */
export default defineNuxtRouteMiddleware(async (to) => {
  // Allow login page and QR approval route without global auth redirect
  if (to.path === '/login' || to.path.startsWith('/qr-approve')) return

  const { checkAuth } = useAuth()
  const valid = await checkAuth()

  if (!valid) {
    return navigateTo('/login')
  }
})
