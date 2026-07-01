<template>
  <button class="hamburger-button" type="button" aria-label="Abrir menú de navegación">
    <ion-icon name="menu"></ion-icon>
  </button>
</template>

<style scoped>
ion-icon {
  flex: 1;
  font-size: 32px;
}

.hamburger-button {
  border: none;
  display: none;
  background: #2c3e50;
  color: #fff;
  font-size: 1.2rem;
  font-weight: 700;
  cursor: pointer;
  height: 100%;
  aspect-ratio: 1 / 1;
}

/* mostrar solo en celular */
@media screen and (max-width: 930px) {
  .hamburger-button {
    display: flex;
  }
}
</style>
