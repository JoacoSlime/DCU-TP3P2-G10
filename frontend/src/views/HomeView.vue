<script setup>
import { useRouter } from 'vue-router'
import Boton from '../components/Boton.vue'

const router = useRouter()

const handleUserInfo = () => {
  router.push('/elegir-usuario')
}

const handleHelp = () => {
  router.push('/ayuda')
}
</script>

<template>
  <main class="welcome-screen">
    <h1 class="welcome-main-title">¡Bienvenido a ContaminApp!</h1>
    <p class="description">App de Contaminación de la franja costera sur</p>
    
    <h3>En esta aplicación encontrarás información sobre la contaminación en determinados puntos de la franja costera sur.
Podes usarla como usuario invitado o como usuario colaborador. Tocando el botón “Información usuarios” podes elegir que usuario queres ser.
</h3>

    <div class="action-buttons">
      <Boton 
        label="Información usuarios" 
        variant="info" 
        @click="handleUserInfo"
      />
      
      <Boton 
        label="Necesito ayuda" 
        variant="help" 
        @click="handleHelp"
      />
    </div>
  </main>
</template>

<style scoped>
.welcome-screen {
  background-color: #f8fafc; 
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center; 
  align-items: center;     
  padding: 2rem;
  font-family: 'Inter', sans-serif;
  flex-wrap: nowrap;
}

.welcome-title {
  color: #2d3748;
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.welcome-main-title{
  color: #40a02b;
  font-size: 3.4rem; 
  font-weight: 800;
  text-align: center;
  margin-bottom: 1rem;
  margin-top: 2rem;
}

.description {
  color: #718096;
  font-size: 1.80rem;
  max-width: 600px;
  line-height: 1.6;
  margin-bottom: 3rem;
}

.action-buttons {
  display: flex;
  gap: 30px;
  flex-direction: row;
  justify-content: center;
  margin-top: 60px;

}

@media (max-width: 600px) {
  .welcome-main-title { font-size: 2.2rem; }
  .welcome-title { font-size: 2rem; }
  .action-buttons { flex-direction: column; align-items: center; gap: 30px; }
}
</style>