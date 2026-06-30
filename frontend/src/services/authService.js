import { API_URL, USAR_MOCKS } from '@/config'
import { authMock } from './mocks/authMock.js'
import { adaptarUsuario } from './adapter.js'

export async function login(email, password) {
  let data

  if (USAR_MOCKS) {
    const response = await authMock.login(email, password)
    data = response.data
  } else {
    const res = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    const response = await res.json()
    if (!res.ok) throw new Error(response.message || 'Credenciales inválidas')
    data = response.data
  }

  if (data?.token) {
    localStorage.setItem('auth_token', data.token)
  }
  if (data?.user) {
    localStorage.setItem('usuario', JSON.stringify(adaptarUsuario(data.user)))
  }

  return data
}

export async function logout() {
  if (USAR_MOCKS) return authMock.logout()

  const token = localStorage.getItem('auth_token')
  if (token) {
    try {
      await fetch(`${API_URL}/auth/logout`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${token}` },
      })
    } catch (e) {}
  }
  localStorage.clear()
  return { status: 'success', message: 'logged out' }
}

export async function obtenerUsuarioActual() {
  const stored = localStorage.getItem('usuario')
  if (stored) return JSON.parse(stored)

  let user

  if (USAR_MOCKS) {
    try {
      const response = await authMock.me()
      user = response.data.user
    } catch {
      return null
    }
  } else {
    const token = localStorage.getItem('auth_token')
    if (!token) return null
    try {
      const res = await fetch(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (!res.ok) return null
      const response = await res.json()
      user = response.data?.user || response.data
    } catch {
      return null
    }
  }

  if (user) {
    const usuarioAdaptado = adaptarUsuario(user)
    localStorage.setItem('usuario', JSON.stringify(usuarioAdaptado))
    return usuarioAdaptado
  }

  return null
}

export async function esAdmin() {
  const user = await obtenerUsuarioActual()
  return user?.rol === 'admin'
}

export async function cambiarEmail(nuevoEmail, contraseñaActual) {
  if (USAR_MOCKS) return authMock.changeEmail(nuevoEmail)

  const token = localStorage.getItem('auth_token')
  const res = await fetch(`${API_URL}/collaborators/change_email`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ email: nuevoEmail }),
  })
  if (!res.ok) throw new Error('Error al cambiar email')
  return res.json()
}

export async function cambiarContraseña(contraseñaActual, nuevaContraseña) {
  if (USAR_MOCKS) return authMock.changePassword(contraseñaActual, nuevaContraseña)

  const token = localStorage.getItem('auth_token')
  const res = await fetch(`${API_URL}/collaborators/change_password`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ old_password: contraseñaActual, new_password: nuevaContraseña }),
  })
  if (!res.ok) throw new Error('Error al cambiar contraseña')
  return res.json()
}

export async function invitarColaborador(email) {
  if (USAR_MOCKS) return authMock.registerCollaborator(email)

  const token = localStorage.getItem('auth_token')
  const res = await fetch(`${API_URL}/collaborators/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ email }),
  })
  if (!res.ok) throw new Error('Error al invitar colaborador')
  return res.json()
}

export async function registrarContraseña(tokenInvite, name, surname, password) {
  if (USAR_MOCKS) return authMock.createPassword(tokenInvite, name, surname, password)

  const res = await fetch(`${API_URL}/collaborators/create_password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token: tokenInvite, name, surname, password }),
  })
  if (!res.ok) throw new Error('Error al registrar contraseña')
  return res.json()
}
