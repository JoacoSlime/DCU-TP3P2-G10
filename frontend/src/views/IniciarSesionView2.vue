<template>
    <div>
        <h2>Iniciar sesión</h2>
        <form @submit.prevent="iniciarSesion">
            <div><label>Email: <input v-model="email" type="email" required></label></div>
            <div><label>Contraseña: <input v-model="password" type="password" required></label></div>
            <button type="submit">Ingresar</button>
        </form>
        <p>¿No tienes cuenta? Solicita acceso a administrador@admin.com</p>
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '@/services/authService.js'

const router = useRouter()
const email = ref('')
const password = ref('')

async function iniciarSesion() {
    try {
        await login(email.value, password.value)
        router.push('/')
    } catch (err) {
        alert(err.message)
    }
}
</script>
