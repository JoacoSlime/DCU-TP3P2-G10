<script setup>
function ayuda() {
    alert('Envía un correo a administrador@admin.com')
}
</script>

<template>
    <div class="app">
        <header class="header">
            <h1>Contaminación de la franja costera sur</h1>
        </header>

        <div class="contenedor-principal">
            <aside class="sidebar">
                <nav class="menu">
                    <router-link to="/" class="menu-item">Mapa</router-link>
                    <router-link to="/listado-puntos" class="menu-item">Listado de puntos</router-link>
                    <router-link to="/ajustes" class="menu-item">Ajustes</router-link>
                </nav>
            </aside>

            <main class="contenido">
                <router-view />
            </main>
        </div>

        <button class="boton-ayuda-flotante" @click="ayuda">Necesito ayuda</button>
    </div>
</template>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

.app {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background: var(--fondo-contenido);
}

.header {
    background: var(--gris-header);
    padding: 16px 24px;
}

.header h1 {
    color: var(--verde-oscuro);
    text-align: center;
}

.contenedor-principal {
    display: flex;
    flex: 1;
    overflow: hidden;
}

.sidebar {
    width: 280px;
    background: var(--gris-sidebar);
    padding: 5px;
}

.menu {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.menu-item {
    display: block;
    padding: 10px 16px;
    color: var(--texto-blanco);
    text-decoration: none;
    border-radius: 8px;
    font-size: 1rem;
}

.menu-item:hover {
    background: rgba(255, 255, 255, 0.1);
}

.menu-item.router-link-active {
    background: var(--verde);
    font-weight: 500;
}

.contenido {
    flex: 1;
    padding: 24px 32px;
    overflow-y: auto;
    background: var(--fondo-contenido);
}

.boton-ayuda-flotante {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: var(--verde);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 40px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    z-index: 9999999; 
}

.boton-ayuda-flotante:hover {
    background: var(--verde-oscuro);
}
</style>