from django.shortcuts import render , get_object_or_404
from .models import Business, ClientService
def infos(request):
    business = Business.objects.all().last()
    sav = ClientService.objects.all()[:4]
    context = {
            'business' : business,
            'sav' : sav
        }
    return context
    

