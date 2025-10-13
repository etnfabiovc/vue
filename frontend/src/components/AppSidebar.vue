<script setup lang="ts">
import etnLogo from "../assets/images/etn_logo2.png"
import { useSidebar } from "@/components/ui/sidebar/utils"

import {
  ClipboardList,
  SquareKanban,
  Info,
  Mail,
  Link,
  ChevronDown,
  ChevronUp,
  Gauge,
  File,
  Flame,
  ClipboardCheck,
  Files,
  AlertTriangle,
} from "lucide-vue-next"

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar"

import {
  Collapsible,
  CollapsibleTrigger,
  CollapsibleContent,
} from "@/components/ui/collapsible"

import SidebarHeader from "./ui/sidebar/SidebarHeader.vue"

const { state, setOpen } = useSidebar()

const ensureExpanded = () => {
  if (state.value === "collapsed") {
    setOpen(true)
  }
}

const infoMenu = [
  { id: "about", title: "Sobre a Aplicação", url: "/about", icon: Info },
  { id: "contact", title: "Contatos", url: "/contact", icon: Mail },
  { id: "link", title: "Links Úteis", url: "/link", icon: Link },
]

const requestList = [
  {
    id: "reqperi",
    title: "Adicional de Periculosidade",
    url: "/reqperi",
    icon: Flame,
  },
  {
    id: "pendencias",
    title: "Gestão de Pendências",
    url: "/pendencias",
    icon: ClipboardCheck,
  },
  {
    id: "documentos",
    title: "Documentos de Segurança",
    url: "/documentos",
    icon: Files,
  },
  {
    id: "acidentes",
    title: "Acidentes e Incidentes de Trabalho",
    url: "/acidentes",
    icon: AlertTriangle,
  },
]

const managerList = [
  { id: "dashboard", title: "Dashboard", url: "/dashboard", icon: Gauge },
  { id: "register", title: "Cadastros", url: "/register", icon: File },
  { id: "followup", title: "Gerir Solicitações", url: "/followup", icon: SquareKanban },
]

</script>

<template>
  <Sidebar collapsible="icon" variant="sidebar" side="left">
    <SidebarHeader>
      <RouterLink to="/dashboard" class="etn-logo">
        <img :src="etnLogo" alt="go_to_dashboard" />
      </RouterLink>
    </SidebarHeader>

    <SidebarContent>
      <!-- GRUPO: Atendimento -->
      <SidebarGroup>
        <SidebarGroupLabel>Atendimento</SidebarGroupLabel>
        <Collapsible defaultOpen class="group/collapsible">
          <template #default="{ open }">
            <SidebarMenuItem>
              <CollapsibleTrigger asChild>
                <SidebarMenuButton @click="ensureExpanded">
                  <component :is="ClipboardList" class="h-4 w-4" />
                  <span>Serviços</span>
                  <ChevronUp v-if="open" class="ml-auto h-4 w-4" />
                  <ChevronDown v-else class="ml-auto h-4 w-4" />
                </SidebarMenuButton>
              </CollapsibleTrigger>

              <CollapsibleContent>
                <SidebarMenuSub>
                  <SidebarMenuSubItem v-for="item in requestList" :key="item.id">
                    <SidebarMenuButton asChild @click="ensureExpanded">
                      <RouterLink
                        :to="item.url"
                        class="flex w-full items-center gap-2 whitespace-normal"
                      >
                        <component :is="item.icon" class="h-4 w-4" />
                        <span>{{ item.title }}</span>
                      </RouterLink>
                    </SidebarMenuButton>
                  </SidebarMenuSubItem>
                </SidebarMenuSub>
              </CollapsibleContent>
            </SidebarMenuItem>
          </template>
        </Collapsible>
      </SidebarGroup>

      <!-- GRUPO: Administração -->
      <SidebarGroup>
        <SidebarGroupLabel>Administração</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem v-for="item in managerList" :key="item.id">
              <SidebarMenuButton asChild @click="ensureExpanded">
                <RouterLink :to="item.url">
                  <component :is="item.icon" class="h-4 w-4" />
                  <span>{{ item.title }}</span>
                </RouterLink>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>

      <!-- GRUPO: Informações -->
      <SidebarGroup>
        <SidebarGroupLabel>Informações</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem v-for="item in infoMenu" :key="item.id">
              <SidebarMenuButton asChild @click="ensureExpanded">
                <RouterLink :to="item.url">
                  <component :is="item.icon" class="h-4 w-4" />
                  <span>{{ item.title }}</span>
                </RouterLink>
              </SidebarMenuButton>
            </SidebarMenuItem>
          </SidebarMenu>
        </SidebarGroupContent>
      </SidebarGroup>
    </SidebarContent>
  </Sidebar>
</template>

<style scoped>
.etn-logo {
  width: 100%;
  padding: 20px;
}
.etn-logo:hover {
  cursor: pointer;
}
</style>
