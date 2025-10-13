<script setup>
import { ref, computed, watch } from 'vue'

const count = ref(0)

const increment = () => count.value++
const decrement = () => count.value--

const doubleCount = computed(() => count.value * 2)

watch(count, (newVal, oldVal) => {
  console.log(`O contador mudou de ${oldVal} para ${newVal}`)
})
</script>

<template>
  <div class="container">
    <h2>Exemplo: Composition API</h2>
    <p>Valor atual: {{ count }}</p>
    <p>Valor dobrado (computed): {{ doubleCount }}</p>

    <div class="actions">
      <button @click="decrement">-</button>
      <button @click="increment">+</button>
    </div>
  </div>
</template>

<style scoped>
.container {
  background: #f8f8f8;
  border-radius: 10px;
  padding: 20px;
  width: 250px;
  text-align: center;
}
.actions {
  display: flex;
  justify-content: center;
  gap: 10px;
}
button {
  padding: 6px 10px;
  border: none;
  background-color: #42b883;
  color: white;
  cursor: pointer;
  border-radius: 4px;
  font-size: 1.1rem;
}
</style>
