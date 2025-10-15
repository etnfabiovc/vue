from rest_framework import serializers
from .models import (
    DimUser, DimUO, DimCargo, DimLocalAtividade, DimRegimeTrabalho, 
    DimTipoRequerimento, DimRisk, FactRequerimento
)

# === 1. SERIALIZERS DE DIMENSÃO (LEITURA) === #

class DimUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimUser
        fields = ['matricula', 'nome', 'email', 'funcao']

class DimUOSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimUO
        fields = '__all__'

class DimCargoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo DimCargo."""
    class Meta:
        model = DimCargo
        fields = '__all__'

class DimLocalAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimLocalAtividade
        fields = '__all__'

class DimTipoRequerimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimTipoRequerimento
        fields = '__all__'

class DimRegimeTrabalhoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimRegimeTrabalho
        fields = '__all__'

class DimRiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = DimRisk
        fields = '__all__'


# === 2. SERIALIZER DO FATO (FactRequerimento) === #

class FactRequerimentoSerializer(serializers.ModelSerializer):
    # --- LEITURA (Nested Serializers) ---
    requerente = DimUserSerializer(read_only=True)
    funcionario = DimUserSerializer(read_only=True)
    uo = DimUOSerializer(read_only=True)
    regime_trabalho = DimRegimeTrabalhoSerializer(read_only=True)
    local_atividade = DimLocalAtividadeSerializer(read_only=True)
    tipo_requerimento = DimTipoRequerimentoSerializer(read_only=True)
    riscos = DimRiskSerializer(many=True, read_only=True)

    # --- ESCRITA (PrimaryKeyRelatedField para receber IDs) ---
    requerente_matricula = serializers.PrimaryKeyRelatedField(
        queryset=DimUser.objects.all(), source='requerente', write_only=True
    )
    funcionario_matricula = serializers.PrimaryKeyRelatedField(
        queryset=DimUser.objects.all(), source='funcionario', write_only=True
    )
    uo_codigo = serializers.PrimaryKeyRelatedField(
        queryset=DimUO.objects.all(), source='uo', write_only=True
    )
    regime_trabalho_codigo = serializers.PrimaryKeyRelatedField(
        queryset=DimRegimeTrabalho.objects.all(), source='regime_trabalho', write_only=True
    )
    local_atividade_codigo = serializers.PrimaryKeyRelatedField(
        queryset=DimLocalAtividade.objects.all(), source='local_atividade', write_only=True
    )
    tipo_requerimento_codigo = serializers.PrimaryKeyRelatedField(
        queryset=DimTipoRequerimento.objects.all(), source='tipo_requerimento', write_only=True
    )
    riscos_ids = serializers.PrimaryKeyRelatedField(
        queryset=DimRisk.objects.all(), many=True, source='riscos', write_only=True
    )

    class Meta:
        model = FactRequerimento
        fields = [
            'req_num', 'status', 'data_inicio', 'data_fim', 'atividades_executadas',
            'data_criacao', 'data_processamento', 'data_aprovacao', 'doc_uuid',
            
            # Leitura
            'requerente', 'funcionario', 'uo', 'regime_trabalho', 'local_atividade', 
            'tipo_requerimento', 'riscos',
            
            # Escrita
            'requerente_matricula', 'funcionario_matricula', 'uo_codigo', 
            'regime_trabalho_codigo', 'local_atividade_codigo', 
            'tipo_requerimento_codigo', 'riscos_ids'
        ]
        read_only_fields = ['req_num', 'data_criacao']
        
    # Método customizado para lidar com a relação ManyToMany na criação/atualização
    def create(self, validated_data):
        risks_data = validated_data.pop('riscos', [])
        instance = super().create(validated_data)
        instance.riscos.set(risks_data)
        return instance

    def update(self, instance, validated_data):
        risks_data = validated_data.pop('riscos', None)
        instance = super().update(instance, validated_data)
        if risks_data is not None:
            instance.riscos.set(risks_data)
        return instance