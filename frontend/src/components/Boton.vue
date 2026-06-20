<template>
  <button 
    :class="['btn', variant]" 
    @click="$emit('click')"
    :aria-label="label"
  >
    <slot name="icon"></slot>
    <span>{{ label }}</span>
  </button>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  variant: { type: String, default: 'info' } 
})

defineEmits(['click'])
</script>

<style scoped>
.btn {
  border: none;
  border-radius: 50px;
  box-shadow: 0px 4px 2px rgba(0, 0, 0, 0.25);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 24px;
  font-weight: 700;
  padding: 20px 30px;
  transition: transform 0.2s;
}

.btn.info { 
  background-color: #19a1a8; 
  border-radius: 50px;
}
.btn.info:hover { 
  transform: translateY(-2px); 
  background-color: #10666b; 
}
.btn.help { 
  background-color: #40a02b; 
  font-size: 10px;
  padding: 0;
  width: 50px;   
  height: 50px;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}
.btn.help:hover { 
  transform: translateY(-2px); 
  background-color: #2b6b1d; 
}
.btn.secondary { background-color: #94a3b8; } 
.btn.colaborador { background-color: #2563eb; }
</style>