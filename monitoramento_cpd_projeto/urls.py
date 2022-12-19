"""monitoramento_cpd_projeto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# imported views
from monitoramento_cpd_app.views import hello_world
from monitoramento_cpd_app.views import ping
from monitoramento_cpd_app.views.impressora import cadastro_impressora
from monitoramento_cpd_app.views.impressora import exibir_impressoras
from monitoramento_cpd_app.views.workstation import exibir_workstation
from monitoramento_cpd_app.views.pdv import exibir_pdvs

urlpatterns = [
    path('admin/', admin.site.urls),
    # configured the url
    path('', hello_world.index, name="homepage"),
    # path('ping',ping.all, name="ping_all"),
    # path('impressoras/cadastro_impressora', cadastro_impressora.cadastrar_impressora, name="cadastro_impressora"),
    path('impressoras/', exibir_impressoras.impressoras, name="exibir_impressoras"),
    path('workstations/', exibir_workstation.workstations, name="exibir_workstations"),
    path('pdvs/', exibir_pdvs.pdvs, name="exibir_pdvs"),
]
