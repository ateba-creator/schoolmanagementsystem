# Generated by Django 3.2.6 on 2021-09-05 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0022_auto_20210905_0451'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='avg2',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='max2',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='min2',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, max_length=4, null=True),
        ),
    ]