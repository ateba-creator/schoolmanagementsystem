from django.shortcuts import render,redirect
from student.models import Student
from administration.models import Classroom,Fee,Course
from accounts.models import Teacher
from django.views.generic import DetailView
from academic.models import Date,Result,GeneralSequence


def my_children(request):
    all_students = Student.objects.all()
    all_classes = Classroom.objects.all()
    dates = Date.objects.all()
    students = []
    for student in all_students:
        if student.parent == request.user:
            students.append(student)
    stud_num = len(students)

    context={
        'students':students,
        'stud_num':stud_num,
        'all_classes':all_classes,
        'dates':dates
    }
    return render(request,'parent/my_children.html',context)

def children_detail(request):
    student_id = request.GET.get('student_id')
    class_id = request.GET.get('class_id')
    student = Student.objects.get(id=student_id)
    classroom = Classroom.objects.get(id=class_id)
    dates = Date.objects.all()
    courses = []

    context={
        'student':student,
        'classroom':classroom,
        'dates':dates,
    }
    return render(request,'parent/children_detail.html',context)

def results_home(request):
    all_students = Student.objects.all()
    all_classes = Classroom.objects.all()
    dates = Date.objects.all()
    students = []
    for student in all_students:
        if student.parent == request.user:
            students.append(student)
    results = []
    all_results = Result.objects.all()
    for result in all_results:
        for student in students:
            if result.student == student:
                results.append(result)

    context = {
        'students': students,
        'dates': dates,
        'results':results,
        'all_classes':all_classes
    }
    return render(request,'parent/results_home.html',context)

def student_results(request):
    dates = Date.objects.all()
    student_id = request.GET.get('student_id')
    class_id = request.GET.get('class_id')
    student = Student.objects.get(id=student_id)
    classroom = Classroom.objects.get(id=class_id)
    courses = []
    all_courses = Course.objects.all()
    for course in all_courses:
        if course.classroom == classroom:
            courses.append(course)
    all_results = Result.objects.all()

    results = []
    for result in all_results:
        if result.student == student:
            results.append(result)
    print(results)
    context = {
        'student': student,
        'dates': dates,
        'classroom':classroom,
        'courses':courses,
        'results':results
    }
    return render(request,'parent/student_results.html',context)


def course_mark_detail(request):
    student_id = request.GET.get('student_id')
    class_id = request.GET.get('class_id')
    course_id = request.GET.get('course_id')
    dates = Date.objects.all()
    course = Course.objects.get(id=course_id)
    student = Student.objects.get(id=student_id)
    classroom = Classroom.objects.get(id=class_id)
    context={
        'student':student,
        'classroom':classroom,
        'course':course,
        'dates':dates
    }
    return render(request,'parent/course_mark_detail.html',context)

def children_report_card(request):
    dates = Date.objects.all()
    students = []
    all_students = Student.objects.all()
    for student in all_students:
        if student.parent == request.user:
            students.append(student)
    results = []
    context = {
        'students': students,
        'dates': dates,
    }
    return render(request,'parent/children_report_card.html',context)

def contact_teacher(request):
    all_teachers = Teacher.objects.all()
    students = []
    for student in Student.objects.all():
        if student.parent == request.user:
            students.append(student)
    courses = []
    for student in students:
        for course in student.course.all():
            courses.append(course)
    context = {
        'courses':courses
    }
    return render(request,'parent/contact_teacher.html',context)

def report_card_home(request):
    student_id = request.GET.get('student_id')
    student = Student.objects.get(id=student_id)

    context = {
        'student':student,
    }

    return render(request, 'parent/report_card_home.html',context)