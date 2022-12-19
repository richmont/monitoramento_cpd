from django.db import models

MODELOS_WORKSTATION = (
    ("Lenovo", "Lenovo"),
    ("HP", "HP")
)
lista_modelos_workstation = [choice[1] for choice in MODELOS_WORKSTATION]


class Workstation(models.Model):
    id = models.AutoField(primary_key=True)
    hostname = models.CharField(max_length=255, unique=True, blank=False)
    IP = models.CharField(unique=True, max_length=255, blank=False)
    local = models.CharField(max_length=255, blank=False)
    dominio = models.CharField(max_length=255, blank=False)
    modelo = models.CharField(
            max_length=255,
            choices=MODELOS_WORKSTATION,
            default='Lenovo',
            blank=False
            )
