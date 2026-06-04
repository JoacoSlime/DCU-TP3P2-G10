let puntos = [
  {
    id: 1,
    nombre: 'BER: BERNAL',
    medicion: 'Alta',
    lat: -34.718,
    lng: -58.285,
    fechaCreacion: '2025-01-01',
    colaborador: 'Francisco B. Lopez',
  },
  {
    id: 2,
    nombre: 'QUI: QUILMES',
    medicion: 'Media',
    lat: -34.72,
    lng: -58.26,
    fechaCreacion: '2025-01-15',
    colaborador: 'Maria Gomez',
  },
  {
    id: 3,
    nombre: 'HUD: HUDSON',
    medicion: 'Baja',
    lat: -34.73,
    lng: -58.24,
    fechaCreacion: '2025-02-01',
    colaborador: 'Carlos Perez',
  },
]

export async function obtenerPuntos() {
  return [...puntos]
}

export async function obtenerPuntoPorId(id) {
  const punto = puntos.find((p) => p.id === Number(id))
  if (!punto) throw new Error('Punto no encontrado')
  return { ...punto }
}

export async function crearPunto(puntoData) {
  const nuevoId = puntos.length > 0 ? Math.max(...puntos.map((p) => p.id)) + 1 : 1
  const nuevoPunto = {
    id: nuevoId,
    ...puntoData,
    fechaCreacion: new Date().toISOString().split('T')[0],
    colaborador: 'anonimo',
  }
  puntos.push(nuevoPunto)
  console.log('Punto creado:', nuevoPunto)
  return { success: true, punto: nuevoPunto }
}

export async function actualizarPunto(id, datosActualizados) {
  const index = puntos.findIndex((p) => p.id === Number(id))
  if (index === -1) throw new Error('Punto no encontrado')
  puntos[index] = { ...puntos[index], ...datosActualizados }
  return { success: true, punto: puntos[index] }
}

export async function eliminarPunto(id) {
  const index = puntos.findIndex((p) => p.id === Number(id))
  if (index === -1) throw new Error('Punto no encontrado')
  puntos.splice(index, 1)
  return { success: true }
}
