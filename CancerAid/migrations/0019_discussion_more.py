# Generated by Django 3.2.6 on 2022-01-04 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CancerAid', '0018_bkashpayment'),
    ]

    operations = [
        migrations.AddField(
            model_name='discussion',
            name='more',
            field=models.TextField(blank=True, null=True),
        ),
    ]
