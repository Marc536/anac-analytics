import { createApp, ref } from 'vue';

const App = {
  setup() {
    const username = ref('');
    const password = ref('');
    const message = ref('');

    const login = async () => {
      message.value = '';
      const response = await fetch('http://34.30.225.223:5000/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: username.value, password: password.value })
      });
      const data = await response.json();
      message.value = data.hash ? `Login successful: ${data.hash}` : data.error;
    };

    return { username, password, message, login };
  },
  template: `
    <div>
      <h1>Login</h1>
      <input v-model="username" placeholder="Username" />
      <input v-model="password" type="password" placeholder="Password" />
      <button @click="login">Login</button>
      <p>{{ message }}</p>
    </div>
  `
};

createApp(App).mount('#app');
