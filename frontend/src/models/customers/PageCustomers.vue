<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import api from '@/api/api'
import { ElMessage } from 'element-plus'
import CustomersTable from '@/models/customers/CustomersTable.vue'
import AddCustomersDialog from '@/models/customers/AddCustomersDialog.vue'

export interface Customer {
  id: number
  number: number
  fio: string
  phone: string
}
export interface NewCustomer {
  name: string
  surname: string
  patronymic: string
  phone: string
}

const tableData = reactive<Customer[]>([])
const dialogVisible = ref(false)
const columns = [
  { label: '№', key: 'number' },
  { label: 'ФИО', key: 'fio' },
  { label: 'Номер телефона', key: 'phone' },
]

const fetchData = async () => {
  try {
    const response = await api.get('/customer')
    tableData.splice(0, tableData.length)
    response.data.forEach((item, index: number) => {
      tableData.push({
        id: item.id,
        number: index + 1,
        fio: `${item.surname} ${item.name} ${item.patronymic}`,
        phone: item.phone,
      })
    })
  } catch (error) {
    console.error('Ошибка при загрузке клиентов:', error)
    ElMessage.error('Не удалось загрузить данные клиентов.')
  }
}

const handleAddItem = async (newItem: NewCustomer) => {
  try {
    await api.post('/customer', newItem)
    dialogVisible.value = false
    await fetchData()
  } catch (error) {
    console.error('Ошибка при добавлении клиента:', error)
    ElMessage.error('Произошла ошибка при добавлении клиента.')
  }
}

onMounted(fetchData)
</script>

<template>
  <div class="flex flex-col gap-4 p-10">
    <div class="self-end">
      <el-button type="success" @click="dialogVisible = true"> Добавить клиента </el-button>
    </div>

    <CustomersTable :items="tableData" :columns="columns"> </CustomersTable>

    <AddCustomersDialog v-model:visible="dialogVisible" @save="handleAddItem" />
  </div>
</template>

<style scoped></style>
