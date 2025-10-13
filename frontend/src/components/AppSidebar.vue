<script setup lang="ts">
import etnLogo from "../assets/images/etn_logo2.png"
import { ref } from "vue"
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

const { state, expand } = useSidebar() // ✅ Aqui está o segredo

const infoMenu = [
  { id: "about", title: "Sobre a Aplicação", url: "/about", icon: Info },
  { id: "contact", title: "Contatos", url: "/contact", icon: Mail },
  { id: "link", title: "Links Úteis", url: "/link", icon: Link },
]

const requestList = [
  { id: "reqperi", title: "Adicional de Periculosidade", url: "/reqperi" },
  { id: "pendencias", title: "Gestão de Pendências", url: "/pendencias" },
  { id: "documentos", title: "Documentos de Segurança", url: "/documentos" },
  { id: "acidentes", title: "Acidentes e Incidentes de Trabalho", url: "/acidentes" },
]

const managerList = [
  { id: "dashboard", title: "Dashboard", url: "/dashboard", icon: Gauge },
  { id: "register", title: "Cadastros", url: "/register", icon: File },
  { id: "followup", title: "Gerir Solicitações", url: "/followup", icon: SquareKanban },
]

const serviceIsOpen = ref(false)
const toggleServiceMenu = () => (serviceIsOpen.value = !serviceIsOpen.value)
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
          <SidebarMenuItem>
            <CollapsibleTrigger asChild>
              <SidebarMenuButton >
                <!-- 👇 ao clicar, força a expansão -->
                <component :is="ClipboardList" @click="expand"/>
                Serviços
                <ChevronDown
                  v-if="!serviceIsOpen"
                  class="ml-auto"
                  @click.stop="toggleServiceMenu"
                />
                <ChevronUp
                  v-if="serviceIsOpen"
                  class="ml-auto"
                  @click.stop="toggleServiceMenu"
                />
              </SidebarMenuButton>
            </CollapsibleTrigger>

            <CollapsibleContent>
              <SidebarMenuSub>
                <SidebarMenuSubItem v-for="item in requestList" :key="item.id">
                  <SidebarMenuButton asChild @click="expand">
                    <RouterLink :to="item.url" class="sub-item">
                      <span>{{ item.title }}</span>
                    </RouterLink>
                  </SidebarMenuButton>
                </SidebarMenuSubItem>
              </SidebarMenuSub>
            </CollapsibleContent>
          </SidebarMenuItem>
        </Collapsible>
      </SidebarGroup>

      <!-- GRUPO: Administração -->
      <SidebarGroup>
        <SidebarGroupLabel>Administração</SidebarGroupLabel>
        <SidebarGroupContent>
          <SidebarMenu>
            <SidebarMenuItem v-for="item in managerList" :key="item.id">
              <SidebarMenuButton asChild @click="expand">
                <RouterLink :to="item.url">
                  <component :is="item.icon" @click="expand"/>
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
              <SidebarMenuButton asChild @click="expand">
                <RouterLink :to="item.url">
                  <component :is="item.icon" />
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
.sub-item {
  display: block;
  width: 100%;
  white-space: normal;
  word-wrap: break-word;
}
</style>
