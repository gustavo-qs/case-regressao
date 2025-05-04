<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const changeView = (path) => {
  router.push(path);
};

const logout = async () => {
  try {
    const res = await fetch('http://localhost:8000/logout/', {
      method: 'POST',
      credentials: 'include',
    });
    if (res.ok) {
      localStorage.removeItem('userSession');
      router.push('/login');
    } else {
      console.error('Logout failed');
    }
  } catch (error) {
    console.error('Error during logout:', error);
  }
};
</script>

<template>
  <div class="app-container">
    <nav class="main-nav">
      <button @click="changeView('/users')" class="nav-btn">Gerenciar Usuário</button>
      <button @click="changeView('/predictions')" class="nav-btn">Prever Novos Dados</button>
      <button @click="changeView('/history')" class="nav-btn">Consultar Histórico</button>
      <button @click="logout" class="nav-btn logout-btn">Sair</button>
    </nav>
    <main class="view-container">
      <router-view />
    </main>
  </div>
</template>

<style scoped>
.app-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #eef2f7;
  color: #1a202c;
  margin: 0;
  padding: 0;
}

.main-nav {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  background-color: #ffffff;
  padding: 0.75rem 1rem;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid #e2e8f0;
}

.nav-btn {
  background-color: #3182ce;
  color: #fff;
  border: none;
  padding: 0.65rem 1.25rem;
  font-size: 0.95rem;
  font-weight: 500;
  border-radius: 0.375rem;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.1s ease;
}

.nav-btn:hover {
  background-color: #2b6cb0;
  transform: translateY(-1px);
}

.nav-btn:active {
  background-color: #2c5282;
  transform: translateY(0);
}

.logout-btn {
  background-color: #e53e3e;
}

.logout-btn:hover {
  background-color: #c53030;
}

.logout-btn:active {
  background-color: #9b2c2c;
}

.view-container {
  flex: 1;
  padding: 2rem;
  background-color: #f7fafc;
  border-top: 1px solid #e2e8f0;
}

@media (max-width: 768px) {
  .main-nav {
    flex-direction: column;
    align-items: stretch;
  }

  .nav-btn {
    width: 100%;
    text-align: center;
    font-size: 0.9rem;
  }
}
</style>
