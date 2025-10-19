<script setup lang="ts">
import type { WorkOrderItem } from './PageWorkOrdersList.vue'

defineProps<{
  items: WorkOrderItem[]
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

    <el-table-column label="Статус" width="120">
      <template #default="{ row }">
        <slot name="status" :item="row"></slot>
      </template>
    </el-table-column>
  </el-table>
</template>
