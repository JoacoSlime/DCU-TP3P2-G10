import { createRouter, createWebHashHistory } from 'vue-router'
import VistaInicioView from '@/views/VistaInicioView.vue'
import DetallePuntoView from '@/views/DetallePuntoView.vue'
import HistorialMedicionesView from '@/views/HistorialMedicionesView.vue'
import AgregarPuntoView from '@/views/AgregarPuntoView.vue'
import AgregarMedicionView from '@/views/AgregarMedicionView.vue'
import CambiarEmailView from '@/views/CambiarEmailView.vue'
import CambiarContrasenaView from '@/views/CambiarContrasenaView.vue'
import InvitarColaboradorView from '@/views/InvitarColaboradorView.vue'
import RegistrarContrasenaView from '@/views/RegistrarContrasenaView.vue'
import AjustesView from '@/views/AjustesView.vue'
import ListadoPuntosView from '@/views/ListadoPuntosView.vue'
import HomeView from '@/views/HomeView.vue'
import ElegirUsuarioView from '@/views/ElegirUsuarioView.vue'
import AyudaView from '@/views/AyudaView.vue'
import MapaView from '@/views/MapaView.vue'

const routes = [
  { path: '/elegir-usuario', component: ElegirUsuarioView },
  { path: '/ayuda', component: AyudaView },
  { path: '/', component: MapaView },
  { path: '/punto/:id', component: DetallePuntoView },
  { path: '/punto/:id/historial', component: HistorialMedicionesView },
  { path: '/agregar-punto', component: AgregarPuntoView },
  { path: '/punto/:id/agregar-medicion', component: AgregarMedicionView },
  { path: '/ajustes', component: AjustesView },
  { path: '/cambiar-email', component: CambiarEmailView },
  { path: '/cambiar-contrasena', component: CambiarContrasenaView },
  { path: '/invitar', component: InvitarColaboradorView },
  { path: '/registrar-contrasena', component: RegistrarContrasenaView },
  { path: '/listado-puntos', component: ListadoPuntosView },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
