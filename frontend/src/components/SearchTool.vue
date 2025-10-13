<script setup lang="ts">
import { useMagicKeys } from "@vueuse/core"
import { ref, watch } from "vue"

const open = ref(false)

const keys = useMagicKeys()

const handleOpenChange = () => {
  open.value = !open.value
}

const ctrlP = keys["Ctrl+P"]
const metaP = keys["Meta+P"]
const escapeKey = keys["Escape"]

const triggerCombos = [ctrlP, metaP].filter(
  (combo): combo is Exclude<typeof ctrlP, undefined> => combo !== undefined,
)

if (triggerCombos.length) {
  triggerCombos.forEach((combo) => {
    watch(combo, (isPressed) => {
      if (isPressed) {
        open.value = true
      }
    })
  })
}

if (escapeKey) {
  watch(escapeKey, (isPressed) => {
    if (isPressed) {
      open.value = false
    }
  })
}
</script>

<template>
  <div>
    <p class="text-sm text-muted-foreground">
      <kbd
        class="pointer-events-none inline-flex h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-[10px] font-medium text-muted-foreground opacity-100"
      >
        <span class="text-xs">ctrl +</span>p
      </kbd>
    </p>
    <CommandDialog :open="open" @update:open="handleOpenChange">
      <CommandInput placeholder="Type a command or search..." />
      <CommandList>
        <CommandEmpty>No results found.</CommandEmpty>
        <CommandGroup heading="Suggestions">
          <CommandItem value="calendar">
            Calendar
          </CommandItem>
          <CommandItem value="search-emoji">
            Search Emoji
          </CommandItem>
          <CommandItem value="calculator">
            Calculator
          </CommandItem>
        </CommandGroup>
        <CommandSeparator />
        <CommandGroup heading="Settings">
          <CommandItem value="profile">
            Profile
          </CommandItem>
          <CommandItem value="billing">
            Billing
          </CommandItem>
          <CommandItem value="settings">
            Settings
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  </div>
</template>