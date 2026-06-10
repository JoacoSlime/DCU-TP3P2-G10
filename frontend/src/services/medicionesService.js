const API_URL = '/api'

export async function obtenerMedicionesPorPunto(puntoId) {
  const res = await fetch(`${API_URL}/spots/measures?uuid=${puntoId}`)
  if (!res.ok) throw new Error('Error al obtener mediciones')
  const data = await res.json()
  return data.data.measures || []
}

export async function crearMedicion(puntoId, medicionData) {
  const token = localStorage.getItem('auth_token')
  const res = await fetch(`${API_URL}/measures/add`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
    },
    body: JSON.stringify({
      spot_id: puntoId,
      items_per_m2: '0',
      weight: '0',
      area: '0',
      pet: 0,
      pead: 0,
      pebd: 0,
      pvc: 0,
      pp: 0,
      ps: 0,
      pa: 0,
      other: 0,
      ihr_plata: '0',
      ibirp: '0',
    }),
  })
  if (!res.ok) throw new Error('Error al crear medición')
  return res.json()
}

export async function eliminarMedicion(id) {
  const token = localStorage.getItem('auth_token')
  const res = await fetch(`${API_URL}/measures/delete?uuid=${id}`, {
    method: 'DELETE',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
  if (!res.ok) throw new Error('Error al eliminar medición')
  return res.json()
}
