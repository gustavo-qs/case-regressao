import os
import joblib
import numpy as np
import pandas as pd

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse

from api.models import Usuario, Predicao
from api.serializers import UsuarioSerializer, PredicaoSerializer

@csrf_exempt
def users(request):
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

@csrf_exempt
def predict(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        model = joblib.load(os.path.join(os.path.dirname(__file__), 'extra_trees_multioutput.joblib'))  

        df = pd.DataFrame(
            [ {
                'X1_compactness':   data['X1_compactness'],
                'X3_wall_area':     data['X3_wall_area'],
                'X5_height':        data['X5_height'],
                'X6_orientation':   data['X6_orientation'],
                'X7_glazing_area':  data['X7_glazing_area'],
                'X8_glazing_dist':  data['X8_glazing_dist'],
            } ]
        )

        preds = model.predict(df)

        return JsonResponse({'predictions': preds.tolist()}, status=200)

    return JsonResponse({'detail': 'Método não suportado'}, status=405)

@csrf_exempt
def predictions(request):
    if request.method == 'GET':
        predicoes = Predicao.objects.all()
        serializer = PredicaoSerializer(predicoes, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = PredicaoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        predicao = Predicao.objects.get(id=data['id'])
        serializer = PredicaoSerializer(predicao, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        data = JSONParser().parse(request)
        predicao = Predicao.objects.get(id=data['id'])
        predicao.delete()
        return JsonResponse({'message': 'Predição deletada com sucesso!'}, status=204)