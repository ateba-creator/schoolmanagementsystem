from django.forms import ModelForm
from. models import *
from django import forms
from administration.models import Course

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = [
            'r_number',
        ]

class MeetingTimeForm(ModelForm):
    class Meta:
        model = MeetingTime
        fields = [
            'time',
            'day'
        ]
        widgets = {
            'pid': forms.TextInput(),
            'time': forms.Select(),
            'day': forms.Select(),
        }


#class CourseForm(ModelForm):
#    class Meta:
#        model = Course
#        fields = ['course_number', 'course_name', 'max_numb_students', 'instructors']


#class DepartmentForm(ModelForm):
#    class Meta:
#        model = Department
#        fields = ['dept_name', 'courses']


class SectionForm(ModelForm):
    #class Meta:
        #model = Lecture
    pass