<template>
  <div />
</template>

<script setup lang="ts">
const { checkAuth } = useAuth()

onMounted(async () => {
  const valid = await checkAuth()
  if (valid) {
    navigateTo('/admin/projects')
  } else {
    navigateTo('/login')
  }
})
</script>
