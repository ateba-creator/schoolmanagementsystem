# Generated by Django 3.2.6 on 2021-09-04 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academic', '0014_semesterreportcard'),
        ('student', '0010_auto_20210831_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='semester_reportcard',
            field=models.ManyToManyField(blank=True, to='academic.SemesterReportCard'),
        ),
    ]