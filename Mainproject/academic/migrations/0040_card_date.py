# Generated by Django 3.2.6 on 2021-09-09 00:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0039_card'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='date',
            field=models.DateTimeField(auto_created=True, null=True),
        ),
    ]