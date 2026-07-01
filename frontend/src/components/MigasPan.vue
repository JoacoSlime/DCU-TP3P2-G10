<script setup>
import { RouterLink } from 'vue-router'
defineProps({ items: { type: Array, required: true } })
</script>
<template>
  <nav class="migas">
    <template v-for="(item, index) in items" :key="index">
      <RouterLink v-if="item.ruta" :to="item.ruta" class="miga-enlace">
        {{ item.texto }}
      </RouterLink>
      <span v-else class="miga-actual">{{ item.texto }}</span>
      <span v-if="index < items.length - 1" class="separador"> > </span>
    </template>
  </nav>
</template>

<style scoped>
.migas {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  font-family: system-ui, 'Segoe UI', sans-serif;
}

.miga-enlace {
  color: #007931;
  text-decoration: none;
  transition: color 0.2s;
}

.miga-enlace:hover {
  text-decoration: underline;
  color: var(--verde-oscuro, #27ae60);
}

.miga-actual {
  color: #555;
  font-weight: 500;
}

.separador {
  color: #999;
  margin: 0 0.2rem;
}
</style>
