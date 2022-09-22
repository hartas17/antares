"""boilerplate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from api.users.views import activation, reset_password

api_url = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    path(f'{api_url}', include('api.users.urls')),
    path('activate/<uuid:activation_token>/', activation),
    path('reset-password/<int:user_id>/<str:token>/', reset_password),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
