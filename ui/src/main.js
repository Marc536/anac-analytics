import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createVuetify } from 'vuetify'  // Correção: Importar corretamente createVuetify
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css' // Importação dos ícones MDI

// Criar a instância do Vuetify corretamente
const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi', // Define o conjunto de ícones padrão como MDI
  },
})

window.onbeforeunload = () => {
  if (performance.navigation.type !== performance.navigation.TYPE_RELOAD) {
    localStorage.removeItem('hash')
  }
};

// Criar a aplicação Vue e adicionar o Vuetify
createApp(App)
  .use(router)
  .use(vuetify)  // Aqui usa a instância correta do Vuetify
  .mount('#app')
