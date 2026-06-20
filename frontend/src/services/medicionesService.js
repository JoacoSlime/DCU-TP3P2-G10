import { API_URL, USAR_MOCKS } from '@/config'
import { medicionesMock } from './mocks/medicionesMock.js'
import {
  adaptarListaMediciones,
  adaptarMedicionFrontendToBackend,
  adaptarMedicion,
} from './adapter.js'

export async function obtenerMedicionesPorPunto(puntoId) {
  let data

  if (USAR_MOCKS) {
    const response = await medicionesMock.get(puntoId)
    data = response.data.measures
  } else {
    const res = await fetch(`${API_URL}/spots/measures?uuid=${puntoId}`)
    if (!res.ok) throw new Error('Error al obtener mediciones')
    const response = await res.json()
    data = response.data.measures
  }

  return adaptarListaMediciones(data || [])
}

export async function crearMedicion(puntoId, medicionData) {
  const body = adaptarMedicionFrontendToBackend(medicionData, puntoId)

  if (USAR_MOCKS) {
    const response = await medicionesMock.add(body)
    return adaptarMedicion(response.data.measure)
  }

  const token = localStorage.getItem('auth_token')
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
  return adaptarMedicion(data.data.measure)
}

export async function eliminarMedicion(id) {
  if (USAR_MOCKS) {
    const response = await medicionesMock.delete(id)
    return response
  }

  const token = localStorage.getItem('auth_token')
  const res = await fetch(`${API_URL}/measures/delete?uuid=${id}`, {
    method: 'DELETE',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
  if (!res.ok) throw new Error('Error al eliminar medición')
  return res.json()
}
