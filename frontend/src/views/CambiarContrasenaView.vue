<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import MigasDePan from '@/components/MigasPan.vue'
import { cambiarContraseña } from '@/services/authService.js'

const router = useRouter()
const passwordActual = ref('')
const nuevaPassword = ref('')
const repetirPassword = ref('')

const migas = [
  { texto: 'Inicio', ruta: '/' },
  { texto: 'Ajustes', ruta: '/ajustes' },
  { texto: 'Cambiar contraseña', ruta: null },
]

async function cambiarPassword() {
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/
  if (!regex.test(nuevaPassword.value)) {
    alert('La contraseña no cumple los requisitos mínimos')
    return
  }
  if (nuevaPassword.value !== repetirPassword.value) {
    alert('Las contraseñas nuevas no coinciden')
    return
  }
  try {
    await cambiarContraseña(passwordActual.value, nuevaPassword.value)
    alert('Contraseña cambiada correctamente')
    router.push('/ajustes')
  } catch (error) {
    alert(error.message)
  }
}
</script>

<template>
  <div>
    <MigasDePan :items="migas" />
    <h2 class="titulo-seccion">Cambiar mi contraseña</h2>

    <div class="aviso">
      La nueva contraseña debe poseer, por lo menos:
      <ul>
        <li>8 (ocho) caracteres.</li>
        <li>Una letra mayúscula.</li>
        <li>Una letra minúscula.</li>
        <li>Un número.</li>
      </ul>
    </div>

    <form @submit.prevent="cambiarPassword" class="formulario">
      <div class="campo">
        <label>Contraseña actual *</label>
        <input v-model="passwordActual" type="password" required placeholder="••••••••" />
      </div>
      <div class="campo">
        <label>Nueva contraseña *</label>
        <input v-model="nuevaPassword" type="password" required placeholder="••••••••" />
      </div>
      <div class="campo">
        <label>Repetir nueva contraseña *</label>
        <input v-model="repetirPassword" type="password" required placeholder="••••••••" />
      </div>
      <div class="acciones">
        <button type="submit" class="boton">Cambiar contraseña</button>
        <button type="button" class="boton boton-cancelar" @click="$router.back()">Cancelar</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
.titulo-seccion {
  font-size: 2rem;
  color: var(--gris-oscuro, #2c3e50);
  text-align: center;
  font-weight: 600;
}

.aviso {
  padding: 1rem;
  border-radius: 8px;
  font-size: 1rem;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}

.aviso ul {
  margin: 0.5rem 0 0 1.5rem;
  padding-left: 0;
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
  background: var(--verde-oscuro);
}
</style>
