<script setup lang="ts">
import type { LucideIcon } from 'lucide-vue-next'
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar'

defineProps<{
  info: Array<{
    name: string
    url: string
    icon: LucideIcon
  }>
}>()
</script>

<template>
  <SidebarGroup class="group-data-[collapsible=icon]:block">
    <SidebarGroupLabel>Informacoes</SidebarGroupLabel>
    <SidebarMenu>
      <SidebarMenuItem v-for="item in info" :key="item.name">
        <SidebarMenuButton as-child>
          <a :href="item.url">
            <component :is="item.icon" />
            <span>{{ item.name }}</span>
          </a>
        </SidebarMenuButton>
      </SidebarMenuItem>
    </SidebarMenu>
  </SidebarGroup>
</template>
