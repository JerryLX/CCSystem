# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
# Create your views here.

process_bar = 0

def index(request):
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render (request, 'home.html')

@csrf_exempt
def runenv(request):
    global process_bar
    process_bar = 0

    knowledge = request.POST["knowledge"]
    bandwidth = request.POST["bandwidth"]
    latency = request.POST["latency"]
    droprate = request.POST["droprate"]
    queuesize = request.POST["queuesize"]

    cmd = '''/home/lixu/pantheon/src/experiments/test.py local --schemes "%s" --uplink-trace /home/lixu/pantheon/src/experiments/traces/%s.trace \
--downlink-trace /home/lixu/pantheon/src/experiments/traces/%s.trace \
--prepend-mm-cmds "mm-delay %s mm-loss uplink %s" \
--extra-mm-link-args "--uplink-queue=droptail --uplink-queue-args=packets=%s" \
--data-dir /home/lixu/CCSystem/static''' % (knowledge, bandwidth, bandwidth, latency, droprate, queuesize)

    process_bar = 95

    os.system(cmd)
    process_bar = 100

    os.system('''/home/lixu/pantheon/src/analysis/analyze.py --data-dir /home/lixu/CCSystem/static''')
    os.system('''pkill -f iperf''')
    context = {}
    context['delay'] = '/static/%s_datalink_delay_run1.png' % (knowledge)
    context['throughput'] = '/static/%s_datalink_throughput_run1.png' % (knowledge)
    context['file'] = '/static/pantheon_report.pdf'
    return render(request, 'showResult.html', context)

def show_progress(request):
    return JsonResponse(process_bar, safe=False)