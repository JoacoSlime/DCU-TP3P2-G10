<script setup>
import { useRoute } from 'vue-router';

const route = useRoute();
const idDelPunto = route.params.id; 
</script>

<template>
  <div>
    <h1>Hola, punto {{ idDelPunto }}</h1>
  </div>
</template>