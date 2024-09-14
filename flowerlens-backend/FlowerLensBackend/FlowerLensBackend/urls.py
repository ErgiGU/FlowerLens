"""
URL configuration for FlowerLensBackend project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve
from FlowerLensBackendComponent.views import LoginView, pipe_filter_user, home, pipe_filter_admin, cnn_model_pipefilter

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    
    # User urls
    path('uploadPhoto/', pipe_filter_user, name='uploadPhoto'),
    
    # CNN urls
    path('modelRequest/', cnn_model_pipefilter, name='modelRequest'),
    path('trainedModel/', cnn_model_pipefilter, name='trainedModel'),
    
    # Admin urls
    path('evaluateModel/', pipe_filter_admin, name='evaluateModel'),
    path('trainModel/', pipe_filter_admin, name='trainModel'),
    path('deployModel/', pipe_filter_admin, name='deployModel'),
    path('api/login/', LoginView.as_view(), name='api_login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        # This is for development purposes. We should look into serving images through web server when we deploy the application
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
