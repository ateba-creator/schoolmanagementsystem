# Generated by Django 3.2.6 on 2021-09-05 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0025_classcouncil'),
    ]

    operations = [
        migrations.AddField(
            model_name='classcouncil',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]