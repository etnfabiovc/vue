<script setup lang="ts">
import { ref, computed, watch } from "vue"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Button } from "@/components/ui/button"
import { ChevronDown, Check } from "lucide-vue-next" // Importado o Check

interface Item {
  value: string
  label: string
}

const props = withDefaults(
  defineProps<{
    modelValue: string | string[] | undefined
    items: Item[]
    placeholder?: string
    multiple?: boolean
  }>(),
  {
    placeholder: "Selecione uma opção",
    multiple: false,
  }
)

const emit = defineEmits<{
  (e: "update:modelValue", value: string | string[] | undefined): void
}>()

const internalValue = ref<string | string[] | undefined>(props.modelValue)

watch(
  () => props.modelValue,
  (val) => {
    internalValue.value = val
  }
)

const displayLabel = computed(() => {
  if (!internalValue.value || (Array.isArray(internalValue.value) && internalValue.value.length === 0)) {
    return props.placeholder
  }
  if (props.multiple) {
    const selected = props.items.filter((i) =>
      (internalValue.value as string[]).includes(i.value)
    )
    return selected.map((i) => i.label).join(", ")
  } else {
    const item = props.items.find((i) => i.value === internalValue.value)
    return item ? item.label : props.placeholder
  }
})

function isChecked(value: string): boolean {
    if (props.multiple) {
        return Array.isArray(internalValue.value) && internalValue.value.includes(value);
    }
    return internalValue.value === value;
}

function toggleItem(value: string) {
    if (!props.multiple) return;

    const set = new Set(Array.isArray(internalValue.value) ? internalValue.value : [])
    const isCurrentlyChecked = set.has(value);

    // Inverte o estado
    const newState = !isCurrentlyChecked;

    if (newState) set.add(value)
    else set.delete(value)
    
    const arr = Array.from(set)
    internalValue.value = arr
    emit("update:modelValue", arr)
}

function selectSingle(value: string) {
  if (props.multiple) return
  internalValue.value = value
  emit("update:modelValue", value)
}
</script>

<template>
  <Popover>
    <PopoverTrigger as-child>
      <Button
        variant="outline"
        class="w-full justify-between text-left font-normal"
      >
        <span
          :class="{
            'text-muted-foreground':
              !internalValue ||
              (Array.isArray(internalValue) && internalValue.length === 0),
          }"
        >
          {{ displayLabel }}
        </span>
        <ChevronDown class="h-4 w-4 opacity-60" />
      </Button>
    </PopoverTrigger>

    <PopoverContent class="w-72 p-2 bg-white border rounded-md shadow-md">
      <div v-if="multiple" class="space-y-2">
        <div
          v-for="item in items"
          :key="item.value"
          class="flex items-center space-x-2 hover:bg-gray-50 px-2 py-1 rounded-md select-none cursor-pointer"
          @click="toggleItem(item.value)"
        >
          <!-- Ícone de Check se selecionado, ou um espaço vazio para alinhamento -->
          <Check v-if="isChecked(item.value)" class="h-4 w-4 text-primary transition-all duration-100 ease-in-out" />
          <div v-else class="h-4 w-4 opacity-0"></div>
          
          <span class="flex-1">
            {{ item.label }}
          </span>
        </div>
      </div>

      <div v-else class="space-y-1">
        <div
          v-for="item in items"
          :key="item.value"
          class="px-2 py-1 rounded-md hover:bg-gray-100 cursor-pointer"
          @click="selectSingle(item.value)"
        >
          {{ item.label }}
        </div>
      </div>
    </PopoverContent>
  </Popover>
</template>

<style scoped>
.hover\:bg-gray-50:hover { background-color: rgba(0,0,0,0.03); }
</style>
