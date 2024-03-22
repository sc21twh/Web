"""
URL configuration for sc21twh_cwk1 project.

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
from newsAggregator.views import handleDeleteStoryRequest, handleGetStoryRequest, handleLoginRequest, handleLogoutRequest, handlePostStoryRequest

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', handleLoginRequest, name='login'),
    path('api/logout', handleLogoutRequest, name='logout'),
    path('api/stories', handlePostStoryRequest),
    path('api/stories/', handleGetStoryRequest),
    path('api/stories/<str:key>', handleDeleteStoryRequest)
]
