import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import Toast from 'vue-toastification'
import VueKonva from 'vue-konva'

// Styles
import './style.css'
import 'vue-toastification/dist/index.css'
import 'vue-loading-overlay/dist/css/index.css'

const app = createApp(App)
const pinia = createPinia()

// Plugins
app.use(pinia)
app.use(router)
app.use(VueKonva)
app.use(Toast, {
    position: 'top-right',
    timeout: 3000,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
})

app.mount('#app')