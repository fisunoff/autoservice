<script setup lang="ts">
import { ref, computed } from 'vue'
import type { WikiItem } from './WikiPage.vue'

defineProps<{
  items: WikiItem[]
  columns: { label: string; key: string }[]
}>()

const viewDialogVisible = ref(false)
const editedItem = ref<WikiItem | null>(null)

const handleRowClick = (row: WikiItem) => {
  editedItem.value = { ...row }
  viewDialogVisible.value = true
}

const handleCloseDialog = () => {
  viewDialogVisible.value = false
  editedItem.value = null
}

const formattedBrands = computed(() => {
  if (!editedItem.value?.brands) return ''
  return editedItem.value.brands.join(', ')
})
</script>

<template>
  <div class="wiki-table-container">
    <el-table
      :data="items"
      border
      style="width: 100%"
      @row-click="handleRowClick"
      class="clickable-table"
    >
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

    <el-dialog
      v-model="viewDialogVisible"
      title="Просмотр записи"
      width="600px"
      @close="handleCloseDialog"
    >
      <div v-if="editedItem" class="view-dialog-content">
        <div class="view-section">
          <h3 class="view-section-title">Проблема</h3>
          <div class="view-section-content">
            {{ editedItem.syndrome || 'Не указано' }}
          </div>
        </div>

        <div class="view-section">
          <h3 class="view-section-title">Решение</h3>
          <div class="view-section-content">
            {{ editedItem.solution || 'Не указано' }}
          </div>
        </div>

        <div class="view-section">
          <h3 class="view-section-title">Бренды автомобилей</h3>
          <div class="view-section-content">
            <div v-if="formattedBrands" class="brands-container">
              <el-tag
                v-for="(brand, index) in editedItem.brands"
                :key="index"
                type="info"
                size="small"
                class="brand-tag"
              >
                {{ brand }}
              </el-tag>
            </div>
            <div v-else class="empty-field">Не указаны</div>
          </div>
        </div>

        <div class="view-section">
          <h3 class="view-section-title">Агрегаты</h3>
          <div class="view-section-content">
            <div v-if="editedItem.components?.length" class="brands-container">
              <el-tag
                v-for="(comp, index) in editedItem.components"
                :key="index"
                type="warning"
                size="small"
                class="brand-tag"
              >
                {{ comp }}
              </el-tag>
            </div>
            <div v-else class="empty-field">Не указаны</div>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<style>
.view-dialog-content {
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 10px;
}
.view-section {
  margin-bottom: 24px;
}
.view-section-title {
  margin: 0 0 8px 0;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}
.view-section-content {
  padding: 12px;
  background-color: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #ebeef5;
  font-size: 14px;
  line-height: 1.5;
  color: #606266;
  min-height: 40px;
}
.brands-container {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.brand-tag {
  margin-right: 4px;
  margin-bottom: 4px;
}
.empty-field {
  color: #909399;
  font-style: italic;
}
</style>
