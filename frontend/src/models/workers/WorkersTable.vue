<script setup lang="ts">
import type { Worker } from './PageWorkers.vue'

defineProps<{
  items: Worker[]
  showActions: boolean
}>()
</script>

<template>
  <el-table :data="items" border style="width: 100%">
    <el-table-column prop="number" label="№" width="60" />
    <el-table-column prop="fio" label="ФИО" />
    <el-table-column prop="hireDate" label="Дата принятия" width="150" />
    <el-table-column prop="fireDate" label="Дата увольнения" width="160" />

    <el-table-column v-if="showActions" label="" width="140">
      <template #default="{ row }">
        <slot name="actions" :item="row"></slot>
      </template>
    </el-table-column>
  </el-table>
</template>
