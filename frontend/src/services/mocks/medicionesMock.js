let mediciones = [
  {
    id: 'a1b2c3d4-5e6f-7890-abcd-ef1234567890',
    spot_id: '1a2b3c4d-5e6f-7890-abcd-ef1234567890',
    collaborator_id: '3c4d5e6f-7890-abcd-ef12-34567890abcd',
    created_at: '2026-01-01T00:00:00Z',
    items_per_m2: '150.0000',
    weight: '73.5000',
    area: '5913253.0000',
    pet: 3,
    pead: 11,
    pebd: 0,
    pvc: 1,
    pp: 26,
    ps: 6,
    pa: 0,
    other: 5,
    ihr_plata: '0.1000',
    ibirp: '0.1000',
  },
  {
    id: 'b2c3d4e5-6f78-90ab-cdef-1234567890ab',
    spot_id: '1a2b3c4d-5e6f-7890-abcd-ef1234567890',
    collaborator_id: '3c4d5e6f-7890-abcd-ef12-34567890abcd',
    created_at: '2025-01-01T00:00:00Z',
    items_per_m2: '120.0000',
    weight: '60.0000',
    area: '5800000.0000',
    pet: 2,
    pead: 9,
    pebd: 1,
    pvc: 0,
    pp: 20,
    ps: 5,
    pa: 0,
    other: 3,
    ihr_plata: '0.0800',
    ibirp: '0.0800',
  },
  {
    id: 'c3d4e5f6-7890-abcd-ef12-34567890abcd',
    spot_id: '4d5e6f78-90ab-cdef-1234-567890abcdef',
    collaborator_id: '6f7890ab-cdef-1234-5678-90abcdef1234',
    created_at: '2025-06-01T00:00:00Z',
    items_per_m2: '80.0000',
    weight: '45.2000',
    area: '3200000.0000',
    pet: 5,
    pead: 8,
    pebd: 2,
    pvc: 3,
    pp: 15,
    ps: 4,
    pa: 1,
    other: 2,
    ihr_plata: '0.0500',
    ibirp: '0.0500',
  },
]

export const medicionesMock = {
  async get(spotId) {
    const result = mediciones.filter((m) => m.spot_id === spotId)
    return {
      status: 'success',
      result: result.length,
      data: { measures: [...result] },
    }
  },

  async add(medicionData) {
    const nuevoId = crypto.randomUUID()
    const nuevaMedicion = {
      id: nuevoId,
      spot_id: medicionData.spot_id,
      collaborator_id: 'usuario-mock-id',
      created_at: new Date().toISOString(),
      items_per_m2: medicionData.items_per_m2 || '0.0010',
      weight: medicionData.weight || '0.0010',
      area: medicionData.area || '0.0010',
      pet: medicionData.pet || 1,
      pead: medicionData.pead || 1,
      pebd: medicionData.pebd || 0,
      pvc: medicionData.pvc || 0,
      pp: medicionData.pp || 0,
      ps: medicionData.ps || 0,
      pa: medicionData.pa || 0,
      other: medicionData.other || 0,
      ihr_plata: medicionData.ihr_plata || '0.0010',
      ibirp: medicionData.ibirp || '0.0010',
    }
    mediciones.push(nuevaMedicion)
    console.log('Medición creada (mock):', nuevaMedicion)
    return {
      status: 'success',
      data: { measure: nuevaMedicion },
    }
  },

  async delete(id) {
    const index = mediciones.findIndex((m) => m.id === id)
    if (index === -1) throw new Error('Medición no encontrada')
    mediciones.splice(index, 1)
    console.log('Medición eliminada (mock):', id)
    return { status: 'success', message: 'Medición eliminada correctamente' }
  },

  async list() {
    return {
      status: 'success',
      result: mediciones.length,
      data: { measures: [...mediciones] },
    }
  },
}
