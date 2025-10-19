<script setup lang="ts">
import type { Customer } from './PageCustomers.vue'

defineProps<{
  items: Customer[]
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
