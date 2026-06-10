const API_URL = '/api'

export async function login(email, password) {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.message || 'Credenciales inválidas')

  // Guarda token
  if (data.token) {
    localStorage.setItem('auth_token', data.token)
    console.log('Token guardado:', data.token.substring(0, 20) + '...')
  } else if (data.data?.token) {
    localStorage.setItem('auth_token', data.data.token)
  }
  return data
}

export async function logout() {
  const token = localStorage.getItem('auth_token')
  if (token) {
    try {
      await fetch(`${API_URL}/auth/logout`, {
        method: 'GET',
        headers: { Authorization: `Bearer ${token}` },
      })
    } catch (e) {}
  }
  localStorage.removeItem('auth_token')
}

export async function obtenerUsuarioActual() {
  const token = localStorage.getItem('auth_token')
  if (!token) return null
  try {
    const res = await fetch(`${API_URL}/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    })
    if (!res.ok) return null
    const data = await res.json()
    return data.data || data.user
  } catch {
    return null
  }
}

export async function esAdmin() {
  const user = await obtenerUsuarioActual()
  return user?.role === 'admin' || user?.rol === 'admin'
}

export async function cambiarEmail(nuevoEmail) {
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

export async function cambiarContraseña(oldPassword, newPassword) {
  const token = localStorage.getItem('auth_token')
  const res = await fetch(`${API_URL}/collaborators/change_password`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
  })
  if (!res.ok) throw new Error('Error al cambiar contraseña')
  return res.json()
}

export async function invitarColaborador(email) {
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
  const res = await fetch(`${API_URL}/collaborators/create_password`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ token: tokenInvite, name, surname, password }),
  })
  if (!res.ok) throw new Error('Error al registrar contraseña')
  return res.json()
}
