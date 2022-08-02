"""mainportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from .celery import app
from .tasks import UpdateBase , upd_base

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth', include('authorization.urls')),
    path('', include('indexpage.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('_debug_/', include(debug_toolbar.urls)),
    ]

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, upd_base.s(), name='ph every 10')

# upd_base.delay()

