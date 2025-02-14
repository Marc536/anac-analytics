<template>
    <div class="login">
      <h2>Login</h2>
      <form @submit.prevent="handleLogin">
        <div>
          <label for="username">Username</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div>
          <label for="password">Password</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <button type="submit">Login</button>
      </form>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
    </div>
  </template>
  
  <script>
  import axios from 'axios'

  export const IP = `localhost`
  export const API_PORT = `5000`
  export const PROTOCOL = `http`
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
        let url = `${PROTOCOL}://${IP}:${API_PORT}/login`
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
  </style>
  