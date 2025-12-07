<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import api from '@/api/api'
import { ElMessage } from 'element-plus'
import WikiTable from './WikiTable.vue'
import WikiDialog from './WikiDialog.vue'
import { useUserStore } from '@/stores/userStore'

export interface WikiItem {
  id: number
  syndrome: string
  solution: string
  brands: string[]
}

const user = useUserStore()
const tableData = reactive<WikiItem[]>([])
const dialogVisible = ref(false)
const editedItem = ref<WikiItem>()
const columns = [
  { label: 'Проблема', key: 'syndrome' },
  { label: 'Решение', key: 'solution' },
  { label: 'Бренды', key: 'brands' },
]

const fetchData = async () => {
  try {
    const response = await api.get('/wiki')
    tableData.splice(0, tableData.length, ...response.data)
  } catch (error) {
    console.error('Ошибка при загрузке базы знаний:', error)
    ElMessage.error('Не удалось загрузить данные базы знаний.')
  }
}

const openDialogHandler = (item?: WikiItem) => {
  if (item) editedItem.value = { ...item }
  dialogVisible.value = true
}
const saveHandler = async (item: Partial<WikiItem>) => {
  try {
    await api.post('/wiki', item)
    dialogVisible.value = false
    ElMessage.success('Позиция успешно добавлена!')
    await fetchData()
  } catch (error) {
    console.error('Ошибка при добавлении позиции:', error)
    ElMessage.error('Произошла ошибка при добавлении позиции.')
  }
}

const deleteItem = async (item: WikiItem) => {
  try {
    await api.delete(`/wiki/${item.id}`)
    await fetchData()
  } catch (err) {
    console.error('Ошибка при удалении записи базы знаний', err)
  }
}
onMounted(fetchData)
</script>

<template>
  <div class="flex flex-col gap-4 p-10">
    <div v-if="user.isMechanic" class="self-end">
      <el-button type="success" @click="openDialogHandler"> Добавить запись </el-button>
    </div>

    <WikiTable :items="tableData" :columns="columns">
      <template v-if="user.isMechanic" #actions="{ item }">
        <el-button type="success" size="small" @click="openDialogHandler(item)">
          Редактировать
        </el-button>
        <el-button type="danger" size="small" @click="deleteItem(item)">Удалить</el-button>
      </template>
    </WikiTable>

    <WikiDialog v-model:visible="dialogVisible" :item="editedItem" @save="saveHandler" />
  </div>
</template>

<style scoped></style>
