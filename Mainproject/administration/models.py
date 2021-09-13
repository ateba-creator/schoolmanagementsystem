from django.db import models
from accounts.models import Teacher
from student.models import Student
from django.conf import settings
# Create your models here.

class Fee(models.Model):
    academic_year_choice = (
        ('2021/2022', '2021/2022'),
        ('2022/2023', '2022/2023'),
        ('2023/2024', '2023/2024'),
        ('2024/2025', '2024/2025'),
        ('2025/2026', '2025/2026')
    )
    year = models.CharField(max_length=100,choices=academic_year_choice,default='2021/2022')
    paid_fee = models.BooleanField(default=False,null=True)

class Department(models.Model):
    section_choice=(
        ('anglophone', 'anglophone'),
        ('francophone', 'francophone')
    )
    studies_choice=(
        ('Generale', 'Generale'),
        ('Technique', 'Technique')
    )
    group_choice = (
        ('science', 'science'),
        ('literaire', 'literaire'),
        ('mechanique', 'mechanique'),
        ('maconerie', 'maconerie'),
        ('generale', 'generale')
    )
    section = models.CharField(max_length=100,choices=section_choice, null=False)
    studies_type = models.CharField(max_length=100,choices=studies_choice, null=False)
    group_type = models.CharField(max_length=100, choices=group_choice, null=False)
    name = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name

class Classroom(models.Model):
    section_choice = (
        ('anglophone', 'anglophone'),
        ('francophone', 'francophone')
    )
    studies_choice = (
        ('Generale', 'Generale'),
        ('Technique', 'Technique')
    )
    group_choice = (
        ('science', 'science'),
        ('literaire', 'literaire'),
        ('bilingue', 'bilingue'),
        ('mechanique', 'mechanique'),
        ('maconerie', 'maconerie'),
        ('generale', 'generale')
    )
    studies_type = models.CharField(max_length=100, choices=studies_choice)
    group_type = models.CharField(max_length=100, choices=group_choice)
    section = models.CharField(max_length=100, choices=section_choice)
    name = models.CharField(max_length=100, null=True)
    students = models.ManyToManyField(Student, blank=True)
    main_teacher = models.ForeignKey('accounts.Teacher', null=True, blank=True, on_delete=models.CASCADE)
    room = models.ForeignKey('time_table.Room', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    department = models.ManyToManyField("administration.Department")
    name = models.CharField(max_length=100)
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE,null=True,blank=True)
    classroom = models.ForeignKey('administration.Classroom' , on_delete=models.CASCADE)
    coeff = models.PositiveIntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.name