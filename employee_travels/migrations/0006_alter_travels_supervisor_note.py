# Generated by Django 5.1 on 2025-03-03 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_travels', '0005_travels_supervisor_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travels',
            name='supervisor_note',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
