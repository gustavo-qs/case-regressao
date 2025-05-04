import os
import joblib
import pandas as pd

from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from api.models import Usuario, Predicao
from api.serializers import UsuarioSerializer, PredicaoSerializer
from api.auth_utils import session_required
from django.contrib.auth.hashers import check_password

@csrf_exempt
def login_view(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Método não suportado'}, status=405)

    data = JSONParser().parse(request)
    email = data.get('email')
    senha = data.get('senha')

    try:
        user = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Credenciais inválidas'}, status=401)

    # Verifica o hash com a senha enviada :contentReference[oaicite:4]{index=4}
    if not check_password(senha, user.senha):
        return JsonResponse({'error': 'Credenciais inválidas'}, status=401)

    # Autentica: salva o ID na sessão
    request.session['user_id'] = user.id
    request.session.set_expiry(60 * 60 * 24)  # expira em 1 dia (opcional)

    return JsonResponse({'message': 'Login bem-sucedido'}, status=200)


@csrf_exempt
def logout_view(request):
    if request.method != 'POST':
        return JsonResponse({'detail': 'Método não suportado'}, status=405)

    # Remove dados da sessão
    request.session.flush()
    return JsonResponse({'message': 'Logout bem-sucedido'}, status=200)

@csrf_exempt
@session_required
def users(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UsuarioSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return JsonResponse(UsuarioSerializer(user).data, status=201)
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
@session_required
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
@session_required
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

@csrf_exempt
@session_required
def predictions_delete(request, id):
    if request.method == 'DELETE':
        try:
            predicao = Predicao.objects.get(id=id)
            predicao.delete()
            return JsonResponse({'message': 'Predição deletada com sucesso!'}, status=204)
        except Predicao.DoesNotExist:
            return JsonResponse({'error': 'Predição não encontrada.'}, status=404)
    return JsonResponse({'detail': 'Método não suportado'}, status=405)