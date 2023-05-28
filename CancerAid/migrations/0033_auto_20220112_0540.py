# Generated by Django 3.2.6 on 2022-01-11 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CancerAid', '0032_alter_bkashpayment_medicine_name_and_quentity'),
    ]

    operations = [
        migrations.AddField(
            model_name='ord',
            name='status',
            field=models.CharField(choices=[('paid', 'paid'), ('unpaid', 'unpaid')], max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bkashpayment',
            name='address',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
