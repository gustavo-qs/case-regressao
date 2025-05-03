from django.db import models

# Create your models here.
class Usuario(models.Model):
  id = models.AutoField(primary_key=True)
  nome_completo = models.CharField(max_length=255)
  email = models.EmailField(unique=True)
  telefone = models.CharField(max_length=15)
  senha = models.CharField(max_length=128)

  def __str__(self):
    return self.nome_completo
  
class Predicao(models.Model):
  id = models.AutoField(primary_key=True)
  usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
  data = models.DateTimeField(auto_now_add=True)
  y1 = models.FloatField()
  y2 = models.FloatField()

  def __str__(self):
    return f"Predição {self.id} - {self.usuario.nome_completo}"