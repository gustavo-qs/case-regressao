from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from api.models import Usuario, Predicao
from api.serializers import UsuarioSerializer, PredicaoSerializer

@csrf_exempt
def usuario_list(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UsuarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        usuario = Usuario.objects.get(id=data['id'])
        serializer = UsuarioSerializer(usuario, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        usuario = Usuario.objects.get(id=data['id'])
        usuario.delete()
        return JsonResponse({'message': 'Usuario deletado com sucesso!'}, status=204)