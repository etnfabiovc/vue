<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useForm } from 'vee-validate'
import { toTypedSchema } from '@vee-validate/zod'
import * as z from 'zod'
import { api } from '@/api'

import {
  FormField,
  FormItem,
  FormLabel,
  FormControl,
  FormMessage,
  FormDescription,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { RadioGroup, RadioGroupItem } from '@/components/ui/radio-group'
import DatePicker from '@/components/DatePicker.vue'
import DropdownMenu from '@/components/DropdownMenu.vue'
import { Check } from 'lucide-vue-next'

type RiskType = 'INFLAMAVEL' | 'ELETRICIDADE' | 'RADIACAO'

interface SelectOption {
  value: string
  label: string
}

interface ApiUser {
  matricula: string
  nome: string
  funcao?: string | null
  email?: string | null
}

interface RiskOption {
  id: number
  descricao: string
}

type GroupedRisks = Record<string, Record<string, RiskOption[]>>

interface FormValues {
  matricula: string
  nome: string
  cargo: string
  orgao: string
  localAtividade: string
  regimeTrabalho: string
  tipoRequerimento: string
  dataInicio: Date | undefined
  dataTermino: Date | null
  tipoRisco: RiskType | undefined
  selecaoRiscos: number[]
}

const dimUser = ref<Record<string, ApiUser>>({})
const dimTipo = ref<SelectOption[]>([])
const dimRegime = ref<SelectOption[]>([])
const dimLocal = ref<SelectOption[]>([])
const dimUO = ref<SelectOption[]>([])
const riscosBase = ref<GroupedRisks>({})
const riskDescriptions = ref<Record<number, string>>({})

function createEmptyRiskSelection(): Record<string, number[]> {
  return {
    inflamavel: [],
    eletricidade: [],
    radiacao: [],
  }
}

const riscosSelecionados = ref<Record<string, number[]>>(createEmptyRiskSelection())

const formSchema = toTypedSchema(
  z.object({
    matricula: z.string().min(1, 'Informe a matricula.'),
    nome: z.string().optional(),
    cargo: z.string().optional(),
    orgao: z.string().min(1, 'Selecione a unidade.'),
    localAtividade: z.string().min(1, 'Selecione o local de atividade.'),
    regimeTrabalho: z.string().min(1, 'Selecione o regime de trabalho.'),
    tipoRequerimento: z.string().min(1, 'Selecione o tipo de requerimento.'),
    dataInicio: z.date({ required_error: 'Informe a data de inicio.' }),
    dataTermino: z.date().optional().nullable(),
    tipoRisco: z.enum(['INFLAMAVEL', 'ELETRICIDADE', 'RADIACAO'], {
      required_error: 'Selecione o tipo de risco.',
    }),
    selecaoRiscos: z.array(z.number()).default([]).refine((val) => val.length > 0, {
      message: 'Selecione ao menos um risco detalhado.',
    }),
  })
)

const initialFormValues: FormValues = {
  matricula: '',
  nome: '',
  cargo: '',
  orgao: '',
  localAtividade: '',
  regimeTrabalho: '',
  tipoRequerimento: '',
  dataInicio: undefined,
  dataTermino: null,
  tipoRisco: undefined,
  selecaoRiscos: [],
}

const { handleSubmit, values, setFieldValue, resetForm } = useForm<FormValues>({
  validationSchema: formSchema,
  initialValues: { ...initialFormValues },
})

function normalize(value: string | null | undefined): string {
  return (value ?? '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
}

onMounted(async () => {
  try {
    const [usersRes, locaisRes, tiposRes, regimesRes, uosRes, riscosRes] = await Promise.all([
      api.get('users/'),
      api.get('locais/'),
      api.get('tipos_req/'),
      api.get('regimes/'),
      api.get('uos/'),
      api.get('riscos/'),
    ])

    dimUser.value = Object.fromEntries(
      usersRes.data.map((user: ApiUser) => [user.matricula, user])
    )

    dimLocal.value = locaisRes.data.map((local: { codigo: string; descricao: string }) => ({
      value: local.codigo,
      label: local.descricao,
    }))

    dimTipo.value = tiposRes.data.map((tipo: { codigo: string; descricao: string }) => ({
      value: tipo.codigo,
      label: tipo.descricao,
    }))

    dimRegime.value = regimesRes.data.map((regime: { codigo: string; descricao: string }) => ({
      value: regime.codigo,
      label: regime.descricao,
    }))

    dimUO.value = uosRes.data.map((uo: { codigo: string; descricao: string }) => ({
      value: uo.codigo,
      label: uo.descricao,
    }))

    const grouped: GroupedRisks = {}
    const lookup: Record<number, string> = {}

    riscosRes.data.forEach(
      (risk: { id: number; codigo: string; subcategoria: string; descricao: string }) => {
        const key = normalize(risk.codigo)
        const bucket = grouped[key] ?? (grouped[key] = {})
        const list = bucket[risk.subcategoria] ?? (bucket[risk.subcategoria] = [])

        const option: RiskOption = { id: risk.id, descricao: risk.descricao }
        list.push(option)
        lookup[risk.id] = risk.descricao
      }
    )

    riscosBase.value = grouped
    riskDescriptions.value = lookup
  } catch (err) {
    console.error('Erro ao carregar dados da API:', err)
  }
})

watch(
  () => values.matricula,
  async (novaMatricula) => {
    if (!novaMatricula) {
      setFieldValue('nome', '')
      setFieldValue('cargo', '')
      return
    }

    let userData = dimUser.value[novaMatricula]

    if (!userData) {
      try {
        const response = await api.get(`users/${novaMatricula}/`)
        userData = response.data as ApiUser
        if (userData) {
          dimUser.value[novaMatricula] = userData
        }
      } catch (error) {
        userData = undefined
        console.warn(`Matricula ${novaMatricula} nao encontrada.`)
      }
    }

    setFieldValue('nome', userData?.nome ?? '')
    setFieldValue('cargo', userData?.funcao ?? '')
  }
)

const riscosDisponiveis = computed(() => {
  const tipo = normalize(values.tipoRisco)
  return riscosBase.value[tipo] ?? {}
})

function toggleSubcategoria(
  subcategoria: string,
  checked: boolean,
  handleChange: (value: number[]) => void
) {
  const tipo = normalize(values.tipoRisco)
  if (!tipo) return

  const items = riscosDisponiveis.value[subcategoria] ?? []
  const ids = items.map((item) => item.id)
  const current = new Set(riscosSelecionados.value[tipo] ?? [])

  if (checked) {
    ids.forEach((id) => current.add(id))
  } else {
    ids.forEach((id) => current.delete(id))
  }

  const updated = Array.from(current)
  riscosSelecionados.value[tipo] = updated
  handleChange(updated)
  setFieldValue('selecaoRiscos', updated)
}

function toggleDescricao(
  risk: RiskOption,
  checked: boolean,
  handleChange: (value: number[]) => void
) {
  const tipo = normalize(values.tipoRisco)
  if (!tipo) return

  const current = new Set(riscosSelecionados.value[tipo] ?? [])

  if (checked) current.add(risk.id)
  else current.delete(risk.id)

  const updated = Array.from(current)
  riscosSelecionados.value[tipo] = updated
  handleChange(updated)
  setFieldValue('selecaoRiscos', updated)
}

watch(
  () => values.tipoRisco,
  (novoTipo, antigoTipo) => {
    if (antigoTipo) {
      const previousKey = normalize(antigoTipo)
      riscosSelecionados.value[previousKey] = [...values.selecaoRiscos]
    }

    if (!novoTipo) {
      setFieldValue('selecaoRiscos', [])
      return
    }

    const key = normalize(novoTipo)
    const stored = riscosSelecionados.value[key] ?? []
    setFieldValue('selecaoRiscos', [...stored])
  }
)

function formatDate(value: Date | null | undefined): string | null {
  if (!value) return null
  const year = value.getFullYear()
  const month = `${value.getMonth() + 1}`.padStart(2, '0')
  const day = `${value.getDate()}`.padStart(2, '0')
  return `${year}-${month}-${day}`
}

const onSubmit = handleSubmit(async (formValues) => {
  try {
    const descriptions = formValues.selecaoRiscos
      .map((id) => riskDescriptions.value[id])
      .filter(Boolean)
      .join('; ')

    const payload = {
      status: 'Aberto',
      data_inicio: formatDate(formValues.dataInicio),
      data_fim: formatDate(formValues.dataTermino),
      atividades_executadas: descriptions,
      doc_uuid: crypto.randomUUID(),
      requerente_matricula: formValues.matricula,
      funcionario_matricula: formValues.matricula,
      uo_codigo: formValues.orgao,
      regime_trabalho_codigo: formValues.regimeTrabalho,
      local_atividade_codigo: formValues.localAtividade,
      tipo_requerimento_codigo: formValues.tipoRequerimento,
      riscos_ids: formValues.selecaoRiscos,
    }

    await api.post('requerimentos/', payload)
    alert('Requerimento enviado com sucesso!')

    resetForm({ values: { ...initialFormValues } })
    riscosSelecionados.value = createEmptyRiskSelection()
  } catch (err) {
    console.error('Erro ao enviar requerimento:', err)
    alert('Nao foi possivel enviar o requerimento.')
  }
})
</script>

<template>
  <div
    class="flex flex-col h-full overflow-hidden p-4 bg-[linear-gradient(rgba(255,255,255,0.7),rgba(255,255,255,0.7))] rounded-md"
  >
    <h1 class="text-2xl font-bold mb-4 flex-shrink-0 sticky top-0 bg-transparent z-10">
      Formulario de Solicitacao de Adicional de Periculosidade
    </h1>

    <div class="flex-grow overflow-y-auto pr-2">
      <form @submit.prevent="onSubmit" class="grid grid-cols-1 lg:grid-cols-3 gap-4">
        <div class="flex flex-col space-y-4 lg:col-span-1">
          <section class="space-y-4 p-4 rounded-lg shadow-sm bg-white border border-gray-200">
            <h2 class="text-lg font-semibold mb-2">Informacoes Pessoais</h2>

            <FormField name="matricula" v-slot="{ componentField }">
              <FormItem>
                <FormLabel>Matricula</FormLabel>
                <FormControl>
                  <Input type="text" maxlength="20" placeholder="Ex: 123456" v-bind="componentField" />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <FormField name="nome" v-slot="{ }">
              <FormItem>
                <FormLabel>Nome</FormLabel>
                <FormControl>
                  <Input type="text" :model-value="values.nome" disabled />
                </FormControl>
              </FormItem>
            </FormField>

            <FormField name="cargo" v-slot="{ }">
              <FormItem>
                <FormLabel>Cargo ou Funcao</FormLabel>
                <FormControl>
                  <Input type="text" :model-value="values.cargo" disabled />
                </FormControl>
              </FormItem>
            </FormField>

            <FormField name="orgao" v-slot="{ value, handleChange }">
              <FormItem>
                <FormLabel>Unidade Organizacional</FormLabel>
                <FormControl>
                  <DropdownMenu
                    :model-value="value"
                    @update:model-value="handleChange"
                    :items="dimUO"
                    placeholder="Selecione a unidade"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>
          </section>

          <section class="space-y-4 p-4 rounded-lg shadow-sm bg-white border border-gray-200">
            <h2 class="text-lg font-semibold mb-2">Informacoes da Atividade</h2>

            <FormField name="localAtividade" v-slot="{ value, handleChange }">
              <FormItem>
                <FormLabel>Local de Atividade</FormLabel>
                <FormControl>
                  <DropdownMenu
                    :model-value="value"
                    @update:model-value="handleChange"
                    :items="dimLocal"
                    placeholder="Selecione o local"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <FormField name="regimeTrabalho" v-slot="{ value, handleChange }">
              <FormItem>
                <FormLabel>Regime de Trabalho</FormLabel>
                <FormControl>
                  <DropdownMenu
                    :model-value="value"
                    @update:model-value="handleChange"
                    :items="dimRegime"
                    placeholder="Selecione o regime"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>

            <FormField name="tipoRequerimento" v-slot="{ value, handleChange }">
              <FormItem>
                <FormLabel>Tipo de Requerimento</FormLabel>
                <FormControl>
                  <DropdownMenu
                    :model-value="value"
                    @update:model-value="handleChange"
                    :items="dimTipo"
                    placeholder="Selecione o tipo"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            </FormField>
          </section>
        </div>

        <div class="flex flex-col space-y-4 lg:col-span-2">
          <section class="space-y-4 p-4 rounded-lg shadow-sm bg-white border border-gray-200 flex flex-col flex-grow">
            <h2 class="text-lg font-semibold mb-2">Detalhamento das Atividades</h2>

            <div class="space-y-4 overflow-y-auto pr-2 flex-grow">
              <FormField name="dataInicio" v-slot="{ value, handleChange }">
                <FormItem>
                  <FormLabel>Data de Inicio</FormLabel>
                  <FormControl>
                    <DatePicker
                      :model-value="value instanceof Date ? value : value ? new Date(value) : undefined"
                      @update:model-value="(v) => handleChange(v instanceof Date ? v : v ? new Date(v) : undefined)"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </FormField>

              <FormField name="dataTermino" v-slot="{ value, handleChange }">
                <FormItem>
                  <FormLabel>Data de Termino (opcional)</FormLabel>
                  <FormControl>
                    <DatePicker
                      :model-value="value instanceof Date ? value : value ? new Date(value) : undefined"
                      @update:model-value="(v) =>
                        handleChange(v instanceof Date ? v : v ? new Date(v) : null)"
                    />
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </FormField>

              <FormField name="tipoRisco" v-slot="{ componentField }">
                <FormItem class="space-y-3">
                  <FormLabel>Tipo de Risco</FormLabel>
                  <FormControl>
                    <RadioGroup v-bind="componentField">
                      <FormItem class="flex items-center space-x-3 space-y-0">
                        <FormControl><RadioGroupItem value="INFLAMAVEL" /></FormControl>
                        <FormLabel class="font-normal">Inflamaveis</FormLabel>
                      </FormItem>
                      <FormItem class="flex items-center space-x-3 space-y-0">
                        <FormControl><RadioGroupItem value="ELETRICIDADE" /></FormControl>
                        <FormLabel class="font-normal">Eletricidade</FormLabel>
                      </FormItem>
                      <FormItem class="flex items-center space-x-3 space-y-0">
                        <FormControl><RadioGroupItem value="RADIACAO" /></FormControl>
                        <FormLabel class="font-normal">Radiacao ionizante ou substancia radioativa</FormLabel>
                      </FormItem>
                    </RadioGroup>
                  </FormControl>
                  <FormMessage />
                </FormItem>
              </FormField>

              <FormField
                v-if="Object.keys(riscosDisponiveis).length > 0"
                name="selecaoRiscos"
                v-slot="{ value, handleChange }"
              >
                <FormItem>
                  <FormLabel>Selecao de riscos (detalhe)</FormLabel>
                  <FormDescription>
                    Escolha os riscos detalhados para o tipo selecionado:
                    <b>{{ values.tipoRisco }}</b>.
                  </FormDescription>

                  <div class="space-y-3 max-h-60 overflow-y-auto border p-3 rounded-md">
                    <div
                      v-for="(descricoes, subcat) in riscosDisponiveis"
                      :key="subcat"
                      class="space-y-2"
                    >
                      <div
                        class="flex items-center justify-between px-2 py-1 rounded-md transition-colors cursor-pointer"
                        :class="{
                          'bg-sky-200': descricoes.every((risk) => (value || []).includes(risk.id)),
                          'hover:bg-neutral-50': true,
                        }"
                        @click="
                          toggleSubcategoria(
                            subcat,
                            !descricoes.every((risk) => (value || []).includes(risk.id)),
                            handleChange
                          )
                        "
                      >
                        <div class="flex items-center gap-2">
                          <Check
                            v-if="descricoes.every((risk) => (value || []).includes(risk.id))"
                            class="h-4 w-4 text-primary"
                          />
                          <div
                            v-else-if="descricoes.some((risk) => (value || []).includes(risk.id))"
                            class="h-4 w-4 text-primary opacity-60"
                          >
                            <Check />
                          </div>
                          <div v-else class="h-4 w-4 opacity-0"><Check /></div>
                          <span class="font-medium">{{ subcat }}</span>
                        </div>
                      </div>

                      <div class="pl-6 space-y-1">
                        <div
                          v-for="risk in descricoes"
                          :key="risk.id"
                          class="flex items-center px-2 py-1 rounded-md transition-colors cursor-pointer hover:bg-neutral-50"
                          :class="{ 'bg-sky-200': (value || []).includes(risk.id) }"
                          @click="
                            toggleDescricao(
                              risk,
                              !(value || []).includes(risk.id),
                              handleChange
                            )
                          "
                        >
                          <div class="flex items-center w-full">
                            <div class="w-6 flex justify-start items-center mr-2">
                              <Check
                                v-if="(value || []).includes(risk.id)"
                                class="h-4 w-4 text-primary"
                              />
                              <div v-else class="h-4 w-4 opacity-0"></div>
                            </div>
                            <span class="text-sm text-left flex-1">{{ risk.descricao }}</span>
                          </div>
                        </div>
                      </div>

                      <hr class="my-2 border-gray-200" />
                    </div>
                  </div>

                  <FormMessage />
                </FormItem>
              </FormField>
            </div>

            <div class="flex-shrink-0 pt-4">
              <Button
                type="submit"
                class="w-50 bg-[#2082c4] text-white hover:cursor-pointer hover:scale-105"
              >
                Enviar Requerimento
              </Button>
            </div>
          </section>
        </div>
      </form>
    </div>
  </div>
</template>
