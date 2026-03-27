from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/<int:company_id>/', views.apply_to_company, name='apply'),
]