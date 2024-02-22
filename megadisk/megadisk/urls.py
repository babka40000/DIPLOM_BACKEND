"""
URL configuration for megadisk project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static
from django.conf import settings

from app.views import home_view, FilesAndFoldersViewSet, auth_login_view, auth_getcurrenuser_view, auth_logout_view, \
                      auth_register_view, AdminOperationsViewSet

urlpatterns = [
    path('api/v1/auth/login/', auth_login_view, name='login'),
    path('api/v1/auth/logout/', auth_logout_view, name='logout'),
    path('api/v1/auth/register/', auth_register_view, name='register'),
    path('api/v1/auth/getcurrentuser/', auth_getcurrenuser_view, name='getcurrenuser'),
]

router = DefaultRouter()
router.register('api/v1/filesandfolders', FilesAndFoldersViewSet)
router.register('api/v1/adminoperations', AdminOperationsViewSet)


urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
