<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { api } from '@/api'

import {
  Form, FormField, FormItem, FormLabel, FormControl, FormMessage, FormDescription,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import { Checkbox } from '@/components/ui/checkbox'
import DatePicker from "@/components/DatePicker.vue"
import DropdownMenu from '@/components/DropdownMenu.vue'

// === Bases ===
const dimUser = ref<Record<string, any>>({})
const dimTipo = ref<{ value: string; label: string }[]>([])
const dimRegime = ref<{ value: string; label: string }[]>([])
const dimLocal = ref<{ value: string; label: string }[]>([])
const riscosBase = ref<Record<string, Record<string, string[]>>>({})

// === Carrega dados das dimensões ===
onMounted(async () => {
  try {
    const [users, locais, tipos, regimes, risks] = await Promise.all([
      api.get('usuarios/'),
      api.get('locais/'),
      api.get('tipos/'),
      api.get('regimes/'),
      api.get('risks/grouped/')
    ])

    // Usuarios
    dimUser.value = Object.fromEntries(users.data.map((u: any) => [u.matricula, u]))

    // Locais
    dimLocal.value = locais.data.map((l: any) => ({
      value: l.codigo, label: l.descricao
    }))

    // Tipos
    dimTipo.value = tipos.data.map((t: any) => ({
      value: t.codigo, label: t.descricao
    }))

    // Regimes
    dimRegime.value = regimes.data.map((r: any) => ({
      value: r.codigo, label: r.descricao
    }))

    // Riscos (agrupado por código)
    riscosBase.value = Object.fromEntries(
      Object.entries(risks.data).map(([codigo, grupos]: any) => [codigo.toLowerCase(), grupos])
    )

    console.log('✅ Dimensões carregadas')
  } catch (err) {
    console.error('❌ Erro ao carregar dimensões:', err)
  }
})

// === Estados ===
const riscosSelecionados = ref<Record<string, string[]>>({
  inflamavel: [],
  eletricidade: [],
  radiacao: [],
})

// === Schema ===
const formSchema = toTypedSchema(
  z.object({
    matricula: z.string().min(1, 'Matrícula é obrigatória.'),
    nome: z.string().optional(),
    cargo: z.string().optional(),
    orgao: z.string().optional(),
    localAtividade: z.string().optional(),
    regimeTrabalho: z.string().optional(),
    tipoRequerimento: z.string().optional(),
    dataInicio: z.date({ required_error: 'Data de início é obrigatória.' }),
    dataTermino: z.date().optional().nullable(),
    tipoRisco: z.enum(['INFLAMAVEL', 'ELETRICIDADE', 'RADIACAO'], {
      required_error: 'Selecione o tipo de risco.',
    }),
    selecaoRiscos: z.array(z.string()).default([]).refine((val) => val.length > 0, {
      message: 'Selecione pelo menos um risco detalhado.',
    }),
  })
)

const { handleSubmit, values, setFieldValue } = useForm({
  validationSchema: formSchema,
  initialValues: { dataTermino: null, selecaoRiscos: [] },
})

// === Watch matrícula (busca automática) ===
watch(() => values.matricula, async (novaMatricula) => {
  if (!novaMatricula) return
  let userData = dimUser.value[novaMatricula]

  if (!userData) {
    try {
      const res = await api.get(`usuarios/?search=${novaMatricula}`)
      if (res.data.length > 0) {
        userData = res.data[0]
        dimUser.value[novaMatricula] = userData
      }
    } catch (err) {
      console.error('Erro ao buscar usuário:', err)
    }
  }

  if (userData) {
    setFieldValue('nome', userData.nome)
    setFieldValue('cargo', userData.funcao)
    setFieldValue('orgao', userData.uo)
  } else {
    setFieldValue('nome', '')
    setFieldValue('cargo', '')
    setFieldValue('orgao', '')
  }
})

// === Computed: riscos dinâmicos ===
function normalize(str: string) {
  return str.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase()
}

const riscosDisponiveis = computed(() => {
  const tipo = values.tipoRisco ? normalize(values.tipoRisco) : ""
  return riscosBase.value[tipo] || {}
})

// === Seleção de riscos ===
function toggleSubcategoria(subcat: string, checked: boolean, handleChange: (v: string[]) => void) {
  const tipo = normalize(values.tipoRisco || "")
  if (!tipo) return

  const descricoes = riscosDisponiveis.value[subcat] || []
  const atual = [...(riscosSelecionados.value[tipo] || [])]

  const novos = checked
    ? Array.from(new Set([...atual, ...descricoes]))
    : atual.filter((v) => !descricoes.includes(v))

  riscosSelecionados.value[tipo] = novos
  handleChange(novos)
  setFieldValue('selecaoRiscos', novos)
}

function toggleDescricao(desc: string, checked: boolean, handleChange: (v: string[]) => void) {
  const tipo = normalize(values.tipoRisco || "")
  if (!tipo) return

  const atual = [...(riscosSelecionados.value[tipo] || [])]
  const novos = checked
    ? Array.from(new Set([...atual, desc]))
    : atual.filter((v) => v !== desc)

  riscosSelecionados.value[tipo] = novos
  handleChange(novos)
  setFieldValue('selecaoRiscos', novos)
}

watch(() => values.tipoRisco, (novoTipo, antigoTipo) => {
  if (antigoTipo)
    riscosSelecionados.value[normalize(antigoTipo)] = [...values.selecaoRiscos]

  const restaurar = riscosSelecionados.value[normalize(novoTipo || '')] || []
  setFieldValue('selecaoRiscos', restaurar)
})

// === Submit ===
const onSubmit = handleSubmit(async (values) => {
  try {
    const payload = {
      status: 'Aberto',
      reqMatricula: values.matricula,
      funcMatricula: values.matricula,
      uo: values.orgao,
      regimeTrabalho: values.regimeTrabalho,
      localAtividade: values.localAtividade,
      tipoRequerimento: values.tipoRequerimento,
      dataInicio: values.dataInicio,
      dataFim: values.dataTermino || null,
      atividadesExecutadas: values.selecaoRiscos.join('; '),
      docUuid: crypto.randomUUID(),
    }

    const res = await api.post('requerimentos/', payload)
    console.log('✅ Requerimento enviado:', res.data)
    alert('Requerimento enviado com sucesso!')
  } catch (err) {
    console.error('❌ Erro ao enviar requerimento:', err)
    alert('Erro ao enviar o requerimento.')
  }
})
</script>



<template>
  <div class="flex flex-col h-full overflow-hidden p-4 bg-[linear-gradient(rgba(255,255,255,0.7),rgba(255,255,255,0.7))] rounded-md">
    <h1 class="text-2xl font-bold mb-4 flex-shrink-0 sticky top-0 bg-transparent z-10">
      Formulário de Solicitação de Adicional de Periculosidade
    </h1>

    <div class="flex-grow overflow-y-auto pr-2">
      <form @submit="onSubmit" class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <!-- COLUNA ESQUERDA -->
        <div class="flex flex-col space-y-4 lg:col-span-1">
          <!-- Seção 1 -->
          <section class="space-y-4 p-4 rounded-lg shadow-sm bg-white border border-gray-200">
            <h2 class="text-lg font-semibold mb-2">Informações Pessoais</h2>

            <FormField name="matricula" v-slot="{ componentField }">
              <FormItem>
                <FormLabel>Matrícula</FormLabel>
                <FormControl>
                  <Input type="text" maxlength="6" minlength="6" placeholder="Ex: 123456" v-bind="componentField" />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <FormField name="nome" v-slot="{ componentField }">
              <FormItem>
                <FormLabel>Nome</FormLabel>
                <FormControl>
                  <Input type="text" :model-value="values.nome" disabled />
                </FormControl>
              </FormItem>
            </FormField>

            <FormField name="cargo" v-slot="{ componentField }">
              <FormItem>
                <FormLabel>Cargo / Função</FormLabel>
                <FormControl>
                  <Input type="text" :model-value="values.cargo" disabled />
                </FormControl>
              </FormItem>
            </FormField>

            <FormField name="orgao" v-slot="{ componentField }">
              <FormItem>
                <FormLabel>Órgão de Lotação</FormLabel>
                <FormControl>
                  <Input type="text" :model-value="values.orgao" disabled />
                </FormControl>
              </FormItem>
            </FormField>
          </section>

          <!-- Seção 2 -->
          <section class="space-y-4 p-4 rounded-lg shadow-sm bg-white border border-gray-200">
            <h2 class="text-lg font-semibold mb-2">Informações Gerais da Atividade</h2>

            <FormField name="localAtividade" v-slot="{ value, handleChange }">
            <FormItem>
                <FormLabel>Local de Atividade</FormLabel>
                <FormControl>
                <DropdownMenu
                    multiple
                    :model-value="value"
                    @update:model-value="handleChange"
                    :items="dimLocal"
                    placeholder="Selecione o(s) local(is)"
                />
                </FormControl>
                <FormMessage />
            </FormItem>
            </FormField>

            <FormField name="regimeTrabalho" v-slot="{ componentField }">
            <FormItem>
                <FormLabel>Regime de Trabalho</FormLabel>
                <FormControl>
                <DropdownMenu
                    v-bind="componentField"
                    :items="[
                    { value: 'adm', label: 'Horário Administrativo' },
                    { value: 'turno', label: 'Turno' },
                    ]"
                />
                </FormControl>
                <FormMessage />
            </FormItem>
            </FormField>

            <FormField name="tipoRequerimento" v-slot="{ componentField }">
            <FormItem>
                <FormLabel>Tipo de Requerimento</FormLabel>
                <FormControl>
                <DropdownMenu
                    v-bind="componentField"
                    :items="dimTipo"
                />
                </FormControl>
                <FormMessage />
            </FormItem>
            </FormField>

          </section>
        </div>

        <!-- COLUNA DIREITA -->
        <div class="flex flex-col space-y-4 lg:col-span-2">
          <section class="space-y-4 p-4 rounded-lg shadow-sm bg-white border border-gray-200 flex flex-col flex-grow">
            <h2 class="text-lg font-semibold mb-2">Detalhamento das Atividades</h2>

            <div class="space-y-4 overflow-y-auto pr-2 flex-grow">
                <FormField name="dataInicio" v-slot="{ value, handleChange }">
                <FormItem>
                    <FormLabel>Data de Início / Mudança</FormLabel>
                    <FormControl>
                    <DatePicker
                        :model-value="value instanceof Date ? value : value ? new Date(value + 'T00:00:00') : undefined"
                        @update:model-value="(v) => handleChange(v instanceof Date ? v : v ? new Date(v + 'T00:00:00') : undefined)"
                    />
                    </FormControl>
                    <FormMessage />
                </FormItem>
                </FormField>

                <FormField name="dataTermino" v-slot="{ value, handleChange }">
                <FormItem>
                    <FormLabel>Data de Término (Opcional)</FormLabel>
                    <FormControl>
                    <DatePicker
                        :model-value="value instanceof Date ? value : value ? new Date(value + 'T00:00:00') : undefined"
                        @update:model-value="(v) => handleChange(v instanceof Date ? v : v ? new Date(v + 'T00:00:00') : undefined)"
                    />
                    </FormControl>
                    <FormMessage />
                </FormItem>
                </FormField>

              <FormField name="tipoRisco" v-slot="{ componentField }">
                <FormItem class="space-y-3">
                  <FormLabel>Tipo de Risco</FormLabel>
                  <FormControl>
                    <div class="flex flex-col space-y-1">
                      <RadioGroup v-bind="componentField">
                        <FormItem class="flex items-center space-x-3 space-y-0">
                          <FormControl><RadioGroupItem value="INFLAMAVEL" /></FormControl>
                          <FormLabel class="font-normal">Inflamáveis</FormLabel>
                        </FormItem>
                        <FormItem class="flex items-center space-x-3 space-y-0">
                          <FormControl><RadioGroupItem value="ELETRICIDADE" /></FormControl>
                          <FormLabel class="font-normal">Eletricidade</FormLabel>
                        </FormItem>
                        <FormItem class="flex items-center space-x-3 space-y-0">
                          <FormControl><RadioGroupItem value="RADIACAO" /></FormControl>
                          <FormLabel class="font-normal">Radiação Ionizante ou Substância Radioativa</FormLabel>
                        </FormItem>
                      </RadioGroup>
                    </div>
                  </FormControl>
                </FormItem>
              </FormField>
