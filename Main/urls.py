"""Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_200_OK, HTTP_400_BAD_REQUEST



def home(request):
    return render(request, 'index.html')

@api_view(['GET'])
def CheckConnection(request):
    return Response('The server is reachable!', HTTP_200_OK)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('Filter/', include('Filter.urls')),
    path('Crawler/', include('Crawler.urls')),
    path('CheckConnection', CheckConnection),
    path('', home, name='home'),
]
