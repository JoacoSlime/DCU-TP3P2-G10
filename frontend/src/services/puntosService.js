export async function obtenerPuntos() {
  const res = await fetch(`${API_URL}/spots/list`)
  if (!res.ok) throw new Error('Error al obtener puntos')
  const data = await res.json()
  return data.data.spots || []
}

export async function obtenerPuntoPorId(id) {
  const res = await fetch(`${API_URL}/spots/get?uuid=${id}`)
  if (!res.ok) throw new Error('Punto no encontrado')
  const data = await res.json()
  return data.data.spot
}

export async function crearPunto(puntoData) {
  const token = localStorage.getItem('auth_token')

  // Verifica token
  if (!token) {
    throw new Error('No hay token de autenticación. Inicia sesión nuevamente.')
  }

  console.log('Token enviado:', token.substring(0, 20) + '...')

  const body = {
    title: puntoData.nombre,
    latitude: String(puntoData.lat),
    longitude: String(puntoData.lng),
  }

  const res = await fetch(`${API_URL}/spots/add`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: ` ${token}`,
    },
    body: JSON.stringify(body),
  })

  const data = await res.json()
  if (!res.ok) {
    console.error('Error respuesta:', data)
    throw new Error(data.message || 'Error al crear punto')
  }
  return data
}

export async function eliminarPunto(id) {
  const token = localStorage.getItem('auth_token')
  const res = await fetch(`${API_URL}/spots/delete?uuid=${id}`, {
    method: 'DELETE',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
  if (!res.ok) throw new Error('Error al eliminar punto')
  return res.json()
}
