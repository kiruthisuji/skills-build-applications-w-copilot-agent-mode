"""octofit_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from octofit_tracker.views import api_root as original_api_root

@api_view(['GET'])
def api_root(request, format=None):
    codespace_name = os.environ.get('CODESPACE_NAME')
    if codespace_name:
        base_url = f"https://{codespace_name}-8000.app.github.dev"
    else:
        base_url = request.build_absolute_uri('/')[:-1]
    original_response = original_api_root(request, format=format)
    data = {}
    for key, value in original_response.data.items():
        if value.startswith('http'):
            idx = value.find('/api/')
            if idx != -1:
                data[key] = f"{base_url}{value[idx:]}"
            else:
                data[key] = value
        else:
            data[key] = value
    return Response(data)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('', include('octofit_tracker.urls')),
]
