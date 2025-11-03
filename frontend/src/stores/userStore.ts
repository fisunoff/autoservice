import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import api from '@/api/api.ts'

export const useUserStore = defineStore('user', ()=>{
  const surname = ref('')
  const name = ref('')
  const patronymic = ref('')
  const id = ref('')
  const isAdmin = ref(false)
  const isMechanic = ref(false)

  const fio = computed(()=> `${surname.value} ${name.value}`)
  const fetchProfile = async() => {
    const response = (await api.get('worker/me')).data
    surname.value = response?.surname
    name.value = response?.name
    patronymic.value = response?.patronymic
    isAdmin.value = response?.is_admin
    isMechanic.value = response?.is_mechanic


    console.log(response.data)

  }
  return {fio, fetchProfile, isAdmin, isMechanic}
})