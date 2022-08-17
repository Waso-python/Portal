from django.urls import path
from . import views

urlpatterns = [
    path('', views.FullBase.as_view(), name='base'),
    path('interesting/', views.InterestingBase.as_view(), name='interesting'),
    path('recomend/', views.RecomendBase.as_view(), name='recomend'),
    path('completed/', views.OldBase.as_view(), name='completed'),
    path('add/', views.InterestingBase.add_Interesting, name='add_int'),
    path('procedure/<str:proc_num>', views.ProcedureView.as_view(), name='procedure'),
    path('create_procedure/', views.CreateProcedure.as_view(), name='create_proc')
]
