from rest_framework import serializers
from .models import Usuario, Predicao

class UsuarioSerializer(serializers.ModelSerializer):
  class Meta:
    model = Usuario
    fields = ['id', 'nome_completo', 'email', 'telefone', 'senha']

class PredicaoSerializer(serializers.ModelSerializer):
  usuario = UsuarioSerializer(read_only=True)

  class Meta:
    model = Predicao
    fields = ['id', 'usuario', 'data', 'y1', 'y2']