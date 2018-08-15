from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='info'),
    path('error/', views.info_Error, name='info_error'),
    path('doing/', views.info_Doing, name='info_doing'),
]