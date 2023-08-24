# Instruções para instalação do sistema
## Pré-requisitos:
- CPython 3.9 ou superior instalado
- Ambiente virtual preparado (virtualenv)
- Banco de dados MySQL

## Criando e ativando um ambiente virtual
#### No Windows
Através do CMD ou Powershell, navegue até um diretório de preferência, e rode os comandos:  
```batch
    python -m venv venv_monitoramento_cpd  
```
Você pode escolher outro nome diferente de venv_monitoramento_cpd se quiser.  
Ative através do comando:  
```batch
    cd venv_monitoramento_cpd
    Scripts\activate
```
Atenção para a aparência do terminal após a execução, deve conter entre parênteses o nome do ambiente virtual.  
Por exemplo:  
```batch
    (venv_monitoramento_cpd) C:\  
```
Prossiga apenas se ativou com sucesso o ambiente virtual  

#### No Linux
Antes de começar, certifique-se que possui as dependências instaladas (Debian):  
python3-dev
libmariadb-dev
São necessários para compilação do pacote cliente mysql do python.

### Clone o projeto
Clone usando git dentro do ambiente virtual já ativado:  
```bash
    git clone --recursive https://gitlab.com/richmont1/monitoramento_cpd
```
Caso tenha clonado o projeto sem os submódulos, execute estes dois comandos:  
```bash
    cd monitoramento_cpd  
    git submodule init  
    git submodule update  
```

### Instale as bibliotecas necessárias
Deve estar dentro da pasta do projeto, "monitoramento_cpd", não apenas dentro do ambiente virtual  
```bash
    pip install -r requirements.txt  
```
Caso esteja usando uma rede protegida ou com certificados próprios, talvez seja preciso marcar os servidores de pacotes pip como confiáveis:  
```bash
    pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt  
```
Aguarde que todos os pacotes estejam instalados.  

## Configurando o arquivo dotenv  
Dentro do diretório do projeto, abra a pasta "conf" e crie um arquivo ".env" dentro. Atenção para não deixar a extensão *.txt por acidente quando usar o bloco de notas.  
Dentro dele são necessárias as seguintes informações:  

#### DJANGO_SECRET_KEY
Chave secreta do Django, pode ser gerada através de sites como [Djecrety](https://djecrety.ir/) ou como descrito [nestas instruções](https://humberto.io/pt-br/blog/tldr-gerando-secret-key-para-o-django/). Sendo secreta, deve ser mantida em sigilo e usada apenas neste arquivo, caso seja exposta, gere uma nova e reinicie o servidor o quanto antes.  
#### HOSTNAME_SERVER
Hostname da máquina em que a aplicação será executada, serve para definir o endereço disponível para acesso, conveniente para redes que utilizem DNS baseado no hostname das máquinas.  
Exemplo:  
```
    monitoramento01
```
#### IP_SERVER
Endereço IP da máquina em que a aplicação será executada, serve para definir o endereço disponível para acesso.  
Exemplo:  
```
    192.168.0.1
```
#### COMANDO_COLETAR_SERIAL_PINPAD
Comando a ser executado toda vez que a página de PDVs for recarregada, presumindo que a informação do número de série do pinpad conectado ao PDV esteja disponível em arquivo de texto ou de configuração e possa ser obtivo com um só comando.  
Exemplo:  
```bash
    cat /home/serial_pinpad.txt | head -1
```
#### COMANDO_PARAR_PDV
Executado antes do comando para iniciar PDV, presumindo que a aplicação de vendas funcione como um serviço que pode ser parado e iniciado. Executado ao clicar no botão de "reinício" na página de PDVs, após confirmar login e senha
Exemplo: 
```bash
    systemctl stop pdv_servico
```
#### COMANDO_INICIAR_PDV
Similar ao de parar, caso prefira reiniciar a máquina toda, pode deixar o comando de parar em branco, e usar simplesmente "reboot" neste aqui, pois será executado em seguida ao de parar pdv.
Exemplo: 
```bash
    systemctl start pdv_servico
```

#### MYSQL_LOGIN
Login do usuário MySQL para acesso ao banco de dados, deve ter permissão de escrita e criar tabelas na database.  
#### MYSQL_SENHA
Senha do usuário
#### MYSQL_SERVIDOR
Endereço do servidor MySQL, esta aplicação foi desenvolvida usando MariaDB 11.6, mas suporta MySQL tradicional também. O modo de conexão é TCP/IP direto, ainda não há suporte para túnel SSH.  
#### MYSQL_PORTA
Porta para acesso ao servidor MySQL, a padrão é 3306.
#### MYSQL_BANCO_NOME
Nome da database escolhida para uso no sistema, o usuário deve receber permissão prévia para criar tabelas, gravar, apagar e alterar dados. Está planejada a criação de instruções de como realizar esta parte.  

Concluindo a configuração, aqui um exemplo de como seria o arquivo:  
```
DJANGO_SECRET_KEY=g78(ji6xnd#-jcgo2g^86g(ng4!m$w$5e0e#of-d_qr@kp*ypg
HOSTNAME_SERVER=monitoramento01
IP_SERVER=192.168.0.1
COMANDO_COLETAR_SERIAL_PINPAD='cat /home/serial_pinpad.txt | head -1'
COMANDO_PARAR_PDV='systemctl stop pdv_servico'
COMANDO_INICIAR_PDV='systemctl start pdv_servico'
MYSQL_LOGIN=usuario_monitoramento
MYSQL_SENHA=swy51x4h7
MYSQL_SERVIDOR=192.168.0.2
MYSQL_PORTA=3306
MYSQL_BANCO_NOME=monitoramento_cpd

```
## Gravação das tabelas e iniciando o servidor
### Tabelas
Execute a migração das tabelas do sistema com o comando:
```bash
    python manage.py migrate
```
Aguarde concluir, caso receba mensagens de erro, verifique se a conexão do banco de dados está correta, e se a database possui as permissões necessárias.
### Iniciando servidor
Execute o arquivo run.bat, presumindo que você utilize Windows, para executar o comando do servidor WSGI.
```batch
    run.bat
```
O resultado será similar a este:  
```batch
    waitress-serve --listen=*:80 monitoramento_cpd_projeto.wsgi:application
    INFO:waitress:Serving on http://[::]:80
    INFO:waitress:Serving on http://0.0.0.0:80
```
Caso precise interromper, pressione CTRL+C neste terminal.
