from django.urls import path
from . import views

urlpatterns = [
    path('', views.maintenance_list, name='maintenance_list'),
    path('create/', views.maintenance_create, name='maintenance_create'),
    path('<int:pk>/update/', views.maintenance_update, name='maintenance_update'),
    path('<int:pk>/delete/', views.maintenance_delete, name='maintenance_delete'),
    path('<int:pk>/', views.maintenance_detail, name='maintenance_detail'),
]
