from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('system-info/', views.system_info, name='system_info'),
]
