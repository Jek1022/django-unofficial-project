from django.db import models

class Department(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

class Employee(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)