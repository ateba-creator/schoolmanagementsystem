# Generated by Django 3.2.6 on 2021-09-08 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0038_auto_20210908_0815'),
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True)),
                ('last_name', models.CharField(blank=True, max_length=100, null=True)),
                ('year', models.CharField(blank=True, max_length=100, null=True)),
                ('date_of_birth', models.CharField(blank=True, max_length=100, null=True)),
                ('place_of_birth', models.CharField(blank=True, max_length=100, null=True)),
                ('father_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mother_name', models.CharField(blank=True, max_length=100, null=True)),
                ('department', models.CharField(blank=True, max_length=100, null=True)),
                ('locality', models.CharField(blank=True, max_length=100, null=True)),
                ('nationality', models.CharField(max_length=100, null=True)),
                ('parent_address', models.CharField(max_length=100, null=True)),
                ('classroom', models.CharField(max_length=100, null=True)),
                ('matricule', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
