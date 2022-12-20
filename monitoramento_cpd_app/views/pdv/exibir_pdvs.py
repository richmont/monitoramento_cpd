from django.shortcuts import render
from django.forms import ValidationError
from django.contrib import messages
from monitoramento_cpd_app.models.pdvs import PDV, lista_tipos_pdv
from monitoramento_cpd_app.forms.form_cadastrar_pdv import FormPDV
from monitoramento_cpd.ping_threads.Ping_threads import Ping_threads
from monitoramento_cpd.nested_ssh.src.Nested_SSH import Nested_SSH
from monitoramento_cpd.nested_ssh.src.t_Nested_SSH import t_Nested_SSH

def pdvs(request):

  def cadastrar_pdv():
    if request.method == "POST":
      if request.POST["operacao"] == 'criar':
        checkout = request.POST["checkout"]
        ip = request.POST["IP"]
        tipo_pdv = str(request.POST["tipo_pdv"])
        num_serial_pinpad = str(request.POST["num_serial_pinpad"])
        conexao_pinpad = str(request.POST["conexao_pinpad"])

        pdv = PDV(checkout=checkout,
                  tipo_pdv=tipo_pdv,
                  IP=ip,
                  num_serial_pinpad=num_serial_pinpad,
                  conexao_pinpad=conexao_pinpad
                  )
        try:
          pdv.full_clean()
          pdv.save()
          messages.add_message(request, messages.INFO, f"PDV {checkout}, inserida com sucesso")
        except ValidationError as ex:
          for x in ex:
            messages.add_message(request, messages.ERROR, f"Campo: {x[0]} Erro: {x[1][0]}")
    
  cadastrar_pdv()                    
  # formulário de cadastro do pdv
  form_pdv = FormPDV()

  # Lista de IPs dos PDVs a partir do banco
  #lista_ips_pdvs = PDV.objects.values_list('IP', flat=True)

  lista_pdvs = PDV.objects.all()
  
    
  return render(request,
                'exibir_pdvs.html',
                {
                  "form_pdv": form_pdv,
                  "PDVs": lista_pdvs,
                  "lista_tipos_pdv": lista_tipos_pdv
                  }
                )
