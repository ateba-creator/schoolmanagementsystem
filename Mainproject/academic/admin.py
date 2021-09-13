from django.contrib import admin
from academic.models import Date,Result,TeacherSequence,GeneralSequence,Report_card,AbsentHours,GeneralAbsentHours, ClassCouncil,Card,HonorRoll
# Register your models here.


admin.site.register([Date,Result,TeacherSequence,GeneralSequence,Report_card, AbsentHours, GeneralAbsentHours,ClassCouncil,Card,HonorRoll])