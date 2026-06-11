<script setup>
defineProps({
    visible: Boolean,
    medicion: Object
})
const emit = defineEmits(['confirmar', 'cancelar'])

function confirmar() { emit('confirmar') }
function cancelar() { emit('cancelar') }
</script>

<template>
    <div v-if="visible" class="modal-overlay" @click.self="cancelar">
        <div class="modal-contenido">
            <h3>¿Estás seguro de que quieres eliminar la siguiente medición?</h3>
            <div class="info-medicion">
                <p><strong>Fecha:</strong> {{ medicion.fecha }}</p>
                <p><strong>Medición:</strong> {{ medicion.medicion }}</p>
                <p><strong>Colaborador:</strong> {{ medicion.colaborador }}</p>
            </div>
            <div class="acciones-modal">
                <button @click="cancelar" class="boton-cancelar">Cancelar</button>
                <button @click="confirmar" class="boton-eliminar">Eliminar medición</button>
            </div>
        </div>
    </div>
</template>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-contenido {
    background: white;
    padding: 2rem;
    border-radius: 16px;
    max-width: 500px;
    width: 90%;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.info-medicion {
    margin: 1rem 0;
    background: #f9f9f9;
    padding: 1rem;
    border-radius: 8px;
}

.acciones-modal {
    display: flex;
    gap: 1rem;
    justify-content: flex-end;
}

.boton-cancelar,
.boton-eliminar {
    padding: 8px 20px;
    border-radius: 30px;
    border: none;
    cursor: pointer;
}

.boton-cancelar {
    background: #95a5a6;
    color: white;
}

.boton-eliminar {
    background: #e74c3c;
    color: white;
}

.boton-eliminar:hover {
    background: #c0392b;
}
</style>