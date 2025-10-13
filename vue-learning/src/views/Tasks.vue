<script setup>
import { ref, watch, computed } from 'vue'
import { useTaskStore } from '../stores/useTaskStore'

const store = useTaskStore()
const newTask = ref('')

// Computed com base na store
const hasTasks = computed(() => store.totalTasks > 0)

// Watcher pra reagir sempre que o número de tarefas mudar
watch(
  () => store.totalTasks,
  (newVal, oldVal) => {
    console.log(`Tarefas: ${oldVal} → ${newVal}`)
  }
)

const addTask = () => {
  if (newTask.value.trim() !== '') {
    store.addTask(newTask.value)
    newTask.value = ''
  }
}
</script>

<template>
  <h2>Tarefas Persistentes</h2>
  <input v-model="newTask" placeholder="Nova tarefa" @keyup.enter="addTask" />
  <button @click="addTask">Adicionar</button>

  <ul>
    <li v-for="(task, i) in store.list" :key="i">{{ task }}</li>
  </ul>

  <p v-if="hasTasks">Total: {{ store.totalTasks }}</p>
  <p v-else>Nenhuma tarefa cadastrada.</p>
</template>
