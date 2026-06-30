<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/services/authService.js'

const router = useRouter()
const emit = defineEmits(['close', 'login-success'])

const step = ref(1)
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function iniciarSesion() {
  error.value = ''
  loading.value = true

  try {
    await login(email.value, password.value)
    emit('login-success')
    emit('close')
    router.push('/')
  } catch (err) {
    error.value = 'Credenciales incorrectas'
    password.value = ''
    step.value = 1
  } finally {
    loading.value = false
  }
}

const cerrar = () => {
  emit('close')
}

const volverAlPaso1 = () => {
  step.value = 1
  error.value = ''
}
</script>

<template>
  <Teleport to="body">
    <div class="modal-overlay" @click.self="cerrar">
      <div class="modal-content">
        <button class="btn-cerrar" @click="cerrar">✕</button>

        <img src="/logoapp.png" alt="Logo ContaminApp" class="modal-logo" />

        <!-- Paso 1: Email -->
        <div v-if="step === 1" class="form-step">
          <h2 class="modal-title">Iniciar sesión</h2>
          <p class="modal-subtitle">Ingresá tu email para continuar</p>

          <div class="input-group">
            <input type="email" placeholder="Email" v-model="email" class="modal-input" @keyup.enter="step = 2" />
          </div>

          <button class="btn-primary" @click="step = 2" :disabled="!email">
            Siguiente
          </button>
        </div>

        <!-- Paso 2: Password -->
        <form v-else @submit.prevent="iniciarSesion" class="form-step">
          <h2 class="modal-title">Hola, {{ email }}</h2>
          <p class="modal-subtitle">Ingresá tu contraseña</p>

          <div class="input-group">
            <input type="password" placeholder="Contraseña" v-model="password" class="modal-input" required />
          </div>

          <div v-if="error" class="error-message">{{ error }}</div>

          <div class="actions-row">
            <button type="button" class="btn-secondary" @click="volverAlPaso1">
              ← Volver
            </button>
            <button type="submit" class="btn-primary" :disabled="!password || loading">
              {{ loading ? 'Cargando...' : 'Iniciar sesión' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.modal-content {
  background: white;
  padding: 40px 35px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  width: 100%;
  max-width: 400px;
  position: relative;
  text-align: center;
}

.btn-cerrar {
  position: absolute;
  top: 12px;
  right: 18px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #999;
  transition: color 0.2s;
}

.btn-cerrar:hover {
  color: #333;
}

.modal-logo {
  height: 70px;
  border-radius: 40px;
  margin-bottom: 10px;
}

.modal-title {
  font-size: 1.6rem;
  color: #2d3748;
  margin: 0.5rem 0 0.2rem 0;
}

.modal-subtitle {
  color: #718096;
  font-size: 0.95rem;
  margin-bottom: 1.5rem;
}

.input-group {
  margin-bottom: 1rem;
}

.modal-input {
  width: 100%;
  padding: 12px 16px;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-size: 1rem;
  transition: border-color 0.2s;
  box-sizing: border-box;
}

.modal-input:focus {
  outline: none;
  border-color: #19a1a8;
  box-shadow: 0 0 0 3px rgba(25, 161, 168, 0.1);
}

.error-message {
  color: #e53e3e;
  font-size: 0.9rem;
  margin: 0.5rem 0 1rem 0;
  background: #fff5f5;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1px solid #fed7d7;
}

.actions-row {
  display: flex;
  gap: 10px;
  justify-content: center;
  margin-top: 0.5rem;
}

.btn-primary {
  background: #19a1a8;
  color: white;
  border: none;
  padding: 10px 28px;
  border-radius: 30px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-primary:hover:not(:disabled) {
  background: #14858b;
}

.btn-primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-secondary {
  background: #edf2f7;
  color: #4a5568;
  border: none;
  padding: 10px 20px;
  border-radius: 30px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.btn-secondary:hover {
  background: #e2e8f0;
}
</style>