<script setup>
import { useRouter } from 'vue-router'
import Boton from '../components/Boton.vue'

const router = useRouter()

const handleMap = () => {
  router.push('/mapa')
}

const handleHelp = () => {
  router.push('/ayuda')
}

const login = () => {
  router.push('/login')
}
</script>

<template>
  <header>
    
  </header>
  <main class="welcome-screen">
    <h1 class="welcome-main-title">¡Bienvenido a ContaminApp!</h1>
    <h2 class="welcome-title">App de gestión de puntos de contaminación en la Franja Costera Sur</h2>

    <div class="action-buttons">
      <Boton 
        label="VER PUNTOS EN EL MAPA" 
        variant="info" 
        @click="handleMap"
      />
    </div>

    <div class="login">
      <span>¿Sos colaborador o administrador? </span>
      <RouterLink to="/iniciar-sesion" class="login-link">Iniciar sesión</RouterLink>
    </div>

    <Boton class="help-float" variant="help" label="?" @click="handleHelp">
    </Boton>
    
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
  position: relative;
}

.welcome-title {
  color: #2d3748;
  font-size: 2rem;
  margin-bottom: 1.5rem;
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
  margin-top: 3rem;
  color: #718096;
  font-size: 1.3rem;
  line-height: 1.6;
  margin-bottom: 3rem;
  text-align: center;
}

.login{
  margin-top: 3rem;
  font-size: 1.2rem;
  color: #4a5568;
}


.action-buttons {
  display: flex;
  gap: 30px;
  flex-direction: row;
  justify-content: center;
  margin-top: 60px;

}

.help-float {
  position: absolute;
  bottom: 30px;
  right: 30px;

}

@media (max-width: 600px) {
  .welcome-main-title { font-size: 2.2rem; }
  .welcome-title { font-size: 2rem; }
  .action-buttons { flex-direction: column; align-items: center; gap: 30px; }
}
</style>