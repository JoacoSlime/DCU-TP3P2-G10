export function adaptarPunto(spot) {
  return {
    id: spot.id,
    nombre: spot.title,
    lat: parseFloat(spot.latitude),
    lng: parseFloat(spot.longitude),
    contaminacion: spot.contaminacion || 'Media',
    descripcion: spot.descripcion || '',
    fechaCreacion: spot.created_at?.split('T')[0] || new Date().toISOString().split('T')[0],
    colaborador: spot.collaborator_id || 'anonimo',
    // Datos de medición (SpotWithMeasure)
    items_per_m2: parseFloat(spot.items_per_m2) || 0,
    weight: parseFloat(spot.weight) || 0,
    area: parseFloat(spot.area) || 0,
    pet: spot.pet || 0,
    pead: spot.pead || 0,
    pebd: spot.pebd || 0,
    pvc: spot.pvc || 0,
    pp: spot.pp || 0,
    ps: spot.ps || 0,
    pa: spot.pa || 0,
    other: spot.other || 0,
    ihr_plata: parseFloat(spot.ihr_plata) || 0,
    ibirp: parseFloat(spot.ibirp) || 0,
  }
}

export function adaptarListaPuntos(spots) {
  return (spots || []).map(adaptarPunto)
}

export function adaptarPuntoFrontendToBackend(punto) {
  return {
    title: punto.nombre,
    latitude: String(punto.lat),
    longitude: String(punto.lng),
    items_per_m2: String(punto.items_per_m2 || 0.001),
    weight: String(punto.weight || 0.001),
    area: String(punto.area || 0.001),
    pet: punto.pet || 1,
    pead: punto.pead || 1,
    pebd: punto.pebd || 0,
    pvc: punto.pvc || 0,
    pp: punto.pp || 0,
    ps: punto.ps || 0,
    pa: punto.pa || 0,
    other: punto.other || 0,
    ihr_plata: String(punto.ihr_plata || 0.001),
    ibirp: String(punto.ibirp || 0.001),
  }
}

export function adaptarMedicion(measure) {
  return {
    id: measure.id,
    puntoId: measure.spot_id,
    fecha: measure.created_at?.split('T')[0] || new Date().toISOString().split('T')[0],
    medicion: `${measure.items_per_m2} items/m2`,
    colaborador: measure.collaborator_id || 'anonimo',
    items_per_m2: parseFloat(measure.items_per_m2) || 0,
    weight: parseFloat(measure.weight) || 0,
    area: parseFloat(measure.area) || 0,
    pet: measure.pet || 0,
    pead: measure.pead || 0,
    pebd: measure.pebd || 0,
    pvc: measure.pvc || 0,
    pp: measure.pp || 0,
    ps: measure.ps || 0,
    pa: measure.pa || 0,
    other: measure.other || 0,
    ihr_plata: parseFloat(measure.ihr_plata) || 0,
    ibirp: parseFloat(measure.ibirp) || 0,
  }
}

export function adaptarListaMediciones(measures) {
  return (measures || []).map(adaptarMedicion)
}

export function adaptarMedicionFrontendToBackend(medicion, puntoId) {
  return {
    spot_id: puntoId,
    items_per_m2: String(medicion.items_per_m2 || 0.001),
    weight: String(medicion.weight || 0.001),
    area: String(medicion.area || 0.001),
    pet: medicion.pet || 1,
    pead: medicion.pead || 1,
    pebd: medicion.pebd || 0,
    pvc: medicion.pvc || 0,
    pp: medicion.pp || 0,
    ps: medicion.ps || 0,
    pa: medicion.pa || 0,
    other: medicion.other || 0,
    ihr_plata: String(medicion.ihr_plata || 0.001),
    ibirp: String(medicion.ibirp || 0.001),
  }
}

export function adaptarUsuario(user) {
  return {
    id: user.id,
    email: user.email,
    nombre: user.name || '',
    apellido: user.surname || '',
    rol: user.rol || user.role || 'colaborador',
  }
}
