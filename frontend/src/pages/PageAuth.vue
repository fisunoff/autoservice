<script setup lang="ts">
import router, { WORK_ORDER_NAME } from '@/router'

const gotoApp = () => {
  router.push({ name: WORK_ORDER_NAME })
}
</script>

<template>
  <RouterView @gotoApp="gotoApp" />
</template>

<style scoped></style>
