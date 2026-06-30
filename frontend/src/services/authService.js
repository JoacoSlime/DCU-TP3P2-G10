import { API_URL, USAR_MOCKS } from '@/config'
import { authMock } from './mocks/authMock.js'
import { adaptarUsuario } from './adapter.js'
import { Preferences } from '@capacitor/preferences'

export async function login(email, password) {
  let access_token
  let refresh_token

  if (USAR_MOCKS) {
    // TODO: Fix mocks
    const response = await authMock.login(email, password)
    access_token = response.token
  } else {
    const res = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    const response = await res.json()
    if (!res.ok) throw new Error(response.message || 'Credenciales inválidas')
    access_token = response.access_token
    refresh_token = response.refresh_token
  }

  if (access_token) {
    await Preferences.set({
      key: 'auth_token',
      value: access_token,
    })
  }
  if (refresh_token) {
    await Preferences.set({
      key: 'refresh_token',
      value: refresh_token,
    })
  }

  return { access_token, refresh_token }
}

export async function logout() {
  if (USAR_MOCKS) return authMock.logout() // TODO: Fix mocks

  const token = (
    await Preferences.get({
      key: 'auth_token',
    })
  ).value
  if (token) {
    //  El endpoint existe, pero no hace nada
    //
    // try {
    //   await fetch(`${API_URL}/auth/logout`, {
    //     method: 'GET',
    //     headers: { Authorization: `Bearer ${token}` },
    //   })
    // } catch (e) {}
    await Preferences.remove({
      key: 'usuario',
    })
    await Preferences.remove({
      key: 'auth_token',
    })
    await Preferences.remove({
      key: 'refresh_token',
    })
    await Preferences.remove({
      key: 'logged',
    })
    await Preferences.remove({
      key: 'role',
    })
  }
  return { status: 'success', message: 'logged out' }
}

export async function obtenerUsuarioActual() {
  const stored = (
    await Preferences.get({
      key: 'usuario',
    })
  ).value
  if (stored) return JSON.parse(stored)

  let user

  if (USAR_MOCKS) {
    // TODO: Fix mocks
    try {
      const response = await authMock.me()
      user = response.data.user
    } catch {
      return null
    }
  } else {
    const token = (
      await Preferences.get({
        key: 'auth_token',
      })
    ).value
    if (!token) return null
    try {
      const res = await fetch(`${API_URL}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (!res.ok) return null
      user = await res.json()
    } catch {
      return null
    }
  }

  if (user) {
    const usuarioAdaptado = adaptarUsuario(user)
    await Preferences.set({
      key: 'usuario',
      value: JSON.stringify(usuarioAdaptado),
    })
    return usuarioAdaptado
  }

  return null
}

export async function esAdmin() {
  const user = await obtenerUsuarioActual()
  return user?.rol?.name === 'administrator'
}

/**
 * Devuelve si el usuario actual posee el permiso establecido (en vez de si tiene un rol)
 * @param {string} permiso
 * @returns {Promise<boolean>}
 */
export async function tienePermiso(permiso) {
  const user = await obtenerUsuarioActual()
  console.log(user)
  if (user?.rol?.permissions?.some((permissionPair) => permissionPair.name === permiso)) {
    return true
  }
  return false
}

export async function cambiarEmail(nuevoEmail, contraseñaActual) {
  if (USAR_MOCKS) return authMock.changeEmail(nuevoEmail) // TODO: Fix mocks

  const token = (
    await Preferences.get({
      key: 'auth_token',
    })
  ).value
  const res = await fetch(`${API_URL}/users/change_email`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ email: nuevoEmail }),
  })
  if (!res.ok) throw new Error(data.message || 'Error al cambiar email')
  return res.json()
}

export async function cambiarContraseña(contraseñaActual, nuevaContraseña) {
  if (USAR_MOCKS) return authMock.changePassword(contraseñaActual, nuevaContraseña) // TODO: Fix mocks

  const token = (
    await Preferences.get({
      key: 'auth_token',
    })
  ).value
  const res = await fetch(`${API_URL}/users/change_password`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ old_password: contraseñaActual, new_password: nuevaContraseña }),
  })
  if (!res.ok) throw new Error(data.message || 'Error al cambiar contraseña')
  return res.json()
}

export async function invitarColaborador(email) {
  if (USAR_MOCKS) return authMock.registerCollaborator(email) // TODO: Fix mocks

  const token = (
    await Preferences.get({
      key: 'auth_token',
    })
  ).value
  const res = await fetch(`${API_URL}/users/register`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ email }),
  })
  if (!res.ok) throw new Error(data.message || 'Error al invitar colaborador')
  return res.json()
}

export async function registrarContraseña(tokenInvite, name, surname, password) {
  if (USAR_MOCKS) return authMock.createPassword(tokenInvite, name, surname, password) // TODO: Fix mocks

  const res = await fetch(`${API_URL}/users/create_password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token: tokenInvite, name, surname, password }),
  })
  if (!res.ok) throw new Error(data.message || 'Error al registrar contraseña')
  return res.json()
}
