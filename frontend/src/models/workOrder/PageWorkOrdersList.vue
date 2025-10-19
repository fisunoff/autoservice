<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import api from '@/api/api'
import { ElMessage } from 'element-plus'
import { formatDateToRu } from '@/api/formatServices.ts'
import OrdersTable from './WorkOrdersTable.vue'
import CreateOrderDialog from './CreateOrderDialog.vue'

export interface WorkOrderItem {
  id: number
  number: number
  car: string
  customer: string
  openDate: string
  status: string
}
export interface NewOrderData {
  customer_id: number | null
  car_id: number | null
  car_received: boolean
  opened_date: string
}
export interface Customer {
  id: number
  name: string
  surname: string
  phone: string
}
export interface Car {
  id: number
  brand: string
  model: string
  state_number: string
}

const tableData = reactive<WorkOrderItem[]>([])
const customersList = reactive<Customer[]>([])
const carsList = reactive<Car[]>([])
const dialogVisible = ref(false)

const columns = [
  { label: '№', key: 'number' },
  { label: 'Автомобиль', key: 'car' },
  { label: 'Клиент', key: 'customer' },
  { label: 'Дата приема', key: 'openDate' },
]

const fetchData = async () => {
  try {
    const [ordersRes, customersRes, carsRes] = await Promise.all([
      api.get('/order'),
      api.get('/customer'),
      api.get('/car'),
    ])

    tableData.splice(0, tableData.length)
    ordersRes.data.forEach((item, index: number) => {
      let status = 'В работе'
      if (item.car_given_out) status = 'Выдан'
      else if (item.paid_date) status = 'Оплачен'
      else if (item.closed_date) status = 'Готов'

      tableData.push({
        id: item.id,
        number: index + 1,
        car: `${item.car.brand} ${item.car.model} (${item.car.state_number})`,
        customer: `${item.customer.surname} ${item.customer.name}`,
        openDate: formatDateToRu(item.opened_date),
        status: status,
      })
    })

    customersList.splice(0, customersList.length, ...customersRes.data)
    carsList.splice(0, carsList.length, ...carsRes.data)
  } catch (error) {
    ElMessage.error('Не удалось загрузить данные.')
    console.error(error)
  }
}

const handleCreateOrder = async (newOrderData: NewOrderData) => {
  try {
    await api.post('/order', newOrderData)
    dialogVisible.value = false
    ElMessage.success('Заказ-наряд успешно создан!')
    await fetchData()
  } catch (error) {
    ElMessage.error('Ошибка при создании заказа.')
    console.error(error)
  }
}

onMounted(fetchData)
</script>

<template>
  <div class="flex flex-col gap-4 p-10">
    <div class="self-end">
      <el-button type="success" @click="dialogVisible = true"> Создать заказ-наряд </el-button>
    </div>

    <OrdersTable :items="tableData" :columns="columns">
      <template #status="{ item }">
        <div class="px-3 py-2 rounded-sm bg-teal-300">{{ item.status }}</div>
      </template>
    </OrdersTable>

    <CreateOrderDialog
      v-model:visible="dialogVisible"
      :customers="customersList"
      :cars="carsList"
      @save="handleCreateOrder"
    />
  </div>
</template>
