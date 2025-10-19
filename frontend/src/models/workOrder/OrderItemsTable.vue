<script setup lang="ts">
interface OrderItem {
  position: { id: number; title: string; unit: string }
  price: number
  quantity: number
  cost: number
}

defineProps<{
  items: OrderItem[]
}>()

const emit = defineEmits(['edit'])

const columns = [
  { key: 'position.title', label: 'Наименование' },
  { key: 'position.unit', label: 'Ед. изм.', width: 100 },
  { key: 'price', label: 'Цена', width: 120 },
  { key: 'quantity', label: 'Количество', width: 120 },
  { key: 'cost', label: 'Стоимость', width: 120 },
]

const handleEdit = (item: OrderItem) => {
  emit('edit', item)
}
</script>

<template>
  <el-table :data="items" border style="width: 100%">
    <el-table-column type="index" label="№" width="50" />
    <el-table-column
      v-for="column in columns"
      :key="column.key"
      :prop="column.key"
      :label="column.label"
      :width="column.width"
    >
      <template #default="{ row }">
        {{
          column.key === 'position.title'
            ? row.position.title
            : column.key === 'position.unit'
              ? row.position.unit
              : row[column.key]
        }}
      </template>
    </el-table-column>
    <el-table-column label="Действия" width="120" align="center">
      <template #default="{ row }">
        <el-button type="primary" link @click="handleEdit(row)">Редактировать</el-button>
      </template>
    </el-table-column>
  </el-table>
</template>
