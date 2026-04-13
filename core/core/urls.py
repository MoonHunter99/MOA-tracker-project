"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# Import settings and static to allow serving uploaded media files during local development
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin Interface
    path('admin/', admin.site.urls),
    
    # Custom University Admin Portal (Protected)
    path('dashboard/admin/', include('university_admin.urls', namespace='university_admin')),
    
    # Partner Portal
    path('partner-portal/', include('companies.portal_urls', namespace='portal')),

    # Apps
    path('', include('companies.urls')),
    path('applications/', include('applications.urls')),
    path('accounts/', include('accounts.urls')),
    path('moas/', include('moas.urls')),
]

# Only serve media files this way during local development. In production, a web server like Nginx handles this.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
