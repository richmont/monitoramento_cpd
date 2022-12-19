import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DJANGO_SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
HOSTNAME_SERVER = os.environ.get("HOSTNAME_SERVER")
IP_SERVER = os.environ.get("IP_SERVER")
