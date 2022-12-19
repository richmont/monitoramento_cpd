from django.db import models

TIPOS_PDV = (
    ("Frente de caixa", "Frente de caixa"),
    ("Cafeteria", "Cafeteria")
)
lista_tipos_pdv = [choice[1] for choice in TIPOS_PDV]


class PDV(models.Model):
    id = models.AutoField(primary_key=True)
    # exemplo: 12A, 5B
    checkout = models.CharField(unique=True, max_length=255, blank=False)
    IP = models.CharField(unique=True, max_length=255, blank=False)
    tipo_pdv = models.CharField(
            max_length=255,
            choices=TIPOS_PDV,
            default='Frente de caixa',
            blank=False
            )
