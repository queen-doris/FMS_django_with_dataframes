from django.contrib import admin
from django.urls import path, include
from authapp import views




urlpatterns = [
    path('', views.landing, name='landing'),
    path('home/', views.home, name='home'),
    path('vehicles/', include('vehicles.urls')),
    path('drivers/', include('drivers.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('authapp/', include('authapp.urls')),
]
