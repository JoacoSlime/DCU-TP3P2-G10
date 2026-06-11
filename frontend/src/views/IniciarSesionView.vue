<script setup>
import { ref } from 'vue'
import Boton from '../components/Boton.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const step = ref(1)
const email = ref('')
const password = ref('')

const API_URL = import.meta.env.VITE_API_URL



const handleLogin = async () => {
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email.value,
        password: password.value
      })
    })

    const data = await response.json()

    if (response.ok) {
      localStorage.setItem('role', data.role)
      localStorage.setItem('logged', 'true')
      if (data.role === 'admin') {
        router.push('/admin/mapa')
      } else {
        router.push('/mapa') 
      }

    } else {
      alert('Credenciales incorrectas')
    }

  } catch (error) {
    console.error('Error al conectar con el servidor:', error)
  }
}  

const goToMap = () => {
  router.push('/admin/mapa')
}

</script>

<template>
  <main class="login-container">
    <div class="login-card">
      <img src="/logoapp.png" alt="Logo ContaminApp" class="login-logo" />
      
      <div v-if="step === 1" class="form-step">
        <h2 class="login-title">Iniciar sesión</h2>
        <div class="input-group">
          <input type="text" placeholder="Usuario o correo" v-model="email" class="login-input" />
        </div>
       <div class="actions">
          <Boton label="Siguiente" variant="info" class="btn-next" @click="step = 2" />
        </div>
      </div>

      <div v-else>
        <h2 class="login-title">Hola, {{ email }}</h2>

        <div class="input-group">
          <input  
            type="password"
            placeholder="Contraseña" 
            v-model="password"
            class="login-input" />
        </div>
        <div class="actions">
          <Boton label="Siguiente" variant="info" class="btn-next" @click="goToMap" />
        </div>
      </div>
    </div>
  </main>
</template>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: #f0f2f5;
}

.login-card {
  background: white;
  padding: 50px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 800px;
  text-align: center;
}

.login-logo {
  height: 100px;
  cursor: pointer; 
  transition: opacity 0.2s;
  border-radius: 40px;
}

.login-title {
  margin-top: 3rem;
  font-size: 2rem;
  color: #4a5568;
  margin-bottom: 1.5rem;
}

.login-input {
  width: 100%;
  padding: 12px;
  margin-bottom: 1rem;
  border: 1px solid #a3a8ad;
  border-radius: 6px;
}

.checkbox-group {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 1.5rem;
  font-size: 0.9rem;
  color: #4a5568;
}
.actions {
  display: flex;
  justify-content: flex-end;
}

.btn-next {
  width: auto;
  padding: 8px 20px;
  font-size: 0.9rem;
}
</style>