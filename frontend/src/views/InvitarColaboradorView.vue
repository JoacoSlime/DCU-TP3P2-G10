<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MigasDePan from '@/components/MigasPan.vue'
import { invitarColaborador } from '@/services/authService.js'

const router = useRouter()
const email = ref('')

const migas = [
  { texto: 'Inicio', ruta: '/' },
  { texto: 'Ajustes', ruta: '/ajustes' },
  { texto: 'Invitar colaborador', ruta: null },
]

async function invitar() {
  try {
    await invitarColaborador(email.value)
    alert(`Invitación enviada a ${email.value}`)
    router.push('/ajustes')
  } catch (error) {
    alert(error.message)
  }
}
</script>

<template>
  <div>
    <MigasDePan :items="migas" />
    <h2 class="titulo-seccion">Invitar colaborador</h2>

    <div class="advertencia">
      Advertencia, el colaborador tendrá permisos de:
      <ul>
        <li>Crear nuevos puntos</li>
        <li>Agregar nuevas mediciones</li>
      </ul>
    </div>

    <form @submit.prevent="invitar" class="formulario">
      <div class="campo">
        <label>Correo electrónico del colaborador *</label>
        <input v-model="email" type="email" required placeholder="johndoe@ejemplo.com" />
      </div>
      <div class="acciones">
        <button type="submit" class="boton-enviar">Enviar invitación</button>
        <button type="button" class="boton-cancelar" @click="$router.back()">Cancelar</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.titulo-seccion {
  font-size: 2rem;
  margin-bottom: 1.5rem;
  color: var(--gris-oscuro, #2c3e50);
  text-align: center;
  font-weight: 600;
}

.advertencia {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 1rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.advertencia ul {
  margin: 0.5rem 0 0 1.5rem;
}

.formulario {
  max-width: 500px;
  margin: 0 auto;
  background: white;
  padding: 1.5rem;
  border-radius: 16px;
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

.campo input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 1rem;
}

.campo input:focus {
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

.boton-enviar {
  background: #ecf0f1;
  border: none;
  padding: 10px 24px;
  border-radius: 30px;
  font-size: 1rem;
  cursor: pointer;
}

.boton-enviar:hover {
  background: var(--verde, #2ecc71);
  color: white;
}

.boton-cancelar {
  background: #ecf0f1;
  border: none;
  padding: 10px 24px;
  border-radius: 30px;
  font-size: 1rem;
  cursor: pointer;
}

.boton-cancelar:hover {
  background: #95a5a6;
  color: white;
}
</style>
