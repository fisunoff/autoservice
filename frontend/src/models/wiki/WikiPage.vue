<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
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
  { label: 'Бренд автомобиля', key: 'brands' },
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

const filterBrand = ref<string>('')
const uniqueBrands = computed<string[]>(() => {
  const brands = new Set<string>()
  tableData.forEach((item) => {
    item.brands.forEach((brand) => {
      if (brand.trim()) brands.add(brand.trim())
    })
  })
  return Array.from(brands).sort()
})

const searchQuery = ref<string>('')

const filteredItems = computed(() => {
  let result = [...tableData]

  if (filterBrand.value) {
    result = result.filter((item) => {
      if (!item.brands) return false
      return item.brands.some((brand) =>
        brand.toLowerCase().includes(filterBrand.value.toLowerCase()),
      )
    })
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter((item) => {
      return (
        item.syndrome.toLowerCase().includes(query) ||
        item.solution.toLowerCase().includes(query) ||
        (item.brands && item.brands.some((brand) => brand.toLowerCase().includes(query)))
      )
    })
  }

  return result
})

const handleEditClick = (event: MouseEvent, item: WikiItem) => {
  event.stopPropagation()
  openDialogHandler(item)
}

const handleDeleteClick = (event: MouseEvent, item: WikiItem) => {
  event.stopPropagation()
  deleteItem(item)
}

const handleAddClick = (event: MouseEvent) => {
  event.stopPropagation()
  openDialogHandler()
}

onMounted(fetchData)
</script>

<template>
  <div class="flex flex-col gap-4 p-10">
    <div class="flex flex-col gap-4">
      <div class="filter-item">
        <label>Поиск по записям:</label>
        <el-input
          v-model="searchQuery"
          placeholder="Введите текст для поиска"
          clearable
          style="width: 300px; margin-left: 10px"
        />
        <el-button
          v-if="searchQuery"
          @click="searchQuery = ''"
          size="small"
          style="margin-left: 10px"
        >
          Сбросить поиск
        </el-button>
      </div>

      <div class="filter-item">
        <label>Фильтр по бренду:</label>
        <el-select
          v-model="filterBrand"
          placeholder="Все бренды"
          clearable
          style="width: 200px; margin-left: 10px"
        >
          <el-option label="Все бренды" value="" />
          <el-option v-for="brand in uniqueBrands" :key="brand" :label="brand" :value="brand" />
        </el-select>
        <el-button
          v-if="filterBrand"
          @click="filterBrand = ''"
          size="small"
          style="margin-left: 10px"
        >
          Сбросить фильтр
        </el-button>
      </div>
    </div>

    <div v-if="user.isMechanic" class="self-end">
      <el-button type="success" @click="handleAddClick"> Добавить запись </el-button>
    </div>

    <WikiTable :items="filteredItems" :columns="columns">
      <template v-if="user.isMechanic" #actions="{ item }">
        <el-button type="success" size="small" @click="handleEditClick($event, item)">
          Редактировать
        </el-button>
        <el-button type="danger" size="small" @click="handleDeleteClick($event, item)"
          >Удалить</el-button
        >
      </template>
    </WikiTable>

    <WikiDialog v-model:visible="dialogVisible" :item="editedItem" @save="saveHandler" />
  </div>
</template>

<style scoped>
.filter-item {
  display: flex;
  align-items: center;
}

.filter-item label {
  font-weight: 500;
  color: #606266;
  min-width: 140px;
}
</style>
