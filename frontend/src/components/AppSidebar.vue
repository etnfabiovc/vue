<script setup lang="ts">
import { ref, onMounted } from "vue"
import type { SidebarProps } from "@/components/ui/sidebar"

import etnLogo from "../assets/images/etn_logo.svg"
import etnAtom from "../assets/images/etn_logo_atom.svg"

import {
  ChartArea,
  BookOpen,
  Bot,
  SquareKanban,
  CircleQuestionMark,
  Mail,
  Link,
  SquarePen,
} from "lucide-vue-next"

import NavMain from "@/components/NavMain.vue"
import NavManager from "@/components/NavManager.vue"
import NavInfo from "@/components/NavInfo.vue"
import NavUser from "@/components/NavUser.vue"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
} from "@/components/ui/sidebar"

// Props padrão do Sidebar (inicia recolhida)
const props = withDefaults(defineProps<SidebarProps>(), {
  collapsible: "icon",
})

const isExpanded = ref(false)

// Expande no hover
const expandSidebar = () => {
  isExpanded.value = true
  const sidebar = document.querySelector("[data-collapsible]")
  if (sidebar) sidebar.setAttribute("data-collapsible", "full")
}

// Recolhe ao sair do hover
const collapseSidebar = () => {
  isExpanded.value = false
  const sidebar = document.querySelector("[data-collapsible]")
  if (sidebar) sidebar.setAttribute("data-collapsible", "icon")
}

// Garante que começa recolhida
onMounted(() => {
  const sidebar = document.querySelector("[data-collapsible]")
  if (sidebar) sidebar.setAttribute("data-collapsible", "icon")
})

// Dados do menu
const data = {
  user: {
    name: "Fabio Carriço",
    email: "fabiovc@eletronuclear.gov.br",
    avatar: Bot,
  },
  navMain: [
    {
      title: "Serviços",
      url: "/service",
      icon: BookOpen,
      items: [
        { title: "Adicional de Periculosidade", url: "/reqperi" },
        { title: "Documentos de Segurança", url: "/documentos" },
        { title: "Gestão de Pendências", url: "/pendencias" },
      ],
    },
  ],
  manager: [
    { name: "Dashboard", url: "/", icon: ChartArea },
    { name: "Gestão de Solicitações", url: "/manager", icon: SquareKanban },
    { name: "Cadastros", url: "/register", icon: SquarePen },
  ],
  info: [
    { name: "Sobre o Aplicativo", url: "/about", icon: CircleQuestionMark },
    { name: "Contatos", url: "/contact", icon: Mail },
    { name: "Links Úteis", url: "/links", icon: Link },
  ],
}
</script>

<template>
  <Sidebar
    v-bind="props"
    class="transition-all duration-200 ease-linear"
    @mouseenter="expandSidebar"
    @mouseleave="collapseSidebar"
  >
    <!-- Cabeçalho -->
    <SidebarHeader class="flex justify-center py-3 transition-all duration-300">
      <a href="/" class="flex justify-center">
        <Transition name="fade" mode="out-in">
          <template v-if="isExpanded">
            <img
              :src="etnLogo"
              alt="ETN Logo"
              class="w-100 h-auto p-5 transition-all duration-300"
              key="logo"
            />
          </template>
          <template v-else>
            <img
              :src="etnAtom"
              alt="ETN Atom"
              class="w-10 h-auto opacity-80 transition-all duration-300"
              key="atom"
            />
          </template>
        </Transition>
      </a>
    </SidebarHeader>

    <!-- Conteúdo -->
    <SidebarContent>
      <NavMain :items="data.navMain" />
      <NavManager :info="data.manager" />
      <NavInfo :info="data.info" />
    </SidebarContent>

    <!-- Rodapé -->
    <SidebarFooter>
      <NavUser :user="data.user" />
    </SidebarFooter>

    <!-- Sem trigger -->
    <!-- <SidebarRail /> removido -->
  </Sidebar>
</template>

<style scoped>
a {
  align-self: center;
}

/* Transição da logo */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.020s ease, transform 0.020s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
