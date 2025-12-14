<script setup lang="ts">
import { onMounted, reactive, ref, computed } from 'vue'
import api from '@/api/api'
import { ElMessage } from 'element-plus'
import PriceListTable from '@/models/priceList/PriceListTable.vue'
import AddPriceListDialog from '@/models/priceList/AddPriceListDialog.vue'
import { useUserStore } from '@/stores/userStore.ts'

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

export interface NewPriceListItem {
  title: string
  unit: string
  price: number
  in_stock_quantity: number
  is_work: boolean
  using: boolean
}

const userStore = useUserStore()
const tableData = reactive<PriceListItem[]>([])
const dialogVisible = ref(false)
const isWork = ref(false)

const editingId = ref<number | null>(null)
const initialDialogData = ref<NewPriceListItem | null>(null)

const searchQuery = ref('')
const filterType = ref('all')
const showArchive = ref(false)

const columns = [
  { label: '№', key: 'number' },
  { label: 'Наименование', key: 'title' },
  { label: 'ед. измерения', key: 'unit' },
  { label: 'Цена', key: 'price' },
  { label: 'В наличии', key: 'inStrokeQuantity' },
]

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

const filteredTableData = computed(() => {
  return tableData.filter((item) => {
    const matchesSearch = item.title.toLowerCase().includes(searchQuery.value.toLowerCase())

    let matchesType = true
    if (filterType.value === 'work') {
      matchesType = item.isWork
    } else if (filterType.value === 'part') {
      matchesType = !item.isWork
    }

    let matchesStatus = true
    if (!showArchive.value) {
      matchesStatus = item.isUsing
    }

    return matchesSearch && matchesType && matchesStatus
  })
})

const handleSaveItem = async (formData: NewPriceListItem) => {
  try {
    if (editingId.value) {
      await api.put(`/price_list/${editingId.value}`, formData)
      ElMessage.success('Позиция успешно обновлена!')
    } else {
      await api.post('/price_list', formData)
      ElMessage.success('Позиция успешно добавлена!')
    }
    dialogVisible.value = false
    await fetchData()
  } catch (error) {
    console.error('Ошибка при сохранении позиции:', error)
    ElMessage.error('Произошла ошибка при сохранении.')
  }
}

const openAddDialog = (work: boolean) => {
  isWork.value = work
  editingId.value = null
  initialDialogData.value = null
  dialogVisible.value = true
}

const openEditItem = (item: PriceListItem) => {
  isWork.value = item.isWork
  editingId.value = item.id
  initialDialogData.value = {
    title: item.title,
    unit: item.unit,
    price: item.price,
    in_stock_quantity: item.inStrokeQuantity,
    is_work: item.isWork,
    using: item.isUsing,
  }
  dialogVisible.value = true
}

const toArchive = async (item: PriceListItem) => {
  try {
    await api.put(`/price_list/${item.id}`, {
      title: item.title,
      unit: item.unit,
      price: item.price,
      in_stock_quantity: item.inStrokeQuantity,
      is_work: item.isWork,
      using: false,
    })
    ElMessage.success('Позиция перемещена в архив')
    await fetchData()
  } catch (error) {
    ElMessage.error('Ошибка при архивации')
  }
}

const restoreFromArchive = async (item: PriceListItem) => {
  try {
    await api.put(`/price_list/${item.id}`, {
      title: item.title,
      unit: item.unit,
      price: item.price,
      in_stock_quantity: item.inStrokeQuantity,
      is_work: item.isWork,
      using: true,
    })
    ElMessage.success('Позиция восстановлена')
    await fetchData()
  } catch (error) {
    ElMessage.error('Ошибка при восстановлении')
  }
}

onMounted(fetchData)
</script>

<template>
  <div class="flex flex-col gap-4 p-10">
    <div class="flex justify-between items-end flex-wrap gap-4">
      <div class="flex gap-4 items-end flex-wrap">
        <div class="filter-block">
          <span class="filter-label">Поиск</span>
          <el-input
            v-model="searchQuery"
            placeholder="Название..."
            clearable
            style="width: 240px"
          />
        </div>

        <div class="filter-block">
          <span class="filter-label">Тип</span>
          <el-select v-model="filterType" style="width: 140px">
            <el-option label="Все" value="all" />
            <el-option label="Товары" value="part" />
            <el-option label="Работы" value="work" />
          </el-select>
        </div>

        <div class="filter-block self-center flex mt-10">
          <el-checkbox v-model="showArchive" label="Показывать архивные" />
        </div>
      </div>

      <div v-if="userStore.isAdmin" class="flex gap-3">
        <el-button type="success" @click="openAddDialog(false)"> Добавить товар </el-button>
        <el-button type="success" @click="openAddDialog(true)"> Добавить работу </el-button>
      </div>
    </div>

    <PriceListTable :items="filteredTableData" :columns="columns">
      <template #actions="{ item }">
        <div class="flex gap-2">
          <el-button
            v-if="userStore.isAdmin"
            type="primary"
            size="small"
            @click="openEditItem(item)"
          >
            Ред.
          </el-button>

          <el-button
            v-if="item.isUsing && userStore.isAdmin"
            type="danger"
            size="small"
            @click="toArchive(item)"
          >
            В архив
          </el-button>

          <el-button
            v-if="!item.isUsing && userStore.isAdmin"
            type="info"
            size="small"
            @click="restoreFromArchive(item)"
          >
            Восстановить
          </el-button>
        </div>
      </template>
    </PriceListTable>

    <AddPriceListDialog
      v-model:visible="dialogVisible"
      :is-work="isWork"
      :initial-data="initialDialogData"
      @save="handleSaveItem"
    />
  </div>
</template>

<style scoped>
.filter-block {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.filter-label {
  font-size: 12px;
  color: #606266;
  margin-left: 2px;
}
</style>
