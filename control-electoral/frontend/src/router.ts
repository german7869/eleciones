import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import Resultados from './views/Resultados.vue';
import ReporteVotos from './views/ReporteVotos.vue';
import SubirActa from './views/SubirActa.vue';
import MisJuntas from './views/MisJuntas.vue';
import NotFound from './views/NotFound.vue';
import Delegados from './views/Admin/Delegados.vue';
import Partidos from './views/Admin/Partidos.vue';
import Territorios from './views/Admin/Territorios.vue';
import AsignarDelegados from './views/Admin/AsignarDelegados.vue';
import CambiarClavesDelegados from './views/Admin/CambiarClavesDelegados.vue';
import AsignarJuntasDelegados from './views/Admin/AsignarJuntasDelegados.vue';
import ResumenJuntas from './views/Admin/ResumenJuntas.vue';

function getRol(): string {
  const token = localStorage.getItem('token');
  if (!token) return '';
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return payload.rol || '';
  } catch { return ''; }
}

const routes: Array<RouteRecordRaw> = [
  { path: '/', name: 'Home', component: Home },
  { path: '/login', name: 'Login', component: Login },
  { path: '/resultados', name: 'Resultados', component: Resultados },
  { path: '/reporte', name: 'ReporteVotos', component: ReporteVotos, meta: { requiresAuth: true } },
  { path: '/ingreso-votos', name: 'IngresarVotos', component: ReporteVotos, meta: { requiresAuth: true } },
  { path: '/acta', name: 'SubirActa', component: SubirActa, meta: { requiresAuth: true } },
  { path: '/mis-juntas', name: 'MisJuntas', component: MisJuntas, meta: { requiresAuth: true, requiresDelegado: true } },
  { path: '/admin/delegados', name: 'AdminDelegados', component: Delegados, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/partidos', name: 'AdminPartidos', component: Partidos, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/territorios', name: 'AdminTerritorios', component: Territorios, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/asignar-delegados', name: 'AdminAsignarDelegados', component: AsignarDelegados, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/asignar-juntas', name: 'AdminAsignarJuntas', component: AsignarJuntasDelegados, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/cambiar-claves', name: 'AdminCambiarClaves', component: CambiarClavesDelegados, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/resumen-juntas', name: 'AdminResumenJuntas', component: ResumenJuntas, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token');
  const rol = getRol();
  
  if (to.meta.requiresAuth && !token) {
    next({ name: 'Login' });
    return;
  }
  
  if (to.meta.requiresAdmin && rol !== 'admin') {
    next({ name: 'Home' });
    return;
  }
  
  if (to.meta.requiresDelegado && rol !== 'delegado') {
    next({ name: 'Home' });
    return;
  }
  
  next();
});

export default router;
