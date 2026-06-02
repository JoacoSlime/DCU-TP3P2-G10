import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/ayuda',
      name: 'Ayuda',
      component: () => import('../views/AyudaView.vue'),
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
      path: '/capacitor',
      name: 'capacitor',
      component: () => import('../views/CapacitorView.vue'),
    },
  ],
})

export default router
