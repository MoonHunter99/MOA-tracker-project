from django.urls import path
from . import views

app_name = 'moas'

urlpatterns = [
    path('request-moa/', views.request_moa, name='request_moa'),
    path('my-requests/', views.my_moa_requests, name='my_moa_requests'),
]