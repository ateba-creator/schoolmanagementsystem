# Generated by Django 3.2.6 on 2021-09-09 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0042_rename_honourroll_honorroll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='honorroll',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
