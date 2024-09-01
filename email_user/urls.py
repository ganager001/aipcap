from django.urls import path
from . import views

urlpatterns = [
    path('', views.emailUser_view, name='emailUser'),
    path('/save_email', views.save_email, name='save_email'),
]
