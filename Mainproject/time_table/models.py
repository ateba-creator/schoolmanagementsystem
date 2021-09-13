from django.db import models
import random as rnd
from django.db import models
import math
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save, post_delete
from datetime import timedelta, date
from accounts.models import Teacher
from administration.models import Course, Department, Classroom

time_slots = (
    ('9:30 - 10:30', '9:30 - 10:30'),
    ('10:30 - 11:30', '10:30 - 11:30'),
    ('11:30 - 12:30', '11:30 - 12:30'),
    ('12:30 - 1:30', '12:30 - 1:30'),
    ('2:30 - 3:30', '2:30 - 3:30'),
    ('3:30 - 4:30', '3:30 - 4:30'),
    ('4:30 - 5:30', '4:30 - 5:30'),
)
DAYS_OF_WEEK = (
    ('Lundi', 'Lundi'),
    ('Mardi', 'Mardi'),
    ('Mercredi', 'Mercredi'),
    ('Jeudi', 'Jeudi'),
    ('Vendredi', 'Vendredi'),
    ('Samedi', 'Samedi'),
)

POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1


class Room(models.Model):
    r_number = models.CharField(max_length=6)
    room_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.room_name


class MeetingTime(models.Model):
    time = models.CharField(max_length=50, choices=time_slots, default='11:30 - 12:30')
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)

    def __str__(self):
        return f'{self.id} {self.day} {self.time}'


class Lecture(models.Model):
    num_class_in_week = models.IntegerField(default=0)
    department = models.ForeignKey('administration.Department', on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True)
    classroom = models.ForeignKey('administration.Classroom', on_delete=models.CASCADE, null=True ,blank=True)

    meeting_time = models.ForeignKey(MeetingTime, on_delete=models.CASCADE, blank=True, null=True)
    room = models.ForeignKey(Room,on_delete=models.CASCADE, blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, blank=True, null=True)

    def set_room(self, room):
        lecture = Lecture.objects.get(pk = self.lecture.id)
        lecture.room = room
        lecture.save()

    def set_meetingTime(self, meetingTime):
        lecture = Lecture.objects.get(pk = self.lecture.id)
        lecture.meeting_time = meetingTime
        lecture.save()

    def set_teacher(self, teacher):
        lecture = Lecture.objects.get(pk=self.lecture.id)
        lecture.teacher = teacher
        lecture.save()


class Timetable(models.Model):
    class_id = models.CharField(max_length=20)
    course = models.CharField(max_length=100)
    room = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)
    day = models.CharField(max_length=100)
    time = models.CharField(max_length=100)