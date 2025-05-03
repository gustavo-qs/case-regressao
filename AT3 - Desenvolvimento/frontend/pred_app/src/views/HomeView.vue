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
      <button @click="changeView('/predict')">Prever Novos Dados</button>
      <button @click="changeView('/history')">Consultar Histórico</button>
    </nav>

    <router-view />
  </div>
</template>
