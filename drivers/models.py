from django.db import models

class Driver(models.Model):
    name = models.CharField(max_length=100)
    license_number = models.BigIntegerField()
    hired_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.name
