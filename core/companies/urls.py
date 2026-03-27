from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('<int:pk>/', views.company_detail, name='company_detail'),
]