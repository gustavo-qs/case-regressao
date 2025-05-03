import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import UsersView from '../views/UsersView.vue'
import PredictionsView from '../views/PredictionsView.vue'
import HistoryView from '../views/HistoryView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/users',
      name: 'users',
      component: UsersView
    },
    {
      path: '/predictions',
      name: 'predictions',
      component: PredictionsView
    },
    {
      path: '/history',
      name: 'history',
      component: HistoryView
    }      
  ],
})

export default router
