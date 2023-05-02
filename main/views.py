import datetime
from decimal import Decimal
from django.shortcuts import get_object_or_404, render, redirect
from .models import Building,Character,Event, Population_change,Settlement,Funds
from django.db.models import Sum
from django.contrib.auth.decorators import login_required,user_passes_test


# Create your views here.

from django.http import HttpResponse


#get current population 

def index(request):
    
    building_list = Building.objects.all()
    character_list = Character.objects.all()
    event_list = Event.objects.all().order_by('-id')[:5]
    settlement_list = Settlement.objects.first()

    #caculate current gold 
    def getFunds():
        pos_funds = Funds.objects.aggregate(Sum('pos_change'))
        neg_funds = Funds.objects.aggregate(Sum('neg_change'))

        #IDK this is redundant? 
        if list(pos_funds.values())[0] > list(neg_funds.values())[0]:
            current_funds = list(pos_funds.values())[0] - list(neg_funds.values())[0]
            return current_funds
        else:
            current_funds =  list(pos_funds.values())[0] - list(neg_funds.values())[0]
            return current_funds

    #get current population 
    def getPop():
        start_pop = Settlement.objects.filter(id=1).values('starting_population').get()['starting_population']

        pos_pop_change = Population_change.objects.aggregate(Sum('pop_pos_change'))
        neg_pop_change = Population_change.objects.aggregate(Sum('pop_neg_change'))

        if list(pos_pop_change.values())[0] is None or list(neg_pop_change.values())[0] is None:
            current_pop = start_pop
            return current_pop
        else: 
            pop_change = list(pos_pop_change.values())[0] + list(neg_pop_change.values())[0]
            current_pop = start_pop+pop_change
            return current_pop

    data =  {
     'building_list' : building_list,
     'character_list': character_list, 
     'event_list_asc' : event_list, 
     'settlement_list':settlement_list,
     'pos_funds': getFunds(),
     'current_pop':getPop(),
     }
    return render(request, 'pages/index.html', data)

#info page
def info(request):

    return render(request, 'pages/info.html')

@login_required
def manage(request):

    #Population calc - redundant --> to be changed 
    def getPop():
        start_pop = Settlement.objects.filter(id=1).values('starting_population').get()['starting_population']

        pos_pop_change = Population_change.objects.aggregate(Sum('pop_pos_change'))
        neg_pop_change = Population_change.objects.aggregate(Sum('pop_neg_change'))

        if list(pos_pop_change.values())[0] is None or list(neg_pop_change.values())[0] is None:
            current_pop = start_pop
            return current_pop
        else: 
            pop_change = list(pos_pop_change.values())[0] + list(neg_pop_change.values())[0]
            current_pop = start_pop+pop_change
            return current_pop

      

    current_pop= getPop()
    pop_mod = Building.objects.aggregate(Sum('pop_mod')).get('pop_mod__sum', 0.00)
    settlement_level = Settlement.objects.filter(id=1).values('settlement_level').get()['settlement_level']

    base_pop_mod = 0
    if  settlement_level == 1: 
        base_pop_mod = Decimal(0.9)
    else:
        base_pop_mod = settlement_level

    print('current pop: ')    
    print(current_pop)

    growth_rate = (base_pop_mod*(1+pop_mod))/100
    print(growth_rate)

    new_pop = (current_pop*growth_rate)
    print(new_pop)

    #Revenue calc


    pop_data = {'pop_mod': pop_mod, 'base_pop_mod':base_pop_mod, 'current_pop' : current_pop,'growth_rate':growth_rate, 'new_pop':new_pop}
    return render(request, 'pages/management.html', pop_data)

@login_required
def progress(request, pk):
#Population calc

    #get current population 
    def getPop():
        start_pop = Settlement.objects.filter(id=1).values('starting_population').get()['starting_population']

        pos_pop_change = Population_change.objects.aggregate(Sum('pop_pos_change'))
        neg_pop_change = Population_change.objects.aggregate(Sum('pop_neg_change'))

        if list(pos_pop_change.values())[0] is None or list(neg_pop_change.values())[0] is None:
            current_pop = start_pop
            return current_pop
        else: 
            pop_change = list(pos_pop_change.values())[0] + list(neg_pop_change.values())[0]
            current_pop = start_pop+pop_change
            return current_pop

    current_pop=getPop()
    
    pop_mod = Building.objects.aggregate(Sum('pop_mod')).get('pop_mod__sum', 0.00)
    settlement_level = Settlement.objects.filter(id=1).values('settlement_level').get()['settlement_level']

    #set base growth rate
    base_pop_mod = 0
    if  settlement_level == 1: 
        base_pop_mod = Decimal(0.9)
    else:
        base_pop_mod = settlement_level
        
    print(current_pop)
    #calc gwoth rate
    growth_rate = (base_pop_mod*(1+pop_mod))/100
    print(growth_rate)

    new_pop = (current_pop*growth_rate)
    print(new_pop)

    #create save object 
 
    popChange = Population_change.objects.create(settlement_id=pk, pop_pos_change=new_pop,pop_neg_change=0,pub_date=datetime.date.today())
    popChange.save()

    print('Success!')

    #Revenue calc

    return redirect('main:index')