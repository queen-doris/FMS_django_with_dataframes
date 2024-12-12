from django.db import models
# from drivers.models import Driver

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    license_plate = models.CharField(max_length=7)
    vehicle_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta: 
        db_table = 'vehicles_table'

    def __str__(self):
        return self.name
