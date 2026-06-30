import { Preferences } from '@capacitor/preferences'

let usuarios = [
  {
    id: 'f1e2d3c4-b5a6-9780-1234-567890abcdef',
    email: 'admin@admin.com',
    password: 'admin',
    rol: 'admin',
    name: 'Admin',
    surname: 'Principal',
  },
  {
    id: 'a2b3c4d5-e6f7-8901-2345-67890abcdef1',
    email: 'colaborador@test.com',
    password: 'colaborador',
    rol: 'colaborador',
    name: 'Colaborador',
    surname: 'Test',
  },
  {
    id: 'b3c4d5e6-f789-0123-4567-890abcdef123',
    email: 'invitado@test.com',
    password: 'invitado',
    rol: 'invitado',
    name: 'Invitado',
    surname: 'Usuario',
  },
]

let usuarioActual = null

export const authMock = {
  async login(email, password) {
    console.log('mock usuario')
    const usuario = usuarios.find((u) => u.email === email && u.password === password)
    if (!usuario) throw new Error('Credenciales inválidas')

    const { password: _, ...usuarioSinPass } = usuario
    usuarioActual = usuarioSinPass
    await Preferences.set({
      key: 'usuario',
      value: JSON.stringify(usuarioSinPass),
    })
    await Preferences.set({
      key: 'auth_token',
      value: 'mock-token-123',
    })
    await Preferences.set({
      key: 'logged',
      value: 'true',
    })
    await Preferences.set({
      key: 'role',
      value: usuario.rol,
    })
    return {
      status: 'success',
      data: {
        user: usuarioSinPass,
        token: 'mock-token-123',
      },
    }
  },

  async me() {
    if (!usuarioActual) {
      const stored = (
        await Preferences.get({
          key: 'usuario',
        })
      ).value
      if (stored) {
        usuarioActual = JSON.parse(stored)
      } else {
        throw new Error('No hay sesión')
      }
    }
    return {
      status: 'success',
      data: { user: usuarioActual },
    }
  },

  async logout() {
    usuarioActual = null
    await Preferences.remove({
      key: 'usuario',
    })
    await Preferences.remove({
      key: 'auth_token',
    })
    await Preferences.remove({
      key: 'logged',
    })
    await Preferences.remove({
      key: 'role',
    })
    return { status: 'success', message: 'logged out' }
  },

  async changeEmail(nuevoEmail) {
    const user = await authMock.me()
    console.log('Email cambiado (mock) a:', nuevoEmail)
    return {
      status: 'success',
      message: 'Email actualizado correctamente',
      data: { email: nuevoEmail },
    }
  },

  async changePassword(oldPassword, newPassword) {
    await authMock.me()
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/
    if (!regex.test(newPassword)) throw new Error('La contraseña no cumple los requisitos')
    console.log('Contraseña cambiada (mock)')
    return { status: 'success', message: 'Contraseña actualizada correctamente' }
  },

  async registerCollaborator(email) {
    await authMock.me()
    console.log('Invitación enviada (mock) a:', email)
    return { status: 'success', data: { user: { email } } }
  },

  async createPassword(token, name, surname, password) {
    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$/
    if (!regex.test(password)) throw new Error('La contraseña no cumple los requisitos')
    console.log('Contraseña registrada (mock) con token:', token)
    return { status: 'success', message: 'Contraseña actualizada correctamente' }
  },
}
