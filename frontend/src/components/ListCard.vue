<script setup>
import Boton from './Boton.vue'

defineProps({
  title: String,
  items: Array
})

defineEmits(['go-to'])

const getLevelColor = (nivel) => {
  const colores = { alto: '#e53e3e', medio: '#dd6b20', bajo: '#d69e2e' }
  return colores[nivel] || '#a0aec0'
}
</script>

<template>
  <div class="lista-card">
  
    <input type="text" placeholder="Buscar punto contaminado" class="search-input" />
    
    <ul>
      <li v-for="item in items" :key="item.id" class="item-row">
        <span class="item-name">{{ item.nombre }}</span>

        <router-link :to="'/punto/:' + item.id" custom v-slot="{ navigate }">
          <Boton 
            label="Ir al punto" 
            variant="info" 
            @click="navigate" 
            class="btn-sm"
          />
         </router-link>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.lista-card {
  background: rgba(255, 255, 255, 0.95); 
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15); 
  border: 1px solid rgba(0, 0, 0, 0.05);
}

.item-row {
  display: flex;
  justify-content: space-between; 
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid #eee;
}

.lista-card ul {
  list-style: none;
  padding: 0;
}

.lista-card li {
  padding: 10px;
  border-bottom: 1px solid #eee;
  cursor: pointer;
  transition: background 0.2s;
  font-family: sans-serif;
  color: #4c4f69;
}

.lista-card li:hover {
  background-color: #f1f5f9; 
}

:deep(.btn-sm) {
  padding: 5px 10px !important;
  font-size: 14px !important;
  gap: 5px !important;
}

.search-input {
  width: 100%;
  padding: 12px;
  margin-bottom: 1rem;
  border: 1px solid #a3a8ad;
  border-radius: 10px;
}
</style>