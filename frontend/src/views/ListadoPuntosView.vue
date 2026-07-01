<template>
  <div class="listado-container">
    <MigasDePan :items="migas" />

    <div class="listado-header">
      <h2 class="titulo-seccion">Listado de puntos contaminados</h2>
      <!-- Botón agregar: solo visible para usuarios autenticados -->
      <router-link v-if="botonAgregar" to="/agregar-punto" class="boton-agregar"
        aria-label="Agregar nuevo punto contaminado">
        <span aria-hidden="true">+</span> Agregar nuevo punto
      </router-link>
    </div>

    <!-- Contador de resultados -->
    <p class="contador" aria-live="polite">
      {{ puntos.length }} punto{{ puntos.length !== 1 ? 's' : '' }} encontrado{{ puntos.length !== 1 ? 's' : '' }}
    </p>

    <!-- Tabla de puntos -->
    <div class="tabla-wrapper" v-if="puntos.length > 0">
      <table class="tabla-puntos" role="table" aria-label="Lista de puntos contaminados">
        <thead>
          <tr>
            <th scope="col">#</th>
            <th scope="col">Nombre del punto</th>
            <th scope="col">Coordenadas</th>
            <th scope="col" class="col-acciones">Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(punto, index) in puntos" :key="punto.id">
            <td class="col-numero">{{ index + 1 }}</td>
            <td class="col-nombre">
              <router-link :to="`/punto/${punto.id}`" class="punto-enlace">
                {{ punto.nombre }}
              </router-link>
            </td>
            <td class="col-coordenadas">
              {{ punto.lat?.toFixed(4) }}, {{ punto.lng?.toFixed(4) }}
            </td>
            <td class="col-acciones">
              <div class="acciones-grupo">
                <router-link :to="`/punto/${punto.id}`" class="btn-ver" :aria-label="`Ver detalles de ${punto.nombre}`"
                  title="Ver detalles">
                  Ver
                </router-link>
                <!-- Botón eliminar: solo visible para admin -->
                <button v-if="botonEliminar" @click="abrirModalEliminar(punto)" class="btn-eliminar"
                  :aria-label="`Eliminar punto ${punto.nombre}`" title="Eliminar punto">
                  Eliminar
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Mensaje vacío -->
    <div v-else class="sin-resultados">
      <p>No hay puntos contaminados registrados.</p>
      <router-link v-if="botonAgregar" to="/agregar-punto" class="boton-agregar">
        + Agregar el primer punto
      </router-link>
    </div>

    <!-- Modal de confirmación -->
    <ModalConfirmacion :visible="mostrarModal" :punto="puntoSeleccionado" @confirmar="eliminar"
      @cancelar="cerrarModal" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import MigasDePan from '@/components/MigasPan.vue'
import ModalConfirmacion from '@/components/ModalConfirmacionPunto.vue'
import { obtenerPuntos, eliminarPunto } from '@/services/puntosService.js'
import { obtenerUsuarioActual, tienePermiso } from '@/services/authService.js'

const puntos = ref([])
const mostrarModal = ref(false)
const puntoSeleccionado = ref(null)
const estaLogueado = ref(false)
const botonEliminar = ref(false)
const botonAgregar = ref(false)

const migas = [
  { texto: 'Inicio', ruta: '/' },
  { texto: 'Listado de puntos', ruta: null }
]

