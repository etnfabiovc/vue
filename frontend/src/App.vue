<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue"
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import AppSidebar from "@/components/AppSidebar.vue"
import AppHeader from "@/components/AppHeader.vue"
import { ChevronLeft, ChevronRight } from "lucide-vue-next"

const isSidebarCollapsed = ref(false)

let observer: MutationObserver | null = null

const updateSidebarState = () => {
  isSidebarCollapsed.value =
    document.documentElement.getAttribute("data-sidebar-state") === "collapsed"
}

onMounted(() => {
  updateSidebarState()

  observer = new MutationObserver(() => updateSidebarState())
  observer.observe(document.documentElement, {
    attributes: true,
    attributeFilter: ["data-sidebar-state"],
  })
})

onBeforeUnmount(() => {
  observer?.disconnect()
  observer = null
})
</script>

<template>
  <SidebarProvider>
    <div class="relative flex h-screen overflow-hidden bg-background">
      <!-- SIDEBAR -->
      <AppSidebar />

      <!-- BOTÃO DE TOGGLE -->
      <SidebarTrigger asChild>
        <button
          class="absolute top-6 left-[calc(var(--sidebar-width)+4px)] z-50 rounded-full border border-sidebar-border bg-sidebar p-1 text-sidebar-foreground shadow-sm transition-all duration-200 hover:bg-sidebar-border"
        >
          <ChevronLeft v-if="!isSidebarCollapsed" class="h-5 w-5" />
          <ChevronRight v-else class="h-5 w-5" />
        </button>
      </SidebarTrigger>

      <!-- CONTEÚDO PRINCIPAL -->
      <div class="flex min-h-0 flex-1 flex-col">
        <AppHeader />
        <main class="flex-1 min-w-0 overflow-y-auto bg-muted/50">
          <RouterView v-slot="{ Component }">
            <component :is="Component" class="block h-full w-full" />
          </RouterView>
        </main>
      </div>
    </div>
  </SidebarProvider>
</template>
