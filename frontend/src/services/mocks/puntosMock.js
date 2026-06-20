let puntos = [
  {
    spot_id: '1a2b3c4d-5e6f-7890-abcd-ef1234567890',
    measure_id: '2b3c4d5e-6f78-90ab-cdef-1234567890ab',
    title: 'BER: BERNAL',
    latitude: '-34.718',
    longitude: '-58.285',
    collaborator_id: '3c4d5e6f-7890-abcd-ef12-34567890abcd',
    created_at: '2025-01-01T00:00:00Z',
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
    spot_id: '4d5e6f78-90ab-cdef-1234-567890abcdef',
    measure_id: '5e6f7890-abcd-ef12-3456-7890abcdef12',
    title: 'QUI: QUILMES',
    latitude: '-34.720',
    longitude: '-58.260',
    collaborator_id: '6f7890ab-cdef-1234-5678-90abcdef1234',
    created_at: '2025-01-15T00:00:00Z',
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
  {
    spot_id: '7g890abc-def1-2345-6789-0abcdef12345',
    measure_id: '8h901abc-def2-3456-7890-abcdef123456',
    title: 'HUD: HUDSON',
    latitude: '-34.730',
    longitude: '-58.240',
    collaborator_id: '9i012abc-def3-4567-8901-abcdef234567',
    created_at: '2025-02-01T00:00:00Z',
    items_per_m2: '30.0000',
    weight: '15.0000',
    area: '1500000.0000',
    pet: 1,
    pead: 3,
    pebd: 0,
    pvc: 0,
    pp: 5,
    ps: 2,
    pa: 0,
    other: 1,
    ihr_plata: '0.0200',
    ibirp: '0.0200',
  },
]

export const puntosMock = {
  async list() {
    return {
      status: 'success',
      result: puntos.length,
      data: { spots: [...puntos] },
    }
  },

  async get(id) {
    const punto = puntos.find((p) => p.spot_id === id)
    if (!punto) throw new Error('Punto no encontrado')
    return {
      status: 'success',
      data: { spot: { ...punto } },
    }
  },

  async add(puntoData) {
    const nuevoId = crypto.randomUUID()
    const nuevaMedidaId = crypto.randomUUID()
    const nuevoPunto = {
      spot_id: nuevoId,
      measure_id: nuevaMedidaId,
      title: puntoData.title,
      latitude: puntoData.latitude,
      longitude: puntoData.longitude,
      collaborator_id: 'usuario-mock-id',
      created_at: new Date().toISOString(),
      items_per_m2: puntoData.items_per_m2 || '0.0010',
      weight: puntoData.weight || '0.0010',
      area: puntoData.area || '0.0010',
      pet: puntoData.pet || 1,
      pead: puntoData.pead || 1,
      pebd: puntoData.pebd || 0,
      pvc: puntoData.pvc || 0,
      pp: puntoData.pp || 0,
      ps: puntoData.ps || 0,
      pa: puntoData.pa || 0,
      other: puntoData.other || 0,
      ihr_plata: puntoData.ihr_plata || '0.0010',
      ibirp: puntoData.ibirp || '0.0010',
    }
    puntos.push(nuevoPunto)
    console.log('Punto creado (mock):', nuevoPunto)
    return {
      status: 'success',
      data: {
        spot: nuevoPunto,
        measure: { id: nuevaMedidaId },
      },
    }
  },

  async delete(id) {
    const index = puntos.findIndex((p) => p.spot_id === id)
    if (index === -1) throw new Error('Punto no encontrado')
    puntos.splice(index, 1)
    console.log('Punto eliminado (mock):', id)
    return { status: 'success', message: 'Punto eliminado correctamente' }
  },
}
