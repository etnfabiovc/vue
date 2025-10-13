import { createRouter, createWebHistory } from 'vue-router'

import Home from '../views/Home.vue'
import Tasks from '../views/Tasks.vue'
import Contador from '../views/Contador.vue'

const routes = [
  { path: '/', name: 'home', component: Home },
  { path: '/tasks', name: 'tasks', component: Tasks},
  { path: '/counter', name: 'counter', component: Contador}
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;