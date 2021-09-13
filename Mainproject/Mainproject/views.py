from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Teacher
from student.models import Student
from academic.models import Date
from django.contrib import messages


@login_required(login_url='login')
def home_page(request):
    teachers = Teacher.objects.filter(is_authorized=False)
    counter = teachers.count
    dates = Date.objects.all()

    all_teachers = Teacher.objects.filter(groups__name='enseignant')
    parents = Teacher.objects.filter(groups__name = 'parent' or 'adminparent' or 'intendparent' or 'parentteacher')
    students = []
    all_students = Student.objects.all()
    context = {
        'counter': counter,
        'all_students':all_students,
        'dates':dates,
        'parents':parents,
        'all_teachers':all_teachers
    }
    return render(request, 'home.html',context)

def index(request):
    return render(request, 'index.html')