# Generated by Django 3.2.6 on 2021-09-03 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0012_auto_20210903_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absenthours',
            name='hr_exclusions',
            field=models.CharField(default=0, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='absenthours',
            name='jr_exclusions',
            field=models.CharField(default=0, max_length=100, null=True),
        ),
    ]
