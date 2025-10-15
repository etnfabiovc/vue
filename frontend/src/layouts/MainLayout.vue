<script setup lang="ts">

  import AppSidebar from "@/components/AppSidebar.vue"
  import AppHeader from "@/components/AppHeader.vue"
  import {
    SidebarProvider,
    SidebarInset,
  } from "@/components/ui/sidebar"

  import backgroundImage from "@/assets/images/cnaaa.jpeg"

</script>

<template>
  <SidebarProvider>
    <div class="flex h-screen w-screen overflow-hidden">
      <!-- Sidebar -->
      <AppSidebar />

      <!-- Área principal -->
      <SidebarInset
        class="flex flex-col flex-1 h-screen w-full bg-background overflow-hidden"
      >
        <!-- Header fixo -->
        <AppHeader />

        <!-- Conteúdo sem rolagem -->
        <main class="flex-1 p-4 overflow-hidden h-full w-full bg-[linear-gradient(rgba(255,255,255,0.7),rgba(255,255,255,0.7)),url('/src/assets/images/cnaaa.jpeg')] bg-cover bg-center">
          <RouterView />
        </main>
      </SidebarInset>
    </div>
  </SidebarProvider>
</template>

<style scoped>
/* Evita qualquer overflow no documento */
  html,
  body,
  #app {
    height: 100%;
    width: 100%;
    margin: 0;
    overflow: hidden !important;
    overscroll-behavior: none;
  }

  /* Impede qualquer container interno de gerar scrolls */
  * {
    scrollbar-width: none; /* Firefox */
  }
  *::-webkit-scrollbar {
    display: none; /* Chrome, Edge, Safari */
  }
</style>
