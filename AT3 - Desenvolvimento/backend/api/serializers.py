from rest_framework import serializers
from .models import Usuario, Predicao

class UsuarioSerializer(serializers.ModelSerializer):
  class Meta:
    model = Usuario
    fields = ['id', 'nome_completo', 'email', 'telefone', 'senha']

class PredicaoSerializer(serializers.ModelSerializer):
  usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

  class Meta:
    model = Predicao
    fields = ['id', 'usuario', 'x1', 'x3', 'x5', 'x6', 'x7', 'x8', 'y1', 'y2']