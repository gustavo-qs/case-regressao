<template>
  <div class="previsoes-view">
    <h1>Predição de Eficiência Energética</h1>

    <!-- Formulário de entrada -->
    <div class="input-form">
      <h2>Parâmetros de Previsão</h2>
      <form @submit.prevent="requestPrediction">
        <div class="grid">
          <div v-for="(field, key) in inputs" :key="key" class="form-group">
            <label :for="key">{{ field.label }}</label>
            <input
              :id="key"
              type="number"
              step="any"
              v-model.number="field.value"
              required
            />
          </div>
        </div>
        <button type="submit" :disabled="isRequesting">
          {{ isRequesting ? 'Aguardando...' : 'Prever' }}
        </button>
        <button type="button" @click="generateRandomInputs()" :disabled="isRequesting" style="margin-left: 10px; background-color: darkorange;">
          Aleatório
        </button>
        <!-- consultar histórico -->
        <button type="button" @click="router.push('/history')" :disabled="isRequesting" style="margin-left: 10px; background-color: darkcyan;">
          Consultar Histórico
        </button>
        <button @click="$router.push('/')" style="background-color: #007bff; margin-left: 5px;">Voltar</button>
      </form>
    </div>
    <!-- Nota sobre parâmetros não utilizados -->
    <div class="note">
      <p>
        <strong>Observações:</strong> 
        <ul>
          <li>
            Os parâmetros <strong>X2 (Surface Area)</strong> e <strong>X4 (Roof Area)</strong> não são necessários para a predição e foram omitidos.
          </li>
          <li>
            <strong>X1 (Relative Compactness)</strong>: variável contínua, valores típicos entre 0.62 e 0.98.
          </li>
          <li>
            <strong>X3 (Wall Area)</strong>: variável contínua, valores típicos entre 61.54 e 351.75 m².
          </li>
          <li>
            <strong>X5 (Overall Height)</strong>: variável discreta, só pode assumir <code>3.50</code> ou <code>7.00</code>.
          </li>
          <li>
            <strong>X6 (Orientation)</strong>: variável discreta, só pode assumir os inteiros
            <code>2</code> (Norte), <code>3</code> (Leste), <code>4</code> (Sul) ou <code>5</code> (Oeste).
          </li>
          <li>
            <strong>X7 (Glazing Area)</strong>: variável contínua, valores típicos entre 0.00 e 0.40.
          </li>
          <li>
            <strong>X8 (Glazing Area Distribution)</strong>: variável discreta, só pode assumir os inteiros
            de <code>0</code> a <code>5</code>.
          </li>
        </ul>
      </p>
    </div>

    <!-- Resultado da predição -->
    <div v-if="prediction !== null" class="result-card">
      <h2>Resultado</h2>
      <p>
        Predição: <strong>{{ prediction }}</strong>
      </p>
      <button @click="savePrediction" :disabled="isSaving">
        {{ isSaving ? 'Salvando...' : 'Salvar' }}
      </button>
    </div>
  </div>
</template>

<script>
import { useRouter } from 'vue-router';

