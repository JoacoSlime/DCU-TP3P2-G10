<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import MigasDePan from '@/components/MigasPan.vue'
import { esAdmin, logout } from '@/services/authService.js'

const router = useRouter()
const isAdmin = ref(false)

onMounted(async () => {
    isAdmin.value = await esAdmin()
})

const migas = [
    { texto: 'Inicio', ruta: '/' },
    { texto: 'Ajustes', ruta: null }
]

function cambiarTema() {
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
    router.push('/login')
}
</script>

<template>
    <div>
        <MigasDePan :items="migas" />
        <h2 class="titulo-seccion">Ajustes</h2>
        <div class="seccion">
            <h3>Opciones de apariencia</h3>
            <button @click="cambiarTema" class="boton-secundario">Cambiar tema</button>
        </div>
        <div class="seccion">
            <h3>Opciones de cuenta</h3>
            <div class="grupo-botones">
                <button @click="irACambiarEmail" class="boton-opcion">Cambiar mi correo</button>
                <button @click="irACambiarContrasena" class="boton-opcion">Cambiar mi contraseña</button>
            </div>
        </div>
        <div class="seccion" v-if="isAdmin">
            <h3>Opciones de administrador</h3>
            <div class="grupo-botones">
                <button @click="irAInvitar" class="boton-opcion">Invitar colaborador</button>
            </div>
        </div>
        <div class="accion-final">
            <button @click="cerrarSesion" class="boton-cerrar">Cerrar sesión</button>
        </div>
    </div>
</template>

<style scoped>
.titulo-seccion {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    color: var(--gris-oscuro, #2c3e50);
    padding-left: 15px;
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
    font-size: 100;
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
}

.boton-opcion:hover {
    background: var(--verde);
}

.boton-secundario {
    background: #ecf0f1;
    border: none;
    padding: 8px 20px;
    border-radius: 30px;
    cursor: pointer;
    font-weight: 500;
}

.boton-secundario:hover {
    background: var(--verde);
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
}

.boton-cerrar:hover {
    background: #c0392b;
}
</style>