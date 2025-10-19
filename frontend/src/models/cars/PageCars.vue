<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import api from '@/api/api'
import { ElMessage } from 'element-plus'
import CarsTable from '@/models/cars/CarsTable.vue'
import AddCarDialog from '@/models/cars/AddCarDialog.vue'

export interface Car {
  id: number
  number: number
  brand: string
  model: string
  state_number: string
  vin: string
  year: number
}

export interface NewCar {
  brand: string
  model: string
  state_number: string
  vin: string
  year: number
}

const tableData = reactive<Car[]>([])
const dialogVisible = ref(false)

const columns = [
  { label: '№', key: 'number' },
  { label: 'Марка', key: 'brand' },
  { label: 'Модель', key: 'model' },
  { label: 'Гос. номер', key: 'state_number' },
  { label: 'VIN', key: 'vin' },
  { label: 'Год выпуска', key: 'year' },
]

const fetchData = async () => {
  try {
    const response = await api.get('/car')
    tableData.splice(0, tableData.length)
    response.data.forEach((item, index: number) => {
      tableData.push({
        ...item,
        number: index + 1,
      })
    })
  } catch (error) {
    console.error('Ошибка при загрузке автомобилей:', error)
    ElMessage.error('Не удалось загрузить данные автомобилей.')
  }
}

const handleAddItem = async (newItem: NewCar) => {
  try {
    await api.post('/car', newItem)
    dialogVisible.value = false
    ElMessage.success('Автомобиль успешно добавлен!')
    await fetchData()
  } catch (error) {
    console.error('Ошибка при добавлении автомобиля:', error)
    ElMessage.error('Произошла ошибка при добавлении автомобиля.')
  }
}

onMounted(fetchData)
</script>

<template>
  <div class="flex flex-col gap-4 p-10">
    <div class="self-end">
      <el-button type="success" @click="dialogVisible = true"> Добавить автомобиль </el-button>
    </div>

    <CarsTable :items="tableData" :columns="columns" />

    <AddCarDialog v-model:visible="dialogVisible" @save="handleAddItem" />
  </div>
</template>
