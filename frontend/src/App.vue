<script setup>
import { RouterView, useRoute } from 'vue-router'
import Navbar from './components/NavBar.vue'

const route = useRoute()
</script>

<template>
  <Navbar v-if="route.path !== '/iniciar-sesion'" />
  <RouterView />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>