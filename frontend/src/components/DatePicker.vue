<script setup lang="ts">
import { ref, watch, onMounted } from 'vue'
import { format, parse } from 'date-fns'
import { ptBR } from 'date-fns/locale'
import { Calendar } from '@/components/ui/calendar'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'

const props = defineProps<{ modelValue: Date | undefined }>()
const emit = defineEmits<{ (e: 'update:modelValue', value: Date | undefined): void }>()

const date = ref<Date | undefined>(props.modelValue)
const inputValue = ref('')

onMounted(() => {
  inputValue.value = date.value ? format(date.value, 'yyyy-MM-dd') : ''
})

watch(() => props.modelValue, (newVal) => {
  date.value = newVal
  inputValue.value = newVal ? format(newVal, 'yyyy-MM-dd') : ''
})

function handleSelect(newDate: Date | undefined) {
  date.value = newDate
  inputValue.value = newDate ? format(newDate, 'yyyy-MM-dd') : ''
  emit('update:modelValue', newDate)
}

function handleInputChange(e: Event) {
  const value = (e.target as HTMLInputElement).value
  inputValue.value = value

  // converte corretamente
  const parsed = value ? new Date(value + 'T00:00:00') : undefined

  if (parsed && !isNaN(parsed.getTime())) {
    date.value = parsed
    emit('update:modelValue', parsed) // <-- sempre um Date aqui
  } else {
    date.value = undefined
    emit('update:modelValue', undefined)
  }
}

</script>

<template>
  <div
    class="flex items-center justify-between gap-1 border rounded-md px-2 py-1 bg-white shadow-sm 
           hover:shadow-md transition-all w-fit"
    style="max-width: 180px; min-width: 150px;"
  >
    <!-- Input editável -->
    <input
      type="date"
      v-model="inputValue"
      @input="handleInputChange"
      class="text-sm border-none outline-none w-full cursor-text bg-transparent"
    />

    <!-- Ícone que abre o calendário -->
    <Popover>
      <PopoverTrigger as-child>
        <button
          type="button"
          class="flex items-center justify-center p-0 w-5 h-5 text-gray-600 hover:text-black"
          title="Selecionar data"
        >
        </button>
      </PopoverTrigger>
      <PopoverContent class="w-auto p-0 bg-white border shadow-md rounded-md">
        <Calendar
          :model-value="date"
          @update:model-value="handleSelect"
          :locale="ptBR"
          initial-focus
        />
      </PopoverContent>
    </Popover>
  </div>
</template>

<style scoped>
:deep([data-reka-popper-content-wrapper]) {
  z-index: 60 !important;
}
</style>
