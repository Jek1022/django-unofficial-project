from django.db import models

class Department(models.Model):
    name = models.CharField(unique=True, max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'departments'
        permissions = (
            ('search_department', 'Can search department'),
            ('print_department', 'Can print department'),
            ('export_department', 'Can export department')
        )