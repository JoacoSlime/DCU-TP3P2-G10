let mediciones = [
  {
    id: 1,
    puntoId: 1,
    fecha: '2026-01-01',
    medicion: 'Medición de ejemplo 1',
    colaborador: 'Francisco B. Lopez',
  },
  {
    id: 2,
    puntoId: 1,
    fecha: '2025-01-01',
    medicion: 'Medición de ejemplo 2',
    colaborador: 'Francisco B. Lopez',
  },
  {
    id: 3,
    puntoId: 2,
    fecha: '2025-06-01',
    medicion: 'Medición de ejemplo 3',
    colaborador: 'Maria Gomez',
  },
]

export async function obtenerMedicionesPorPunto(puntoId) {
  return mediciones.filter((m) => m.puntoId === Number(puntoId))
}

export async function crearMedicion(puntoId, medicionData) {
  const nuevoId = mediciones.length > 0 ? Math.max(...mediciones.map((m) => m.id)) + 1 : 1
  const nuevaMedicion = {
    id: nuevoId,
    puntoId: Number(puntoId),
    fecha: new Date().toISOString().split('T')[0],
    colaborador: 'anonimo',
    ...medicionData,
  }
  mediciones.push(nuevaMedicion)
  console.log('Medición creada:', nuevaMedicion)
  return { success: true, medicion: nuevaMedicion }
}

export async function eliminarMedicion(id) {
  const index = mediciones.findIndex((m) => m.id === Number(id))
  if (index === -1) throw new Error('Medición no encontrada')
  mediciones.splice(index, 1)
  return { success: true }
}
