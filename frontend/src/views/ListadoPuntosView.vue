<script setup>
import { ref, onMounted } from 'vue'
import MigasDePan from '@/components/MigasPan.vue'
import ModalConfirmacion from '@/components/ModalConfirmacionPunto.vue'
import { obtenerPuntos, eliminarPunto } from '@/services/puntosService.js'

const puntos = ref([])
const mostrarModal = ref(false)
const puntoSeleccionado = ref(null)

const migas = [
    { texto: 'Inicio', ruta: '/' },
    { texto: 'Listado de puntos', ruta: null }
]

onMounted(async () => {
    await cargarPuntos()
})

async function cargarPuntos() {
    puntos.value = await obtenerPuntos()
}

function abrirModalEliminar(punto) {
    puntoSeleccionado.value = punto
    mostrarModal.value = true
}

function cerrarModal() {
    mostrarModal.value = false
    puntoSeleccionado.value = null
}

async function eliminar() {
    try {
        await eliminarPunto(puntoSeleccionado.value.id)
        await cargarPuntos()
        cerrarModal()
    } catch (error) {
        alert('Error al eliminar: ' + error.message)
        cerrarModal()
    }
}
</script>
<template>
    <div>
        <MigasDePan :items="migas" />
        <h2>Listado de puntos contaminados</h2>
        <div style="margin-bottom: 1rem;">
            <router-link to="/agregar-punto" class="boton">
                + Agregar nuevo punto
            </router-link>
        </div>
        <ul>
            <li v-for="punto in puntos" :key="punto.id">
                <router-link :to="`/punto/${punto.id}`">{{ punto.nombre }}</router-link>
                <button @click="abrirModalEliminar(punto)">Eliminar</button>
            </li>
        </ul>

        <ModalConfirmacion :visible="mostrarModal" :punto="puntoSeleccionado" @confirmar="eliminar"
            @cancelar="cerrarModal" />
    </div>
</template>