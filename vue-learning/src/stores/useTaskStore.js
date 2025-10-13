// src/stores/useTaskStore.js
import { defineStore } from 'pinia'

export const useTaskStore = defineStore('tasks', {
  state: () => ({
    list: [],
  }),

  persist: true,

  actions: {
    addTask(task) {
      this.list.push(task)
    },
    removeTask(index) {
      this.list.splice(index, 1)
    },
    clearTasks() {
      this.list = []
    },
  },

  getters: {
    totalTasks: (state) => state.list.length,
  },
})
