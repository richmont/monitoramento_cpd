# Instruções para instalação do sistema
## Pré-requisitos:
- CPython 3.9 ou superior instalado
- Ambiente virtual preparado (virtualenv)
- Banco de dados MySQL

### Criando e ativando um ambiente virtual
#### No Windows
Através do CMD ou Powershell, navegue até um diretório de preferência, e rode os comandos:  
    python -m venv venv_monitoramento_cpd  
Você pode escolher outro nome diferente de venv_monitoramento_cpd se quiser.  
Ative através do comando:  
    cd venv_monitoramento_cpd  
    Scripts\activate  
Atenção para a aparência do terminal após a execução, deve conter entre parênteses o nome do ambiente virtual.  
Por exemplo:  
    (venv_monitoramento_cpd) C:\  
Prossiga apenas se ativou com sucesso o ambiente virtual  

#### No Linux  
Na instalação padrão presente em distribuições baseadas no debian, não há o pip ou o venv, instale-os se necessário:  
    sudo apt install python3-venv python3-pip  

Através do terminal Bash, navegue até um diretório de preferência, e rode os comandos:
    python3 -m venv venv_monitoramento_cpd  
E ative o ambiente virtual:  
    cd venv_monitoramento_cpd  
    source bin/activate
Atenção para a aparência do terminal após a execução, deve conter entre parênteses o nome do ambiente virtual.  
Por exemplo:  
    (venv_monitoramento_cpd) usuario@hostname$  
Prossiga apenas se ativou com sucesso o ambiente virtual  

### Clone o projeto
Clone usando git dentro do ambiente virtual já ativado:  
    git clone --recursive https://gitlab.com/richmont1/monitoramento_cpd

Caso tenha clonado o projeto sem os submódulos, execute estes dois comandos:  
    cd monitoramento_cpd  
    git submodule init  
    git submodule update  

### Instale as bibliotecas necessárias
Deve estar dentro da pasta do projeto, "monitoramento_cpd", não apenas dentro do ambiente virtual  
    pip install -r requirements.txt  
Caso esteja usando uma rede protegida ou com certificados próprios, talvez seja preciso marcar os servidores de pacotes pip como confiáveis:  
    pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org -r requirements.txt  
Aguarde que todos os pacotes estejam instalados.  

### Configurando o arquivo dotenv  
