# Generated by Django 5.1 on 2025-03-10 09:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0011_alter_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
