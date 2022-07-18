from django.urls import path
from . import views

# app_name = 'indexpage'
urlpatterns = [
    path('', views.IndexPageView.as_view(), name='indexpage'),
    path('updatebase', views.UpdateBase.as_view(), name='updatebase'),
    path('test/', views.PublisherListView.as_view(), name='test'),
]
