<script setup lang="ts">
import { RouterLink } from 'vue-router'

import {
  WORK_ORDER_NAME,
  LEFT_OVERS_NAME,
  PRICE_LIST_NAME,
  WORKERS_NAME,
  DEFECTS_NAME,
} from '@/router'

const navLinks = [
  { text: 'Заказ наряд', name: WORK_ORDER_NAME },
  { text: 'Остатки', name: LEFT_OVERS_NAME },
  { text: 'Прейскурант', name: PRICE_LIST_NAME },
  { text: 'Работники', name: WORKERS_NAME },
  { text: 'Дефекты', name: DEFECTS_NAME },
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

.router-link-exact-active {
  background-color: #5cbaba;
  cursor: default;
  pointer-events: none;
}
</style>
