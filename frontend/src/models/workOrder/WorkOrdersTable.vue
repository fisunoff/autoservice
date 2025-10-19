<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { WorkOrderItem } from './PageWorkOrdersList.vue'

defineProps<{
  items: WorkOrderItem[]
  columns: { label: string; key: string }[]
}>()

const router = useRouter()

const handleRowClick = (row: WorkOrderItem) => {
  router.push(`/work_order/${row.id}`)
}
</script>

<template>
  <el-table
    :data="items"
    border
    style="width: 100%"
    class="clickable-rows"
    @row-click="handleRowClick"
  >
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

<style scoped>
.clickable-rows :deep(.el-table__row) {
  cursor: pointer;
}
</style>
