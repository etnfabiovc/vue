<script setup lang="ts">
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import AppSidebar from "@/components/AppSidebar.vue"
import AppHeader from "@/components/AppHeader.vue"
import { ChevronLeft, ChevronRight } from "lucide-vue-next"
</script>

<template>
  <SidebarProvider>
    <div class="flex h-screen overflow-hidden bg-background">
      <!-- SIDEBAR -->
      <AppSidebar />

      <!-- BOTÃO DE TOGGLE -->
      <SidebarTrigger asChild>
        <button
          class="fixed top-6 left-[calc(var(--sidebar-width)+4px)] z-50
                 rounded-full bg-sidebar text-sidebar-foreground border
                 border-sidebar-border shadow-sm p-1 transition-all duration-200
                 hover:bg-sidebar-border"
        >
          <ChevronLeft
            v-if="document.documentElement.getAttribute('data-sidebar-state') !== 'collapsed'"
            class="w-5 h-5"
          />
          <ChevronRight v-else class="w-5 h-5" />
        </button>
      </SidebarTrigger>

      <!-- CONTEÚDO PRINCIPAL -->
      <div class="flex-1 flex flex-col overflow-auto">
        <AppHeader />
        <main class="flex-1 p-6 overflow-y-hidden overflow-x-hidden bg-gray-100">
          <RouterView />
        </main>
      </div>
    </div>
  </SidebarProvider>
</template>
