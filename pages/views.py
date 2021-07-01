from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render
from .models import *
import ast
from time import time
from datetime import datetime, timedelta
from django.db.models import Sum
import json
import pickle

max_ts_diff = 5

def dashboard(request):
    args = {
        'current': '-',
        'tot_enery': '-',
        'set_voltage': '-',
        'pwr': '-'
    }

    last_log = EnergyLog.objects.order_by('-pk')[0]
    last_ts = last_log.ts
    current_ts = int(time())
    diff = current_ts - last_ts
    if diff <= max_ts_diff:
        args['current'] = last_log.current
        args['tot_enery'] = last_log.tot_enery
        args['set_voltage'] = last_log.set_voltage
        args['pwr'] = last_log.pwr
    
    print('diff: ', diff)
    print('args: ', args)
    print(last_log.ts)
    return render(request, 'pages/dashboard.html', args)

def log(request, d=''):
    print(d)
    if(d == 'd={}'):
        logs = EnergyLog.objects.all().order_by('-pk')[0:100]
        start = str(logs[len(logs)-1].date.strftime('%m-%d-%Y')).split(' ')[0]
        end = str(logs[0].date.strftime('%m-%d-%Y')).split(' ')[0]
    else: 
        data = ast.literal_eval(d)
        start = datetime.strptime(data['start_timestamp'], '%m-%d-%Y')
        end = datetime.strptime(data['end_timestamp'], '%m-%d-%Y')
        print('........')
        print('end: ', end)
        end += timedelta(days=1)
        print('incrimented: ', end)
        print('........')
        print('start : ', start)
        print('end: ', end)
        logs = EnergyLog.objects.filter(date__gte=start, date__lte=end)
        
        start = str(start.strftime('%m-%d-%Y')).split(' ')[0]
        end += timedelta(days=-1)
        end = str(end.strftime('%m-%d-%Y')).split(' ')[0]
        

    
    try:
        tot_energy_consumed = logs.aggregate(Sum('pwr'))['pwr__sum']/(1000.0*3600)
    except:
        tot_energy_consumed = 0.0

    if tot_energy_consumed > 1:
        tot_energy_consumed = round(tot_energy_consumed, 2)
    else:
        tot_energy_consumed = round(tot_energy_consumed, 6)
    args = {
        'logs': logs,
        'start': start,
        'end': end,
        'tot_energy_consumed': tot_energy_consumed
    }
    return render(request, 'pages/log.html', args)

def log_data(request, d):
    data = ast.literal_eval(d)
    # d={"current": current_rms, 'set_voltage': voltage, 'tot_energy': total_energy, 'pwr': power}
    new_log = EnergyLog()
    new_log.current = data['current']
    new_log.set_voltage = data['set_voltage']
    new_log.tot_enery = data['tot_energy']
    new_log.pwr = data['pwr']
    new_log.ts = time()
    new_log.save()
    for i in data:
        print(i, data[i])
    return JsonResponse({})


def lattest_data(request):
    args = {
        'current': '',
        'tot_enery': '',
        'set_voltage': '',
        'pwr': ''
    }

    last_log = EnergyLog.objects.order_by('-pk')[0]
    last_ts = last_log.ts
    current_ts = int(time())
    diff = current_ts - last_ts
    if diff <= max_ts_diff:
        args['current'] = str(last_log.current) + ' A'
        args['tot_enery'] = str(round(last_log.tot_enery, 6)) + ' kWh'
        args['set_voltage'] = str(last_log.set_voltage) + ' V'
        args['pwr'] = str(round(last_log.pwr, 2)) + ' W'

    return JsonResponse(args)


def peak_hours(request      ):
    data = {
        "Jan":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "Feb":[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "Mar":[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "Apr":[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        "May":[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "Jun":[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1],
        "Jul":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
        "Aug":[1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        "Sep":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "Oct":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        "Nov":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        "Dec":[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
    }
    data_json = json.dumps(data)
    return JsonResponse(data)

def l_stat_api(request):
    with open('/home/ubuntu/app/pages/lc-log.pickle', 'rb') as handle:
        data = pickle.load(handle)[-1]
    
    k=list(data.keys())[0]
    ts=int(k)*1000
    v=[list(i) for i in data[k]]
    args = {
        'd': data,
        'key': k,
        'vals': v,
        'ts': ts,
    }
    return JsonResponse(args)

def l_stat(request):
    with open('/home/ubuntu/app/pages/lc-log.pickle', 'rb') as handle:
        data = pickle.load(handle)[-1]
    k=list(data.keys())[0]
    ts=int(k)*1000
    v=[list(i) for i in data[k]]
    args = {
        'data': data,
        'key': k,
        'vals': v,
        'ts': ts,
    }
    return render(request, 'pages/l-stat.html', args)

def log_temp_hum_mot(request, temp, hum, mot):
    new_log = EnvironmentalDataLog()
    new_log.ts = int(time())
    new_log.temp = float(temp)
    new_log.humidity = float(hum)
    new_log.motion = 0 if mot == '0' else 1
    new_log.save()
    args = {
        'temp': temp,
        'humidity': hum,
        'motion': mot,
    }
    return JsonResponse(args)
