# Generated by Django 5.1 on 2025-02-26 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0006_user_otp_user_otp_expiry'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='reset_otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='reset_otp_expiry',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
