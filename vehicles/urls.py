from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_vehicle, name='create_vehicle'),
    path('', views.vehicle_list, name='vehicle_list'),
    path('update/<int:pk>/', views.update_vehicle, name='update_vehicle'),
    path('delete/<int:pk>/', views.delete_vehicle, name='delete_vehicle'),
]
