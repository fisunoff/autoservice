<script setup lang="ts">
import { computed, reactive, watch, ref } from 'vue'
import type { WikiItem } from './WikiPage.vue'
import api from '@/api/api'

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
  components: [],
}

const newItemForm = ref<NewWiki>({})
const carsList = reactive<string[]>([])
const componentsList = reactive<string[]>([])

const fetchOptions = async () => {
  try {
    const response = await api.options(`/wiki`)
    carsList.splice(0, carsList.length, ...(response.data.options?.brands || []))
    componentsList.splice(0, componentsList.length, ...(response.data.options?.components || []))
  } catch (e) {
    console.error(e)
  }
}

watch(
  () => props.visible,
  async (newValue) => {
    if (newValue) {
      await fetchOptions()
      if (props.item) {
        newItemForm.value = JSON.parse(JSON.stringify(props.item)) // Глубокая копия
        if (!newItemForm.value.components) newItemForm.value.components = []
      } else {
        newItemForm.value = JSON.parse(JSON.stringify(defaultNewItem))
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
          placeholder="Выберите или введите бренд"
          style="width: 100%"
        >
          <el-option v-for="brand in carsList" :key="brand" :label="brand" :value="brand" />
        </el-select>
      </el-form-item>
      <el-form-item label="Агрегаты">
        <el-select
          v-model="newItemForm.components"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="Выберите или введите агрегат (Двигатель, КПП...)"
          style="width: 100%"
        >
          <el-option v-for="comp in componentsList" :key="comp" :label="comp" :value="comp" />
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
