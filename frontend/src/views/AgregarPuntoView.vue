<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import MigasDePan from '@/components/MigasPan.vue'
import { crearPunto } from '@/services/puntosService.js'

const router = useRouter()
const form = reactive({
    nombre: '',
    lat: 0,
    lng: 0,
    medicion: ''
})

const migas = [
    { texto: 'Inicio', ruta: '/' },
    { texto: 'Agregar punto', ruta: null }
]

async function guardar() {
    try {
        await crearPunto(form)
        router.push('/')
    } catch (err) {
        alert('Error al guardar el punto: ' + err.message)
    }
}
</script>
<template>
    <div>
        <MigasDePan :items="migas" />
        <h2 class="titulo-seccion">Agregar punto contaminado</h2>

        <form @submit.prevent="guardar" class="formulario">
            <div class="campo">
                <label>Nombre del punto *</label>
                <input v-model="form.nombre" required placeholder="Ej: Nombre">
            </div>
            <div class="campo">
                <label>Latitud *</label>
                <input v-model.number="form.lat" type="number" step="any" required>
            </div>
            <div class="campo">
                <label>Longitud *</label>
                <input v-model.number="form.lng" type="number" step="any" required>
            </div>
            <div class="campo">
                <label>Medicion</label>
                <textarea v-model="form.medicion" rows="3" placeholder="Medicion del punto..."></textarea>
            </div>
            <div class="acciones">
                <button type="submit" class="boton">Guardar punto</button>
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

.campo input,
.campo textarea,
.campo select {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 1rem;
    transition: border 0.2s;
}

.campo input:focus,
.campo textarea:focus,
.campo select:focus {
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
    background: var(--verde);
}


.boton-cancelar:hover {
    background: #bdc3c7;
}
</style>