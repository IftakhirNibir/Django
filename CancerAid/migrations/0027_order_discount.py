# Generated by Django 3.2.6 on 2022-01-08 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CancerAid', '0026_bkashpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='discount',
            field=models.CharField(choices=[('You will get 30 percent discount for all services', 'You will get 30 percent discount for all services'), ('You will get 50 percent discount for all services', 'You will get 50 percent discount for all services'), ('You will get 70 percent discount for all services', 'You will get 70 percent discount for all services')], max_length=200, null=True),
        ),
    ]
