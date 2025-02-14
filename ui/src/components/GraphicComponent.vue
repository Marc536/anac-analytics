<template>
  <div class="graphic">
    <h2>Bem-vindo!</h2>
    <!-- Conteúdo adicional -->
    <button @click="goToLogin" class="logout-button">Sair</button>
  </div>
</template>

<script>
export default {
  name: 'GraphicComponent',
  data() {
    return {
      isLoggedIn: false,
    };
  },
  mounted() {
    // Verificar se a chave 'hash' existe no localStorage
    const hash = localStorage.getItem('hash');

    if (hash) {
      this.isLoggedIn = true;
    } else {
      this.$router.push('/');
    }
  },
  methods: {
    goToLogin() {
      localStorage.removeItem('hash');
      this.$router.push({ name: 'Login' });
    }
  }
}
</script>

<style scoped>
.graphic {
  text-align: center;
  padding: 50px;
}

.logout-button {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.logout-button:hover {
  background-color: #d32f2f;
}
</style>
