from django.db import migrations
from django.contrib.auth.hashers import make_password

def create_default_user(apps, schema_editor):
    Usuario = apps.get_model('api', 'Usuario')
    # evita recriar caso já exista
    if not Usuario.objects.filter(email='senai@senai.com').exists():
        Usuario.objects.create(
            nome_completo='Senai',
            email='senai@senai.com',
            telefone='4332945100',
            senha=make_password('Senai@2025') 
        )

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_predicao_x1_predicao_x3_predicao_x5_predicao_x6_and_more'),
    ]

    operations = [
        migrations.RunPython(create_default_user),
    ]
