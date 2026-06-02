<script setup>
import { RouterView } from 'vue-router'
import Navbar from './components/NavBar.vue'
</script>

<template>
  <Navbar />
  <RouterView />
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}
</style>