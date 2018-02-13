"""showme URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from wagtail.admin import urls as wagtail_admin_urls
from wagtail.documents import urls as wagtail_docs_urls
from wagtail.core import urls as wagtail_urls

urlpatterns = [
    # Administration
    path('admin/', admin.site.urls),

    # Api
    path('api/', include('api.urls')),

    # WagTail
    path('cms/',  include(wagtail_admin_urls)),
    path('docs/', include(wagtail_docs_urls)),
    path('',      include(wagtail_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)