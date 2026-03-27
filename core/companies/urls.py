from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.company_list, name='company_list'),
]