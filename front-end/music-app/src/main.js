import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import store from './store/store'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App);
app.use(router)
app.use(store)
app.use(ElementPlus)
app.mount('#app');

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
  }

