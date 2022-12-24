from django.shortcuts import render
from django.forms import ValidationError
from django.contrib import messages
from monitoramento_cpd_app.models.pdvs import PDV, lista_tipos_pdv
from monitoramento_cpd_app.forms.form_cadastrar_pdv import FormPDV
from monitoramento_cpd_app.forms.form_login_ssh_gateway import FormLoginGateway
from monitoramento_cpd.nested_ssh.src.t_Nested_SSH import t_Nested_SSH, Nested_SSH
from conf.configuracoes import COMANDO_COLETAR_SERIAL_PINPAD, COMANDO_INICIAR_PDV, COMANDO_PARAR_PDV
import paramiko
import socket
import logging
logger = logging.getLogger("")
logging.basicConfig(level=logging.INFO)

def pdvs(request):
    def cadastrar_pdv():
        checkout = request.POST["checkout"]
        ip = request.POST["IP"]
        tipo_pdv = str(request.POST["tipo_pdv"])
        login_pdv = str(request.POST["login_pdv"])
        pwd_pdv = str(request.POST["pwd_pdv"])
        porta_ssh_pdv = str(request.POST["porta_ssh_pdv"])
        conexao_pinpad = str(request.POST["conexao_pinpad"])

        pdv = PDV(checkout=checkout,
            tipo_pdv=tipo_pdv,
            IP=ip,
            login_pdv=login_pdv,
            pwd_pdv=pwd_pdv,
            porta_ssh_pdv=porta_ssh_pdv,
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
#        if request.POST["id_PDV"] is None or len(request.POST["id_PDV"]):
#            messages.add_message(request, messages.ERROR, f"ID do PDV inválido: ", request.POST["id_PDV"])
#        else:
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
    
    def reiniciar_pdv():
        id_PDV_reiniciar = int(request.POST["id_PDV"])
        login_pdv = str(request.POST["login_pdv"])
        pwd_pdv = str(request.POST["senha_pdv"])
        try:
            pdv_reiniciar = PDV.objects.filter(id=id_PDV_reiniciar).values()[0]
        except IndexError:
            logger.error("PDV não encontrado, ID inválido")
            messages.add_message(request, messages.INFO,
                                    f"PDV de id {id_PDV_reiniciar}, não encontrado, tente novamente")
        dados_pdv = {
                "ip": str(pdv_reiniciar["IP"]),
                "port": int(pdv_reiniciar["porta_ssh_pdv"]),
                "login": str(login_pdv),
                "pwd": str(pwd_pdv)
            }
        try:
            dados_gateway = {
                "ip": request.session["hostname_gateway"],
                "port": int(request.session["porta_ssh_gateway"]),
                "login": request.session["usuario_ssh_gateway"],
                "pwd":request.session["senha_ssh_gateway"]
            }
            g_reiniciar = Nested_SSH(gateway_dados=dados_gateway)
            r_parar_pdv = g_reiniciar.executar(
                destino_dados=dados_pdv, 
                comando=COMANDO_PARAR_PDV)
            r_iniciar_pdv = g_reiniciar.executar(
                destino_dados=dados_pdv, 
                comando=COMANDO_INICIAR_PDV)
        except Nested_SSH.erros.FalhaConexao:
            messages.add_message(request, messages.INFO,
                                    f"PDV {pdv_reiniciar['checkout']}, falhou a conexão, verifique endereço")
        except Nested_SSH.erros.FalhaAutenticacao:
            messages.add_message(request, messages.INFO,
                                    f"Reinício do PDV {pdv_reiniciar['checkout']}, falhou por login ou senha incorretos")
        except Nested_SSH.erros.EnderecoIncorreto:
            messages.add_message(request, messages.INFO,
                                    f"Reinício do PDV {pdv_reiniciar['checkout']}, por endereço incorreto")
        except KeyError:
            return render(request,
            'exibir_pdvs.html',
            {
                "form_pdv": form_pdv,
                "lista_tipos_pdv": lista_tipos_pdv,
                "form_login_gateway": form_login_gateway
                }
            )
        
    
    # formulário de cadastro do pdv
    form_pdv = FormPDV()
    form_login_gateway = FormLoginGateway()

    # Lista de IPs dos PDVs a partir do banco
    def exibir_pdvs():
        lista_pdvs_completa = PDV.objects.all()
        lista_destinos = list()
        for pdv in lista_pdvs_completa:
            logger.debug("Criando dicionário com valores dos pdvs")
            
            dados_pdv = {
                "ip": str(pdv.IP),
                "port": int(pdv.porta_ssh_pdv),
                "login": str(pdv.login_pdv),
                "pwd": str(pdv.pwd_pdv)
            }
            
            lista_destinos.append(dados_pdv)
            dados_pdv = None
        
        try:
            dados_gateway = {
                "ip": request.session["hostname_gateway"],
                "port": request.session["porta_ssh_gateway"],
                "login": request.session["usuario_ssh_gateway"],
                "pwd":request.session["senha_ssh_gateway"]
            }
        except KeyError:
            return render(request,
            'exibir_pdvs.html',
            {
                "form_pdv": form_pdv,
                "lista_tipos_pdv": lista_tipos_pdv,
                "form_login_gateway": form_login_gateway
                }
            )
        
        # posso logo mandar o comando pra coletar o número do pinpad né
        t_n = t_Nested_SSH(lista_destinos, gateway=dados_gateway, comando=str(COMANDO_COLETAR_SERIAL_PINPAD))
        # para cada resposta dos comandos, constrói a lista dos PDVs
        lista_pdvs = list()
        print(t_n.respostas)
        for resposta in t_n.respostas:
            if resposta["conectou"]:
                # quebra a resposta usando o \n para quando há múltiplos seriais no diretório
                serial = resposta["resposta"].split("\n")[0]
                
                pdv_on = PDV.objects.filter(IP=resposta["maquina"]).values()[0]
                p = {
                    "checkout": pdv_on["checkout"],
                    "IP": pdv_on["IP"],
                    "login_pdv": pdv_on["login_pdv"],
                    "pwd_pdv": pdv_on["pwd_pdv"],
                    "porta_ssh_pdv": pdv_on["porta_ssh_pdv"],
                    "conexao_pinpad": pdv_on["conexao_pinpad"],
                    "num_serial_pinpad": serial,
                    "tipo_pdv": pdv_on["tipo_pdv"],
                    "id_pdv": pdv_on["id"],
                    "online": "online"
                }
                lista_pdvs.append(p)
                
            else:
                pdv_off = PDV.objects.filter(IP=resposta["maquina"]).values()[0]
                p = {
                    "checkout": pdv_off["checkout"],
                    "IP": pdv_off["IP"],
                    "login_pdv": pdv_off["login_pdv"],
                    "pwd_pdv": pdv_off["pwd_pdv"],
                    "porta_ssh_pdv": pdv_off["porta_ssh_pdv"],
                    "conexao_pinpad": pdv_off["conexao_pinpad"],
                    "tipo_pdv": pdv_off["tipo_pdv"],
                    "id_pdv": pdv_off["id"],
                    "online": "offline"
                }
                lista_pdvs.append(p)
        
        return lista_pdvs
    
    if request.method == "POST":
        if request.POST["operacao"] == 'login_servidor_gateway':
            login_gateway()
        if request.POST["operacao"] == 'criar':
            cadastrar_pdv()
        if request.POST["operacao"] == 'excluir':
            excluir_pdv()
        if request.POST["operacao"] == 'editar':
            editar_pdv()
        if request.POST["operacao"] == 'reiniciar':
            reiniciar_pdv()

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
