<script setup lang="ts">
import { RouterLink } from 'vue-router'

import {
  PRICE_LIST_NAME,
  WORKERS_NAME,
  WORK_ORDERS_NAME,
  CUSTOMER_NAME,
  CARS_NAME,
  WIKI_NAME,
} from '@/router'

const navLinks = [
  { text: 'Заказ наряд', name: WORK_ORDERS_NAME },
  { text: 'Прейскурант', name: PRICE_LIST_NAME },
  { text: 'Работники', name: WORKERS_NAME },
  { text: 'Клиенты', name: CUSTOMER_NAME },
  { text: 'Автомобили', name: CARS_NAME },
  { text: 'База знаний', name: WIKI_NAME },
]
</script>

<template>
  <header class="app-header">
    <nav class="navigation">
      <RouterLink
        v-for="link in navLinks"
        :key="link.name"
        :to="{ name: link.name }"
        class="nav-button"
      >
        {{ link.text }}
      </RouterLink>
    </nav>
  </header>
</template>

<style scoped>
.app-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-color: #ffffff;
  border-bottom: 1px solid black;
}

.navigation {
  width: 100%;

  display: flex;
  gap: 0 10px;
}

.nav-button {
  font-size: 32px;
  text-align: center;
  width: 20%;
  display: inline-block;
  padding: 12px 24px;
  background-color: #67dada6b;
  text-decoration: none;
  font-weight: bold;
  border: none;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.nav-button:hover {
  background-color: #80cbc4;
}
</style>
