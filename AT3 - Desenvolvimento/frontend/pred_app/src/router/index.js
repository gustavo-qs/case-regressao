import { createRouter, createWebHistory } from 'vue-router';
import HomeView        from '../views/HomeView.vue';
import UsersView       from '../views/UsersView.vue';
import PredictionsView from '../views/PredictionsView.vue';
import HistoryView     from '../views/HistoryView.vue';
import LoginView       from '../views/LoginView.vue';

const routes = [
  { path: '/login',      name: 'login',       component: LoginView },
  { path: '/',            name: 'home',        component: HomeView,        meta: { requiresAuth: true } },
  { path: '/users',       name: 'users',       component: UsersView,       meta: { requiresAuth: true } },
  { path: '/predictions', name: 'predictions', component: PredictionsView, meta: { requiresAuth: true } },
  { path: '/history',     name: 'history',     component: HistoryView,     meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
});

// Navigation guard global
router.beforeEach((to, from, next) => {
  const authRequired = to.matched.some(record => record.meta.requiresAuth);
  const isLoggedIn   = !!localStorage.getItem('userSession');

  if (authRequired && !isLoggedIn) {
    return next('/login');
  }
  if (to.path === '/login' && isLoggedIn) {
    return next('/');
  }
  next();
});

export default router;