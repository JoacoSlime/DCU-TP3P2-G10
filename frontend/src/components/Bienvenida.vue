<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Boton from './Boton.vue'
import UserCard from './UserCard.vue'

const emit = defineEmits(['close'])
const router = useRouter()
const currentPage = ref('welcome')

const closeModal = () => {
  localStorage.setItem('hasVisited', 'true')
  emit('close')
}
const login = () => {
  localStorage.setItem('hasVisited', 'true')
  router.push('/login')
  emit('close')
}
</script>

<template>
  <section id="welcome-screen">
    <div class="modal-content" v-if="currentPage === 'welcome'">
      <h1 class="welcome-main-title">¡Bienvenido a ContaminApp!</h1>
      <p class="description">App de Contaminación de la franja costera sur</p>

      <!-- Bienvenida -->
      <p class="info">
        En esta aplicación encontrarás información sobre la contaminación en determinados puntos de
        la franja costera sur.
      </p>
      <p class="info">Podes usarla como usuario invitado o como usuario colaborador.</p>
      <p class="info">
        Tocando el botón “Información usuarios” podes elegir que usuario queres ser.
      </p>

      <div class="action-buttons">
        <Boton label="Información usuarios" variant="info" @click="currentPage = 'select-user'" />

        <Boton label="Necesito ayuda" variant="help" @click="currentPage = 'help'" />
      </div>
    </div>

    <!-- Elegir usuario -->
    <div class="modal-content" v-if="currentPage === 'select-user'">
      <h1 class="welcome-main-title">Elegí cómo querés ingresar a la app</h1>

      <div class="cards-container">
        <UserCard
          title="Usuario invitado"
          :description="[
            'Ver mapa y listado de puntos',
            'Ver datos históricos de un punto contaminado',
            'Ajustar colores y letras',
          ]"
          buttonLabel="Quiero ser usuario invitado"
          variant="info"
          @select="closeModal()"
        />

        <UserCard
          title="Usuario colaborador"
          :description="[
            'Todo lo del invitado',
            'Agregar puntos y mediciones',
            'Cambiar contraseña',
          ]"
          buttonLabel="Quiero ser usuario colaborador"
          variant="colaborador"
          @select="login()"
        />
      </div>
    </div>
    <div class="modal-content" v-if="currentPage === 'help'">
      <h1>Ayuda</h1>
    </div>
  </section>
</template>

<style scoped>
#welcome-screen {
  background-color: rgba(0, 0, 0, 0.5);
  height: 100vh;
  width: 100vw;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  position: absolute;
  display: flex;
}

.modal-content {
  background-color: #f8fafc;
  display: flex;
  flex: 1;
  margin: 5%;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  font-family: 'Inter', sans-serif;
  flex-wrap: nowrap;
  border-radius: 3em;
  box-shadow: 0.5em 0.5em 0.5em 0.25em rgba(0, 0, 0, 0.2);
}

.welcome-title {
  color: #2d3748;
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.welcome-main-title {
  color: #40a02b;
  font-size: 3.4rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 1rem;
  margin-top: 2rem;
}

.description {
  color: #718096;
  font-size: 1.8rem;
  max-width: 600px;
  line-height: 1.6;
  margin-bottom: 3rem;
}

.info {
  font-size: 1.3rem;
}

.action-buttons {
  display: flex;
  gap: 30px;
  flex-direction: row;
  justify-content: center;
  margin-top: 60px;
}

.selection-screen {
  padding: 40px;
  text-align: center;
}
.selection-screen {
  background-color: #f8fafc;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px;
  font-family: 'Inter', sans-serif;
}

.welcome-main-title {
  color: #40a02b;
  font-size: 3.4rem;
  font-weight: 800;
  margin-bottom: 1rem;
}

.description {
  color: #718096;
  font-size: 1.2rem;
  margin-bottom: 40px;
}

.cards-container {
  display: flex;
  grid-template-columns: 1fr, 1fr;
  gap: 2em;
  margin-top: 2em;
  flex-wrap: wrap;
  justify-content: center;
  align-items: stretch;
}

.footer-actions {
  margin-top: 50px;
  display: flex;
  gap: 20px;
  width: 100%;
  justify-content: center;
  max-width: 800px;
}

@media screen and (max-width: 1000px) {
  .welcome-main-title {
    font-size: 2.2rem;
  }
  .welcome-title {
    font-size: 2rem;
  }
  .action-buttons {
    flex-direction: column;
    align-items: center;
    gap: 30px;
  }
}
</style>
