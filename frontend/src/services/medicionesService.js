import { API_URL } from '@/config'

console.log('API_URL actual:', API_URL)

export async function obtenerMedicionesPorPunto(puntoId) {
  const res = await fetch(`${API_URL}/spots/measures?uuid=${puntoId}`)
  if (!res.ok) throw new Error('Error al obtener mediciones')
  const data = await res.json()

  // Transformar directamente las mediciones al formato que usa el frontend
  return (data.data.measures || []).map((m) => ({
    id: m.id,
    puntoId: m.spot_id,
    fecha: m.created_at?.split('T')[0] || new Date().toISOString().split('T')[0],
    medicion: `${m.items_per_m2} items/m2`,
    items_per_m2: m.items_per_m2,
    colaborador: m.collaborator_id,
  }))
}

export async function crearMedicion(puntoId, medicionData) {
  const token = localStorage.getItem('auth_token')

  const body = {
    spot_id: puntoId,
    items_per_m2: '0.001',
    weight: '0.001',
    area: '0.001',
    pet: 1,
    pead: 1,
    pebd: 0,
    pvc: 0,
    pp: 0,
    ps: 0,
    pa: 0,
    other: 0,
    ihr_plata: '0.001',
    ibirp: '0.001',
  }

  const res = await fetch(`${API_URL}/measures/add`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(body),
  })

  const data = await res.json()
  if (!res.ok) throw new Error(data.message || 'Error al crear medición')
  return data
}

export async function eliminarMedicion(id) {
  const token = localStorage.getItem('auth_token')

  const res = await fetch(`${API_URL}/measures/delete?uuid=${id}`, {
    method: 'DELETE',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })

  const data = await res.json()
  if (!res.ok) throw new Error(data.message || 'Error al eliminar medición')

  return { success: true, message: data.message || 'Medición eliminada' }
}
