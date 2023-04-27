from django.shortcuts import render

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import user_passes_test
from django.utils import timezone

from eggs.models import *
from eggs.forms import *
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
                return HttpResponseRedirect('/select')

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
def select(request):
    bt_lyrs_status = bt_lyr.objects.filter(active = True).exists()
    return render(request,'selection.html',{'bt_lyrs':bt_lyrs_status})

@login_required()
def chicks_menu(request):
    layer_status = layer.objects.filter(occupied = False).exists()
    batch_status = chicks.objects.filter(active = True).exists()
    return render(request,'chicks_menu.html',{'layer_status':layer_status,'batch_status':batch_status})

@login_required()
def new_batch(request):
    if request.method == 'POST':
        batch_number = int(request.POST.get("batch_number"))
        total_birds = int(request.POST.get('total_birds'))
        if(chicks.objects.filter(batch_no =  batch_number).exists()):
            return HttpResponse("Batch Already Exists")
        chicks_dt = chicks()
        data_chicks = chicks_data()
        data_feed = feed_chicks()

        chicks_dt.active = True
        chicks_dt.date = timezone.now()
        chicks_dt.batch_no = batch_number
        chicks_dt.total_birds = total_birds
        chicks_dt.save()
        data_chicks.batch_no = chicks.objects.get(batch_no = batch_number)
        data_chicks.total_birds = total_birds
        data_feed.batch_no = chicks.objects.get(batch_no = batch_number)
        data_chicks.save()
        data_feed.save()
        
        return HttpResponseRedirect("/select")
    else:
        date = timezone.now().strftime("%Y-%m-%d")
        batch_no_suggest = chicks.objects.all().count() + 1
        return render(request,'chicks_new_batch.html',{'date':date,'batch_no_suggest':batch_no_suggest})

@login_required()
def update_batch(request):
    return render(request,'update_menu.html')

@login_required()
def feed_input(request):
    if(request.method == 'POST'):
        received = int(request.POST.get("received"))
        meter_reading = int(request.POST.get("meter_reading"))
        print(request.POST.get("batch_no"))
        batch_no = int(request.POST.get("batch_no"))

        feed_dt = feed_chicks()
        feed_dt.batch_no = chicks.objects.get(batch_no = batch_no)
        feed_dt.received = received
        feed_dt.meter_reading = meter_reading
        prev_meter_reading = feed_chicks.objects.filter(batch_no = batch_no).order_by('-id')[0].meter_reading
        used = prev_meter_reading + received - meter_reading
        feed_dt.used = used
        feed_dt.gram_per_bird = (used/10)*100
        feed_dt.save()
        ## batch is unique for chicks or duplicate??
        return HttpResponseRedirect('/select')
    else:
        date = timezone.now().strftime("%Y-%m-%d")
        batch_nos = chicks.objects.filter(active = True)
        return render(request,"feed_input.html",{'date':date,'batch_nos':batch_nos}) 

@login_required()
def chicks_input(request):
    if(request.method == 'POST'):
        mortality = int(request.POST.get("mortality"))
        sold = int(request.POST.get("sold"))
        batch_no = int(request.POST.get("batch_no"))
        
        chicks_dt = chicks_data()
        chicks_dt.batch_no = chicks.objects.get(batch_no = batch_no)
        chicks_dt.mortality = mortality
        chicks_dt.sold = sold
        prev_total_birds = chicks_data.objects.filter(batch_no = batch_no).order_by('-id')[0].total_birds
        total_birds = prev_total_birds - mortality - sold
        chicks_dt.total_birds = total_birds
        chicks_dt.save()
        return HttpResponseRedirect('/select')
    else:
        date = timezone.now().strftime("%Y-%m-%d")
        batch_nos = chicks.objects.filter(active = True)
        return render(request,"chicks_input.html",{'date':date,'batch_nos':batch_nos})

@login_required()
def move_batch(request):
    if(request.method == 'POST'):
        batch_no = int(request.POST.get("batch_no"))
        layer_no = int(request.POST.get("layer_no"))
        chicks_id = chicks.objects.get(batch_no = batch_no)
        chicks_id.active = False
        chicks_id.save()
        layer_id = layer.objects.get(layer_no = layer_no)
        layer_id.occupied = True
        layer_id.save()
        bt_lyr_id = bt_lyr.objects.create(layer_no = layer_id,batch_no = chicks_id,active = True)
        feed_hen.objects.create(bt_lyr_no = bt_lyr_id)
        total_birds = chicks_data.objects.filter(batch_no = batch_no).order_by('-id')[0].total_birds
        eggs_update = eggs.objects.create(bt_lyr_no = bt_lyr_id,total_birds = total_birds)
        #eggs _ conversion
        return HttpResponseRedirect('/select')
    else:
        batch_nos = chicks.objects.filter(active = True)
        layer_nos = layer.objects.filter(occupied = False)
        return render(request,"move_to_layer.html",{'batch_nos':batch_nos,'layer_nos':layer_nos})

@login_required()
def eggs_menu(request):
    bt_lyrs_status = bt_lyr.objects.filter(active = True).exists()
    return render(request,'eggs_menu.html',{'bt_lyrs_status':bt_lyrs_status})

