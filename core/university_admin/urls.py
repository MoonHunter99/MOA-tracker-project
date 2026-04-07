from django.urls import path
from . import views

app_name = 'university_admin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('moas/', views.moa_requests_list, name='moa_list'),
    path('moas/<int:pk>/', views.manage_moa_request, name='manage_moa'),
    path('applications/', views.applications_list, name='app_list'),
    path('applications/<int:pk>/', views.manage_application, name='manage_app'),
]
