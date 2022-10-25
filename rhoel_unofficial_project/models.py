from django.db import models

class Department(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()

class Employee(models.Model):
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)