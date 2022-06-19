from django.db import models

nacional_extranjero= [
    (1, 'Nacional'),
    (2, 'Extranjero')
]
tipo_Documento=[
    (1, 'DUI'),
    (2, 'Pasaporte')
]

class persona(models.Model):
    extrajero = models.ForeignKey('Extranjero', on_delete=models.CASCADE, null=True)
    ciudadano = models.ForeignKey('Ciudadano', on_delete=models.CASCADE, null=True)
    pasaporte = models.CharField(max_length=9, unique=True, default="", null=True)
    dui = models.CharField(max_length=10, unique=True, default="", null=True)
    nombre = models.CharField(max_length= 50, default="")
    apellido = models.CharField(max_length=50, default="")
    tipoDocumento = models.IntegerField(
        blank=True,
        choices=tipo_Documento
    ) 
    nacionalidad = models.IntegerField(
        blank=True,
        choices=nacional_extranjero
    ) 
    fechaSalida = models.DateField()
    fechaIngreso = models.DateField()
    TiempoPermanencia = models.CharField(max_length=10, default="")



class Extranjero(models.Model):
    idExtranjero = models.AutoField(primary_key=True)

class Ciudadano(models.Model):
    idCiudadano = models.AutoField(primary_key=True)