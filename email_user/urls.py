from django.urls import path
from . import views

urlpatterns = [
    path('', views.emailUser_view, name='emailUser'),
    # path('system-info/', views.system_info, name='system_info'),
]
