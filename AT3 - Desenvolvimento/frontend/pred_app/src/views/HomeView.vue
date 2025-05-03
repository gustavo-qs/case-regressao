<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const changeView = (path) => {
  router.push(path);
};
</script>

<template>
  <div>
    <nav>
      <button @click="changeView('/users')">Gerenciar Usuário</button>
      <button @click="changeView('/predictions')">Prever Novos Dados</button>
      <button @click="changeView('/history')">Consultar Histórico</button>
    </nav>

    <router-view />
  </div>
</template>

<style scoped>
/* Container geral */
div {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background: #f0f4f8;
  color: #333;
  margin: 0;
  padding: 0;
}

/* Nav principal */
nav {
  display: flex;
  justify-content: center;
  gap: 1rem;
  background: #ffffff;
  padding: 1rem 0;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  position: sticky;
  top: 0;
  z-index: 10;
}

/* Botões de navegação */
nav button {
  background: #007acc;
  color: #fff;
  border: none;
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}

nav button:hover {
  background: #005fa3;
  transform: translateY(-2px);
}

nav button:active {
  background: #004a80;
  transform: translateY(0);
}

/* Área de conteúdo */
router-view {
  flex: 1;
  padding: 2rem;
}

/* Responsividade */
@media (max-width: 600px) {
  nav {
    flex-direction: column;
    gap: 0.5rem;
  }

  nav button {
    width: 100%;
    padding: 0.75rem;
    font-size: 0.9rem;
  }
}
</style>
