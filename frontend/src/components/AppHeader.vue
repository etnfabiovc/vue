<script setup lang="ts">
import { ref } from "vue"
import { Search, UserRound } from "lucide-vue-next"

import Input from "@/components/ui/input/Input.vue"

const searchQuery = ref("")
</script>

<template>
  <header
    class="sticky top-0 z-30 flex h-20 w-full shrink-0 items-center justify-between gap-6 border-b border-border bg-background px-6 shadow-sm"
  >
    <div class="flex flex-col">
      <h1 class="text-2xl font-semibold tracking-tight">
        Sistema de Solicitações e Serviços
      </h1>
      <p class="text-sm font-medium text-muted-foreground">
        DEPARTAMENTO DE SAÚDE, SEGURANÇA E BEM-ESTAR NO TRABALHO - DSS.A
      </p>
    </div>

    <div class="flex flex-1 items-center justify-end gap-6">
      <div class="relative flex w-full max-w-md items-center">
        <Search class="pointer-events-none absolute left-3 h-4 w-4 text-muted-foreground" />
        <Input
          v-model="searchQuery"
          type="search"
          placeholder="Buscar..."
          class="w-full pl-9"
        />
      </div>

      <button
        type="button"
        class="flex h-10 w-10 items-center justify-center rounded-full border border-border bg-muted text-muted-foreground transition-colors hover:bg-muted/80"
        aria-label="Perfil"
      >
        <UserRound class="h-5 w-5" />
      </button>
    </div>
  </header>
</template>
