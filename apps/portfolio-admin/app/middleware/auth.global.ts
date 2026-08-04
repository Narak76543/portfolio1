/**
 * Auth middleware — guards protected admin routes using backend auth check.
 */
export default defineNuxtRouteMiddleware(async (to) => {
  // Allow login page
  if (to.path === '/login') return

  const { checkAuth } = useAuth()
  const valid = await checkAuth()

  if (!valid) {
    return navigateTo('/login')
  }
})
