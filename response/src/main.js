import "./assets/main.css"
import { createApp } from 'vue'
import App from './App.vue'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

import {createRouter,createWebHashHistory} from 'vue-router'
import general from './components/general.vue'
import Analys from './components/Analys.vue'

const start = {
    path:"/",
    name:"general",
    component:general
}

const datashow = {
    path:"/datashow",
    name:"datashow",
    component:Analys
}

const  routes = [start,datashow]
const router = createRouter({
    history:createWebHashHistory(),
    routes
})


const app = createApp(App);

app.use(router);

app.use(ElementPlus)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {//import the icon globally
    app.component(key, component)
}

app.mount('#app');
