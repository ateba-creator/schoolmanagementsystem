from django.db import models
# Create your models here.

class Date(models.Model):
    name = models.CharField(max_length=200, null=True)
    date = models.CharField(max_length=100, null=True)

class Sequence(models.Model):
    sequence_choice = (
        ('1 ere Sequence', '1 ere Sequence'),
        ('2 eme Sequence', '2 eme Sequence'),
        ('3 eme Sequence', '3 eme Sequence'),
        ('4 eme Sequence', '4 eme Sequence'),
        ('5 eme Sequence', '5 eme Sequence'),
        ('6 eme Sequence', '6 eme Sequence'),
    )
    course = models.ForeignKey('administration.Course', on_delete=models.CASCADE, blank=True, null=True)
    sequence= models.CharField(max_length=100, null=True, blank=True,choices=sequence_choice)
    result_status = models.BooleanField(default=False,null=True)

class GeneralSequence(models.Model):
    sequence = models.CharField(max_length=100, null=True)
    academic_year = models.CharField(max_length=100, null=True)
    classroom = models.ForeignKey('administration.Classroom', on_delete=models.CASCADE, null=True)

class TeacherSequence(models.Model):
    academic_year = models.CharField(max_length=50, blank=True, null=True)
    sequence = models.CharField(max_length=100, null=True, blank=True)
    course = models.ForeignKey('administration.Course', on_delete=models.CASCADE, blank=True,null=True)
    course_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.course.name} {self.sequence} {self.academic_year}'

class Result(models.Model):
    academic_year_choice = (
        ('2021/2022', '2021/2022'),
        ('2022/2023', '2022/2023'),
        ('2023/2024', '2023/2024'),
        ('2024/2025', '2024/2025'),
        ('2025/2026', '2025/2026')
    )
    academic_year = models.CharField(max_length=50, blank=True, null=True, choices=academic_year_choice)
    sequence = models.CharField(max_length=100,blank=True,null=True)
    sequence2 = models.CharField(max_length=100, blank=True, null=True)
    course = models.ForeignKey('administration.Course', on_delete=models.CASCADE, blank=True, null=True)
    mark = models.DecimalField(max_length=4,max_digits=4,decimal_places=2,null=True,blank=True ,default=0)
    mark2 = models.DecimalField(max_length=4, max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    average_mark = models.DecimalField(max_length=4, max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    rank = models.IntegerField(blank=True, null=True)
    rank2 = models.IntegerField(blank=True, null=True)

    min = models.DecimalField(max_length=4, max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    max = models.DecimalField(max_length=4, max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    avg = models.DecimalField(max_length=4, max_digits=4, decimal_places=2, null=True, blank=True, default=0)

    min2 = models.DecimalField(max_length=4, max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    max2 = models.DecimalField(max_length=4, max_digits=4, decimal_places=2, null=True, blank=True, default=0)
    avg2 = models.DecimalField(max_length=4, max_digits=4, decimal_places=2, null=True, blank=True, default=0)

    total = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)
    total2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    average = models.DecimalField(max_digits=10,decimal_places=2, null=True, blank=True)
    average2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    student = models.ForeignKey('student.Student',on_delete=models.CASCADE, blank=True, null=True)
    student_name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return f'{self.course.name} {self.course.classroom.name} {self.sequence} {self.academic_year}'

class Report_card(models.Model):
    average = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    average2 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sem_average = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    sequence = models.CharField(max_length=100, null=True)
    academic_year = models.CharField(max_length=100, null=True)
    results = models.ManyToManyField('academic.Result',blank=True)
    student_name = models.CharField(max_length=100, null=True)
    classroom = models.ForeignKey('administration.Classroom', on_delete=models.CASCADE, null=True)

    first_average = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    last_average = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    class_average = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    rank = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


class Remark(models.Model):
    year = models.CharField(max_length=100, null=True)
    remark = models.TextField(null=True)

class AbsentHours(models.Model):
    year = models.CharField(max_length=100, null=True)
    sequence = models.CharField(max_length=100, null=True)
    hours_no = models.IntegerField(null=True, default=0)
    consignes = models.CharField(max_length=100, null=True)
    hr_exclusions = models.CharField(max_length=100, null=True, default=0)
    jr_exclusions = models.CharField(max_length=100, null=True, default=0)
    def_exclusion = models.BooleanField(default=False, null=True)
    convocation = models.BooleanField(default=False, null=True)

class GeneralAbsentHours(models.Model):
    year = models.CharField(max_length=50, blank=True, null=True)
    sequence = models.CharField(max_length=100, null=True, blank=True)
    classroom = models.ForeignKey('administration.Classroom', on_delete=models.CASCADE, blank=True, null=True)

class DisciplinaryCouncil(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    hours = models.IntegerField(null=True, blank=True)
    hours2 = models.IntegerField(null=True, blank=True)
    conclusion = models.CharField(max_length=100, null=True)

class ExclusionHours(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    ex_hours = models.DecimalField(max_digits=4, null=True, decimal_places=2)
    hours = models.IntegerField(null=True, blank=True)
    hours2 = models.IntegerField(null=True, blank=True)

class ExclusionDays(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    ex_days = models.DecimalField(max_digits=4, null=True, decimal_places=2)
    hours = models.IntegerField(null=True, blank=True)
    hours2 = models.IntegerField(null=True, blank=True)

class ClassCouncil(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    average = models.DecimalField(max_digits=4, null=True,decimal_places=2)
    average2 = models.DecimalField(max_digits=4, null=True, decimal_places=2)
    hours = models.IntegerField(null=True, blank=True)
    hours2 = models.IntegerField(null=True, blank=True)
    conclusion = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.name}'

class Card(models.Model):
    first_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    year = models.CharField(null=True, blank=True, max_length=100)
    date_of_birth = models.CharField(null=True, blank=True, max_length=100)
    place_of_birth = models.CharField(null=True, blank=True, max_length=100)
    father_name = models.CharField(null=True, blank=True, max_length=100)
    mother_name = models.CharField(null=True, blank=True, max_length=100)
    department = models.CharField(null=True, blank=True, max_length=100)
    locality = models.CharField(null=True, blank=True, max_length=100)
    nationality = models.CharField(max_length=100, null=True)
    parent_address = models.CharField(max_length=100, null=True)
    classroom = models.CharField(max_length=100, null=True)
    matricule = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_created=True, null=True)


class HonorRoll(models.Model):
    first_name = models.CharField(null=True, blank=True, max_length=100)
    last_name = models.CharField(null=True, blank=True, max_length=100)
    year = models.CharField(null=True, blank=True, max_length=100)
    date_of_birth = models.CharField(null=True, blank=True, max_length=100)
    place_of_birth = models.CharField(null=True, blank=True, max_length=100)
    average = models.CharField(null=True, blank=True, max_length=100)
    class_average = models.CharField(null=True, blank=True, max_length=100)
    rank = models.CharField(max_length=100, null=True)
    encouragement = models.BooleanField(null=True, default=False)
    congrats = models.BooleanField(null=True, default=False)
    sequence = models.CharField(max_length=100, null=True)
    classroom = models.CharField(max_length=100, null=True)
    main_teacher = models.CharField(max_length=100, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)
    stud_no = models.CharField(max_length=20, null=True)