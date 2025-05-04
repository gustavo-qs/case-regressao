from django.http import JsonResponse
from functools import wraps

def session_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return JsonResponse({'error': 'Usuário não autenticado'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped
