<script setup>
import UserCard from '../components/UserCard.vue'
import Boton from '../components/Boton.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const handleSelect = (role) => {
  console.log(`Usuario seleccionado: ${role}`)
  if (role === 'Invitado') {
    router.push('/usuario-invitado')
  } else if (role === 'Colaborador') {
    router.push('/usuario-colaborador')
  }
}

const handleHelp = () => {
  router.push('/ayuda')
}
</script>

<template>

  <main class="selection-screen">
    <h1 class="welcome-main-title">Elegí cómo querés ingresar a la app</h1>
    
    <div class="cards-container">
      <UserCard 
        title="Usuario invitado"
        :description="['Ver mapa y listado de puntos', 'Ver datos históricos de un punto contaminado', 'Ajustar colores y letras']"
        buttonLabel="Quiero ser usuario invitado"
        variant="info"
        @select="handleSelect('Invitado')"
      />

      <UserCard 
        title="Usuario colaborador"
        :description="['Todo lo del invitado', 'Agregar puntos y mediciones', 'Cambiar contraseña']"
        buttonLabel="Quiero ser usuario colaborador"
        variant="colaborador"
        @select="handleSelect('Colaborador')"
      />
    </div>

    <footer class="footer-actions">
       <Boton label="?" variant="help" @click="handleHelp()"/>
    </footer>
  </main>
</template>

<style scoped>
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
  gap: 30px;
  margin-top: 40px;
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
</style>