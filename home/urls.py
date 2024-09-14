from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home_view, name='home'),
    path('system-info/', views.system_info, name='system_info'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
