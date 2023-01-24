from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
import datetime

from eggs.models import eggs,bt_lyr
# Create your views here.

# @user_passes_test(lambda u: u.is_superuser)
@csrf_protect
def user_login(request):
    if(request.user.is_authenticated):
        logout(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        user = authenticate(username=username, password=password)

        if user:
            if(user.is_active):
                login(request, user)
                return HttpResponseRedirect('/batch_layer')

            else:
                return HttpResponse("Account Not Active")
        else:
            # print("u={}p={}".format(username, password))
            return render(request, 'login/login.html', {'invaliduser': True})
    else:
        return render(request, 'login/login.html', {'invaliduser': False})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login')

def home(request):
    return render(request,'home.html')
@login_required()
def batch_layer(request):
    bt_lyrs = bt_lyr.objects.all()
    request.session['pp_bt_layer'] = True
    return render(request,'batch_layer.html',{"bt_lyrs":bt_lyrs})

@login_required()
def check(request,batch_id):
    request.session['batch_id'] = batch_id
    if request.user.is_superuser :
        return HttpResponseRedirect("/display")
    else:
        return HttpResponseRedirect("/input")

@login_required()
@user_passes_test(lambda u: u.is_superuser)
def display(request):
    if('pp_bt_layer' not in request.session):
        return HttpResponseRedirect('/batch_layer')
    egg_dataset = eggs.objects.filter(batch_no = request.session.get("batch_id"))
    return render(request,'display_child.html',{"eggs_dataset":egg_dataset})

@login_required()
def eggs_input(request):
    if('pp_bt_layer' not in request.session):
        return HttpResponseRedirect('/batch_layer')
    #if(eggs.objects.filter(date_time =  datetime.datetime.now().date()).exists()):
    #   return HttpResponse('Data for this date has already been stored.')
    boolean = eggs.objects.filter(batch_no = request.session.get("batch_id")).exists()
    if request.method == 'POST':
        if(boolean):
            normal_eggs = int(request.POST.get("normal"))
            small_eggs = int(request.POST.get("small"))
            big_eggs = int(request.POST.get("big"))
            broken_eggs = int(request.POST.get("broken"))
            damage_eggs = int(request.POST.get("damage"))
            delivery_eggs = int(request.POST.get("delivery"))
            to_gate_eggs = int(request.POST.get("to_gate"))
            spoiled_eggs = int(request.POST.get("spoiled"))
            sold_birds = int(request.POST.get("sold"))
            mortality_birds = int(request.POST.get("mortality"))
            total_eggs = normal_eggs+small_eggs+big_eggs+broken_eggs
            info = eggs()
            info.batch_no = bt_lyr.objects.get(id = request.session.get("batch_id"))
            info.date_time = datetime.datetime.now()
            info.normal = normal_eggs
            info.small = small_eggs
            info.big = big_eggs
            info.broken = broken_eggs
            info.damage = damage_eggs
            info.day_total = total_eggs
            info.delivery = delivery_eggs
            info.to_gate = to_gate_eggs
            info.spoiled = spoiled_eggs
            info.sold = sold_birds
            info.mortality = mortality_birds
            info.save()
            return HttpResponseRedirect('/input/')
            
        else:
            closing_eggs = int(request.POST.get("closing"))
            total_birds = int(request.POST.get("total_birds"))
            d1 = eggs()
            d1.batch_no = bt_lyr.objects.get(id = request.session.get("batch_id"))
            d1.closing = closing_eggs
            d1.total_birds = total_birds
            d1.save()
            return HttpResponseRedirect('/input/')
    else:
        if(boolean):
            exists = True
        else:
            exists = False
        return render(request,'input/input1.html',{'exists':exists})