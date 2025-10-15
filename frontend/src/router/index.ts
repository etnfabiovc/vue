import { createRouter, createWebHistory } from "vue-router"
import Dashboard from "@/pages/Dashboard.vue"
import About from "@/pages/About.vue"

//services
import ReqPeri from "@/pages/ReqPeriForm.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "dashboard", component: Dashboard },
    { path: "/about", name: "about", component: About },
    { path: "/reqperi", name: "reqperi", component: ReqPeri },
  ],
})

export default router
