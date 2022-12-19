from django.contrib import admin
from .models import impressoras, workstations, thinclients, pdvs
# Register your models here.
admin.site.register(impressoras.Impressora)
admin.site.register(workstations.Workstation)
admin.site.register(thinclients.Thinclient)
admin.site.register(pdvs.PDV)
