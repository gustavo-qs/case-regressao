from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Usuario, Predicao

class UsuarioSerializer(serializers.ModelSerializer):
    senha = serializers.CharField(write_only=True)

    class Meta:
        model = Usuario
        fields = ['id', 'nome_completo', 'email', 'telefone', 'senha']

    def create(self, validated_data):
        validated_data['senha'] = make_password(validated_data['senha'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        senha = validated_data.pop('senha', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if senha:
            instance.senha = make_password(senha)
        instance.save()
        return instance

class PredicaoSerializer(serializers.ModelSerializer):
  usuario = serializers.PrimaryKeyRelatedField(queryset=Usuario.objects.all())

  class Meta:
    model = Predicao
    fields = ['id', 'usuario', 'x1', 'x3', 'x5', 'x6', 'x7', 'x8', 'y1', 'y2', 'data']
    read_only_fields = ['data'] 