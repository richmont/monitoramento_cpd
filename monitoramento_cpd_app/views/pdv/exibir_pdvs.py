from django.shortcuts import render
from django.forms import ValidationError
from django.contrib import messages
from monitoramento_cpd_app.models.pdvs import PDV, lista_tipos_pdv
from monitoramento_cpd_app.forms.form_cadastrar_pdv import FormPDV
from monitoramento_cpd.ping_threads.Ping_threads import Ping_threads
from monitoramento_cpd.nested_ssh.src.Nested_SSH import Nested_SSH
from monitoramento_cpd.nested_ssh.src.t_Nested_SSH import t_Nested_SSH


def pdvs(request):
    # formulário de cadastro do pdv
    form_pdv = FormPDV()
    form_pdv

    # Lista de IPs dos PDVs a partir do banco
    lista_ips_pdvs = PDV.objects.values_list('IP', flat=True)

    lista_pdvs = list()
    """
    Necessário criar um ping nested
    """

    return render(request,
                  'exibir_pdvs.html',
                  {
                    "form_pdv": form_pdv,
                    "lista_pdvs": lista_pdvs,
                    "lista_tipos_pdv": lista_tipos_pdv
                   }
                  )
