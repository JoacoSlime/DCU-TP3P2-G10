<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { obtenerPuntoPorId } from '@/services/puntosService.js'
import { computed } from 'vue'
import MigasDePan from '@/components/MigasPan.vue'

const route = useRoute()
const punto = ref(null)

onMounted(async () => {
    const id = route.params.id
    punto.value = await obtenerPuntoPorId(id)
})
const migas = computed(() => [
    {
        texto: 'Inicio',
        ruta: '/'
    },
    {
        texto: 'Listado de puntos',
        ruta: '/listado-puntos'
    },
    {
        texto: punto.value?.nombre || 'Punto'
    }
])
</script>

<template>
    <div v-if="punto">
        <MigasDePan :items="migas" />
        <h2>{{ punto.nombre }}</h2>
        <p><strong>Nivel contaminación:</strong> {{ punto.contaminacion }}</p>
        <p><strong>Descripción:</strong> {{ punto.descripcion }}</p>
        <p><strong>Colaborador:</strong> {{ punto.colaborador }}</p>
        <p><strong>Fecha creación:</strong> {{ punto.fechaCreacion }}</p>
        <div>
            <router-link :to="`/punto/${punto.id}/agregar-medicion`">Agregar medición</router-link>
            |
            <router-link :to="`/punto/${punto.id}/historial`">Ver datos históricos</router-link>
        </div>
    </div>
    <div v-else>Cargando...</div>
</template>
