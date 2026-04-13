from django.urls import path
from . import portal_views

app_name = 'portal'

urlpatterns = [
    path('', portal_views.portal_dashboard, name='dashboard'),
    path('application/<int:pk>/', portal_views.portal_app_detail, name='portal_app_detail'),
]
