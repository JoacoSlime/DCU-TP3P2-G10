<script setup>
import { useRouter, useRoute} from 'vue-router'

const router = useRouter()
const route = useRoute();

const irAlInicio = () => {
  router.push('/') 
}

const irAtras = () => {
  router.back();
};

const irAListadoPuntos = () => {
  router.push('/listado-puntos');
};


const irALogin = () => {
  router.push('/login');
};

const irALogout = () => {
  localStorage.removeItem('logged')
  localStorage.removeItem('role')
  router.push('/')
  window.location.reload()
  console.log('cierro sesion')
};

</script>

<template>
  <header class="navbar">
   <img src="/logoapp.png" 
   alt="Logo ContaminApp" 
   class="logo" 
   @click="irAlInicio" />

   <button 
      v-if="route.path !== '/'" 
      class="nav-option" 
      @click="irAtras"
    >
      ← Volver
    </button>

     <button 
      id="b-listaP"
      class="nav-option push-right" 
      @click="irAListadoPuntos"
    >
      Listado de puntos
    </button>

    <button 
      id="b-login"
      v-if="route.path == '/'" 
      class="nav-option push-right" 
      @click="irALogin"
    >
      Iniciar Sesión
    </button>

    <button 
      id="b-logout"
      v-if="route.path == '/admin/mapa'" 
      class="nav-option push-right" 
      @click="irALogout"
    >
      Cerrar Sesión
    </button>
    
  </header>
</template>

<style scoped>
.navbar {
  width: 100%;
  height: 60px;
  background-color: #ffffff;
  padding: 0 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky; 
  top: 0;
  z-index: 1000;
}

.logo {
  height: 40px;
  cursor: pointer; 
  transition: opacity 0.2s;
  border-radius: 40px;
}

.logo:hover {
  opacity: 0.8; 
}

.nav-option {
  background: none;
  border: none;
  font-size: 0.95rem;
  font-weight: 600;
  color: #4c4f69;
  cursor: pointer;
  padding: 8px 25px;
  border-radius: 4px;
  transition: all 0.2s ease;
  gap: 40px;
  justify-content: flex-start;
  position: sticky;
  top: 0;
  z-index: 1000;
  height: 60px;
}

.nav-option:hover {
  background-color: #f1f5f9; 
  color: #179299; 
}

.push-right {
  margin-left: auto;
}

#b-listaP {
  margin-left: 30px;
}
</style>