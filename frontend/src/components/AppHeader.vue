<script setup lang="ts">
    import QuickSearch from "@/components/QuickSearch.vue"
</script>

<template>
  <header
    class="flex justify-between h-16 shrink-0 items-center gap-2 px-4 py-10 border-b bg-white dark:bg-zinc-900 shadow-sm z-40"
  >
    <div class="flex-col">
        <h1 class="text-3xl tracking-tight text-neutral-600 font-sans">Sistema de Solicitações e Serviços</h1>
        <p class="text-xs text-neutral-700">DEPARTAMENTO DE SAÚDE, SEGURANÇA E BEM-ESTAR NO TRABALHO - DSS.A</p>
    </div>
    <QuickSearch />
  </header>
</template>

<script setup lang="ts"></script>

<style scoped>
header {
  transition: background 0.2s ease;
}
</style>
