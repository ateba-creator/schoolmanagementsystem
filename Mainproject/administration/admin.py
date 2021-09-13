from django.contrib import admin
from administration.models import Course, Classroom, Department, Fee
# Register your models here.

admin.site.register([Course, Classroom, Department, Fee])