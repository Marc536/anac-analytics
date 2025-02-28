<template>
  <div>
    <canvas ref="chartCanvas" style="height: 400px;"></canvas>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import Chart from 'chart.js/auto';

export default {
  props: {
    chartData: Array // Recebe os dados como prop
  },
  setup(props) {
    const chartCanvas = ref(null);
    let chartInstance = null; // Para armazenar a instância do gráfico

    // Função para criar ou atualizar o gráfico
    const createChart = () => {
      // Se o gráfico já existir, destrói a instância anterior
      if (chartInstance) {
        chartInstance.destroy();
      }

      // Cria um novo gráfico com os dados mais recentes
      chartInstance = new Chart(chartCanvas.value, {
        type: 'line',
        data: {
          labels: props.chartData.map(item => item.date), // Usando as datas dos dados
          datasets: [{
            label: 'RPK',
            data: props.chartData.map(item => item.rpk), // Usando os valores de RPK
            borderColor: 'blue',
            backgroundColor: 'rgba(0, 0, 255, 0.1)',
            fill: true,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              beginAtZero: false
            }
          },
          plugins: {
            legend: {
              display: false // Remove a legenda (logo "RPK")
            },
            tooltip: {
              enabled: true, // Habilita o tooltip
              mode: 'index', // Exibe informações de todos os pontos na linha onde o mouse está
              intersect: false, // Exibe o tooltip mesmo quando o mouse está em uma linha, não apenas nos pontos
              callbacks: {
                // Personalize o conteúdo do tooltip
                title: (tooltipItems) => {
                  // Exibe a data no título
                  return tooltipItems[0].label;
                },
                label: (tooltipItem) => {
                  // Exibe o valor do rpk no tooltip
                  return `RPK: ${tooltipItem.raw.toFixed(2)}`; // Mostra o valor formatado
                }
              }
            }
          }
        }
      });
    };

    onMounted(() => {
      createChart(); // Cria o gráfico quando o componente for montado
    });

    // Monitorando mudanças em chartData e atualizando o gráfico
    watch(() => props.chartData, (newData) => {
      if (newData && newData.length > 0) {
        createChart(); // Atualiza o gráfico com os novos dados
      }
    }, { immediate: true });

    return { chartCanvas };
  }
};
</script>
