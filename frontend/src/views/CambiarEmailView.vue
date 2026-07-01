<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MigasDePan from '@/components/MigasPan.vue'
import { cambiarEmail } from '@/services/authService.js'

const router = useRouter()
const nuevoEmail = ref('')
const password = ref('')

const migas = [
  { texto: 'Inicio', ruta: '/' },
  { texto: 'Ajustes', ruta: '/ajustes' },
  { texto: 'Cambiar correo', ruta: null },
]

async function cambiar() {
  try {
    await cambiarEmail(nuevoEmail.value, password.value)
    alert('Correo actualizado correctamente')
    router.push('/ajustes')
  } catch (error) {
    alert(error.message)
  }
}
</script>

<template>
  <div>
    <MigasDePan :items="migas" />
    <h2 class="titulo-seccion">Cambiar mi correo</h2>

    <div class="aviso">Recibirás una confirmación por mail al realizar el cambio de correo.</div>

    <form @submit.prevent="cambiar" class="formulario">
      <div class="campo">
        <label>Nuevo correo electrónico *</label>
        <input v-model="nuevoEmail" type="email" required placeholder="ejemplo@dominio.com" />
      </div>
      <div class="acciones">
        <button type="submit" class="boton">Cambiar correo</button>
        <button type="button" class="boton boton-cancelar" @click="$router.back()">Cancelar</button>
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

.aviso {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  text-align: center;
}

.formulario {
  max-width: 500px;
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
  background: var(--verde-oscuro, #27ae60);
}

.boton-cancelar {
  background: #ecf0f1;
}

.boton-cancelar:hover {
  background: var(--verde-oscuro, #27ae60);
}
</style>
