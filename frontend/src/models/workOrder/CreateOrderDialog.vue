<script setup lang="ts">
import { reactive, watch } from 'vue'
import { ElMessage } from 'element-plus'
import type { NewOrderData, Customer, Car } from './PageWorkOrdersList.vue'

const props = defineProps<{
  visible: boolean
  customers: Customer[]
  cars: Car[]
}>()
const emit = defineEmits(['update:visible', 'save'])

const defaultOrderForm: NewOrderData = {
  customer_id: null,
  car_id: null,
  car_received: true,
  opened_date: new Date().toISOString().split('T')[0],
}
const newOrderForm = reactive<NewOrderData>({ ...defaultOrderForm })

watch(
  () => props.visible,
  (newValue) => {
    if (newValue) {
      Object.assign(newOrderForm, defaultOrderForm)
    }
  },
)

const handleSaveClick = () => {
  if (!newOrderForm.customer_id || !newOrderForm.car_id) {
    ElMessage.warning('Пожалуйста, выберите клиента и автомобиль.')
    return
  }
  emit('save', newOrderForm)
}

const handleClose = () => {
  emit('update:visible', false)
}
</script>

<template>
  <el-dialog
    :model-value="visible"
    title="Создать новый заказ-наряд"
    width="600px"
    @close="handleClose"
  >
    <el-form :model="newOrderForm" label-width="150px">
      <el-form-item label="Клиент" required>
        <el-select v-model="newOrderForm.customer_id" placeholder="Выберите клиента" filterable>
          <el-option
            v-for="customer in customers"
            :key="customer.id"
            :label="`${customer.surname} ${customer.name} (${customer.phone})`"
            :value="customer.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="Автомобиль" required>
        <el-select v-model="newOrderForm.car_id" placeholder="Выберите автомобиль" filterable>
          <el-option
            v-for="car in cars"
            :key="car.id"
            :label="`${car.brand} ${car.model} (${car.state_number})`"
            :value="car.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="Дата приема">
        <el-date-picker v-model="newOrderForm.opened_date" type="date" value-format="YYYY-MM-DD" />
      </el-form-item>

      <el-form-item label="Машина принята">
        <el-switch v-model="newOrderForm.car_received" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="handleClose">Отмена</el-button>
      <el-button type="primary" @click="handleSaveClick">Создать</el-button>
    </template>
  </el-dialog>
</template>
