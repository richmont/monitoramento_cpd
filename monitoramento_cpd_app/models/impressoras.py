from wsgiref.validate import validator
from django.db import models
from django.core.exceptions import ValidationError
import ipaddress
"""
https://www.geeksforgeeks.org/how-to-use-django-field-choices/
"""
MODELOS_IMPRESSORA = (
    ("Lexmark MS811", "Lexmark MS811"),
    ("Lexmark MX611dhe", "Lexmark MX611dhe"),
    ("M4206-MarkII", "M4206-MarkII")
)

lista_modelos_impressora = [choice[1] for choice in MODELOS_IMPRESSORA]


def validar_ip(value):
    try:
        ip = ipaddress.ip_address(value)
    except ValueError:
        raise ValidationError(
            ('IP Inválido'),
            params={'value': value},
        )


class Impressora(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=30, blank=False)
    local = models.CharField(max_length=30, blank=False)
    IP = models.CharField(unique=True,
                          max_length=255,
                          validators=[validar_ip],
                          blank=False)
    modelo = models.CharField(
        max_length=20,
        choices=MODELOS_IMPRESSORA,
        default='Lexmark MS811',
        blank=False
        )
