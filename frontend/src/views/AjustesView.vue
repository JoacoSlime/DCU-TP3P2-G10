<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MigasDePan from '@/components/MigasPan.vue'
import IniciarSesionModal from '@/components/IniciarSesionModal.vue'
import { esAdmin, logout, obtenerUsuarioActual } from '@/services/authService.js'

const router = useRouter()
const isAdmin = ref(false)
const logueado = ref(false)
const rol = ref('')
const mostrarLogin = ref(false)

onMounted(async () => {
    await cargarEstado()
})

async function cargarEstado() {
    const usuario = await obtenerUsuarioActual()
    logueado.value = !!usuario
    rol.value = usuario?.rol || localStorage.getItem('role') || 'invitado'
    isAdmin.value = await esAdmin()
}

const migas = [
    { texto: 'Inicio', ruta: '/' },
    { texto: 'Ajustes', ruta: null }
]

function abrirLogin() {
    mostrarLogin.value = true
}

function cerrarLogin() {
    mostrarLogin.value = false
}

async function manejarLoginExitoso() {
    mostrarLogin.value = false
    await cargarEstado()  // Recargar el estado del usuario
}

function cambiarTema() {
    document.body.classList.toggle('dark-theme')
}

function irACambiarEmail() {
    router.push('/cambiar-email')
}

function irACambiarContrasena() {
    router.push('/cambiar-contrasena')
}

function irAInvitar() {
    router.push('/invitar')
}

async function cerrarSesion() {
    await logout()
    await cargarEstado()
    router.push('/')
}
</script>
<template>
    <div>
        <MigasDePan :items="migas" />
        <h2 class="titulo-seccion">Ajustes</h2>
        <!-- Opciones de apariencia -->
        <div class="seccion">
            <h3>Opciones de apariencia</h3>
            <button @click="cambiarTema" class="boton-secundario">Cambiar tema</button>
        </div>
        <!-- USUARIO INVITADO -->
        <div v-if="rol === 'invitado' || !logueado" class="seccion invitado">
            <h3>Opciones de cuenta</h3>
            <p class="mensaje-invitado">
                Iniciá sesión para acceder a más opciones como cambiar tu email, contraseña y más.
            </p>
            <button @click="abrirLogin" class="boton-iniciar-sesion">
                Iniciar sesión
            </button>
        </div>

        <!-- USUARIO LOGUEADO -->
        <template v-else>


            <!-- Opciones de cuenta -->
            <div class="seccion">
                <h3>Opciones de cuenta</h3>
                <div class="grupo-botones">
                    <button @click="irACambiarEmail" class="boton-opcion">Cambiar mi correo</button>
                    <button @click="irACambiarContrasena" class="boton-opcion">Cambiar mi contraseña</button>
                </div>
            </div>

            <!-- Opciones de administrador -->
            <div class="seccion" v-if="isAdmin">
                <h3>Opciones de administrador</h3>
                <div class="grupo-botones">
                    <button @click="irAInvitar" class="boton-opcion">Invitar colaborador</button>
                </div>
            </div>

            <div class="accion-final">
                <button @click="cerrarSesion" class="boton-cerrar">Cerrar sesión</button>
            </div>
        </template>
    </div>

    <IniciarSesionModal v-if="mostrarLogin" @close="cerrarLogin" @login-success="manejarLoginExitoso" />
</template>



<style scoped>
.titulo-seccion {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    color: var(--gris-oscuro, #2c3e50);
    text-align: center;
    font-weight: 600;
}

.seccion {
    background: white;
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.seccion h3 {
    margin-top: 0;
    margin-bottom: 1rem;
    color: var(--gris-oscuro, #2c3e50);
    font-size: 1.2rem;
    text-align: center;
}

.grupo-botones {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    justify-content: center;
}

.boton-opcion {
    background: #ecf0f1;
    border: none;
    padding: 10px 20px;
    border-radius: 30px;
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
    transition: background 0.2s;
}

.boton-opcion:hover {
    background: var(--verde, #2ecc71);
    color: white;
}

.boton-secundario {
    background: #ecf0f1;
    border: none;
    padding: 8px 20px;
    border-radius: 30px;
    cursor: pointer;
    font-weight: 500;
    transition: background 0.2s;
}

.boton-secundario:hover {
    background: var(--verde, #2ecc71);
    color: white;
}

.invitado {
    background: #f8fafc;
    border: 2px dashed #cbd5e0;
}

.mensaje-invitado {
    color: #4a5568;
    font-size: 1rem;
    margin-bottom: 1.5rem;
}

.boton-iniciar-sesion {
    background: var(--verde, #2ecc71);
    color: white;
    border: none;
    padding: 10px 30px;
    border-radius: 30px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.2s;
}

.boton-iniciar-sesion:hover {
    background: var(--verde-oscuro, #27ae60);
}

.accion-final {
    margin-top: 2rem;
    text-align: center;
}

.boton-cerrar {
    background: #e74c3c;
    color: white;
    border: none;
    padding: 10px 24px;
    border-radius: 30px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.2s;
}

.boton-cerrar:hover {
    background: #c0392b;
}
</style>