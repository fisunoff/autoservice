import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'

import App from './App.vue'
import router from './router'
import axios from 'axios'

const app = createApp(App)

// app.use(axios)
app.use(ElementPlus)
app.use(createPinia())
app.use(router)

app.mount('#app')
