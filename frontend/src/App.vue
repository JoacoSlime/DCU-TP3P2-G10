<script setup>
import { RouterView, useRoute, useRouter} from 'vue-router'
import Navbar from './components/NavBar.vue'
import Boton from './components/Boton.vue'

const route = useRoute()
const router = useRouter()

const help = () => {
  router.push('/ayuda')
}
</script>

<template>
  <Navbar v-if="route.path !== '/login'" />
  <RouterView />

  <Boton 
      id="b-help"
      class="nav-option" 
      @click.="help"
      label="Ayuda"
    >

  </Boton>
    
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#b-help{
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 999999 !important;
}
</style>
