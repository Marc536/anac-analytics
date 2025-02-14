import { createApp } from 'vue'
import App from './App.vue'
import router from './router'  // Importe o Vue Router

window.onbeforeunload = () => {
  localStorage.removeItem('hash');  // Remove a chave 'hash' ao fechar a aba/navegador
};

createApp(App)
  .use(router)  // Use o Vue Router na sua aplicação
  .mount('#app')
