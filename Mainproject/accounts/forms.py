from accounts.models import Teacher
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
class AddTeacherForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = [
            'first_name',
            'email',
            'nationality',
            'religion',
            'gender',
            'marital_status',
            'phone_no',
            'address',
            'date_of_birth',
            'place_of_birth',
            'photo'
        ]

class AddcollegueForm(UserCreationForm):
    class Meta:
        model = Teacher
        fields = [
            'first_name',
            'email',
            'nationality',
            'religion',
            'gender',
            'marital_status',
            'phone_no',
            'address',
            'photo',
            'phone_no'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['value'] = '00000000'
        self.fields['password2'].widget.attrs['value'] = '00000000'

class CustomUserChangeForm(UserChangeForm):
          class Meta:
            model = Teacher
            fields = [
                'email',
                ]


