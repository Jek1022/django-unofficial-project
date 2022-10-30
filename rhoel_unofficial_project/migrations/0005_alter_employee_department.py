# Generated by Django 4.1.2 on 2022-10-30 04:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rhoel_unofficial_project', '0004_rename_department_id_employee_department'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='rhoel_unofficial_project.department'),
        ),
    ]
