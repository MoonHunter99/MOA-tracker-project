from django.urls import path
from . import views

app_name = 'applications'

urlpatterns = [
    path('apply/<int:company_id>/', views.apply_to_company, name='apply'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
]