<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import api from '@/api/api'
import { ElMessage, ElMessageBox } from 'element-plus'
import { formatDateToRu } from '@/api/formatServices.ts'
import WorkersTable from './WorkersTable.vue'
import HireWorkerDialog from '@/models/workers/HireWorkerDialog.vue'
export interface Worker {
  id: number
  number: number
  fio: string
  hireDate: string
  fireDate: string | null
}
export interface NewWorkerData {
  name: string
  surname: string
  patronymic: string
  tabel_number: string
  hire_date: string
  is_admin: boolean
  is_mechanic: boolean
  is_active: boolean
  login: string
  password: string
}

const workersData = reactive<Worker[]>([])
const dialogVisible = ref(false)

const fetchWorkers = async () => {
  try {
    const response = await api.get('/worker')
    workersData.splice(0, workersData.length)
    response.data.forEach((worker, index: number) => {
      workersData.push({
        id: worker.id,
        number: index + 1,
        fio: `${worker.surname} ${worker.name} ${worker.patronymic || ''}`.trim(),
        hireDate: formatDateToRu(worker.hire_date),
        fireDate: formatDateToRu(worker.fire_date),
      })
    })
  } catch (error) {
    ElMessage.error('Не удалось загрузить список сотрудников.')
    console.error(error)
  }
}

const handleHireWorker = async (newWorkerData: NewWorkerData) => {
  try {
    await api.post('/worker/hire', newWorkerData)
    dialogVisible.value = false
    ElMessage.success('Сотрудник успешно принят на работу!')
    await fetchWorkers()
  } catch (error) {
    ElMessage.error('Ошибка при приеме на работу.')
    console.error(error)
  }
}

const handleFireWorker = async (worker: Worker) => {
  try {
    await ElMessageBox.confirm(
      `Вы уверены, что хотите уволить сотрудника ${worker.fio}?`,
      'Подтверждение',
      {
        confirmButtonText: 'Уволить',
        cancelButtonText: 'Отмена',
        type: 'warning',
      },
    )

    await api.post(`/worker/${worker.id}/fire`)
    ElMessage.success('Сотрудник уволен.')
    await fetchWorkers()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('Ошибка при увольнении сотрудника.')
      console.error(error)
    }
  }
}

onMounted(fetchWorkers)
</script>

<template>
  <div class="flex flex-col gap-4 p-10">
    <div class="self-end">
      <el-button type="success" @click="dialogVisible = true"> Принять на работу </el-button>
    </div>

    <WorkersTable :items="workersData">
      <template #actions="{ item }">
        <el-button v-if="!item.fireDate" type="danger" size="small" @click="handleFireWorker(item)">
          Уволить
        </el-button>
      </template>
    </WorkersTable>
    <HireWorkerDialog v-model:visible="dialogVisible" @save="handleHireWorker" />
  </div>
</template>
