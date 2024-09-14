from django.shortcuts import render, redirect
import psutil
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
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

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Đổi 'home' thành trang bạn muốn chuyển đến sau khi đăng nhập
        else:
            messages.error(request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')