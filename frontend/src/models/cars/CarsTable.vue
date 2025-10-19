<script setup lang="ts">
import type { Car } from './PageCars.vue'

defineProps<{
  items: Car[]
  columns: { label: string; key: string }[]
}>()
</script>

<template>
  <el-table :data="items" border style="width: 100%">
    <el-table-column
      v-for="column in columns"
      :key="column.key"
      :prop="column.key"
      :label="column.label"
    />
  </el-table>
</template>
