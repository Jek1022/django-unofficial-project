# Generated by Django 4.2.dev20221019003145 on 2022-11-08 06:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='created_at',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='department',
            name='updated_at',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
