<script setup lang="ts">
import { ref, onMounted, onUnmounted } from "vue"
import {
  Command,
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@/components/ui/command"
import { useRouter } from "vue-router"
import { Search } from "lucide-vue-next"

const open = ref(false)
const router = useRouter()

// Comandos / rotas
const commands = [
  { label: "Dashboard", route: "/" },
  { label: "Adicional de Periculosidade", route: "/reqperi" },
  { label: "Gestão de Solicitações", route: "/manager" },
  { label: "Cadastros", route: "/register" },
  { label: "Documentos de Segurança", route: "/documentos" },
  { label: "Sobre o Aplicativo", route: "/about" },
  { label: "Contato", route: "/contact" },
  { label: "Links Úteis", route: "/links" },
]

// Atalho Ctrl+K / Cmd+K
const onKeydown = (e: KeyboardEvent) => {
  if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === "k") {
    e.preventDefault()
    open.value = !open.value
  }
}

onMounted(() => window.addEventListener("keydown", onKeydown))
onUnmounted(() => window.removeEventListener("keydown", onKeydown))

// Navega ao selecionar
const onSelect = (route: string) => {
  open.value = false
  router.push(route)
}
</script>

<template>
  <div>
    <!-- Botão de abertura no header -->
    <button
      @click="open = true"
      class="flex items-center w-50 gap-2 px-3 py-1.5 text-sm text-muted-foreground bg-muted/30 hover:bg-muted/50 rounded-md border border-border"
    >
      <Search class="w-4 h-4" />
      <span class="hidden sm:inline">Buscar...</span>
      <kbd class="ml-auto text-xs text-gray-500">Ctrl + K</kbd>
    </button>

    <!-- Command Dialog -->
    <CommandDialog :open="open" @update:open="open = $event">
      <Command>
        <CommandInput placeholder="Digite um comando ou rota..." />
        <CommandList>
          <CommandEmpty>Nenhum resultado encontrado.</CommandEmpty>

          <CommandGroup heading="Navegação">
            <CommandItem
              v-for="cmd in commands"
              :key="cmd.route"
              @select="onSelect(cmd.route)"
              class="hover:cursor-pointer hover:bg-neutral-200"
            >
              {{ cmd.label }}
            </CommandItem>
          </CommandGroup>

          <CommandSeparator />

          <CommandGroup heading="Outros">
            <CommandItem 
            @select="onSelect('/profile')"
            class="hover:cursor-pointer hover:bg-neutral-200"
            >
            Perfil
            </CommandItem>
          </CommandGroup>
        </CommandList>
      </Command>
    </CommandDialog>
  </div>
</template>
