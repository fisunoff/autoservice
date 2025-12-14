<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import api from '@/api/api'
import { ElMessage } from 'element-plus'
import PriceListTable from '@/models/priceList/PriceListTable.vue'
import AddPriceListDialog from '@/models/priceList/AddPriceListDialog.vue'

export interface PriceListItem {
  id: number
  number: number
  title: string
  unit: string
  price: number
  inStrokeQuantity: number
  isWork: boolean
  isUsing: boolean
}
interface NewPriceListItem {
  title: string
  unit: string
  price: number
  in_stock_quantity: number
  is_work: boolean
  using: boolean
}

const tableData = reactive<PriceListItem[]>([])
const dialogVisible = ref(false)
const columns = [
  { label: '№', key: 'number' },
  { label: 'Наименование', key: 'title' },
  { label: 'ед. измерения', key: 'unit' },
  { label: 'Цена', key: 'price' },
  { label: 'В наличии', key: 'inStrokeQuantity' },
]

const isWork = ref(false)
const fetchData = async () => {
  try {
    const response = await api.get('/price_list')
    tableData.splice(0, tableData.length)
    response.data.forEach((item: any, index: number) => {
      tableData.push({
        id: item.id,
        number: index + 1,
        title: item.title,
        unit: item.unit,
        price: item.price,
        inStrokeQuantity: item.in_stock_quantity,
        isWork: item.is_work,
        isUsing: item.using,
      })
    })
  } catch (error) {
    console.error('Ошибка при загрузке прейскуранта:', error)
    ElMessage.error('Не удалось загрузить данные прейскуранта.')
  }
}

const handleAddItem = async (newItem: NewPriceListItem) => {
  try {
    await api.post('/price_list', newItem)
    dialogVisible.value = false
    ElMessage.success('Позиция успешно добавлена!')
    await fetchData()
  } catch (error) {
    console.error('Ошибка при добавлении позиции:', error)
    ElMessage.error('Произошла ошибка при добавлении позиции.')
  }
}
const openAddWork = () => {
  isWork.value = true
  dialogVisible.value = true
}
const openAddTovar = () => {
  isWork.value = false
  dialogVisible.value = true
}
onMounted(fetchData)
</script>

<template>
  <div class="flex flex-col gap-4 p-10">
    <div class="self-end flex gap-3">
      <el-button type="success" @click="openAddTovar"> Добавить товар </el-button>
      <el-button type="success" @click="openAddWork"> Добавить работу </el-button>
    </div>

    <PriceListTable :items="tableData" :columns="columns">
      <template #actions="{ item }">
        <el-button v-if="item.isUsing && item.inStrokeQuantity > 0" type="success" size="small">
          Использовать
        </el-button>
        <el-button type="danger" size="small">В архив</el-button>
      </template>
    </PriceListTable>

    <AddPriceListDialog v-model:visible="dialogVisible" :is-work="isWork" @save="handleAddItem" />
  </div>
</template>

<style scoped></style>
