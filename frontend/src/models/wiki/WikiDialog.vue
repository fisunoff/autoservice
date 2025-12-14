<script setup lang="ts">
import { computed, reactive, watch } from 'vue'
import type { WikiItem } from './WikiPage.vue'
import api from '@/api/api'
import type { Car } from '../workOrder/PageWorkOrdersList.vue'
import { ref } from 'vue'

type NewWiki = Partial<WikiItem>

const props = defineProps<{
  item?: NewWiki
  visible: boolean
}>()
const emit = defineEmits(['update:visible', 'save'])

const defaultNewItem: NewWiki = {
  syndrome: '',
  solution: '',
  brands: [],
}
const newItemForm = ref<NewWiki>({})
const carsList = reactive<Car[]>([])
const fetchBrands = async () => {
  const cars = await api.options(`/wiki`)
  carsList.splice(0, carsList.length, ...cars.data.options.brands)
}

watch(
  () => props.visible,
  async (newValue) => {
    await fetchBrands()
    if (newValue) {
      if (props.item) {
        newItemForm.value = {
          ...props.item,
        }
      } else {
        newItemForm.value = { ...defaultNewItem }
      }
    }
  },
)

const handleSaveClick = () => {
  emit('save', newItemForm.value)
}

const handleClose = () => {
  emit('update:visible', false)
}

const title = computed(() =>
  newItemForm.value.id ? 'Изменить запись базы знаний' : 'Добавить новую запись в базу знаний',
)
</script>

<template>
  <el-dialog :model-value="visible" :title="title" width="800px" @close="handleClose">
    <el-form :model="newItemForm" label-width="150px">
      <el-form-item label="Проблема">
        <el-input v-model="newItemForm.syndrome" />
      </el-form-item>
      <el-form-item label="Решение">
        <el-input v-model="newItemForm.solution" type="textarea" :rows="3" />
      </el-form-item>
      <el-form-item label="Бренд автомобиля">
        <el-select
          v-model="newItemForm.brands"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder=""
          style="width: 100%"
        >
          <el-option v-for="brand in carsList" :key="brand" :label="brand" :value="brand" />
        </el-select>
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="handleClose">Отмена</el-button>
        <el-button type="primary" @click="handleSaveClick">Сохранить</el-button>
      </span>
    </template>
  </el-dialog>
</template>
