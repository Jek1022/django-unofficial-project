# Generated by Django 4.2.dev20221019003145 on 2022-11-02 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('department', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('position', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('employed_at', models.DateTimeField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='department.department')),
            ],
            options={
                'db_table': 'employees',
                'permissions': (('search_employee', 'Can search employee'), ('print_employee', 'Can print employee'), ('export_employee', 'Can export employee')),
            },
        ),
    ]
