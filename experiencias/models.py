from django.db import models

from django.db import models

class Experiencia(models.Model):
    idexp = models.IntegerField(primary_key=True)
    nombreexp = models.CharField(max_length=255)
    url = models.CharField(max_length=255)    
    titulo = models.CharField(max_length=255)    
    precioeur = models.CharField(max_length=255)
    fecha = models.CharField(max_length=255)
    sku = models.CharField(max_length=255)

    class Meta:
        db_table = 'experiencia'