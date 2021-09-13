# Generated by Django 3.2.6 on 2021-09-05 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0021_auto_20210905_0428'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='avg',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='max',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='min',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, max_length=4, null=True),
        ),
    ]
