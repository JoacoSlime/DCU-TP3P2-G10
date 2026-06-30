import { API_URL, USAR_MOCKS } from '@/config'
import { puntosMock } from './mocks/puntosMock.js'
import { adaptarListaPuntos, adaptarPuntoFrontendToBackend, adaptarPunto } from './adapter.js'

export async function obtenerPuntos() {
  let data

  if (USAR_MOCKS) {
    const response = await puntosMock.list()
    data = response.data.spots
  } else {
    const res = await fetch(`${API_URL}/spots/list`)
    if (!res.ok) throw new Error('Error al obtener puntos')
    const response = await res.json()
    data = response.data.spots
  }

  return adaptarListaPuntos(data || [])
}

export async function obtenerPuntoPorId(id) {
  let spot

  if (USAR_MOCKS) {
    const response = await puntosMock.get(id)
    spot = response.data.spot
  } else {
    const res = await fetch(`${API_URL}/spots/get?uuid=${id}`)
    if (!res.ok) throw new Error('Punto no encontrado')
    const response = await res.json()
    spot = response.data.spot
  }

  return adaptarPunto(spot)
}

export async function crearPunto(puntoData) {
  const body = adaptarPuntoFrontendToBackend(puntoData)

  if (USAR_MOCKS) {
    const response = await puntosMock.add(body)
    return adaptarPunto(response.data.spot)
  }

  const token = localStorage.getItem('auth_token')
  const res = await fetch(`${API_URL}/spots/add`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(body),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.message || 'Error al crear punto')
  return adaptarPunto(data.data.spot)
}

export async function eliminarPunto(id) {
  if (USAR_MOCKS) {
    const response = await puntosMock.delete(id)
    return response
  }

  const token = localStorage.getItem('auth_token')
  const res = await fetch(`${API_URL}/spots/delete?uuid=${id}`, {
    method: 'DELETE',
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
  if (!res.ok) throw new Error('Error al eliminar punto')
  return res.json()
}