onMounted(async () => {
  await cargarPuntos()
  tienePermiso('spots.remove').then((res) => (botonEliminar.value = res))
  tienePermiso('spots.add').then((res) => (botonAgregar.value = res))
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

<style scoped>
.listado-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* ===== HEADER ===== */
.listado-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 0.5rem;
}

.titulo-seccion {
  font-size: 1.8rem;
  color: #2c3e50;
  font-weight: 600;
  margin: 0;
}

.boton-agregar {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: #008737;
  color: white;
  padding: 10px 20px;
  border-radius: 30px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: background 0.2s, transform 0.1s;
  border: none;
  cursor: pointer;
}

.boton-agregar:hover {
  background: #006b2c;
}

.boton-agregar:active {
  transform: scale(0.97);
}

.boton-agregar:focus-visible {
  outline: 2px solid #008737;
  outline-offset: 2px;
}

/* ===== CONTADOR ===== */
.contador {
  color: #5f6c7f;
  font-size: 0.9rem;
  margin-bottom: 1rem;
  padding-left: 4px;
}

/* ===== TABLA ===== */
.tabla-wrapper {
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
  overflow-x: auto;
  overflow-y: auto;
}

.tabla-puntos {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

.tabla-puntos thead {
  background: #f7fafc;
  border-bottom: 2px solid #e2e8f0;
}

.tabla-puntos th {
  padding: 14px 16px;
  text-align: left;
  font-weight: 600;
  color: #4a5568;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.tabla-puntos td {
  padding: 12px 16px;
  border-bottom: 1px solid #f0f0f0;
  vertical-align: middle;
}

.tabla-puntos tbody tr {
  transition: background 0.15s;
}

.tabla-puntos tbody tr:hover {
  background: #f8fafc;
}

.tabla-puntos tbody tr:last-child td {
  border-bottom: none;
}

/* ===== COLUMNAS ===== */
.col-numero {
  width: 50px;
  text-align: center;
  color: #a0aec0;
  font-weight: 500;
  font-size: 0.85rem;
}

.col-nombre {
  font-weight: 500;
}

.punto-enlace {
  color: #2d3748;
  text-decoration: none;
  transition: color 0.2s;
  display: inline-block;
}

.punto-enlace:hover {
  color: #008737;
  text-decoration: underline;
}

.punto-enlace:focus-visible {
  outline: 2px solid #008737;
  outline-offset: 2px;
  border-radius: 4px;
}

.col-coordenadas {
  font-family: 'Courier New', monospace;
  font-size: 0.85rem;
  color: #657286;
}

.col-acciones {
  width: 200px;
}

.acciones-grupo {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

/* ===== BOTONES DE ACCIÓN ===== */
.btn-ver,
.btn-eliminar {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 14px;
  border-radius: 30px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  border: none;
  text-decoration: none;
}

.btn-ver {
  background: #ebf8ff;
  color: #2b6cb0;
  border: 1px solid #bee3f8;
}

.btn-ver:hover {
  background: #bee3f8;
}

.btn-ver:focus-visible {
  outline: 2px solid #2b6cb0;
  outline-offset: 2px;
}

.btn-eliminar {
  background: #fef2f2;
  color: #c54033;
  border: 1px solid #fecaca;
}

.btn-eliminar:hover {
  background: #fee2e2;
  border-color: #fca5a5;
}

.btn-eliminar:focus-visible {
  outline: 2px solid #c54033;
  outline-offset: 2px;
}

.btn-ver:active,
.btn-eliminar:active {
  transform: scale(0.95);
}

/* ===== SIN RESULTADOS ===== */
.sin-resultados {
  text-align: center;
  padding: 3rem 1rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
}

.sin-resultados p {
  color: #718096;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

/* ===== RESPONSIVE ===== */
@media (max-width: 700px) {
  .listado-header {
    flex-direction: column;
    align-items: stretch;
  }

  .titulo-seccion {
    font-size: 1.4rem;
  }

  .boton-agregar {
    justify-content: center;
    padding: 12px 20px;
  }

  .tabla-puntos {
    font-size: 0.85rem;
  }

  .tabla-puntos th,
  .tabla-puntos td {
    padding: 10px 12px;
  }

  .col-numero {
    width: 35px;
    font-size: 0.75rem;
  }

  .col-coordenadas {
    font-size: 0.75rem;
  }

  .col-acciones {
    width: 130px;
  }

  .btn-ver,
  .btn-eliminar {
    font-size: 0.7rem;
    padding: 4px 10px;
  }
}

@media (max-width: 500px) {

  .tabla-puntos th,
  .tabla-puntos td {
    padding: 8px 8px;
  }

  .col-numero {
    display: none;
  }

  .col-coordenadas {
    display: none;
  }

  .col-acciones {
    width: auto;
  }

  .btn-ver,
  .btn-eliminar {
    padding: 3px 8px;
    font-size: 0.65rem;
    gap: 2px;
  }
}
</style>