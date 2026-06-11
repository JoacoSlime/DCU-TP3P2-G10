<template>
  <main class="ayuda-container">
    <div class="ayuda-card">
      <div class="header">
        <h1>¿Necesitas ayuda?</h1>
        <p>Estamos aquí para asistirte con lo que necesites sobre la gestión de puntos de contaminación.</p>
      </div>

      <div class="contact-box">
        <div class="icon">✉️</div>
        <h3>Contacta a un administrador</h3>
        <p>Si tienes problemas técnicos, dudas sobre los permisos o necesitas reportar una anomalía, no dudes en escribirnos.</p>
        <a href="mailto:admin@admin.com" class="btn-mail">Enviar correo a soporte</a>
      </div>

    </div>
  </main>
</template>

<style scoped>
.ayuda-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f8fafc;
  padding: 20px;
  font-family: sans-serif;
}

.ayuda-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.05);
  max-width: 500px;
  width: 100%;
  text-align: center;
}

.header h1 { color: #1a202c; margin-bottom: 10px; }
.header p { color: #718096; margin-bottom: 30px; }

.contact-box {
  background: #f7fafc;
  padding: 30px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
}

.icon { font-size: 3rem; margin-bottom: 15px; }

.btn-mail {
  display: inline-block;
  margin-top: 20px;
  background-color: #19a1a8;
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  transition: background 0.3s;
}

.btn-mail:hover { background-color: #14858b; }

.footer-links { margin-top: 25px; }
.footer-links a { color: #19a1a8; text-decoration: none; font-size: 0.9rem; }
</style>