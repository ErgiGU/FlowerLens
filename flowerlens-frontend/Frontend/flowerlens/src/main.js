import { createApp, ref } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import axios from 'axios'


const app = createApp(App)

app.config.globalProperties.$axios = axios


app.use(router)

app.mount('#app')