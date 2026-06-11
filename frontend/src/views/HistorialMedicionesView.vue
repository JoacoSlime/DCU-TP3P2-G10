<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import MigasDePan from '@/components/MigasPan.vue'
import ModalConfirmacionMedicion from '@/components/ModalConfirmacionMedicion.vue'
import { obtenerMedicionesPorPunto, eliminarMedicion } from '@/services/medicionesService.js'

const route = useRoute()
const puntoId = route.params.id
const mediciones = ref([])
const mostrarModal = ref(false)
const medicionSeleccionada = ref(null)

const migas = [
    { texto: 'Inicio', ruta: '/' },
    { texto: `Punto ${puntoId}`, ruta: `/punto/${puntoId}` },
    { texto: 'Datos históricos', ruta: null }
]

onMounted(async () => {
    await cargarMediciones()
})

async function cargarMediciones() {
    mediciones.value = await obtenerMedicionesPorPunto(puntoId)
}

function abrirModalEliminar(medicion) {
    medicionSeleccionada.value = medicion
    mostrarModal.value = true
}

function cerrarModal() {
    mostrarModal.value = false
    medicionSeleccionada.value = null
}

async function eliminar() {
    try {
        await eliminarMedicion(medicionSeleccionada.value.id)
        await cargarMediciones()
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
        <h2>Datos históricos</h2>

        <table border="1" cellpadding="8" style="border-collapse: collapse; width: 100%;">
            <thead>
                <tr>
                    <th>Fecha</th>
                    <th>Medición</th>
                    <th>Colaborador</th>
                    <th>Acciones</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="m in mediciones" :key="m.id">
                    <td>{{ m.fecha }}</td>
                    <td>{{ m.medicion }}</td>
                    <td>{{ m.colaborador }}</td>
                    <td>
                        <button @click="abrirModalEliminar(m)">Eliminar</button>
                    </td>
                </tr>
                <tr v-if="mediciones.length === 0">
                    <td colspan="4">No hay mediciones registradas.</td>
                </tr>
            </tbody>
        </table>

        <ModalConfirmacionMedicion :visible="mostrarModal" :medicion="medicionSeleccionada" @confirmar="eliminar"
            @cancelar="cerrarModal" />
    </div>
</template>