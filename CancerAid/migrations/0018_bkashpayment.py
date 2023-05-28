# Generated by Django 3.2.6 on 2022-01-02 01:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CancerAid', '0017_ord_posting_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='BkashPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bkashNumber', models.CharField(max_length=20)),
                ('bkashTransaction', models.CharField(max_length=512)),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
    ]
