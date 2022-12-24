from django.http import JsonResponse
import sys
 
# setting path
#sys.path.append('...')
from  ping_threads.Ping_threads import Ping_threads

def all(request):
    lista_ips = []
    for x in range(1,254):
        ip = f"192.168.0.{x}"
        lista_ips.append(ip)
    ping_thread = Ping_threads(lista_ips)
    
    dict_ping_all = {}
    for x in ping_thread.respostas:
        
        dict_ping_all[x["ip"]] = x["responde"]
        
        
    
    return JsonResponse(dict_ping_all)