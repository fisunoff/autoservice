import { createRouter, createWebHistory } from 'vue-router'
import PageWorkOrder from '@/models/workOrder/PageWorkOrder.vue'
import PageApp from '@/pages/PageApp.vue'
import PageAuth from '@/pages/PageAuth.vue'
import PageDefects from '@/models/defects/PageDefects.vue'
import PageLeftovers from '@/models/leftovers/PageLeftovers.vue'
import PagePriceList from '@/models/priceList/PagePriceList.vue'
import PageWorkers from '@/models/workers/PageWorkers.vue'
import PageLogin from '@/models/login/PageLogin.vue'
import PageRegister from '@/models/login/PageRegister.vue'
import { getLocalAccessToken } from '@/api/tokensSrvices.ts'
import PageWorkOrdersList from '@/models/workOrder/PageWorkOrdersList.vue'
import PageCustomers from '@/models/customers/PageCustomers.vue'
import PageCars from '@/models/cars/PageCars.vue'
import WikiPage from '@/models/wiki/WikiPage.vue'

export const WORK_ORDERS_NAME = 'workOrders'
export const WORK_ORDERS_ROUTE = ''
export const WORK_ORDER_NAME = 'workOrder'
export const WORK_ORDER_ROUTE = 'work_order/:id'
export const DEFECTS_NAME = 'defects'
export const DEFECTS_ROUTE = 'defects'
export const LEFT_OVERS_NAME = 'leftOvers'
export const LEFT_OVERS_ROUTE = 'left_overs'
export const PRICE_LIST_NAME = 'priceList'
export const PRICE_LIST_ROUTE = 'price_list'
export const WORKERS_NAME = 'workers'
export const WORKERS_ROUTE = 'workers'
export const LOGIN_NAME = 'login'
export const LOGIN_ROUTE = ''
export const REGISTER_NAME = 'register'
export const REGISTER_ROUTE = 'register'
export const CUSTOMER_NAME = 'customer'
export const CUSTOMER_ROUTE = 'customer'
export const CARS_NAME = 'car'
export const CARS_ROUTE = 'car'
export const WIKI_NAME = 'wiki'
export const WIKI_ROUTE = 'wiki'

// const user = useUserStore();
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      name: 'app',
      path: '/',
      meta: { requiresAuth: true },
      component: PageApp,
      children: [
        {
          name: WORK_ORDER_NAME,
          path: WORK_ORDER_ROUTE,
          component: PageWorkOrder,
        },
        {
          name: WORK_ORDERS_NAME,
          path: WORK_ORDERS_ROUTE,
          component: PageWorkOrdersList,
        },
        {
          name: DEFECTS_NAME,
          path: DEFECTS_ROUTE,
          component: PageDefects,
        },
        {
          name: LEFT_OVERS_NAME,
          path: LEFT_OVERS_ROUTE,
          component: PageLeftovers,
        },
        {
          name: PRICE_LIST_NAME,
          path: PRICE_LIST_ROUTE,
          component: PagePriceList,
        },
        {
          name: WORKERS_NAME,
          path: WORKERS_ROUTE,
          component: PageWorkers,
        },
        {
          name: CUSTOMER_NAME,
          path: CUSTOMER_ROUTE,
          component: PageCustomers,
        },
        {
          name: CARS_NAME,
          path: CARS_ROUTE,
          component: PageCars,
        },
        {
          name: WIKI_NAME,
          path: WIKI_ROUTE,
          component: WikiPage,
        },
      ],
    },
    {
      name: 'auth',
      path: '/auth',
      meta: { requiresAuth: false },
      component: PageAuth,
      children: [
        {
          name: LOGIN_NAME,
          path: LOGIN_ROUTE,
          component: PageLogin,
        },
        {
          name: REGISTER_NAME,
          path: REGISTER_ROUTE,
          component: PageRegister,
        },
      ],
    },
  ],
})

router.beforeEach((to) => {
  const token = getLocalAccessToken()
  if (to.meta.requiresAuth && token == null) {
    return {
      name: LOGIN_NAME,
      query: { redirect: to.fullPath },
    }
  }
})
export default router
