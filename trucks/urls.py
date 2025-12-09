from django.urls import path
from . import views

app_name = 'trucks'

urlpatterns = [
    path('', views.truck_list, name='list'),
    path('drivers/', views.driver_list, name='driver_list'),
    path('drivers/<int:pk>/', views.driver_detail, name='driver_detail'),
    path('<slug:slug>/', views.truck_detail, name='detail'),
]