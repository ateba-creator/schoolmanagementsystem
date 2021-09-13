from student.models import Student
from accounts.models import Teacher
from academic.models import Result
from django.contrib.auth.forms import UserCreationForm
from django.forms import  ModelForm

class AddStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = [
            'place_of_birth',
            'nationality',
            'religion',
            'gender',
            'photo',
            'phone_no',
            'parent',
            'status',
            'matricule',
            'mother_name',
            'father_name',
            'school_of_origin',
            'department',
            'locality'
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['matricule'].widget.attrs['placeholder'] = '006hz09123'
        self.fields['school_of_origin'].widget.attrs['placeholder'] = 'LYCEE TECHNIQUE DE BAFIA'