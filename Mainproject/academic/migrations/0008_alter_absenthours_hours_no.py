# Generated by Django 3.2.6 on 2021-09-03 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0007_rename_academic_year_generalabsenthours_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='absenthours',
            name='hours_no',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
