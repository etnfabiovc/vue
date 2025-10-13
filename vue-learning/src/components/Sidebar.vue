<script setup>
import { ref, computed, watch } from 'vue'
import { useTaskStore } from '../stores/useTaskStore'

const store = useTaskStore()
const novaTarefa = ref('')

// computed derivado da store
const temTarefas = computed(() => store.totalTasks > 0)

// watch: observa mudanças globais
watch(
  () => store.totalTasks,
  (novo, antigo) => {
    console.log(`Total mudou de ${antigo} para ${novo}`)
  }
)

const adicionar = () => {
  if (novaTarefa.value.trim()) {
    store.addTask(novaTarefa.value)
    novaTarefa.value = ''
  }
}
</script>

<template>
  <input v-model="novaTarefa" @keyup.enter="adicionar" placeholder="Nova tarefa" />
  <button @click="adicionar">Adicionar</button>

  <ul>
    <li v-for="(t, i) in store.list" :key="i">{{ t }}</li>
  </ul>

  <p v-if="temTarefas">Total: {{ store.totalTasks }}</p>
  <p v-else>Nenhuma tarefa cadastrada.</p>
</template>
