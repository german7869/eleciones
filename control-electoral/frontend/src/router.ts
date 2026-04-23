import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import Resultados from './views/Resultados.vue';
import ReporteVotos from './views/ReporteVotos.vue';
import SubirActa from './views/SubirActa.vue';


const routes: Array<RouteRecordRaw> = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/resultados', name: 'Resultados', component: Resultados },
  { path: '/reporte', name: 'ReporteVotos', component: ReporteVotos, meta: { requiresAuth: true } },
  { path: '/acta', name: 'SubirActa', component: SubirActa, meta: { requiresAuth: true } },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('token');
    if (!token) {
      next({ name: 'Login' });
      return;
    }
  }
  next();
});

export default router;
