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
  border-radius: 20px;
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

.btn.info { background-color: #179299; }
.btn.help { background-color: #40a02b; }
.btn:hover { transform: translateY(-2px); }
.btn.secondary { background-color: #94a3b8; } 
.btn.colaborador { background-color: #2563eb; }
</style>