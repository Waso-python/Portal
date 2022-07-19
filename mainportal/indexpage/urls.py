from django.urls import path
from . import views

# app_name = 'indexpage'
urlpatterns = [
    path('', views.FullBase.as_view(), name='base'),
    path('interesting/', views.InterestingBase.as_view(), name='interesting'),
    path('works/', views.FullBase.as_view(), name='works'),
    path('completed/', views.FullBase.as_view(), name='completed'),
    path('updatebase', views.UpdateBase.as_view(), name='updatebase'),
    path('add/', views.add_Interesting, name='add_int'),
]
