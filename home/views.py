from django.shortcuts import render
import psutil
from django.http import JsonResponse


def home_view(request):
    context = {
        'title': 'Home Page',
        'content': 'Welcome to the Home Page',
    }
    return render(request, 'home/index.html', context)


def system_info(request):
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    data = {
        'cpu_percent': float(cpu_percent),
        'memory_used': float(memory.percent),
        'disk_used': float(disk.percent),
    }
    return JsonResponse(data)