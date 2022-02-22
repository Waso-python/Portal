from django.urls import path
from . import views

app_name = 'indexpage'
urlpatterns = [
    path('', views.IndexPageView.as_view()),
]