<!--init SELEÇÃO DOS RISCOS ENVOLVIDOS -->
                <FormField
                v-if="Object.keys(riscosDisponiveis).length > 0"
                name="selecaoRiscos"
                v-slot="{ value, handleChange }"
                >
                <FormItem>
                    <FormLabel>Seleção de Riscos (Detalhe)</FormLabel>
                    <FormDescription>
                    Selecione os riscos detalhados para o tipo
                    <b>{{ values.tipoRisco }}</b>.
                    </FormDescription>

                    <div class="space-y-3 max-h-60 overflow-y-auto border p-3 rounded-md">
                    <div
                        v-for="(descricoes, subcat) in riscosDisponiveis"
                        :key="subcat"
                        class="space-y-2"
                    >
                        <!-- Subcategoria -->
                        <div
                        class="flex items-center justify-between px-2 py-1 rounded-md transition-colors cursor-pointer"
                        :class="{
                            'bg-sky-200': descricoes.every((d) => (value || []).includes(d)),
                            'hover:bg-neutral-50': true
                        }"
                        @click="toggleSubcategoria(subcat, !(descricoes.every((d) => (value || []).includes(d))), handleChange)"
                        >
                        <div class="flex items-center gap-2">
                            <Check
                            v-if="descricoes.every((d) => (value || []).includes(d))"
                            class="h-4 w-4 text-primary"
                            />
                            <div v-else-if="descricoes.some((d) => (value || []).includes(d))" class="h-4 w-4 text-primary opacity-60">
                            <Check />
                            </div>
                            <div v-else class="h-4 w-4 opacity-0"><Check /></div>
                            <span class="font-medium">{{ subcat }}</span>
                        </div>
                        </div>

                        <!-- Descrições -->
                        <div class="pl-6 space-y-1">
                            <div
                                v-for="desc in descricoes"
                                :key="desc"
                                class="flex items-center px-2 py-1 rounded-md transition-colors cursor-pointer hover:bg-neutral-50"
                                :class="{'bg-sky-200': (value || []).includes(desc)}"
                                @click="toggleDescricao(desc, !(value || []).includes(desc), handleChange)"
                            >
                                <!-- Use 'flex' para alinhar ícone e texto -->
                                <div class="flex items-center w-full"> 
                                    
                                    <!-- 1. Contêiner do Ícone: Dê uma largura fixa para o ícone (e seu placeholder) e aplique margin à direita -->
                                    <div class="w-6 flex justify-start items-center mr-2">
                                        <Check
                                            v-if="(value || []).includes(desc)"
                                            class="h-4 w-4 text-primary"
                                        />
                                        <!-- O placeholder h-4 w-4 deve ser o mesmo para manter o alinhamento vertical/horizontal -->
                                        <div v-else class="h-4 w-4 opacity-0"></div> 
                                    </div>
                                    
                                    <!-- 2. Span da Descrição: Use 'flex-1' para que o span ocupe todo o espaço restante e alinhe o texto à esquerda -->
                                    <span class="text-sm text-left flex-1">{{ desc }}</span>
                                </div>
                            </div>
                        </div>

                        <hr class="my-2 border-gray-200" />
                    </div>
                    </div>

                    <FormMessage />
                </FormItem>
                </FormField>
<!--end SELEÇÃO DOS RISCOS ENVOLVIDOS -->

            </div>

            <div class="flex-shrink-0 pt-4">
              <Button type="submit" class="w-50 bg-[#2082c4] text-white hover:cursor-pointer hover:scale-108">Enviar Requerimento</Button>
            </div>
          </section>
        </div>
      </form>
    </div>
  </div>
</template>
