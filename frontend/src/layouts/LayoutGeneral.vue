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
/* Reset global */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    background: #ecf0f1;
    font-family: 'Segoe UI', Roboto, sans-serif;
}
</style>

<style scoped>
.app {
    display: flex;
    flex-direction: column;
    height: 100vh;
    background: #ecf0f1;
}

/* ===== HEADER ===== */
.header {
    background: #2c3e50;
    /* Fondo oscuro para buen contraste */
    padding: 16px 24px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.header h1 {
    margin: 0;
    font-size: 1.8rem;
    font-weight: 700;
    color: #ffffff;
    /* Blanco sobre fondo oscuro → contraste alto */
    text-align: center;
    letter-spacing: 0.5px;
}

/* ===== LAYOUT ===== */
.contenedor-principal {
    display: flex;
    flex: 1;
    overflow: hidden;
}

/* ===== SIDEBAR ===== */
.sidebar {
    width: 280px;
    background: #3a4a5f;
    /* Gris oscuro (contraste 4.54:1 con blanco) */
    padding: 24px 16px;
}

.menu {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.menu-item {
    display: block;
    padding: 10px 16px;
    color: #ffffff;
    text-decoration: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 500;
    transition: background 0.2s;
}

.menu-item:hover {
    background: rgba(255, 255, 255, 0.15);
}

/* ===== ACTIVO ===== */
.menu-item.router-link-active {
    background: #008737;
    /* Verde oscuro (contraste 4.65:1 con blanco) */
    color: #ffffff;
    font-weight: 600;
}

/* ===== CONTENIDO ===== */
.contenido {
    flex: 1;
    padding: 24px 32px;
    overflow-y: auto;
    background: #ecf0f1;
}

/* ===== BOTÓN AYUDA ===== */
.boton-ayuda-flotante {
    position: fixed;
    bottom: 24px;
    right: 24px;
    background: #008737;
    /* Verde oscuro (contraste 4.65:1) */
    color: #ffffff;
    border: none;
    padding: 12px 24px;
    border-radius: 40px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.25);
    transition: background 0.2s, transform 0.1s;
    z-index: 1000;
}

.boton-ayuda-flotante:hover {
    background: #006b2c;
}

.boton-ayuda-flotante:active {
    transform: scale(0.97);
}
</style>