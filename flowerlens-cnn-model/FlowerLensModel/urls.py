"""
URL configuration for FlowerLensModel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from .views import pipe_filter


urlpatterns = [
    path("admin/", admin.site.urls),
    #so when a request gets sent to http://127.0.0.1:8000/predict, call the pipe_filter function, idk what name='predict' is
    path('predict/', pipe_filter, name='predict'),
    path('trainModel/', pipe_filter, name='trainModel'),

]
