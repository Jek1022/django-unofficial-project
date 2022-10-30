from django.db import models
from users.modules.department.models import Department
 
class Employee(models.Model):
    class Meta:
        db_table = 'employees'

    department = models.ForeignKey(Department, related_name='employees', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    employed_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)