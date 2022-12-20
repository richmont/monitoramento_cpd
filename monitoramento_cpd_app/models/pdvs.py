from django.db import models

TIPOS_PDV = (
    ("Frente de caixa", "Frente de caixa"),
    ("Cafeteria", "Cafeteria")
)
TIPO_CONEXAO_PINPAD = (
    ("USB", "USB"),
    ("SERIAL", "SERIAL")
)
lista_tipos_pdv = [choice[1] for choice in TIPOS_PDV]
lista_tipos_conexao_pinpad = [choice[1] for choice in TIPO_CONEXAO_PINPAD]


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
    # Número de série pode ser atualizado automaticamente com comando ssh
    num_serial_pinpad = models.CharField(unique=True, max_length=255, blank=True)
    # tipo de conexão obrigatória
    conexao_pinpad = models.CharField(
            max_length=255,
            choices=TIPO_CONEXAO_PINPAD,
            default='SERIAL',
            blank=False
            )