<template>
  <div v-if="predictions.length" class="history-view">
    <h1>Histórico de Predições</h1>
    <table class="predictions-table">
      <thead>
        <tr>
          <th>#</th>
          <th>Usuário</th>
          <th>X1 Compactness</th>
          <th>X3 Wall Area</th>
          <th>X5 Height</th>
          <th>X6 Orientation</th>
          <th>X7 Glazing Area</th>
          <th>X8 Glazing Dist</th>
          <th>Y1 Predição</th>
          <th>Y2 Predição</th>
          <th>Data</th>
          <th>Ações</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(pred, index) in predictions" :key="pred.id">
          <td>{{ index + 1 }}</td>
          <td v-if="users.length">{{ users.find(u => u.id == pred.usuario)?.nome_completo || 'Desconhecido' }}</td>
          <td>{{ pred.x1 }}</td>
          <td>{{ pred.x3 }}</td>
          <td>{{ pred.x5 }}</td>
          <td>{{ pred.x6 }}</td>
          <td>{{ pred.x7 }}</td>
          <td>{{ pred.x8 }}</td>
          <td>{{ pred.y1.toFixed(2) }}</td>
          <td>{{ pred.y2.toFixed(2) }}</td>
          <td>{{ formatDate(pred.data) }}</td>
          <td>
            <button @click="deletePrediction(pred.id)">Excluir</button>
          </td>
        </tr>
      </tbody>
      <tfoot>
        <tr>
          <td colspan="12" class="table-actions">
            <button @click="$router.push('/')" style="background-color: #007bff;">Voltar</button>
          </td>
        </tr>
      </tfoot>
    </table>


  </div>
  <div v-else class="history-view">
    <h1>Histórico de Predições</h1>
    <p>Nenhuma previsão encontrada.</p>
    <button @click="$router.push('/predictions')" style="background-color: darkcyan;">Adicionar Previsão</button>
    <button @click="$router.push('/')" style="background-color: #007bff; margin-left: 5px;">Voltar</button>
  </div>
  <div class="chart-container">
    <canvas id="predictionsChart"></canvas>
  </div>

</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue';
import Chart from 'chart.js/auto';

const predictions = ref([]);
const users       = ref([]);
let   chart       = null;

function initChart() {
  const canvas = document.getElementById('predictionsChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: [],
      datasets: [
        { label: 'Y1', data: [], fill: false, tension: 0.1 },
        { label: 'Y2', data: [], fill: false, tension: 0.1 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        x: { display: true, title: { display: true, text: 'Predição' } },
        y: { display: true, title: { display: true, text: 'Valor' } }
      }
    }
  });
}

watch(predictions, (list) => {
  if (!chart) return;
  chart.data.labels           = list.map((_, i) => i + 1);
  chart.data.datasets[0].data = list.map(p => p.y1);
  chart.data.datasets[1].data = list.map(p => p.y2);
  chart.update();
}, { immediate: true });

async function fetchUsers() {
  try {
    const res = await fetch('http://localhost:8000/usuarios');
    users.value   = await res.json();
  } catch (err) {
    console.error('Erro ao buscar usuários:', err);
  }
}

async function fetchPredictions() {
  try {
    const res = await fetch('http://localhost:8000/previsoes/');
    predictions.value = await res.json();
  } catch (err) {
    console.error('Erro ao buscar previsões:', err);
  }
}

async function deletePrediction(id) {
  if (!confirm('Tem certeza que deseja excluir esta previsão?')) return;
  try {
    await fetch(`http://localhost:8000/previsoes/${id}/`, { method: 'DELETE' });
    predictions.value = predictions.value.filter(p => p.id !== id);
  } catch (err) {
    console.error('Erro ao excluir previsão:', err);
  }
}

function formatDate(iso) {
  return new Date(iso).toLocaleString();
}

onMounted(async () => {
  await nextTick();       // garante que o <canvas> exista
  initChart();            // só inicializa aqui
  await fetchUsers();
  await fetchPredictions();
});
</script>


<style scoped>
button {
  background-color: red;
  color: white;
  border: none;
  padding: 10px 20px;
  cursor: pointer;
  border-radius: 5px;
}
button:hover {
  background-color: darkred;
}
.history-view {
  max-width: 1000px;
  margin: 40px auto;
  padding: 0 20px;
  font-family: sans-serif;
}
.predictions-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 30px;
}
.predictions-table th,
.predictions-table td {
  padding: 8px 12px;
  border: 1px solid #ddd;
  text-align: center;
}
.predictions-table thead {
  background-color: #f5f5f5;
}
.chart-container {
  position: relative;
  height: 400px;
}
</style>
