<script setup>
import { reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MigasDePan from '@/components/MigasPan.vue'
import { crearMedicion } from '@/services/medicionesService.js'

const route = useRoute()
const router = useRouter()
const puntoId = route.params.id

const form = reactive({
    items_per_m2: 0,
    weight: 0,
    area: 0,
    pet: 0,
    pead: 0,
    pebd: 0,
    pvc: 0,
    pp: 0,
    ps: 0,
    pa: 0,
    other: 0,
    ihr_plata: 0,
    ibirp: 0
})

const migas = [
    { texto: 'Inicio', ruta: '/' },
    { texto: `Punto`, ruta: `/punto/${puntoId}` },
    { texto: 'Agregar medición', ruta: null }
]

async function guardar() {
    try {
        await crearMedicion(puntoId, form)
        router.push(`/punto/${puntoId}/historial`)
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
                <label>Items por m² *</label>
                <input v-model.number="form.items_per_m2" type="number" step="0.01" required placeholder="Ej: 150.00">
            </div>

            <div class="campo">
                <label>Peso (kg) *</label>
                <input v-model.number="form.weight" type="number" step="0.01" required placeholder="Ej: 73.50">
            </div>

            <div class="campo">
                <label>Área (m²) *</label>
                <input v-model.number="form.area" type="number" step="0.01" required placeholder="Ej: 5913253.00">
            </div>

            <h4 class="subtitulo">Tipos de residuos</h4>

            <div class="row-campos">
                <div class="campo">
                    <label>PET</label>
                    <input v-model.number="form.pet" type="number" min="0">
                </div>
                <div class="campo">
                    <label>PEAD</label>
                    <input v-model.number="form.pead" type="number" min="0">
                </div>
                <div class="campo">
                    <label>PEBD</label>
                    <input v-model.number="form.pebd" type="number" min="0">
                </div>
                <div class="campo">
                    <label>PVC</label>
                    <input v-model.number="form.pvc" type="number" min="0">
                </div>
            </div>

            <div class="row-campos">
                <div class="campo">
                    <label>PP</label>
                    <input v-model.number="form.pp" type="number" min="0">
                </div>
                <div class="campo">
                    <label>PS</label>
                    <input v-model.number="form.ps" type="number" min="0">
                </div>
                <div class="campo">
                    <label>PA</label>
                    <input v-model.number="form.pa" type="number" min="0">
                </div>
                <div class="campo">
                    <label>Otros</label>
                    <input v-model.number="form.other" type="number" min="0">
                </div>
            </div>

            <div class="row-campos">
                <div class="campo">
                    <label>IHR Plata</label>
                    <input v-model.number="form.ihr_plata" type="number" step="0.01" placeholder="0.00">
                </div>
                <div class="campo">
                    <label>IBIRP</label>
                    <input v-model.number="form.ibirp" type="number" step="0.01" placeholder="0.00">
                </div>
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

.subtitulo {
    font-size: 1.2rem;
    margin: 1.5rem 0 1rem 0;
    color: var(--gris-oscuro, #2c3e50);
    border-bottom: 2px solid var(--verde, #2ecc71);
    padding-bottom: 0.5rem;
}

.formulario {
    max-width: 700px;
    margin: 0 auto;
    background: white;
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.campo {
    margin-bottom: 1rem;
}

.campo label {
    display: block;
    margin-bottom: 0.3rem;
    font-weight: 600;
    color: #333;
    font-size: 0.9rem;
}

.campo input {
    width: 100%;
    padding: 10px 12px;
    border: 1px solid #ccc;
    border-radius: 8px;
    font-size: 1rem;
    transition: border 0.2s;
}

.campo input:focus {
    outline: none;
    border-color: var(--verde, #2ecc71);
    box-shadow: 0 0 0 2px rgba(46, 204, 113, 0.2);
}

.row-campos {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 0.8rem;
}

.row-campos .campo input {
    padding: 8px 10px;
    font-size: 0.9rem;
}

.acciones {
    display: flex;
    gap: 1rem;
    justify-content: center;
    margin-top: 1.5rem;
}

.boton {
    background: var(--verde, #2ecc71);
    color: white;
    border: none;
    padding: 10px 28px;
    border-radius: 30px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: background 0.2s;
}

.boton:hover {
    background: var(--verde-oscuro, #27ae60);
}

.boton-cancelar {
    background: #95a5a6;
}

.boton-cancelar:hover {
    background: #7f8c8d;
}

@media (max-width: 600px) {
    .row-campos {
        grid-template-columns: 1fr 1fr;
    }
}
</style>