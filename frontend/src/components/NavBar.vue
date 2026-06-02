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
  </header>
</template>

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


</script>

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
}

.logo:hover {
  opacity: 0.8; 
}

.nav-option {
  background: none;
  border: none;
  font-size: 1rem;
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
</style>