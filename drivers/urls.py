from django.urls import path
from . import views

urlpatterns = [
    path('', views.driver_list, name='driver_list'), 
    path('<int:driver_id>/', views.driver_detail, name='driver_detail'),
    path('create/', views.driver_create, name='driver_create'),
    path('<int:driver_id>/update/', views.driver_update, name='driver_update'),
    path('<int:driver_id>/delete/', views.driver_delete, name='driver_delete'),
]
