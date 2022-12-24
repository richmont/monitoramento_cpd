from django.shortcuts import render
from django.forms import ValidationError
from monitoramento_cpd_app.models.workstations import Workstation, lista_modelos_workstation
from monitoramento_cpd_app.forms.form_cadastrar_workstation import WorkstationForm
from django.contrib import messages
from  ping_threads.Ping_threads import Ping_threads


def workstations(request):
    def cadastrar_workstation():
        """Recebe a requisição e cadastra impressora

        Returns:
            form: Formulário do Django para cadastro
        """
        ws = None
        if request.method == "POST":
            if request.POST["operacao"] == 'criar':
                hostname = request.POST["hostname"]
                ip = request.POST["IP"]
                local = str(request.POST["local"])
                modelo = str(request.POST["modelo"])
                dominio = str(request.POST["dominio"])

                ws = Workstation(hostname=hostname,
                                 modelo=modelo,
                                 local=local,
                                 IP=ip,
                                 dominio=dominio)
                try:
                    ws.full_clean()
                    ws.save()
                    messages.add_message(request, messages.INFO, f"Workstation {hostname}, inserida com sucesso")
                except ValidationError as ex:
                    for x in ex:
                        messages.add_message(request, messages.ERROR, f"Campo: {x[0]} Erro: {x[1][0]}")

            if request.POST["operacao"] == 'excluir':
                id_workstation_excluir = request.POST["id_workstation"]
                try:
                    Workstation.objects.filter(
                        id=id_workstation_excluir
                        ).delete()

                    messages.add_message(request, messages.WARNING,
                                         f"Workstation deletada com sucesso")
                except ValidationError as ex:
                    for x in ex:
                        messages.add_message(request, messages.ERROR, f"Campo: {x[0]} Erro: {x[1][0]}")
            if request.POST["operacao"] == 'editar':
                id_workstation_editar = request.POST["id_workstation"]
                hostname = request.POST["hostname"]
                ip = request.POST["IP"]
                local = str(request.POST["local"])
                modelo = str(request.POST["modelo"])
                dominio = str(request.POST["dominio"])
                instancia_ws_editar = Workstation.objects.filter(
                    id=id_workstation_editar)
                try:
                    instancia_ws_editar.update(hostname=hostname,
                                               modelo=modelo,
                                               local=local,
                                               IP=ip,
                                               dominio=dominio)
                    messages.add_message(request, messages.INFO,
                                         f"Workstation {hostname}, editada com sucesso")
                except ValidationError as ex:
                    for x in ex:
                        messages.add_message(request, messages.ERROR, 
                                             f"Campo: {x[0]} Erro: {x[1][0]}")
        form = WorkstationForm()
        return form

    def ips_workstations():
        return Workstation.objects.values_list('IP', flat=True)
    lista_ips_workstations = ips_workstations()
    form_ws = cadastrar_workstation()
    lista_workstations = list()
    ping_thread = Ping_threads(lista_ips_workstations)
    for resposta in ping_thread.respostas:
        # ping_thread mostra True ou False para resposta do ping
        if resposta["responde"]:
            ping = "online"
        else:
            ping = "offline"

        #  Pede ao banco a workstation que possui este IP
        workstation = Workstation.objects.filter(IP=resposta["ip"]).values()[0]
        dict_ws = {
            "id": workstation["id"],
            "hostname": workstation["hostname"],
            "IP": workstation["IP"],
            "dominio": workstation["dominio"],
            "modelo": workstation["modelo"],
            "local": workstation["local"],
            "online": ping
        }
        lista_workstations.append(dict_ws)

    return render(request,
                  "exibir_workstations.html",
                  {"workstations": lista_workstations,
                   "form_ws": form_ws,
                   "lista_modelos_workstation": lista_modelos_workstation})
