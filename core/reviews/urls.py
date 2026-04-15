from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('submit/<int:application_id>/', views.submit_review, name='submit_review'),
    path('company/<int:company_id>/', views.company_reviews, name='company_reviews'),
]
