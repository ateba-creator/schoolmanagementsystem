from django.forms import forms,ModelForm
from administration.models import Department,Classroom,Course
from academic.models import Date, ClassCouncil

class AddDepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = [
            'section',
            'studies_type',
            'group_type',
            'name'
        ]

class AddClassroomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = [
            'studies_type',
            'group_type',
            'section',
            'name'
        ]


class AddCourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name','classroom','coeff']


