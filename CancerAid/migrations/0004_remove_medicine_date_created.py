# Generated by Django 3.2.6 on 2021-12-22 14:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CancerAid', '0003_auto_20211221_0030'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='date_created',
        ),
    ]
