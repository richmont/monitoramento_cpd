from django.shortcuts import render
from django.forms import ValidationError
from monitoramento_cpd_app.models.impressoras import Impressora, lista_modelos_impressora
from monitoramento_cpd_app.forms.form_cadastrar_impressora import ImpressoraForm
from django.contrib import messages
from  impressora_scraper.ScraperLexmarkMS811 import ScraperLexmarkMS811
from  impressora_scraper.Scraper import Scraper
from  ping_threads.Ping_threads import Ping_threads
import logging
logging.basicConfig()
logger = logging.getLogger("View Exibir impressoras")
logger.setLevel(logging.DEBUG)


def impressoras(request):
    def cadastrar_imp():
        """Recebe a requisição e cadastra impressora

        Returns:
            form: Formulário do Django para cadastro
        """
        imp = None
        if request.method == "POST":
            if request.POST["operacao"] == 'criar':
                nome = request.POST["nome"]
                ip = request.POST["IP"]
                local = str(request.POST["local"])
                modelo = str(request.POST["modelo"])

                imp = Impressora(nome=nome, local=local, IP=ip, modelo=modelo)
                try:
                    imp.full_clean()
                    imp.save()
                    messages.add_message(request, messages.INFO, f"Impressora {nome}, inserida com sucesso")
                except ValidationError as ex:
                    for x in ex:
                        messages.add_message(request, messages.ERROR, f"Campo: {x[0]} Erro: {x[1][0]}")

            if request.POST["operacao"] == 'excluir':
                id_impressora_excluir = request.POST["id_impressora"]
                try:
                    Impressora.objects.filter(
                        id=id_impressora_excluir
                        ).delete()

                    messages.add_message(request, messages.WARNING,
                                         f"Impressora deletada com sucesso")
                except ValidationError as ex:
                    for x in ex:
                        messages.add_message(request, messages.ERROR, f"Campo: {x[0]} Erro: {x[1][0]}")
            
            if request.POST["operacao"] == 'editar':
                id_impressora_editar = request.POST["id_impressora"]
                nome = request.POST["nome"]
                ip = request.POST["IP"]
                local = str(request.POST["local"])
                modelo = str(request.POST["modelo"])
                instancia_imp_editar = Impressora.objects.filter(
                    id=id_impressora_editar)
                try:
                    instancia_imp_editar.update(nome=nome,
                                                modelo=modelo,
                                                local=local,
                                                IP=ip
                                                )
                    messages.add_message(request, messages.INFO,
                                         f"Impressora {nome}, editada com sucesso")
                except ValidationError as ex:
                    for x in ex:
                        messages.add_message(request, messages.ERROR,
                                             f"Campo: {x[0]} Erro: {x[1][0]}")
        form_imp = ImpressoraForm()
        return form_imp

    def ips_impressoras():
        return Impressora.objects.values_list('IP', flat=True)

    lista_ips_impressoras = ips_impressoras()
    logger.debug("Lista de ips de impressora, tamanho: ", len(lista_ips_impressoras))
    form_imp = cadastrar_imp()
    lista_impressoras = list()
    ping_thread = Ping_threads(lista_ips_impressoras)
    for resposta in ping_thread.respostas:
        #  Pede ao banco a impressora que possui este IP
        impressora = Impressora.objects.filter(IP=resposta["ip"]).values()[0]
        # ping_thread mostra True ou False para resposta do ping
        if resposta["responde"]:
            logger.debug(f"Impressora de IP {resposta['ip']} está online")
            if impressora["modelo"] == "Lexmark MS811":
                try:
                    scraper_lexmarkms811 = ScraperLexmarkMS811(f"http://{impressora['IP']}")
                    dict_ms811 = {
                        "online": True,
                        "id": impressora['id'],
                        "IP": impressora['IP'],
                        "nome": impressora['nome'],
                        "local": impressora['local'],
                        "modelo": scraper_lexmarkms811.modelo,
                        "status": scraper_lexmarkms811.status_impressora,
                        "bandeja1": scraper_lexmarkms811.bandeja1,
                        "bandeja2": scraper_lexmarkms811.bandeja2,
                        "bandeja_padrao": scraper_lexmarkms811.bandeja_padrao,
                        "toner": scraper_lexmarkms811.toner,
                        "kit_rolo": scraper_lexmarkms811.kit_rolo,
                        "kit_manutencao": scraper_lexmarkms811.kit_manutencao,
                        "unidade_imagem": scraper_lexmarkms811.unidade_imagem
                    }
                    lista_impressoras.append(dict_ms811)
                except Scraper.ScraperErrors.ElementoAusente:
                    logger.debug(f"Impressora de IP {resposta['ip']} possui elemento ausente")
                    dict_ms811 = {
                        "online": False,
                        "id": impressora['id'],
                        "IP": impressora['IP'],
                        "nome": impressora['nome'],
                        "local": impressora['local'],
                        "modelo": impressora['modelo'],
                        "motivo": "Elemento de suprimento ausente na página"
                    }
                    lista_impressoras.append(dict_ms811)
                except Scraper.ScraperErrors.FalhaRequisicao:
                    logger.debug(f"Impressora de IP {resposta['ip']} falhou a requisição")
                    dict_ms811 = {
                        "online": False,
                        "id": impressora['id'],
                        "IP": impressora['IP'],
                        "nome": impressora['nome'],
                        "local": impressora['local'],
                        "modelo": impressora['modelo'],
                        "motivo": "Falha ao obter dados, o IP é de uma impressora?"
                    }
                    lista_impressoras.append(dict_ms811)
        else:
            logger.debug(f"Impressora de IP {resposta['ip']} está offline")
            ping = "offline"
            dict_ms811 = {
                "online": False,
                "id": impressora['id'],
                "IP": impressora['IP'],
                "nome": impressora['nome'],
                "local": impressora['local'],
                "modelo": impressora['modelo'],
                "motivo": "Impressora desconectada da rede"
            }
            lista_impressoras.append(dict_ms811)
    return render(request, "exibir_impressoras.html", {"impressoras": lista_impressoras, "form_imp": form_imp, "lista_modelos_impressora": lista_modelos_impressora})