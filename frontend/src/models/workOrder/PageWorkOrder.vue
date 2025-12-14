<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api/api'
import { ElMessage } from 'element-plus'
import OrderItemsTable from './OrderItemsTable.vue'
import AddOrderItemDialog from './AddOrderItemDialog.vue'

interface Worker {
  id: number
  name: string
  surname: string
  patronymic: string
  is_admin: boolean
  is_mechanic: boolean
}

interface OrderDetail {
  id: number
  customer: { name: string; surname: string; patronymic: string; phone: string }
  car: { brand: string; model: string; state_number: string; vin: string; year: number }
  details: OrderItem[]
  works: OrderItem[]
  paid_date: string | null
  closed_date: string | null
  responsible_mechanic_id: number | null
  responsible_admin_id: number | null
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

const admins = ref<Worker[]>([])
const mechanics = ref<Worker[]>([])

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

const isOrderFinished = computed(() => {
  return !!(order.value?.paid_date || order.value?.closed_date)
})

const formatWorkerName = (worker: Worker) => {
  return `${worker.surname} ${worker.name} ${worker.patronymic}`
}

const fetchOrderData = async () => {
  try {
    const { data } = await api.get(`/order/${orderId}`)
    order.value = data
  } catch (error) {
    ElMessage.error('Не удалось загрузить данные заказа.')
    console.error(error)
  }
}

const fetchWorkers = async () => {
  try {
    const { data } = await api.get('/worker/')
    const allWorkers: Worker[] = data.items || data

    admins.value = allWorkers.filter((w) => w.is_admin)
    mechanics.value = allWorkers.filter((w) => w.is_mechanic)
  } catch (error) {
    console.error('Ошибка загрузки сотрудников:', error)
  }
}

const fetchPriceLists = async () => {
  try {
    const [worksRes, detailsRes] = await Promise.all([
      api.get('/price_list/works'),
      api.get('/price_list/details'),
    ])
    priceListWorks.value = worksRes.data.filter((w) => w.using)
    priceListDetails.value = detailsRes.data.filter((w) => w.using)
  } catch (error) {
    ElMessage.error('Не удалось загрузить прайс-листы.')
    console.error(error)
  }
}

const setResponsibleAdmin = async (adminId: number) => {
  try {
    await api.post(`/order/${orderId}/set_responsible_admin/${adminId}/`)
    ElMessage.success('Администратор назначен')
    await fetchOrderData()
  } catch (error) {
    ElMessage.error('Ошибка назначения администратора')
    console.error(error)
  }
}

const setResponsibleMechanic = async (mechanicId: number) => {
  try {
    await api.post(`/order/${orderId}/set_responsible_mechanic/${mechanicId}/`)
    ElMessage.success('Механик назначен')
    await fetchOrderData()
  } catch (error) {
    ElMessage.error('Ошибка назначения механика')
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

const payOrder = async () => {
  try {
    await api.post(`/order/${orderId}/set_paid`)
    ElMessage.success('Статус обновлен')
    await fetchOrderData()
  } catch (e) {
    console.error(e)
  }
}

const closeOrder = async () => {
  try {
    await api.post(`/order/${orderId}/close`)
    ElMessage.success('Заказ закрыт')
    await fetchOrderData()
  } catch (e) {
    console.error(e)
  }
}

onMounted(async () => {
  await fetchWorkers()
  await fetchOrderData()
  await fetchPriceLists()
})
</script>

<template>
  <div v-if="order" class="p-10 space-y-6">
    <el-card>
      <template #header>
        <div class="flex justify-between items-center">
          <div class="flex items-center gap-3">
            <span class="text-lg">Заказ-наряд №{{ order.id }}</span>
            <el-tag v-if="order.closed_date" type="info">Закрыт</el-tag>
            <el-tag v-else-if="order.paid_date" type="success">Оплачен</el-tag>
            <el-tag v-else type="warning">В работе</el-tag>
          </div>
          <span class="font-bold text-xl">Общая стоимость: {{ totalCost.toFixed(2) }} ₽</span>
        </div>
      </template>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <h3 class="font-semibold mb-2 text-gray-500 uppercase text-xs">Клиент</h3>
          <p class="font-medium">
            {{ order.customer.surname }} {{ order.customer.name }} {{ order.customer.patronymic }}
          </p>
          <p class="text-sm text-gray-600">Телефон: {{ order.customer.phone }}</p>
        </div>

        <div>
          <h3 class="font-semibold mb-2 text-gray-500 uppercase text-xs">Автомобиль</h3>
          <p class="font-medium">
            {{ order.car.brand }} {{ order.car.model }} ({{ order.car.year }})
          </p>
          <p class="text-sm text-gray-600">Гос. номер: {{ order.car.state_number }}</p>
          <p class="text-sm text-gray-600">VIN: {{ order.car.vin }}</p>
        </div>

        <div class="flex flex-col gap-4">
          <div>
            <h3 class="font-semibold mb-1 text-gray-500 uppercase text-xs">Администратор</h3>
            <el-select
              v-model="order.responsible_admin_id"
              placeholder="Не назначен"
              class="w-full"
              :disabled="isOrderFinished"
              @change="setResponsibleAdmin"
            >
              <el-option
                v-for="admin in admins"
                :key="admin.id"
                :label="formatWorkerName(admin)"
                :value="admin.id"
              />
            </el-select>
          </div>
          <div>
            <h3 class="font-semibold mb-1 text-gray-500 uppercase text-xs">Механик</h3>
            <el-select
              v-model="order.responsible_mechanic_id"
              placeholder="Не назначен"
              class="w-full"
              :disabled="isOrderFinished"
              @change="setResponsibleMechanic"
            >
              <el-option
                v-for="mech in mechanics"
                :key="mech.id"
                :label="formatWorkerName(mech)"
                :value="mech.id"
              />
            </el-select>
          </div>
        </div>

        <div class="md:col-span-3 flex justify-end gap-2 border-t pt-4 mt-2">
          <el-button v-if="!order.paid_date && !order.closed_date" type="success" @click="payOrder">
            Оплачен
          </el-button>
          <el-button v-if="order.paid_date && !order.closed_date" type="danger" @click="closeOrder">
            Закрыть
          </el-button>
        </div>
      </div>
    </el-card>

    <el-card>
      <div class="flex justify-between items-center mb-4">
        <el-radio-group v-model="activeTab">
          <el-radio-button label="works">Работы</el-radio-button>
          <el-radio-button label="details">Запчасти</el-radio-button>
        </el-radio-group>
        <el-button
          v-if="!order.paid_date && !order.closed_date"
          type="primary"
          @click="openAddDialog"
        >
          Добавить {{ activeTab === 'works' ? 'работу' : 'запчасть' }}
        </el-button>
      </div>

      <OrderItemsTable
        v-if="activeTab === 'works'"
        :items="order.works"
        :readonly="isOrderFinished"
        @edit="openEditDialog"
      />
      <OrderItemsTable
        v-if="activeTab === 'details'"
        :items="order.details"
        :readonly="isOrderFinished"
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
  <div v-else class="p-10 text-center">Загрузка данных...</div>
</template>
