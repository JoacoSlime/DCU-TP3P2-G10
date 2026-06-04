import { createRouter, createWebHashHistory } from 'vue-router'
import VistaInicioView from '@/views/VistaInicioView.vue'
import DetallePuntoView from '@/views/DetallePuntoView.vue'
import HistorialMedicionesView from '@/views/HistorialMedicionesView.vue'
import AgregarPuntoView from '@/views/AgregarPuntoView.vue'
import AgregarMedicionView from '@/views/AgregarMedicionView.vue'
import IniciarSesionView from '@/views/IniciarSesionView.vue'
import CambiarEmailView from '@/views/CambiarEmailView.vue'
import CambiarContrasenaView from '@/views/CambiarContrasenaView.vue'
import InvitarColaboradorView from '@/views/InvitarColaboradorView.vue'
import RegistrarContrasenaView from '@/views/RegistrarContrasenaView.vue'
import AjustesView from '@/views/AjustesView.vue'
import ListadoPuntosView from '@/views/ListadoPuntosView.vue'

const routes = [
  { path: '/', component: VistaInicioView },
  { path: '/punto/:id', component: DetallePuntoView },
  { path: '/punto/:id/historial', component: HistorialMedicionesView },
  { path: '/agregar-punto', component: AgregarPuntoView },
  { path: '/punto/:id/agregar-medicion', component: AgregarMedicionView },
  { path: '/login', component: IniciarSesionView },
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
