<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/api'
import { ElMessage } from 'element-plus'
import OrderItemsTable from './OrderItemsTable.vue'
import AddOrderItemDialog from './AddOrderItemDialog.vue'

interface OrderDetail {
  id: number
  customer: { name: string; surname: string; patronymic: string; phone: string }
  car: { brand: string; model: string; state_number: string; vin: string; year: number }
  details: OrderItem[]
  works: OrderItem[]
}
interface OrderItem {
  position: { id: number; title: string; unit: string }
  price: number
  quantity: number
  cost: number
}
interface PriceListItem {
  id: number
  title: string
}

const route = useRoute()
const orderId = Number(route.params.id)

const order = ref<OrderDetail | null>(null)
const priceListWorks = ref<PriceListItem[]>([])
const priceListDetails = ref<PriceListItem[]>([])
const activeTab = ref('works')
const isDialogVisible = ref(false)
const dialogMode = ref<'add' | 'edit'>('add')
const editingItem = ref<OrderItem | null>(null)

const dialogTitle = computed(() => {
  const action = dialogMode.value === 'add' ? 'Добавление' : 'Редактирование'
  const subject = activeTab.value === 'works' ? 'работы' : 'запчасти'
  return `${action} ${subject}`
})

const dialogItemsList = computed(() => {
  return activeTab.value === 'works' ? priceListWorks.value : priceListDetails.value
})

const totalCost = computed(() => {
  if (!order.value) return 0
  const worksCost = order.value.works.reduce((sum, item) => sum + item.cost, 0)
  const detailsCost = order.value.details.reduce((sum, item) => sum + item.cost, 0)
  return worksCost + detailsCost
})

const fetchOrderData = async () => {
  try {
    const { data } = await api.get(`/order/${orderId}`)
    order.value = data
  } catch (error) {
    ElMessage.error('Не удалось загрузить данные заказа.')
    console.error(error)
  }
}

const fetchPriceLists = async () => {
  try {
    const [worksRes, detailsRes] = await Promise.all([
      api.get('/price_list/works'),
      api.get('/price_list/details'),
    ])
    priceListWorks.value = worksRes.data
    priceListDetails.value = detailsRes.data
  } catch (error) {
    ElMessage.error('Не удалось загрузить прайс-листы.')
    console.error(error)
  }
}

const openAddDialog = () => {
  dialogMode.value = 'add'
  editingItem.value = null
  isDialogVisible.value = true
}

const openEditDialog = (item: OrderItem) => {
  dialogMode.value = 'edit'
  editingItem.value = item
  isDialogVisible.value = true
}

const handleSave = async (payload: { itemId?: number; quantity: number; price?: number }) => {
  try {
    if (dialogMode.value === 'add' && payload.itemId) {
      const url = `/order/${orderId}/${activeTab.value}`
      const body =
        activeTab.value === 'works'
          ? { work_id: payload.itemId, quantity: payload.quantity }
          : { detail_id: payload.itemId, quantity: payload.quantity }
      await api.post(url, body)
      ElMessage.success('Позиция успешно добавлена!')
    } else if (dialogMode.value === 'edit' && editingItem.value) {
      const positionId = editingItem.value.position.id
      const url = `/order/${orderId}/${activeTab.value}/${positionId}`
      const body = { price: payload.price, quantity: payload.quantity }
      await api.put(url, body)
      ElMessage.success('Позиция успешно обновлена!')
    }

    isDialogVisible.value = false
    await fetchOrderData()
  } catch (error) {
    ElMessage.error('Произошла ошибка при сохранении.')
    console.error(error)
  }
}

onMounted(async () => {
  await fetchOrderData()
  await fetchPriceLists()
})
</script>

<template>
  <div v-if="order" class="p-10 space-y-6">
    <el-card>
      <template #header>
        <div class="flex justify-between items-center">
          <span>Заказ-наряд №{{ order.id }}</span>
          <span class="font-bold text-xl">Общая стоимость: {{ totalCost.toFixed(2) }} ₽</span>
        </div>
      </template>
      <div class="grid grid-cols-2 gap-4">
        <div>
          <h3 class="font-semibold mb-2">Клиент</h3>
          <p>
            {{ order.customer.surname }} {{ order.customer.name }} {{ order.customer.patronymic }}
          </p>
          <p>Телефон: {{ order.customer.phone }}</p>
        </div>
        <div>
          <h3 class="font-semibold mb-2">Автомобиль</h3>
          <p>{{ order.car.brand }} {{ order.car.model }} ({{ order.car.year }})</p>
          <p>Гос. номер: {{ order.car.state_number }}</p>
          <p>VIN: {{ order.car.vin }}</p>
        </div>
      </div>
    </el-card>

    <el-card>
      <div class="flex justify-between items-center mb-4">
        <el-radio-group v-model="activeTab">
          <el-radio-button label="works">Работы</el-radio-button>
          <el-radio-button label="details">Запчасти</el-radio-button>
        </el-radio-group>
        <el-button type="primary" @click="openAddDialog">
          Добавить {{ activeTab === 'works' ? 'работу' : 'запчасть' }}
        </el-button>
      </div>

      <OrderItemsTable v-if="activeTab === 'works'" :items="order.works" @edit="openEditDialog" />
      <OrderItemsTable
        v-if="activeTab === 'details'"
        :items="order.details"
        @edit="openEditDialog"
      />
    </el-card>
    <AddOrderItemDialog
      v-model:visible="isDialogVisible"
      :mode="dialogMode"
      :title="dialogTitle"
      :items-list="dialogItemsList"
      :item-to-edit="editingItem"
      :select-label="activeTab === 'works' ? 'Работа' : 'Запчасть'"
      @save="handleSave"
    />
  </div>
  <div v-else class="p-10">Загрузка данных...</div>
</template>
