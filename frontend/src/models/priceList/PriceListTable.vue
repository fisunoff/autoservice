<script setup lang="ts">
import type { PriceListItem } from './PagePriceList.vue'

defineProps<{
  items: PriceListItem[]
  columns: { label: string; key: string }[]
}>()

const tableRowClassName = ({ row }: { row: PriceListItem }) => {
  if (!row.isUsing) {
    return 'dimmed-row'
  }
  return ''
}
</script>

<template>
  <el-table :data="items" border style="width: 100%" :row-class-name="tableRowClassName">
    <el-table-column
      v-for="column in columns"
      :key="column.key"
      :prop="column.key"
      :label="column.label"
    />

    <el-table-column label="" width="220">
      <template #default="{ row }">
        <slot name="actions" :item="row"></slot>
      </template>
    </el-table-column>
  </el-table>
</template>

<style>
.el-table .dimmed-row {
  opacity: 0.5;
  background-color: #f5f7fa;
}

.el-table .dimmed-row:hover > td.el-table__cell {
  background-color: #f5f7fa !important;
}
</style>
