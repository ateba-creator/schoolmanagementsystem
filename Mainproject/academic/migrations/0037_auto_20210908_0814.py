# Generated by Django 3.2.6 on 2021-09-08 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0036_teachersequence_course_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='absenthours',
            name='convocation',
            field=models.CharField(default=0, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='absenthours',
            name='def_exclusion',
            field=models.CharField(default=0, max_length=100, null=True),
        ),
    ]
