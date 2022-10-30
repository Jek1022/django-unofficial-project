from django.db import models

class Department(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'departments'