export default {
  name: 'PrevisoesView',
  data() {
    return {
      inputs: {
        X1_compactness:    { label: 'Compactness (X1)', value: null },
        X3_wall_area:      { label: 'Wall Area (X3)', value: null },
        X5_height:         { label: 'Height (X5)', value: null },
        X6_orientation:    { label: 'Orientation (X6)', value: null },
        X7_glazing_area:   { label: 'Glazing Area (X7)', value: null },
        X8_glazing_dist:   { label: 'Glazing Dist (X8)', value: null },
      },
      prediction: null,
      isRequesting: false,
      isSaving: false,
    };
  },
  methods: {
    // Monta payload a partir dos inputs
    buildPayload() {
      const out = {};
      for (const key in this.inputs) {
        out[key] = this.inputs[key].value;
      }
      return out;
    },
    /**
     * Gera um número float aleatório entre min (inclusivo) e max (inclusivo).
     * @param {number} min - O valor mínimo.
     * @param {number} max - O valor máximo.
     * @returns {number} - Um número float aleatório entre min e max.
     */
    randFloat(min, max) {
      return Math.random() * (max - min) + min;
    },

    /**
     * Gera um número inteiro aleatório entre min (inclusivo) e max (inclusivo).
     * @param {number} min - O valor mínimo.
     * @param {number} max - O valor máximo.
     * @returns {number} - Um número inteiro aleatório entre min e max
     */
    randInt(min, max) {
      return Math.floor(Math.random() * (max - min + 1)) + min;
    },

    /**
     * Gera inputs aleatórios plausíveis para as 8 variáveis do Energy Efficiency Dataset.
     * @returns {Object} - Um objeto contendo os inputs aleatórios.     * 
     */
    generateRandomInputs() {
      var randomInputs = {
        X1_compactness:    parseFloat(this.randFloat(0.62, 0.98).toFixed(3)), // contínuo :contentReference[oaicite:6]{index=6}
        X3_wall_area:      parseFloat(this.randFloat(61.54, 351.75).toFixed(1)), // contínuo :contentReference[oaicite:7]{index=7}
        X5_height:         [3.50, 7.00][this.randInt(0, 1)],                   // discreto :contentReference[oaicite:8]{index=8}
        X6_orientation:    this.randInt(2, 5),                                 // inteiro :contentReference[oaicite:9]{index=9}
        X7_glazing_area:   parseFloat(this.randFloat(0.00, 0.40).toFixed(2)),  // contínuo :contentReference[oaicite:10]{index=10}
        X8_glazing_dist:   this.randInt(0, 5)                                  // inteiro :contentReference[oaicite:11]{index=11}
      };

      this.inputs = {
        X1_compactness:    { label: 'Compactness (X1)', value: randomInputs.X1_compactness },
        X3_wall_area:      { label: 'Wall Area (X3)', value: randomInputs.X3_wall_area },
        X5_height:         { label: 'Height (X5)', value: randomInputs.X5_height },
        X6_orientation:    { label: 'Orientation (X6)', value: randomInputs.X6_orientation },
        X7_glazing_area:   { label: 'Glazing Area (X7)', value: randomInputs.X7_glazing_area },
        X8_glazing_dist:   { label: 'Glazing Dist (X8)', value: randomInputs.X8_glazing_dist },
      };
    },
    getLoggedUser(){
      return 1;
    },
    async requestPrediction() {
      this.prediction = null;
      this.isRequesting = true;
      try {
        const res = await fetch('http://localhost:8000/prever/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(this.buildPayload()),
        });
        if (!res.ok) throw new Error(res.statusText);
        const data = await res.json();
        // espera {'predictions': [...]}
        this.prediction = data.predictions[0];
      } catch (err) {
        console.error('Erro na predição:', err);
        alert('Falha ao obter predição. Veja console.');
      } finally {
        this.isRequesting = false;
      }
    },

    // Salva input + resultado no backend
    async savePrediction() {
      this.isSaving = true;
      const payload ={
        x1: this.inputs.X1_compactness.value,
        x3: this.inputs.X3_wall_area.value,
        x5: this.inputs.X5_height.value,
        x6: this.inputs.X6_orientation.value,
        x7: this.inputs.X7_glazing_area.value,
        x8: this.inputs.X8_glazing_dist.value,
        y1: this.prediction[0],
        y2: this.prediction[1],
        usuario: this.getLoggedUser()
      }
      try {
        const res = await fetch('http://localhost:8000/previsoes/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          credentials: 'include',
          body: JSON.stringify(payload),
        });
        if (!res.ok) throw new Error(res.statusText);
        alert('Salvo com sucesso!');
        this.prediction = null;
      } catch (err) {
        console.error('Erro ao salvar:', err);
        alert('Falha ao salvar. Veja console.');
      } finally {
        this.isSaving = false;
      }
    }
  },
  setup() {
    const router = useRouter();
    return { router };
  },
};
</script>

<style scoped>
.note {
  margin: 20px 0;
  padding: 12px;
  background: #f0f8ff;
  border-radius: 8px;
  font-size: 0.9rem;
}

.previsoes-view {
  max-width: 700px;
  margin: 40px auto;
  padding: 0 20px;
  font-family: sans-serif;
}
.input-form {
  background: #fff;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  margin-bottom: 24px;
}
.input-form .grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
}
.input-form .form-group {
  flex: 1 1 calc(50% - 16px);
  display: flex;
  flex-direction: column;
}
.input-form label {
  margin-bottom: 8px;
  font-weight: 500;
}
.input-form input {
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
}
.input-form button {
  margin-top: 16px;
  padding: 10px 20px;
  background: #007bff;
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
}
.input-form button:disabled {
  opacity: 0.6;
  cursor: default;
}

.result-card {
  background: #f9faff;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.result-card p {
  font-size: 1.2rem;
}
.result-card button {
  margin-top: 12px;
  padding: 8px 16px;
  background: #28a745;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
.result-card button:disabled {
  opacity: 0.6;
  cursor: default;
}
</style>