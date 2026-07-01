import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/main.css'

import { API_URL } from './config'

console.log('Usando la api ' + API_URL)

const app = createApp(App)
app.use(router)
app.provide('API_URL', API_URL)
app.mount('#app')
