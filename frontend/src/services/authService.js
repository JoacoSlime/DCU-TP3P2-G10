let usuarios = [
  { id: 1, email: 'admin@mail.com', password: '1234', rol: 'admin', invitado: false },
  {
    id: 2,
    email: 'colaborador@mail.com',
    password: '1234',
    rol: 'colaborador',
    invitado: false,
  },
]

export function obtenerUsuarioActual() {
  const userStr = localStorage.getItem('usuario_actual')
  return userStr ? JSON.parse(userStr) : null
}

function guardarUsuarioActual(usuario) {
  if (usuario) {
    localStorage.setItem('usuario_actual', JSON.stringify(usuario))
  } else {
    localStorage.removeItem('usuario_actual')
  }
}

export async function login(email, password) {
  console.log('Email recibido:', email)
  console.log('Password recibida:', password)
  const usuario = usuarios.find((u) => u.email === email && u.password === password)
  console.log('Usuario encontrado:', usuario)
  if (!usuario) throw new Error('Credenciales inválidas')
  const { password: _, ...usuarioSinPass } = usuario
  guardarUsuarioActual(usuarioSinPass)
  return { success: true, usuario: usuarioSinPass }
}

export async function logout() {
  guardarUsuarioActual(null)
}

export async function estaLogueado() {
  return obtenerUsuarioActual() !== null
}

export async function esAdmin() {
  const user = obtenerUsuarioActual()
  return user?.rol === 'admin'
}

export async function cambiarEmail(nuevoEmail, contraseñaActual) {
  const usuarioActual = obtenerUsuarioActual()
  if (!usuarioActual) throw new Error('No hay sesión')
  const usuarioEnArray = usuarios.find((u) => u.id === usuarioActual.id)
  if (usuarioEnArray.password !== contraseñaActual) throw new Error('Contraseña incorrecta')
  usuarioEnArray.email = nuevoEmail
  const { password: _, ...usuarioSinPass } = usuarioEnArray
  guardarUsuarioActual(usuarioSinPass)
  return { success: true, nuevoEmail }
}

export async function cambiarContraseña(contraseñaActual, nuevaContraseña) {
  const usuarioActual = obtenerUsuarioActual()
  if (!usuarioActual) throw new Error('No hay sesión')
  const usuarioEnArray = usuarios.find((u) => u.id === usuarioActual.id)
  if (usuarioEnArray.password !== contraseñaActual) throw new Error('Contraseña actual incorrecta')
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/
  if (!regex.test(nuevaContraseña)) throw new Error('Requisitos de contraseña no cumplidos')
  usuarioEnArray.password = nuevaContraseña
  return { success: true }
}

export async function invitarColaborador(email) {
  if (!(await esAdmin())) throw new Error('No autorizado')
  if (usuarios.find((u) => u.email === email)) throw new Error('El usuario ya existe')
  const nuevoId = Math.max(...usuarios.map((u) => u.id)) + 1
  usuarios.push({
    id: nuevoId,
    email,
    password: '',
    rol: 'colaborador',
    invitado: true,
    token: `invite_${Date.now()}`,
  })
  return { success: true }
}

export async function registrarContraseña(token, nuevaContraseña) {
  const usuario = usuarios.find((u) => u.token === token)
  if (!usuario) throw new Error('Token inválido')
  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/
  if (!regex.test(nuevaContraseña)) throw new Error('Requisitos no cumplidos')
  usuario.password = nuevaContraseña
  usuario.invitado = false
  delete usuario.token
  return { success: true }
}
