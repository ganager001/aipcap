from django.urls import path
from . import views

urlpatterns = [
    path('/', views.detect_view, name='detect'),
    path('/detect-data', views.detect_filter, name='detect_filter'),
]
