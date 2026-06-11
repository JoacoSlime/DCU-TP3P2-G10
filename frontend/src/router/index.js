import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import MapaView from '../views/MapaView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: MapaView,
    },
    {
      path: '/ayuda',
      name: 'Ayuda',
      component: () => import('../views/AyudaView.vue'),
    },
    {
      path: '/iniciar-sesion',
      name: 'Iniciar sesion',
      component: () => import('../views/IniciarSesionView.vue'),
    },
    {
      path: '/elegir-usuario',
      name: 'Elegir usuario',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ElegirUsuarioView.vue'),
    },
    {
      path: '/usuario-invitado',
      name: 'Usuario invitado',
      component: () => import('../views/InvitadoView.vue'),
    },
    {
      path: '/usuario-colaborador',
      name: 'Usuario colaborador',
      component: () => import('../views/ColaboradorView.vue'),
    },
     {
      path: '/mapa',
      name: 'Mapa',
      component: () => import('../views/MapaView.vue'),
    },
    {
      path: '/lista-puntos',
      name: 'ListaPuntos',
      component: () => import('../views/ListaPuntosView.vue'),
    },
    {
      path: '/lista-puntos/punto/:id',
      name: 'PuntoContaminado',
      component: () => import('../views/PuntoView.vue'),
    },
  ],
})

export default router
