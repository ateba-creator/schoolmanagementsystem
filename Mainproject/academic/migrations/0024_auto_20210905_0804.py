# Generated by Django 3.2.6 on 2021-09-05 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0023_auto_20210905_0647'),
    ]

    operations = [
        migrations.AddField(
            model_name='report_card',
            name='average',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='report_card',
            name='average2',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
