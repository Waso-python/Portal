from django.urls import path
from . import views
from django.views.decorators.cache import cache_page

# app_name = 'indexpage'
urlpatterns = [
    path('', views.FullBase.as_view(), name='base'),
    path('interesting/', views.InterestingBase.as_view(), name='interesting'),
    path('works/', views.FullBase.as_view(), name='works'),
    path('completed/', views.OldBase.as_view(), name='completed'),
    path('add/', views.add_Interesting, name='add_int'),
]
