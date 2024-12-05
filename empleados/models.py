from django.db import models

from django.db import models

class Empleado(models.Model):
    id_empleado = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    email = models.EmailField()

    class Meta:
        db_table = 'empleados'

