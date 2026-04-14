from django.urls import path
from . import views

app_name = 'university_admin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('moas/', views.moa_requests_list, name='moa_list'),
    path('moas/<int:pk>/', views.manage_moa_request, name='manage_moa'),
    path('export/moas/', views.export_moas_csv, name='export_moas'),
    path('applications/', views.applications_list, name='app_list'),
    path('applications/<int:pk>/', views.manage_application, name='manage_app'),
    path('applications/<int:pk>/endorsement/', views.download_endorsement_letter, name='download_endorsement'),
    path('export/applications/', views.export_applications_csv, name='export_applications'),
    path('evaluations/', views.evaluations_list, name='evaluations_list'),
    path('evaluations/<int:pk>/', views.evaluation_detail, name='evaluation_detail'),
    path('roles/', views.manage_roles, name='manage_roles'),
    path('roles/edit/<int:user_id>/', views.edit_user_role, name='edit_user_role'),
]
