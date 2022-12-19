from django.forms import ValidationError
from django.shortcuts import render
from monitoramento_cpd_app.forms.form_cadastrar_impressora import ImpressoraForm
from monitoramento_cpd_app.models.impressoras import Impressora
from django.contrib import messages

def cadastrar_impressora(request):
    imp = None
    if request.method == "POST":
        nome = request.POST["nome"]
        ip = request.POST["IP"]
        local = str(request.POST["local"])
        modelo = str(request.POST["modelo"])
        
        imp = Impressora(nome = nome, local=local, IP=ip, modelo=modelo)
        try:
            imp.full_clean()
            imp.save()
            messages.add_message(request, messages.INFO, f"Impressora {nome}, inserida com sucesso")
        except ValidationError as ex:
            for x in ex:
                messages.add_message(request, messages.ERROR, f"Campo: {x[0]} Erro: {x[1][0]}")
    form = ImpressoraForm()
    return render(request, "form_cadastro_impressora.html", {"form": form})