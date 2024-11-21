# context_processors.py
from authp.models import Setting

def user_settings(request):
    if request.user.is_authenticated:
        try:
            setting = Setting.objects.get(usuario=request.user)
            return {'user_setting': setting}
        except Setting.DoesNotExist:
            return {'user_setting': None}
    return {}
