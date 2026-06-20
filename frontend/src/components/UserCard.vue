<script setup>
import Boton from './Boton.vue'

defineProps({
  title: String,
  description: Array,
  buttonLabel: String,
  variant: String
})

defineEmits(['select'])
</script>
<template>
  <div class="user-card">
    <h3 class="card-title">{{ title }}</h3>
    <ul class="card-list">
      <li v-for="(item, index) in description" :key="index">{{ item }}</li>
    </ul>
    <Boton :label="buttonLabel" :variant="variant" @click="$emit('select')" />
  </div>
</template>

<style scoped>
.user-card {
  background: #d1d5db;
  padding: 30px;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  height: 100%;
  min-height: 400px;
  width: 405px;
}

.card-title {
  color: #2d3748;
  font-size: 1.5rem;
  margin-bottom: 20px;
  text-align: center;
}

.card-list {
  color: #4c4f69;
  text-align: left;
  margin-bottom: 25px;
  line-height: 1.6;
  padding-left: 20px;
}
</style>