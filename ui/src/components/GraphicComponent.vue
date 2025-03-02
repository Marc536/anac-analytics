<template>
  <div class="graphic-container">

    <v-dialog v-model="errorDialog" max-width="400px">
      <v-card>
        <v-card-title class="error-title">Erro</v-card-title>
        <v-card-text>{{ errorMessage }}</v-card-text>
        <v-card-actions>
          <v-btn color="red darken-3" text @click="errorDialog = false">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <div class="filters">
      <div>
        RANGE DE DATAS DE VOO
      </div>
      <div style="margin-left: 5px">
        DE:
        <input v-model="mesInicio" type="number" placeholder="Mês" min="1" max="12" class="custom-input-month" />
        <input v-model="anoInicio" type="number" placeholder="Ano"  class="custom-input-year"/>
      </div>
      <div>
        ATÉ:
        <input v-model="mesFim" type="number" placeholder="Mês" min="1" max="12" class="custom-input-month" />
        <input v-model="anoFim" type="number" placeholder="Ano" class="custom-input-year"/>
      </div>
      <br>
      <br>
      <div>
        MERCADO
      </div>
      <input v-model="mercado" type="text" placeholder="Mercado" maxlength="8" class="custom-input-market" />
      <div>
        <button @click="fetchData(true)">Buscar</button>
      </div>

      <br>
      <br>
      <div>
        Gráfico RPK
      </div>
    </div>

    <div class="chart-container">
      <AnacChart :chartData="chartData" />
    </div>

    <div>
      Page:
      <button style="margin-left: 10px" @click="goToLeft">⬅️</button>
      <button style="margin-left: 10px; margin-right: 50px" @click="goToRight">➡️</button>
      Zoom:
      <button style="margin-left: 10px" @click="goToUp">➖</button>
      <button style="margin-left: 10px" @click="goToDown">➕</button>
    </div>

    <button @click="goToLogin" class="logout-button">Logout</button>
  </div>
</template>

<script>
import axios from "axios";
import { API_CONFIG } from '@/config/config'
import { defineComponent, nextTick } from "vue";
import AnacChart from "./AnacChart.vue"
import { 
  VDialog, 
  VCard, 
  VCardTitle, 
  VCardText, 
  VCardActions, 
  VBtn 
} from 'vuetify/components';

export default defineComponent({
  name: "GraphicComponent",
  components: {
  AnacChart,
  VDialog,
  VCard,
  VCardTitle,
  VCardText,
  VCardActions,
  VBtn
  },
  data() {
    return {
      errorMessage: "",
      errorDialog: false,
      anoInicio: "",
      mesInicio: "",
      anoFim: "",
      mesFim: "",
      mercado: "",
      qtdVoos: 10,
      page: 1,
      totalPage: 2,
      chartData: [],
      hash: null,
    };
  },
  mounted() {
    this.hash = localStorage.getItem("hash")
    if (!this.hash) {
      this.$router.push("/");
    }
  },
  methods: {
    showError(message) {
      this.errorMessage = message
      this.errorDialog = true
    },
    goToLeft() {
      if (this.page >= 2) {
        this.page = this.page - 1
        this.fetchData()
      }
    },
    goToRight() {
      if ( this.totalPage >= this.page + 1 ) {
        this.page = this.page + 1
        this.fetchData()
      }
    },
    goToUp() {
      this.page = 1
      this.qtdVoos = this.qtdVoos + 10
      this.fetchData()
    },
    goToDown() {
      if (this.qtdVoos >= 20) {
        this.page = 1
        this.qtdVoos = this.qtdVoos - 10
        this.fetchData()
      }
    },
    getTableAnacFiltered () {
      let url = `${API_CONFIG.PROTOCOL}://${API_CONFIG.IP}:${API_CONFIG.API_PORT}/get_table_anac_filtered`
        return axios.get(url, {
          params: {
            ano_inicio: this.anoInicio,
            mes_inicio: this.mesInicio,
            ano_fim: this.anoFim,
            mes_fim: this.mesFim,
            mercado: this.mercado,
            limit: this.qtdVoos,
            page: this.page
          },
          headers: { Authorization: this.hash }
        })
    },
    fetchData(clean = false) {
      if(clean){
        this.errorMessage = ""
        this.qtdVoos = 10
        this.page = 1
        this.totalPage = 2
        this.chartData = []
      }
      this.getTableAnacFiltered()
      .then((response) => {
        if (response.status === 200) {
          if (Number.isFinite(response.data.total_pages)) {
            this.totalPage = response.data.total_pages
          }
          const rawData = response.data.data;
          nextTick(() => {
            this.chartData = rawData.map(item => {
              const rpkValue = parseFloat(item[3]);
              return {
                date: `${item[1].toString().padStart(2, '0')}/${item[0].toString()}`,
                rpk: isNaN(rpkValue) ? 0 : rpkValue
              };
            });
          });
        } else {
          this.showError('Entrada inválida. Verifique os campos e tente novamente.')
        }
      })
      .catch((error) => {
        console.log(error);
        this.showError('Entrada inválida. Verifique os campos e tente novamente.')
      });
    },
    goToLogin() {
      localStorage.removeItem("hash");
      this.$router.push("/");
    }
  }
});
</script>

<style scoped>
.error-title {
  background-color: #d32f2f;
  color: white;
  padding: 10px;
  font-size: 18px;
}
.graphic-container {
  text-align: center;
  padding: 20px;
}
.filters input {
  margin: 5px;
  padding: 8px;
}
.filters button {
  padding: 8px 15px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
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
.error {
    color: red;
    margin-top: 10px;
}
.custom-input-month {
  width: 80px;
  padding: 10px;
  border: 2px solid #1976d2;
  border-radius: 5px;
  background-color: #e3f2fd;
  box-sizing: border-box;
  margin-left: 8px;
}
.custom-input-year {
  width: 300px;
  padding: 10px;
  border: 2px solid #1976d2;
  border-radius: 5px;
  background-color: #e3f2fd;
  box-sizing: border-box;
  margin-left: 8px;
}
.custom-input-market {
  width: 300px;
  padding: 10px;
  border: 2px solid #1976d2;
  border-radius: 5px;
  background-color: #e3f2fd;
  box-sizing: border-box;
}
.chart-container {
  width: 100%; /* Garante que o container ocupe todo o espaço disponível */
  overflow-x: auto; /* Adiciona rolagem horizontal quando necessário */
  white-space: nowrap; /* Evita que o conteúdo quebre */
}
</style>
