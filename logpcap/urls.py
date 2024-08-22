from django.urls import path
from . import views

urlpatterns = [
    path('/', views.logpcap_view, name='logpcap'),
    path('/load-data', views.logpcap_filter, name='logpcap_filter'),
]
