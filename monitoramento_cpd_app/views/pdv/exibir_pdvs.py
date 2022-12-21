from django.shortcuts import render
from django.forms import ValidationError
from django.contrib import messages
from monitoramento_cpd_app.models.pdvs import PDV, lista_tipos_pdv
from monitoramento_cpd_app.forms.form_cadastrar_pdv import FormPDV
from monitoramento_cpd_app.forms.form_login_ssh_gateway import FormLoginGateway
from monitoramento_cpd.ping_threads.Ping_threads import Ping_threads
from monitoramento_cpd.nested_ssh.src.Nested_SSH import Nested_SSH
from monitoramento_cpd.nested_ssh.src.t_Nested_SSH import t_Nested_SSH
import paramiko
import bcrypt
import socket
import logging
logger = logging.getLogger("View exibir PDVs")
logging.basicConfig(level=logging.INFO)

def pdvs(request):
    def cadastrar_pdv():
        checkout = request.POST["checkout"]
        ip = request.POST["IP"]
        tipo_pdv = str(request.POST["tipo_pdv"])
        login_pdv = str(request.POST["login_pdv"])
        pwd_pdv = str(request.POST["pwd_pdv"])
        porta_ssh_pdv = str(request.POST["porta_ssh_pdv"])
        num_serial_pinpad = str(request.POST["num_serial_pinpad"])
        conexao_pinpad = str(request.POST["conexao_pinpad"])

        pdv = PDV(checkout=checkout,
            tipo_pdv=tipo_pdv,
            IP=ip,
            login_pdv=login_pdv,
            pwd_pdv=pwd_pdv,
            porta_ssh_pdv=porta_ssh_pdv,
            num_serial_pinpad=num_serial_pinpad,
            conexao_pinpad=conexao_pinpad
        )
        try:
            pdv.full_clean()
            pdv.save()
            messages.add_message(request, messages.INFO, f"PDV {checkout}, inserido com sucesso")
        except ValidationError as ex:
            for x in ex:
                messages.add_message(request, messages.ERROR, f"Campo: {x[0]} Erro: {x[1][0]}")

    def excluir_pdv():
        id_PDV_excluir = request.POST["id_PDV"]
        try:
            PDV.objects.filter(
                id=id_PDV_excluir
                ).delete()

            messages.add_message(request, messages.WARNING,
                                    f"PDV deletado com sucesso")
        except ValidationError as ex:
            for x in ex:
                messages.add_message(request, messages.ERROR, f"Campo: {x[0]} Erro: {x[1][0]}")

    def editar_pdv():

        id_PDV_editar = request.POST["id_PDV"]
        checkout = request.POST["checkout"]
        ip = request.POST["IP"]
        tipo_pdv = str(request.POST["tipo_pdv"])
        login_pdv = str(request.POST["login_pdv"])
        pwd_pdv = str(request.POST["pwd_pdv"])
        porta_ssh_pdv = str(request.POST["porta_ssh_pdv"])
        num_serial_pinpad = str(request.POST["num_serial_pinpad"])
        conexao_pinpad = str(request.POST["conexao_pinpad"])
        instancia_pdv_editar = PDV.objects.filter(
            id=id_PDV_editar)
        try:
            instancia_pdv_editar.update(
                checkout=checkout,
                tipo_pdv=tipo_pdv,
                IP=ip,
                login_pdv=login_pdv,
                pwd_pdv=pwd_pdv,
                porta_ssh_pdv=porta_ssh_pdv,
                num_serial_pinpad=num_serial_pinpad,
                conexao_pinpad=conexao_pinpad)
            messages.add_message(request, messages.INFO,
                                    f"PDV {checkout}, editado com sucesso")
        except ValidationError as ex:
            for x in ex:
                messages.add_message(request, messages.ERROR, 
                                        f"Campo: {x[0]} Erro: {x[1][0]}")
  
    def tentar_login_ssh(servidor: str, usuario_ssh_gateway: str, porta_ssh_gateway: int, senha_ssh_gateway: str) -> bool:
        """Tenta validar login e senha através de conexão SSH

        Args:
            servidor (str): Endereço do servidor de destino
            usuario_ssh_gateway (str): Usuário do servidor
            senha_ssh_gateway (str): Senha do servidor

        Returns:
            bool:
                True para login bem sucedido  
                False para login malsucedido
        """ 
        with paramiko.SSHClient() as cliente_ssh:
            try:
                cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                cliente_ssh.connect(hostname=servidor, port=porta_ssh_gateway, username=usuario_ssh_gateway, password=senha_ssh_gateway)
                stdin, stdout, stderr = cliente_ssh.exec_command("hostname")
                return True
            except paramiko.AuthenticationException:
                logger.error("tentar_login_ssh: Autenticação falhou com servidor gateway ", servidor)
                return False
            except socket.gaierror:
                logger.error("tentar_login_ssh: Conexão falhou com servidor gateway ", servidor)
                return False
            except socket.timeout:
                logger.error("tentar_login_ssh: Conexão atingiu tempo limite com servidor gateway ", servidor)
                return False

    def login_gateway():
        """Tenta fazer login no servidor SSH Gateway, 
        onde os comandos de PDV serão executados
       
        """
        
        hostname_gateway = str(request.POST["hostname_gateway"])
        usuario_ssh_gateway = str(request.POST["login_gateway"])
        porta_ssh_gateway = str(request.POST["porta_gateway"])
        senha_ssh_gateway = str(request.POST["senha_gateway"])
        
        if tentar_login_ssh(hostname_gateway, usuario_ssh_gateway, porta_ssh_gateway, senha_ssh_gateway):
            # grava na sessão os dados de hostname_gateway gateway informados pelo usuário
            logger.info("login_gateway: bem sucedido, gravando dados do hostname_gateway na sessão")
            
            request.session["hostname_gateway"] = str(hostname_gateway)
            request.session["usuario_ssh_gateway"] = str(usuario_ssh_gateway)
            request.session["porta_ssh_gateway"] = str(porta_ssh_gateway)
            request.session["senha_ssh_gateway"] = str(senha_ssh_gateway)
        else:
            logger.info("login_gateway: Falhou, servidor, login ou senha não reconhecidos")
            messages.add_message(request, messages.ERROR, f"Login falhou, verifique servidor, usuário ou senha")
    
    
    # formulário de cadastro do pdv
    form_pdv = FormPDV()
    form_login_gateway = FormLoginGateway()

    # Lista de IPs dos PDVs a partir do banco
    def exibir_pdvs():
        lista_pdvs_completa = PDV.objects.all()
        lista_destinos = list()
        for pdv in lista_pdvs_completa:
            dados_pdv = {
                "ip": pdv.IP,
                "port": pdv.porta_ssh_pdv,
                "login": pdv.login_pdv,
                "pwd": pdv.pwd_pdv
            }
            lista_destinos.append(dados_pdv)
            dados_pdv = None
        dados_gateway = {
            "ip": request.session["hostname_gateway"],
            "port": request.session["porta_ssh_gateway"],
            "login": request.session["usuario_ssh_gateway"],
            "pwd":request.session["senha_ssh_gateway"]
        }
        # posso logo mandar o comando pra coletar o número do pinpad né
        t_n = t_Nested_SSH(lista_destinos, gateway_dados=dados_gateway, comando="hostname")
        # para cada resposta dos comandos, constrói a lista dos PDVs
        dict_pdvs = dict()
        for resposta in t_n.respostas:
            if resposta["conectou"]:
                # busca no banco o pdv com este IP
                pdv_on = PDV.objects.filter(IP=resposta["ip"]).values()[0]
                p = {
                    "checkout": pdv_on.checkout,
                    "IP": pdv_on.IP,
                    "login_pdv": pdv_on.login_pdv,
                    "pwd_pdv": pdv_on.pwd_pdv,
                    "porta_ssh_pdv": pdv_on.porta_ssh_pdv,
                    "conexao_pinpad": pdv_on.conexao_pinpad,
                    "num_serial_pinpad": pdv_on.num_serial_pinpad,
                    "tipo_pdv": pdv_on.tipo_pdv,
                    "id_pdv": pdv_on.id
                }
                dict_pdvs.append(p)
                
        return dict_pdvs
    
    if request.method == "POST":
        if request.POST["operacao"] == 'login_servidor_gateway':
            login_gateway()
        if request.POST["operacao"] == 'criar':
            cadastrar_pdv()
        if request.POST["operacao"] == 'excluir':
            excluir_pdv()
        if request.POST["operacao"] == 'editar':
            editar_pdv()

    
    try: 
        dict_pdvs = exibir_pdvs()
        return render(request,
                'exibir_pdvs.html',
                {
                    "form_pdv": form_pdv,
                    "lista_tipos_pdv": lista_tipos_pdv,
                    "form_login_gateway": form_login_gateway,
                    "PDVs": dict_pdvs
                    }
                )
    except KeyError:
        # se parametros de gateway não estiverem definidos, exibe apenas o form de login
        return render(request,
                'exibir_pdvs.html',
                {
                    "form_login_gateway": form_login_gateway
                    }
                )
    
