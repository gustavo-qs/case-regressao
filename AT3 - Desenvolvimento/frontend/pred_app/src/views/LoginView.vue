<template>
  <div class="login-container">
    <form @submit.prevent="handleLogin" class="login-form">
      <h2>Login</h2>
      <div class="form-group">
        <label for="email">E-mail</label>
        <input v-model="email" type="email" id="email" required />
      </div>
      <div class="form-group">
        <label for="password">Senha</label>
        <input v-model="password" type="password" id="password" required />
      </div>
      <p v-if="error" class="error-message">{{ error }}</p>
      <button type="submit" class="btn-login">Entrar</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const email = ref('');
const password = ref('');
const error = ref('');
const router = useRouter();

async function handleLogin() {
  error.value = '';
  try {
    const res = await fetch('http://localhost:8000/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email: email.value, senha: password.value })
    });
    if (!res.ok) {
      const data = await res.json();
      error.value = data.error || 'Erro ao logar. Tente novamente.';
      return;
    }
    const data = await res.json();
    localStorage.setItem('userSession', { ...data, email: email.value });
    await router.push('/');
  } catch (e) {
    error.value = 'Erro de conexão. Tente novamente.';
    console.error(e);
  }
}
</script>

<style scoped>

*, *::before, *::after {
  box-sizing: border-box;
}


.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  background: #f0f4f8;
  padding: 20px;
}


.login-form {
  background: #ffffff;
  padding: 2rem;
  border-radius: 0.5rem;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  width: 100%;
  max-width: 400px;
  font-family: sans-serif;
}


.login-form h2 {
  margin-bottom: 1.5rem;
  text-align: center;
  color: #333;
}


.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
}


.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
  font-size: 1rem;
  box-sizing: border-box;  
}


.error-message {
  color: #d9534f;
  margin-bottom: 1rem;
  text-align: center;
}


.btn-login {
  width: 100%;
  padding: 0.75rem;
  background-color: #007acc;
  color: #fff;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
  box-sizing: border-box;  
}


.btn-login:hover {
  background-color: #005fa3;
  transform: translateY(-2px);
}

.btn-login:active {
  background-color: #004a80;
  transform: translateY(0);
}
</style>
