import { API_URL, USAR_MOCKS } from '@/config'
import { puntosMock } from './mocks/puntosMock.js'
import { adaptarListaPuntos, adaptarPuntoFrontendToBackend, adaptarPunto } from './adapter.js'
import { Preferences } from '@capacitor/preferences'

export async function obtenerPuntos(page = 1) {
  let data

  if (USAR_MOCKS) {
    // TODO: Fix mocks
    const response = await puntosMock.list()
    data = response.data.spots
  } else {
    const res = await fetch(`${API_URL}/spots/list/${page}`)
    if (!res.ok) throw new Error(data.message || 'Error al obtener puntos')
    const response = await res.json()
    data = response
  }

  return adaptarListaPuntos(data || [])
}

export async function obtenerPuntoPorId(id) {
  let spot

  if (USAR_MOCKS) {
    // TODO: Fix mocks
    const response = await puntosMock.get(id)
    spot = response.data.spot
  } else {
    const res = await fetch(`${API_URL}/spots/get/${id}`)
    if (!res.ok) throw new Error(data.message || 'Punto no encontrado')
    const response = await res.json()
    spot = response
  }

  return adaptarPunto(spot)
}

export async function crearPunto(puntoData) {
  const body = adaptarPuntoFrontendToBackend(puntoData)

  if (USAR_MOCKS) {
    // TODO: Fix mocks
    const response = await puntosMock.add(body)
    return adaptarPunto(response.data.spot)
  }

  const token = (
    await Preferences.get({
      key: 'auth_token',
    })
  ).value
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
  return adaptarPunto(data)
}

export async function eliminarPunto(id) {
  if (USAR_MOCKS) {
    const response = await puntosMock.delete(id)
    return response
  }

  const token = (await Preferences.get({ key: 'auth_token' })).value
  console.log('Token en eliminarPunto:', token ? token.substring(0, 20) + '...' : 'NO HAY TOKEN')

  if (!token) {
    throw new Error('No hay token de autenticación. Iniciá sesión nuevamente.')
  }

  console.log('Eliminando punto ID:', id)
  console.log('URL:', `${API_URL}/spots/delete/${id}`)

  const res = await fetch(`${API_URL}/spots/delete/${id}`, {
    method: 'DELETE',
    headers: {
      Authorization: `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  })

  console.log('Status:', res.status)

  const data = await res.json()
  console.log('Data:', data)

  if (!res.ok) {
    throw new Error(data.message || data.msg || 'Error al eliminar punto')
  }
  return data
}
