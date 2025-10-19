<script setup lang="ts">
import { onMounted, reactive } from 'vue'
import api from '@/api/api.ts'
import { formatDateToRu } from '@/api/formatServices.ts'

export interface WorkorderListItem {
  id: number
  number: number
  car: string
  worker: string
  openDate: string
  status: string
}

const colums = [
  { label: '№', key: 'number' },
  { label: 'Автомобиль', key: 'car' },
  { label: 'Ответственный', key: 'worker' },
  { label: 'Дата приема', key: 'openDate' },
]
const tableData = reactive<WorkorderListItem[]>([])
const fetchData = async () => {
  try {
    const response = await api.get('/order')
    tableData.splice(0, tableData.length)
    response.data.forEach((item, index) => {
      const res: WorkorderListItem = {} as WorkorderListItem
      res.id = item.id
      res.number = index + 1
      res.car = `${item.car.brand} ${item.car.model} \n ${item.car.vin}`
      res.worker = `${item.worker.surname} ${item.worker.name}`
      res.openDate = formatDateToRu(item.openDate)
      if (item.car_given_out) res.status = 'Выдан'
      else if (item.car_received) res.status = 'Получен'
      tableData.push(res)
    })
  } catch (error) {
    console.log(error)
  }
}

onMounted(async () => {
  await fetchData()
})
</script>

<template>
  <div class="flex flex-col gap-2 p-10">
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column
        v-for="colum in colums"
        :prop="colum.key"
        :label="colum.label"
        :key="colum.key"
      />

      <el-table-column label="Статус">
        <template #default="item">
          <div class="px-3 py-2 rounded-sm bg-teal-300">{{ item.status }}</div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<style scoped></style>
