<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import IniciarSesionModal from './IniciarSesionModal.vue'
import { Preferences } from '@capacitor/preferences'

const emit = defineEmits(['close'])

defineProps({ show: Boolean })

const mostrarLogin = ref(false)

const entrarComoInvitado = async () => {
  // Guardar que el usuario es invitado
  await Preferences.set({
    key: 'role',
    value: 'invitado',
  })
  await Preferences.set({
    key: 'logged',
    value: 'true',
  })
  await Preferences.set({
    key: 'yaVioModal',
    value: 'true',
  })
  emit('close')
}

const abrirLogin = () => {
  mostrarLogin.value = true
}

const cerrarLogin = async () => {
  mostrarLogin.value = false
  await Preferences.set({
    key: 'yaVioModal',
    value: 'true',
  })
  emit('close')
}
</script>

<template>
  <Teleport to="body">
    <div v-if="show" class="modal-overlay">
      <div class="modal-content">
        <img src="/logoapp.png" alt="Logo ContaminApp" class="modal-logo" />
        <h1>¡Bienvenido a ContaminApp!</h1>
        <p>App de gestión de puntos de contaminación en la Franja Costera Sur</p>
        <button class="btn-bienvenida" @click="entrarComoInvitado">VER PUNTOS EN EL MAPA</button>

        <p class="footer-text">
          ¿Sos colaborador o administrador?
          <span class="login-link" @click="abrirLogin">Iniciar sesión</span>
        </p>
      </div>
    </div>
  </Teleport>

  <IniciarSesionModal v-if="mostrarLogin" @close="cerrarLogin" />
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.735);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  font-family: sans-serif;
  background: rgb(255, 255, 255);
  padding: 30px;
  border-radius: 20px;
  text-align: center;
  width: 90%;
  max-width: 500px;
  margin: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
  max-height: 90vh;
  overflow-y: auto;
}

.btn-bienvenida {
  background: #19a1a8;
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 50px;
  cursor: pointer;
  font-weight: 700;
  margin: 20px 0;
}

.btn-bienvenida:hover {
  background: #14858b;
}

.modal-logo {
  width: 200px;
  height: auto;
  margin-bottom: 15px;
  display: block;
  margin-left: auto;
  margin-right: auto;
  max-width: 100%;
  margin: 0 auto 15px auto;
  border-radius: 40px;
}

.login-link {
  color: #19a1a8;
  text-decoration: none;
  font-weight: 600;
  cursor: pointer;
}

.login-link:hover {
  text-decoration: underline;
}
</style>
