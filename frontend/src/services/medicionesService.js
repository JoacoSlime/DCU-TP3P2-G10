import { API_URL, USAR_MOCKS } from '@/config'
import { medicionesMock } from './mocks/medicionesMock.js'
import {
  adaptarListaMediciones,
  adaptarMedicionFrontendToBackend,
  adaptarMedicion,
} from './adapter.js'
import { Preferences } from '@capacitor/preferences'

export async function obtenerMedicionesPorPunto(puntoId) {
  let data

  if (USAR_MOCKS) {
    // TODO: Fix mocks
    const response = await medicionesMock.get(puntoId)
    data = response.data.measures
  } else {
    const res = await fetch(`${API_URL}/spots/measures/${puntoId}`)
    if (!res.ok) throw new Error(data.message || 'Error al obtener mediciones')
    const response = await res.json()
    data = response
  }

  return adaptarListaMediciones(data || [])
}

export async function crearMedicion(puntoId, medicionData) {
  const body = adaptarMedicionFrontendToBackend(medicionData, puntoId)

  if (USAR_MOCKS) {
    // TODO: Fix mocks
    const response = await medicionesMock.add(body)
    return adaptarMedicion(response.data.measure)
  }

  const token = (
    await Preferences.get({
      key: 'auth_token',
    })
  ).value
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
  return adaptarMedicion(data)
}

export async function eliminarMedicion(id) {
  if (USAR_MOCKS) {
    // TODO: Fix mocks
    const response = await medicionesMock.delete(id)
    return response
  }

  const token = (
    await Preferences.get({
      key: 'auth_token',
    })
  ).value
  const res = await fetch(`${API_URL}/measures/delete/${id}`, {
    method: 'DELETE',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
  if (!res.ok) throw new Error(data.message || 'Error al eliminar medición')
  return res.json()
}