@login_required()
def update_feed_hens(request):
    if(request.method == 'POST'):
        received = int(request.POST.get("received"))
        meter_reading = int(request.POST.get("meter_reading"))
        bt_lyr_no = int(request.POST.get("bt_lyr"))

        feed_dt = feed_hen()
        feed_dt.bt_lyr_no = bt_lyr.objects.get(id = bt_lyr_no)
        feed_dt.received = received
        feed_dt.meter_reading = meter_reading
        prev_meter_reading = feed_hen.objects.filter(bt_lyr_no = bt_lyr_no).order_by('-id')[0].meter_reading
        used = prev_meter_reading + received - meter_reading
        feed_dt.used = used
        feed_dt.gram_per_bird = (used/10)*100
        feed_dt.save()
        ## batch is unique for chicks or duplicate??
        return HttpResponseRedirect('/select')
    else:
        date = timezone.now().strftime("%Y-%m-%d")
        bt_lyrs = bt_lyr.objects.filter(active = True)
        return render(request,"feed_input_hen.html",{'date':date,'bt_lyrs':bt_lyrs})

'''
@login_required()
def check(request,batch_id):
    request.session['batch_id'] = batch_id
    if request.user.is_superuser :
        return HttpResponseRedirect("/display")
    else:
        return HttpResponseRedirect("/input")
'''


@login_required()
def update_eggs_hens(request):
    # if(eggs.objects.filter(date_time =  datetime.datetime.now().date()).exists()):
        # return HttpResponse('Data for this date has already been stored.')
    if request.method == 'POST':
        bt_lyr_no = int(request.POST.get("bt_lyr"))
        normal_eggs = int(request.POST.get("normal"))
        small_eggs = int(request.POST.get("small"))
        big_eggs = int(request.POST.get("big"))
        broken_eggs = int(request.POST.get("broken"))
        damage_eggs = int(request.POST.get("damage"))
        to_gate_eggs = int(request.POST.get("to_gate"))
        spoiled_eggs = int(request.POST.get("spoiled"))
        sold_birds = int(request.POST.get("sold"))
        mortality_birds = int(request.POST.get("mortality"))
        
        total_eggs = normal_eggs+small_eggs+big_eggs+broken_eggs
        
        info = eggs()
        info.bt_lyr_no = bt_lyr.objects.get(id = bt_lyr_no)
        prev_closing = eggs.objects.filter(bt_lyr_no = bt_lyr_no).order_by('-id')[0].closing
        prev_total_birds = eggs.objects.filter(bt_lyr_no = bt_lyr_no).order_by('-id')[0].total_birds

        # total_delivery = delivery_normal + delivery_small + delivery_broken + delivery_big
        # closing = prev_closing + total_eggs - total_delivery - to_gate_eggs - spoiled_eggs

        total_birds = prev_total_birds - sold_birds - mortality_birds

        info.normal = normal_eggs
        info.small = small_eggs
        info.big = big_eggs
        info.broken = broken_eggs
        info.damage = damage_eggs
        info.day_total = total_eggs
        
        info.delivery = 0
        info.to_gate = to_gate_eggs
        info.spoiled = spoiled_eggs

        info.sold = sold_birds
        info.mortality = mortality_birds
        # info.closing = closing
        info.total_birds = total_birds
        info.production = round(((total_eggs/total_birds)*100),3)

        #info.save()
        return render(request,'input/success.html')
    else:
        date = timezone.now().strftime("%Y-%m-%d")
        bt_lyrs = bt_lyr.objects.filter(active = True)
        return render(request,"eggs_input_hen.html",{'date':date,'bt_lyrs':bt_lyrs})
    
def update_delivery_hens(request):
    if request.method == 'POST':
        # bt_lyr_no = int(request.POST.get("bt_lyr"))

        vendor_name = int(request.POST.get("vendor_name"))
        delivery_normal = int(request.POST.get("deliver_normal"))
        delivery_small = int(request.POST.get("deliver_small"))
        delivery_big = int(request.POST.get("deliver_big"))
        delivery_broken = int(request.POST.get("deliver_broken"))

        info = delivery()
        # info.bt_lyr_no = bt_lyr.objects.get(id = bt_lyr_no)

        info.name = vendor.objects.get(id = vendor_name)
        info.delivery_normal = delivery_normal*30
        info.delivery_big = delivery_big*30
        info.delivery_small = delivery_small*30
        info.delivery_broken = delivery_broken*30


        return HttpResponseRedirect('/success')
    else:
        date = timezone.now().strftime("%Y-%m-%d")
        # bt_lyrs = bt_lyr.objects.filter(active = True)
        vendor_names = vendor.objects.all()
        return render(request,"delivery_input_hen.html",{'date':date,'vendor_names':vendor_names})


def success(request):
    return render(request,'input/success.html')

def close_production(request):
    if request.method == 'POST':
        bt_lyr_no = int(request.POST.get("bt_lyr"))
        bt_lyrs = bt_lyr.objects.get(id = bt_lyr_no)
        bt_lyrs.active = False
        bt_lyrs.save()
        return HttpResponse('Production Stopped')
    else:
        date = timezone.now().strftime("%Y-%m-%d")
        bt_lyrs = bt_lyr.objects.filter(active = True)
        return render(request,"close_production.html",{'date':date,'bt_lyrs':bt_lyrs})


#Admin Views
def admin_menu(request):
    batches = chicks.objects.filter(active = True)
    layers = bt_lyr.objects.filter(active = True)

    
    return render(request,'admin/admin_menu.html',{'batches':batches, 'layers':layers})


def layer_report(request):
    report = eggs.objects.all()

    if request.method == 'POST':
        form = flt_form(request.POST)
        if(form.is_valid()):
            bt_lyr_no = form.cleaned_data.get('bt_lyr_no')

            filters = {}
            if bt_lyr_no:
                filters['bt_lyr_no'] = bt_lyr.objects.get(id = bt_lyr_no)
            
            report = eggs.objects.filter(**filters)

    else:
        form = flt_form()

    context = {
        'form': form,
        'report': report,
    }
    return render(request,'office_staff/layer_report.html',context)