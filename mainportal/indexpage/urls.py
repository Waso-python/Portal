from django.urls import path
from . import views

app_name = 'indexpage'
urlpatterns = [
    path('', views.IndexPageView.as_view()),
    path('updatebase', views.UpdateBase.as_view()),
    path('test', views.Test.as_view()),
]
