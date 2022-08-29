import json
from django.shortcuts import get_object_or_404, render
from .models import Building,Character,Event,Settlement,Funds
from django.db.models import Sum


# Create your views here.

from django.http import HttpResponse


def index(request):
    
    building_list = Building.objects.all()
    character_list = Character.objects.all()
    event_list = Event.objects.all().order_by('-id')[:5]
    settlement_list = Settlement.objects.first()

    def getFunds():
        pos_funds = Funds.objects.aggregate(Sum('pos_change'))
        neg_funds = Funds.objects.aggregate(Sum('neg_change'))

        if list(pos_funds.values())[0] > list(neg_funds.values())[0]:
            current_funds = list(pos_funds.values())[0] - list(neg_funds.values())[0]
            return current_funds
        else:
            current_funds =  list(pos_funds.values())[0] - list(neg_funds.values())[0]
            return current_funds

    data =  {
     'building_list' : building_list,
     'character_list':  character_list, 
     'event_list_asc' : event_list, 
     'settlement_list':settlement_list,
     'pos_funds': getFunds()
     }
    
    return render(request, 'pages/index.html', data)

def info(request):

    return render(request, 'pages/info.html')