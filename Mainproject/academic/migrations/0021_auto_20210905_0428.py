# Generated by Django 3.2.6 on 2021-09-05 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0020_auto_20210905_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='average_mark',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=4, max_length=4, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='rank2',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]