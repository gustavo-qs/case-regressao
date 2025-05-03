<template>
  <div class="users-view">
    <h1>Gerenciamento de Usuários</h1>

    <!-- Formulário de criação/edição -->
    <div class="user-form">
      <h2>{{ isEditing ? 'Editar Usuário' : 'Adicionar Usuário' }}</h2>
      <form @submit.prevent="saveUser">
        <input
          type="text"
          v-model="newUser.nome_completo"
          placeholder="Nome Completo"
          required
        />

        <!-- Email com pattern HTML5 e validação JS -->
        <input
          type="email"
          v-model="newUser.email"
          placeholder="Email"
          required
          pattern="^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
        />
        <small v-if="newUser.email && !isEmailValid" class="error">
          Email inválido
        </small>

        <!-- Telefone com máscara e pattern -->
        <input
          type="text"
          v-model="newUser.telefone"
          placeholder="(99) 99999-9999"
          required
          maxlength="15"
          @input="maskTelefone"
          pattern="^\(\d{2}\)\s\d{4,5}-\d{4}$"
        />
        <small v-if="newUser.telefone && !isTelefoneValid" class="error">
          Telefone deve ser (99) 9999-9999 ou (99) 99999-9999
        </small>

        <input
          type="password"
          v-model="newUser.senha"
          placeholder="Senha"
          :required="!isEditing"
        />

        <button
          type="submit"
          :disabled="!isFormValid"
        >
          {{ isEditing ? 'Salvar Alterações' : 'Adicionar' }}
        </button>
        <button
          type="button"
          v-if="isEditing"
          @click="cancelEdit"
          class="cancel-btn"
        >
          Cancelar
        </button>
        <button @click="$router.push('/')" style="background-color: #007bff; margin-left: 5px;">Voltar</button>
      </form>
    </div>

    <!-- Lista de cards -->
    <h2>Lista de Usuários</h2>
    <div class="user-list">
      <div
        class="user-card"
        v-for="user in users"
        :key="user.id"
      >
        <h3>{{ user.nome_completo }}</h3>
        <p>Email: {{ user.email }}</p>
        <p>Telefone: {{ user.telefone }}</p>
        <div class="actions">
          <button @click="selectUser(user)">Editar</button>
          <button @click="deleteUser(user.id)">Excluir</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      newUser: {
        id: null,
        nome_completo: "",
        email: "",
        telefone: "",
        senha: ""
      },
      isEditing: false,
    };
  },
  computed: {
    // valida email com regex JS
    isEmailValid() {
      const re = /^[a-zA-Z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$/
      return re.test(this.newUser.email)
    },
    // valida telefone com regex JS
    isTelefoneValid() {
      const re = /^\(\d{2}\)\s\d{4,5}-\d{4}$/
      return re.test(this.newUser.telefone)
    },
    // o form é válido se nome, senha (quando cria) e patterns estiverem ok
    isFormValid() {
      if (!this.newUser.nome_completo) return false
      if (!this.isEmailValid) return false
      if (!this.isTelefoneValid) return false
      if (!this.isEditing && !this.newUser.senha) return false
      return true
    }
  },
  methods: {
    maskTelefone(event) {
      let v = event.target.value.replace(/\D/g, "")
      if (v.length > 11) v = v.slice(0,11)
      // (99) 9999-9999 ou (99) 99999-9999
      v = v.replace(/^(\d{2})(\d)/, "($1) $2")
      v = v.replace(/(\d)(\d{4})$/, "$1-$2")
      this.newUser.telefone = v
    },

    async getUsers() {
      const res = await fetch("http://localhost:8000/usuarios")
      this.users = await res.json()
    },

    async saveUser() {
      if (this.isEditing) await this.updateUser()
      else await this.addUser()
      this.cancelEdit()
      this.getUsers()
    },

    async addUser() {
      const payload = { ...this.newUser }
      delete payload.id
      await fetch("http://localhost:8000/usuarios/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })
    },

    async updateUser() {
      await fetch("http://localhost:8000/usuarios/", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.newUser),
      })
    },

    selectUser(user) {
      this.newUser = { ...user }
      this.isEditing = true
    },

    cancelEdit() {
      this.isEditing = false
      this.newUser = { id: null, nome_completo: "", email: "", telefone: "", senha: "" }
    },

    async deleteUser(id) {
      if (!confirm("Confirma exclusão?")) return
      await fetch("http://localhost:8000/usuarios/", {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id }),
      })
      this.users = this.users.filter(u => u.id !== id)
    },
  },
  mounted() {
    this.getUsers()
  },
}
</script>

<style scoped>
.error {
  color: #d00;
  font-size: 0.85rem;
}
.users-view {
  max-width: 900px;
  margin: 40px auto;
  padding: 0 20px;
  font-family: sans-serif;
}
.actions {
  margin-top: 10px;
  display: flex;
  gap: 10px;
}
.cancel-btn {
  background: #ccc;
  color: #333;
  margin-left: 10px;
}

h1{
  font-size: 3rem;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}

h2 {
  font-size: 2rem;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
}
.user-form {
  margin: 30px auto;
  max-width: 800px;
  background: #ffffff;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  gap: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.user-form h2 {
  font-size: 1.8rem;
  margin-bottom: 10px;
  color: #333;
  text-align: center;
}

.user-form form {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-between;
}

.user-form input {
  flex: 1 1 48%;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: border-color 0.3s ease;
  font-size: 1rem;
}

.user-form input:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
}

.user-form button {
  padding: 12px 24px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.user-form button:hover {
  background-color: #0056b3;
  transform: translateY(-2px);
}

.user-form button:active {
  transform: scale(0.98);
}
.user-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: center;
  padding: 20px;
}

.user-card {
  background-color: #fff;
  border: 1px solid #eee;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  padding: 20px;
  width: 280px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.user-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.user-card h3 {
  margin: 0;
  font-size: 1.2rem;
  color: #333;
}

.user-card p {
  margin: 0;
  font-size: 0.95rem;
  color: #666;
}
</style>
