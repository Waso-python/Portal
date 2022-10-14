from django.urls import path
from . import views

urlpatterns = [
    path('registration/', views.RegistrationPortal.as_view(),
         name='registration'),
    path('login/', views.LoginPortal.as_view(), name='login'),
    path('log_out/', views.LogoutPortal.as_view(), name='logout'),
]
