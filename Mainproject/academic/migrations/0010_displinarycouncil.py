# Generated by Django 3.2.6 on 2021-09-03 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0009_auto_20210903_0958'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisplinaryCouncil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scenario', models.CharField(max_length=100, null=True)),
                ('conclusion', models.CharField(max_length=100, null=True)),
                ('year', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
