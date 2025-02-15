<template>
    <div class="login">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <br>
        <div>
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required class="custom-input" />
        </div>
        <br>
        <div>
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required class="custom-input" />
        </div>
        <br>
        <button type="submit">Login</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import { API_CONFIG } from '@/config/config'

  export default {
    data() {
      return {
        username: '',
        password: '',
        errorMessage: '',
      };
    },
    methods: {
      postLogin (name, password) {
        let url = `${API_CONFIG.PROTOCOL}://${API_CONFIG.IP}:${API_CONFIG.API_PORT}/login`
        return axios.post(url, {
          name: name,
          password: password,
        }, {
          headers: {
              'Content-Type': 'application/json',
          },
        })
      },
      handleLogin() {
        this.postLogin(this.username, this.password)
        .then((response) => {
          if(response.status === 200) {
            localStorage.setItem('hash', response.data.hash)
            this.$router.push({ name: 'Graphic' });
          } else {
            this.errorMessage = 'Usuário ou senha inválidos. Tente novamente.'
          }

        })
        .catch((error) => {
          console.log(error)
          this.errorMessage = 'Usuário ou senha inválidos. Tente novamente.'
        })

      }
    }
  }
  </script>
  
  <style scoped>
  .login {
    max-width: 400px;
    margin: auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
  }
  button {
    background-color: #42b983;
    color: white;
    border: none;
    padding: 10px;
    cursor: pointer;
    width: 100%;
  }
  button:hover {
    background-color: #35a173;
  }
  .error {
    color: red;
    margin-top: 10px;
  }
  .custom-input {
    width: 75%;
    padding: 10px;
    border: 2px solid #1976d2; /* Cor do contorno */
    border-radius: 5px; /* Arredondamento das bordas */
    background-color: #e3f2fd; /* Cor de fundo */
    box-sizing: border-box;
    margin-left: 8px;
  }
  </style>
  