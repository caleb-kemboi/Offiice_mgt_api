# Generated by Django 5.1 on 2025-02-28 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_travels', '0002_employee_date_created_employee_date_updated_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='date_updated',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='name',
        ),
        migrations.AlterField(
            model_name='employee',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
