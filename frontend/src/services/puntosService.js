import { API_URL } from '@/config'

console.log('API_URL actual:', API_URL)

export async function obtenerPuntos() {
  const res = await fetch(`${API_URL}/spots/list`)
  if (!res.ok) throw new Error('Error al obtener puntos')
  const data = await res.json()

  // Transformar los puntos para que tengan un campo 'id'
  return (data.data.spots || []).map((spot) => ({
    id: spot.spot_id || spot.id, // ← Agregar campo 'id'
    title: spot.title,
    latitude: spot.latitude,
    longitude: spot.longitude,
    // ... otros campos que necesites
  }))
}

export async function obtenerPuntoPorId(id) {
  if (!id) {
    throw new Error('ID no proporcionado')
  }

  const res = await fetch(`${API_URL}/spots/get/${id}`)
  if (!res.ok) throw new Error('Punto no encontrado')
  const data = await res.json()
  return data.data.spot
}

export async function crearPunto(puntoData) {
  const token = localStorage.getItem('auth_token')

  if (!token) {
    throw new Error('No hay token de autenticación. Inicia sesión nuevamente.')
  }

  console.log('Token enviado:', token.substring(0, 20) + '...')

  const body = {
    title: puntoData.nombre,
    latitude: parseFloat(puntoData.lat),
    longitude: parseFloat(puntoData.lng),
    items_per_m2: 0.001,
    weight: 0.001,
    area: 0.001,
    pet: 1,
    pead: 1,
    pebd: 0,
    pvc: 0,
    pp: 0,
    ps: 0,
    pa: 0,
    other: 0,
    ihr_plata: 0.001,
    ibirp: 0.001,
  }

  console.log('Enviando body:', body)

  const res = await fetch(`${API_URL}/spots/add`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
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
