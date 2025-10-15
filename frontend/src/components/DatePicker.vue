<script setup lang="ts">
import { ref, watch } from 'vue'
import { format } from 'date-fns'
import { Calendar } from '@/components/ui/calendar'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { CalendarIcon } from 'lucide-vue-next'
import { DateValue, getLocalTimeZone, parseDate, toDate } from '@internationalized/date'

const INPUT_FORMAT = 'yyyy-MM-dd'
const TIME_ZONE = getLocalTimeZone()

const props = defineProps<{
  modelValue?: Date | null
}>()

const emit = defineEmits<{
  (e: 'update:modelValue', value: Date | undefined): void
}>()

const calendarValue = ref<DateValue | undefined>(
  props.modelValue ? parseDate(format(props.modelValue, INPUT_FORMAT)) : undefined
)
const inputValue = ref(props.modelValue ? format(props.modelValue, INPUT_FORMAT) : '')

function syncFromDate(value: Date | null | undefined) {
  if (value && !Number.isNaN(value.getTime())) {
    const formatted = format(value, INPUT_FORMAT)
    inputValue.value = formatted
    calendarValue.value = parseDate(formatted)
  } else {
    inputValue.value = ''
    calendarValue.value = undefined
  }
}

watch(
  () => props.modelValue,
  (newValue) => {
    syncFromDate(newValue ?? undefined)
  }
)

function handleSelect(value: DateValue | undefined) {
  calendarValue.value = value

  if (value) {
    const selected = toDate(value, TIME_ZONE)
    inputValue.value = format(selected, INPUT_FORMAT)
    emit('update:modelValue', selected)
  } else {
    inputValue.value = ''
    emit('update:modelValue', undefined)
  }
}

function handleInput(event: Event) {
  const value = (event.target as HTMLInputElement).value
  inputValue.value = value

  if (!value) {
    calendarValue.value = undefined
    emit('update:modelValue', undefined)
    return
  }

  const parsed = new Date(`${value}T00:00:00`)
  if (!Number.isNaN(parsed.getTime())) {
    calendarValue.value = parseDate(value)
    emit('update:modelValue', parsed)
  } else {
    calendarValue.value = undefined
    emit('update:modelValue', undefined)
  }
}
</script>

<template>
  <div
    class="flex items-center justify-between gap-1 border rounded-md px-2 py-1 bg-white shadow-sm hover:shadow-md transition-all w-fit"
    style="max-width: 180px; min-width: 150px;"
  >
    <input
      type="date"
      :value="inputValue"
      @input="handleInput"
      class="text-sm border-none outline-none w-full cursor-text bg-transparent"
    />

    <Popover>
      <PopoverTrigger as-child>
        <button
          type="button"
          class="flex items-center justify-center p-0 w-5 h-5 text-gray-600 hover:text-black"
          title="Selecionar data"
        >
          <CalendarIcon class="h-4 w-4" />
        </button>
      </PopoverTrigger>
      <PopoverContent class="w-auto p-0 bg-white border shadow-md rounded-md">
        <Calendar
          :model-value="calendarValue"
          @update:model-value="handleSelect"
          locale="pt-BR"
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
