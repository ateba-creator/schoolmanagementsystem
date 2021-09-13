from django.contrib import admin
from.models import *

admin.site.register(Room)
admin.site.register(MeetingTime)
admin.site.register([Lecture,Timetable])
