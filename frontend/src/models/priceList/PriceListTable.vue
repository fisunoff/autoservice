<script setup lang="ts">
import type { PriceListItem } from './PagePriceList.vue'

defineProps<{
  items: PriceListItem[]
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

    <el-table-column label="" width="220">
      <template #default="{ row }">
        <slot name="actions" :item="row"></slot>
      </template>
    </el-table-column>
  </el-table>
</template>
