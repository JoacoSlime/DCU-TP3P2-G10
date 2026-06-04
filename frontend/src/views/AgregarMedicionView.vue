<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MigasDePan from '@/components/MigasPan.vue'
import { crearMedicion } from '@/services/medicionesService.js'

const route = useRoute()
const router = useRouter()
const medicion = ref('')
const puntoId = route.params.id

const migas = [
    { texto: 'Inicio', ruta: '/' },
    { texto: `Punto ${puntoId}`, ruta: `/punto/${puntoId}` },
    { texto: 'Agregar medición', ruta: null }
]

async function guardar() {
    try {
        await crearMedicion(puntoId, { medicion: medicion.value })
        router.push(`/punto/${puntoId}`)
    } catch (err) {
        alert('Error al guardar la medición: ' + err.message)
    }
}
</script>
<template>
    <div>
        <MigasDePan :items="migas" />
        <h2 class="titulo-seccion">Agregar medición</h2>

        <form @submit.prevent="guardar" class="formulario">
            <div class="campo">
                <label>Medición *</label>
                <textarea v-model="medicion" rows="4" required placeholder="Ej: Medición de ejemplo..."></textarea>
            </div>
            <div class="acciones">
                <button type="submit" class="boton">Guardar medición</button>
                <button type="button" class="boton boton-cancelar" @click="$router.back()">Cancelar</button>
            </div>
        </form>
    </div>
</template>

<style scoped>
.titulo-seccion {
    font-size: 1.8rem;
    margin-bottom: 1.5rem;
    color: var(--gris-oscuro, #2c3e50);
    text-align: center;
    font-weight: 600;
}

.formulario {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.campo {
    margin-bottom: 1.2rem;
}

.campo label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: #333;
}

.campo textarea {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 1rem;
    font-family: inherit;
    resize: vertical;
    transition: border 0.2s;
}

.campo textarea:focus {
    outline: none;
    border-color: var(--verde, #2ecc71);
    box-shadow: 0 0 0 2px rgba(46, 204, 113, 0.2);
}

.acciones {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 1.5rem;
}

.boton {
    background: #ecf0f1;
    border: none;
    padding: 10px 24px;
    border-radius: 30px;
    font-size: 1rem;
    cursor: pointer;
}

.boton:hover {
    background: var(--verde, #2ecc71);
    color: white;
}

.boton-cancelar {
    background: #ecf0f1;
    font-weight: normal;
}

.boton-cancelar:hover {
    background: #bdc3c7;
    color: #333;
}
</style>