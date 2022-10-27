# Generated by Django 4.2.dev20221019003145 on 2022-10-27 03:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rhoel_unofficial_project', '0002_delete_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rhoel_unofficial_project.department')),
            ],
        ),
    ]
