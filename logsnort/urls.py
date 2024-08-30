from django.urls import path
from . import views

urlpatterns = [
    path('/', views.logsnort_view, name='logsnort'),
    path('/call_logsnort', views.call_logsnort, name='call_logsnort'),
]
