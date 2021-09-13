# Generated by Django 3.2.6 on 2021-08-29 06:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_classroom_course_department'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('academic', '0002_generalsequence_report_card_result_sequence_teachersequence'),
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='academic_year',
        ),
        migrations.RemoveField(
            model_name='student',
            name='parent_address',
        ),
        migrations.RemoveField(
            model_name='student',
            name='parent_name',
        ),
        migrations.AddField(
            model_name='student',
            name='course',
            field=models.ManyToManyField(to='administration.Course'),
        ),
        migrations.AddField(
            model_name='student',
            name='fee',
            field=models.ManyToManyField(to='administration.Fee'),
        ),
        migrations.AddField(
            model_name='student',
            name='report_card',
            field=models.ManyToManyField(blank=True, to='academic.Report_card'),
        ),
        migrations.AlterField(
            model_name='student',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_no',
            field=models.CharField(max_length=11),
        ),
    ]