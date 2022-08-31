from decimal import Decimal
import json
from django.shortcuts import get_object_or_404, render
from .models import Building,Character,Event,Settlement,Funds
from django.db.models import Sum
from django.contrib.auth.decorators import login_required,user_passes_test


# Create your views here.

from django.http import HttpResponse


def index(request):
    
    building_list = Building.objects.all()
    character_list = Character.objects.all()
    event_list = Event.objects.all().order_by('-id')[:5]
    settlement_list = Settlement.objects.first()

    #caculate current gold 
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
     'character_list': character_list, 
     'event_list_asc' : event_list, 
     'settlement_list':settlement_list,
     'pos_funds': getFunds()
     }

    return render(request, 'pages/index.html', data)

def info(request):

    return render(request, 'pages/info.html')

@login_required
def manage(request):

    #Population calc
    current_pop = Settlement.objects.filter(id=1).values('population').get()['population']
    pop_mod = Building.objects.aggregate(Sum('pop_mod')).get('pop_mod__sum', 0.00)
    
    settlement_level = Settlement.objects.filter(id=1).values('settlement_level').get()['settlement_level']
    base_pop_mod = 0
    if  settlement_level == 1: 
        base_pop_mod = Decimal(0.9)
    else:
        base_pop_mod = settlement_level
        
   
    growth_rate = (base_pop_mod*(1+pop_mod))/100
    print(growth_rate)

    new_pop = current_pop+(current_pop*growth_rate)
    print(new_pop)

    #calc tax
  




    data = {'pop_mod': pop_mod, 'base_pop_mod':base_pop_mod, 'current_pop' : current_pop}
    return render(request, 'pages/management.html', data)

def progress(request, pk):


    return render(request, 'pages/index.html')