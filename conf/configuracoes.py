import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DJANGO_SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
HOSTNAME_SERVER = os.environ.get("HOSTNAME_SERVER")
IP_SERVER = os.environ.get("IP_SERVER")
COMANDO_COLETAR_SERIAL_PINPAD = os.environ.get("COMANDO_COLETAR_SERIAL_PINPAD")
COMANDO_PARAR_PDV = os.environ.get("COMANDO_PARAR_PDV")
COMANDO_INICIAR_PDV = os.environ.get("COMANDO_INICIAR_PDV")
MYSQL_LOGIN = os.environ.get("MYSQL_LOGIN")
MYSQL_SENHA = os.environ.get("MYSQL_SENHA")
MYSQL_PORTA = os.environ.get("MYSQL_PORTA")
MYSQL_SERVIDOR = os.environ.get("MYSQL_SERVIDOR")
MYSQL_BANCO_NOME = os.environ.get("MYSQL_BANCO_NOME")