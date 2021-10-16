from django.shortcuts import render
from .models import Commune, Wilaya
# Create your views here.

def load_communes(request):
    wilaya_id = request.GET.get('wilaya_id')
    print('wilaya id', wilaya_id)
    if wilaya_id:
        communes = Commune.objects.filter(wilaya__id=wilaya_id)
    else:
        communes = []
    # print('les wilayas', communes)
    return render(request, 'snippets/communes_options.html', {'communes': communes})

def delivery_cost(request):
    wilaya_id = request.GET.get('wilaya_id')
    if wilaya_id:
        wilaya = Wilaya.objects.get(id=wilaya_id)
        cost = wilaya.price
    else:
        cost = ''
    return render(request, 'snippets/delivery_cost.html', {'cost' : cost})

