from django.shortcuts import render, redirect
#from notifications.signals import notify
from administration.models import Department, Classroom, Course
from accounts.models import Teacher
from academic.models import Result, TeacherSequence,GeneralSequence,Date,DisciplinaryCouncil, AbsentHours,\
    Report_card, ClassCouncil,ExclusionDays, ExclusionHours, HonorRoll
from django.http import HttpResponse
from student.models import Student
from django.contrib.auth.models import Group
from Mainproject.utils import render_to_pdf
from django.views.generic import DetailView, ListView
from django.contrib import messages
from administration.forms import (AddDepartmentForm, AddClassroomForm, AddCourseForm
                                  )
from django.db.models import Q


# Create your views here.

def add_department(request):
    form = AddDepartmentForm()
    departments = Department.objects.all().order_by('name')

    if request.method == 'POST':
        form = AddDepartmentForm(request.POST)
        if form.is_valid():
            dep_name = form.cleaned_data.get('name')

            for dep in departments:
                if dep_name == dep.name:
                    messages.error(request, 'Le departement de ' + dep_name + ' a deja ete ajoute', extra_tags='error')
                    return redirect('add department')
                else:
                    form.save()
                    messages.success(request, 'Departement Ajoutee avec succes !', extra_tags='success')
                    return redirect('add department')
        else:
            print(form.errors)
    context = {
        'form': form,
        'departments': departments
    }
    return render(request, 'administration/add_department.html', context)


def add_classroom(request):
    form = AddClassroomForm()
    classrooms = Classroom.objects.all()
    if request.method == 'POST':
        form = AddClassroomForm(request.POST)
        if form.is_valid():
            classroom_name = form.cleaned_data.get('name')
            for classroom in classrooms:
                if classroom.name == classroom_name:
                    messages.error(request, 'Cette classe a deja ete enregistre', extra_tags='error')
                    return redirect('add classroom')
                else:
                    pass
            form.save()
            messages.success(request, 'Salle de classe ajoutee avec succes !', extra_tags='success')
            return redirect('class list')
        else:
            print(form.errors)
    context = {
        'form': form,
        'classrooms': classrooms
    }
    return render(request, 'administration/add_classroom.html', context)


def add_course(request):
    form = AddCourseForm()
    departments = Department.objects.all()
    courses = Course.objects.all()

    if request.method == 'POST':
        form = AddCourseForm(request.POST)
        if form.is_valid():
            dep_name = request.POST.get('department')
            department = Department.objects.get(name=dep_name)
            course_name = form.cleaned_data.get('name')
            class_name = form.cleaned_data.get('classroom')
            classroom = Classroom.objects.get(name=class_name)

            for course in courses:
                if course_name == course.name and course.classroom == classroom:
                    messages.error(request,
                                   str(course_name) + ' a deja ete ajoute a la liste des matieres de la ' + str(
                                       class_name), extra_tags='error')
                    return redirect('add course')
                else:
                    pass

            new_course = form.save()
            new_course.classroom = classroom
            new_course.department.add( department)
            new_course.save()
            messages.success(request, str(course_name) + ' a ete ajoute avec succes a la liste des matieres de la ' + str(class_name), extra_tags='success')

        else:
            print(form.errors)
    context = {
        'form': form,
        'departments': departments,
    }
    return render(request, 'administration/add_course.html', context)


def assign_teacher(request):
    classrooms = Classroom.objects.all()
    context = {
        'classrooms': classrooms
    }
    return render(request, 'administration/assign_teacher.html', context)


def display_class_course_list(request):
    classroom_name = request.GET.get('classroom')
    classroom = Classroom.objects.get(name=classroom_name)
    classrooms = Classroom.objects.all()

    section = classroom.section

    all_courses = Course.objects.all()
    courses = []

    for course in all_courses:
        if course.classroom.name == classroom_name:
            courses.append(course)

    context = {
        'courses': courses,
        'classrooms': classrooms,
        'classroom': classroom,
        'classroom_name': classroom_name
    }
    if not courses:
        messages.error(request, "La " + str(classroom_name) + " n'a pas encore de matieres enregistrees !",
                       extra_tags='error')
    else:
        messages.info(request, 'La liste de toutes les matieres enregistrées dans le system', extra_tags='info')
    return render(request, 'administration/assign_teacher.html', context)


def assign_choose_teacher(request):
    course_id = request.GET.get('course_id')
    class_id = request.GET.get('class_id')
    classroom = Classroom.objects.get(id=class_id)
    section = classroom.section

    course = Course.objects.get(id=course_id)

    all_teachers = Teacher.objects.all()
    teachers = []
    for teacher in all_teachers:
        for dep in teacher.department.all():
            for course_dep in course.department.all():
                print(course_dep)
                if dep == course_dep:
                    teachers.append(teacher)
                else:
                    pass

    context = {
        'course': course,
        'classroom': classroom,
        'teachers': teachers
    }
    return render(request, 'administration/assign_choose_teacher.html', context)


def assign_teacher_done(request):
    course_id = request.GET.get('course_id')
    teacher_id = request.GET.get('teacher_id')
    classroom_id = request.GET.get('classroom_id')
    classroom = Classroom.objects.get(id=classroom_id)
    classrooms = Classroom.objects.all()
    all_courses = Course.objects.all()
    courses = []
    for course in all_courses:
        if course.classroom == classroom:
            courses.append(course)

    course_num = len(courses)
    section = classroom.section
    all_courses = Course.objects.all()
    courses = []

    for course in all_courses:
        if course.classroom == classroom:
            courses.append(course)

    context = {
        'courses': courses,
        'classrooms': classrooms,
        'classroom': classroom,
        'course_num':course_num
    }
    censeurteacher = Group.objects.get_or_create(name='censeurteacher')
    adminteacher = Group.objects.get_or_create(name='adminteacher')

    course = Course.objects.get(id=course_id)
    teacher = Teacher.objects.get(id=teacher_id)
    for group in teacher.groups.all():
        if group.name == 'administrateur':
            group.user_set.remove(teacher)
            adminteacher[0].user_set.add(teacher)
            teacher.save()
        if group.name == 'censeur':
            group.user_set.remove(teacher)
            censeurteacher[0].user_set.add(teacher)
            teacher.save()

    course.teacher = teacher
    teacher.save()
    course.save()
    messages.success(request, str(teacher.first_name) + ' prendra en charge la classe de ' + str(
        classroom.name) + ' en ' + str(course.name), extra_tags='success')
    return render(request, 'administration/class_detail.html', context)


def course_detail(request):
    course_id = request.GET.get('course_id')
    class_id = request.GET.get('class_id')
    course = Course.objects.get(id=course_id)
    classroom = Classroom.objects.get(id=class_id)

    context = {
        'course': course,
        'classroom': classroom
    }
    return render(request, 'administration/course_detail.html', context)


def department_list(request):
    object_list = Department.objects.all()
    context = {
        'object_list': object_list
    }
    return render(request, 'administration/department_list.html', context)


def department_sorted_list(request):
    cathegory = request.GET.get('cathegory')
    print(cathegory)
    context = {}
    if cathegory == 'science' or 'literaire':
        object_list = Department.objects.filter(group_type=cathegory)
        context = {'object_list': object_list}
    if cathegory == 'tous':
        object_list = Department.objects.all()
        context = {'object_list':object_list}
    return render(request, 'administration/department_list.html', context)


class department_search_results(ListView):
    model = Department
    template_name = 'administration/department_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Department.objects.filter(
            Q(name__icontains=query) | Q(section__icontains=query) | Q(group_type__icontains=query) | Q(
                studies_type__icontains=query)
        )
        return object_list

def department_detail(request):
    id=request.GET.get('id')
    department = Department.objects.get(id=id)
    all_courses = Course.objects.all()
    all_teachers = Teacher.objects.all()
    courses=[]
    teachers=[]
    for teacher in all_teachers:
        for dep in teacher.department.all():
            if dep == department:
                teachers.append(teacher)

    for course in all_courses:
        for dep in course.department.all():
            if dep == department:
                courses.append(course)

    course_num = len(courses)
    teacher_num = len(teachers)
    context={
        'department': department,
        'courses': courses,
        'course_num': course_num,
        'teacher_num': teacher_num,
        'teachers': teachers
    }
    return render(request,'administration/department_detail.html',context)

def class_list(request):
    object_list = Classroom.objects.all()
    context={
        'object_list':object_list
    }
    return render(request,'administration/class_list.html',context)

class class_search_results(ListView):
    model = Classroom
    template_name = 'administration/class_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Classroom.objects.filter(
            Q(name__icontains=query) | Q(section__icontains=query) | Q(group_type__icontains=query) | Q(
                studies_type__icontains=query)
        )
        return object_list

class headmaster_class_search_results(ListView):
    model = Classroom
    template_name = 'administration/add_headmaster_class.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Classroom.objects.filter(
            Q(name__icontains=query) | Q(section__icontains=query) | Q(group_type__icontains=query) | Q(
                studies_type__icontains=query)
        )
        return object_list

class chose_class_search_results(ListView):
    model = Classroom
    template_name = 'administration/view_result_chose_class.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Classroom.objects.filter(
            Q(name__icontains=query) | Q(section__icontains=query) | Q(group_type__icontains=query) | Q(
                studies_type__icontains=query)
        )
        return object_list


class reportcard_chose_class_search_results(ListView):
    model = Classroom
    template_name = 'administration/reportcard_chose_class.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Classroom.objects.filter(
            Q(name__icontains=query) | Q(section__icontains=query) | Q(group_type__icontains=query) | Q(
                studies_type__icontains=query)
        )
        return object_list

def class_sorted_list(request):
    cathegory = request.GET.get('cathegory')
    print(cathegory)
    context = {}
    if cathegory == 'anglophone' or 'francophone':
        object_list = Classroom.objects.filter(section=cathegory)
        context = {'object_list': object_list}
    else:
        pass
    return render(request,'administration/class_list.html',context)

def headmaster_class_sorted_list(request):
    cathegory = request.GET.get('cathegory')
    context = {}
    if cathegory == 'anglophone':
        object_list = Classroom.objects.filter(section='anglophone')
        context = {
            'object_list': object_list
        }
        return render(request, 'administration/add_headmaster_class.html', context)

    if cathegory == 'francophone':
        object_list = Classroom.objects.filter(section='francophone')
        context = {
            'object_list': object_list
        }
        return render(request, 'administration/add_headmaster_class.html', context)

    if cathegory == 'science':
        object_list = Classroom.objects.filter(group_type='science')
        context = {
            'object_list': object_list
        }
        return render(request, 'administration/add_headmaster_class.html', context)

    if cathegory == 'literaire':
        object_list = Classroom.objects.filter(group_type='literaire')
        context = {
            'object_list': object_list
        }
        return render(request, 'administration/add_headmaster_class.html', context)
    else:
        pass
    return render(request,'administration/add_headmaster_class.html',context)

def chose_class_sorted_list(request):
    cathegory = request.GET.get('cathegory')
    print(cathegory)
    context = {}
    if cathegory == 'anglophone' or 'francophone':
        object_list = Classroom.objects.filter(section=cathegory)
        context = {'object_list': object_list}
    else:
        pass
    return render(request,'administration/view_result_chose_class.html',context)

def reportcard_class_sorted_list(request):
    cathegory = request.GET.get('cathegory')
    print(cathegory)
    context = {}
    if cathegory == 'anglophone' or 'francophone':
        object_list = Classroom.objects.filter(section=cathegory)
        context = {'object_list': object_list}
    else:
        pass
    return render(request,'administration/reportcard_chose_class.html',context)

def class_detail(request):
    id = request.GET.get('id')
    classroom = Classroom.objects.get(id=id)
    all_courses = Course.objects.all()
    courses = []
    for course in all_courses:
        if course.classroom == classroom:
            courses.append(course)

    course_num = len(courses)
    context = {
        'classroom':classroom,
        'courses':courses,
        'course_num':course_num
    }
    return render(request,'administration/class_detail.html',context)


def view_result_chose_class(request):
    object_list = Classroom.objects.all()
    context = {
        'object_list': object_list
    }
    return render(request, 'administration/view_result_chose_class.html',context)

def chose_course(request):
    id = request.GET.get('id')
    classroom = Classroom.objects.get(id=id)
    all_courses = Course.objects.all()
    all_results = Result.objects.all()
    results = []
    teacher_sequence = TeacherSequence.objects.all()
    courses = []
    for course in all_courses:
        if course.classroom == classroom:
            courses.append(course)

    for result in teacher_sequence:
        if result.course.classroom == classroom:
                results.append(result)

    course_num = len(courses)

    context = {
        'classroom': classroom,
        'courses': courses,
        'course_num': course_num,
        'results' : results
    }
    return render(request, 'administration/chose_course.html', context)

def search_result(request):
    id = request.GET.get('id')
    query = request.GET.get('q')
    classroom = Classroom.objects.get(id=id)
    all_courses = Course.objects.all()
    results = []
    teacher_sequence = TeacherSequence.objects.all()
    courses = []
    for course in all_courses:
        if course.classroom == classroom:
            courses.append(course)

    for result in teacher_sequence:
        if result.course.classroom == classroom:
                results.append(result)

    course_num = len(courses)


    results = TeacherSequence.objects.filter(
        Q(academic_year__icontains=query) | Q(sequence__icontains=query) | Q(course_name__icontains=query)
    )

    context = {
        'classroom': classroom,
        'courses': courses,
        'course_num': course_num,
        'results' : results
    }
    return render(request, 'administration/chose_course.html', context)

def results_sorted_list(request):
    id = request.GET.get('id')
    cathegory = request.GET.get('cathegory')
    classroom = Classroom.objects.get(id=id)
    all_courses = Course.objects.all()
    all_results = Result.objects.all()
    results = []
    teacher_sequence = TeacherSequence.objects.all()
    courses = []
    for course in all_courses:
        if course.classroom == classroom:
            courses.append(course)

    course_num = len(courses)

    if cathegory == '1 ere Sequence':
        for result in teacher_sequence:
            if result.course.classroom == classroom and result.sequence == '1 ere Sequence':
                results.append(result)

    if cathegory == '2 eme Sequence':
        for result in teacher_sequence:
            if result.course.classroom == classroom and result.sequence == '2 eme Sequence':
                results.append(result)
    if cathegory == '3 eme Sequence':
        for result in teacher_sequence:
            if result.course.classroom == classroom and result.sequence == '3 eme Sequence':
                results.append(result)
    if cathegory == '4 eme Sequence':
        for result in teacher_sequence:
            if result.course.classroom == classroom and result.sequence == '4 eme Sequence':
                results.append(result)
    if cathegory == '5 eme Sequence':
        for result in teacher_sequence:
            if result.course.classroom == classroom and result.sequence == '5 eme Sequence':
                results.append(result)
    if cathegory == '6 eme Sequence':
        for result in teacher_sequence:
            if result.course.classroom == classroom and result.sequence == '6 eme Sequence':
                results.append(result)
    context = {
        'classroom': classroom,
        'courses': courses,
        'course_num': course_num,
        'results' : results
    }
    return render(request, 'administration/chose_course.html', context)

def class_students_results(request):
    teacher_sequence_id = request.GET.get('teacher_result_id')
    teacher_sequence = TeacherSequence.objects.get(id=teacher_sequence_id)
    course_id = request.GET.get('course_id')
    course = Course.objects.get(id=course_id)
    all_results = Result.objects.all()
    results = []

    for result in all_results:
        if result.course == teacher_sequence.course and result.academic_year == teacher_sequence.academic_year and result.sequence == teacher_sequence.sequence:
            results.append(result)

    course = teacher_sequence.course
    sequence = teacher_sequence.sequence
    academic_year = teacher_sequence.academic_year
    context = {
        'results':results,
        'course':course,
        'sequence':sequence,
        'academic_year':academic_year,
        'teacher_sequence_id':teacher_sequence_id
    }

    return render(request,'administration/class_students_results.html',context)

def reportcard_chose_class(request):
    object_list = Classroom.objects.all()
    context = {
        'object_list': object_list
    }
    return render(request, 'administration/reportcard_chose_class.html',context)

def class_reportcards(request):
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)
    sequences = []

    courses =[]
    for course in Course.objects.all():
        if course.classroom == classroom:
            courses.append(course)

    course_num = len(courses)



    all_sequences = GeneralSequence.objects.all()
    for seq in all_sequences:
        if seq.classroom == classroom:
            sequences.append(seq)

    context={
        'classroom':classroom,
        'sequences':sequences,
        'course_num':course_num
    }
    return render(request,'administration/class_reportcards.html',context)

def report_card_list(request):
    class_id = request.GET.get('class_id')
    classroom = Classroom.objects.get(id=class_id)
    object_list = classroom.students.all()
    academic_year = request.GET.get('academic_year')
    sequence = request.GET.get('sequence')
    context = {
        'object_list': object_list,
        'classroom': classroom,
        'academic_year':academic_year,
        'sequence':sequence
    }
    return render(request,'administration/report_card_list.html',context)


def report_card_sorted_list(request):
    cathegory = request.GET.get('cathegory')
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)
    academic_year = request.GET.get('academic_year')
    sequence = request.GET.get('sequence')
    print(cathegory)
    context = {}
    if cathegory == 'masculin' or 'feminin':
        object_list = classroom.students.filter(gender=cathegory)
        context = {
            'object_list': object_list,
            'classroom':classroom,
            'academic_year':academic_year,
            'sequence':sequence
        }
    if cathegory == 'ordre alphabetique':
        object_list = classroom.students.all().order_by('first_name','last_name')
        context = {
            'object_list': object_list,
            'classroom': classroom,
            'academic_year': academic_year,
            'sequence': sequence
        }

    if cathegory == 'tous':
        object_list = classroom.students.all()
        context = {
            'object_list': object_list,
            'classroom': classroom,
            'academic_year': academic_year,
            'sequence': sequence
        }
    return render(request,'administration/report_card_list.html',context)


def report_card_list_search_results(request):
    class_id = request.GET.get('id')
    academic_year = request.GET.get('academic_year')
    sequence = request.GET.get('sequence')

    classroom = Classroom.objects.get(id=class_id)
    query = request.GET.get('q')
    object_list = Student.objects.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(date_of_birth__icontains=query) | Q(gender__icontains=query)
    )
    context={
        'object_list':object_list,
        'classroom':classroom,
        'academic_year': academic_year,
        'sequence': sequence
        }
    return render(request,'administration/report_card_list.html',context)

def student_report_card(request):
    global classroom
    global report_card
    global remark
    academic_year = request.GET.get('academic_year')
    sequence = request.GET.get('sequence')
    student_id = request.GET.get('student_id')
    student = Student.objects.get(id=student_id)

    for a in student.absent_hours.all():
        if a.sequence == sequence and a.year == academic_year:
            remark = a

    for report in student.report_card.all():
        if report.sequence == sequence and report.academic_year == academic_year:
            report_card = report

    for new_classroom in Classroom.objects.all():
        for new_student in new_classroom.students.all():
            if student == new_student:
                classroom = new_classroom
    coeff_total = 0
    coeff_total2 = 0
    notes_total = 0
    notes_total2 = 0
    greate_total = 0
    greate_total2 = 0
    average_mark = 0
    average = 0
    total_class_average =0
    average2 = 0
    seq2_tot = 0
    seq2_greate_tot = 0

    if sequence != '1 ere Sequence' and sequence != '3 eme Sequence' and sequence != '5 eme Sequence':
        for result in report_card.results.all():
            coeff_total2 = int(result.course.coeff) + coeff_total2
            notes_total2 = int(result.average_mark) + int(notes_total2)
            greate_total2 = int(result.total2) + int(greate_total2)
            notes_total = int(result.mark) + int(notes_total)
            greate_total = int(result.total) + int(greate_total)

            seq2_tot = int(result.mark2) * int(result.course.coeff)
            seq2_greate_tot = int(seq2_tot) + int(seq2_greate_tot)
            print(seq2_greate_tot)

        average2 = int(seq2_greate_tot) / int(coeff_total2)
        average2 = average2.__round__(2)
        average_list = []
        if sequence == '2 eme Sequence':
            for report in student.report_card.all():
                if report.sequence == '1 ere Sequence' and report.academic_year == academic_year:
                    report_card.average = report.average
                    report_card.save()

        if sequence == '4 eme Sequence':
            for report in student.report_card.all():
                if report.sequence == '3 eme Sequence' and report.academic_year == academic_year:
                    report_card.average = report.average
                    report_card.save()

        if sequence == '6 eme Sequence':
            for report in student.report_card.all():
                if report.sequence == '5 eme Sequence' and report.academic_year == academic_year:
                    report_card.average = report.average
                    report_card.save()

        sequence_results = Report_card.objects.filter(sequence=sequence, academic_year=academic_year,classroom=classroom)
        for a in sequence_results:
            average_list.append(a.average2)
            print(a)
        for b in average_list:
            total_class_average = int(b) + total_class_average

        report_card.class_average = (total_class_average / int(len(average_list))).__round__(2)
        report_card.save()

        data = list(sorted(average_list, reverse=True))
        report_card.rank = int(data.index(report_card.average2)) + 1
        report_card.save()

        report_card.average2 = average2
        report_card.first_average = max(average_list)
        report_card.last_average = min(average_list)
        report_card.save()
        sem_average = (float (report_card.average) + float (report_card.average2))/2
        sem_average = sem_average.__round__(2)
        report_card.sem_average = sem_average
        report_card.save()

        encouragement = ClassCouncil.objects.get(name='encouragements')
        felicitations = ClassCouncil.objects.get(name='felicitations')
        table = ClassCouncil.objects.get(name="tableau d'honneur")
        avert_travail = ClassCouncil.objects.get(name='avertissement travail')
        blame_travail = ClassCouncil.objects.get(name='blame travail')
        blame_conduite = ClassCouncil.objects.get(name='blame conduite')
        avert_conduite = ClassCouncil.objects.get(name='avertissement conduite')
        reussite = ClassCouncil.objects.get(name='reussite')
        travail_null = ClassCouncil.objects.get(name='travail null')
        travail_mauvais = ClassCouncil.objects.get(name="travail mauvais")
        travail_passable = ClassCouncil.objects.get(name='travail passable')
        travail_assez_bien = ClassCouncil.objects.get(name='travail assez bien')
        travail_bien = ClassCouncil.objects.get(name='travail bien')
        travail_tres_bien = ClassCouncil.objects.get(name='travail tres bien')
        travail_excellent = ClassCouncil.objects.get(name='travail excellent')
        context = {
            'travail_null': travail_null,
            'travail_mauvais': travail_mauvais,
            'travail_passable': travail_passable,
            'travail_assez_bien': travail_assez_bien,
            'travail_bien': travail_bien,
            'travail_tres_bien': travail_tres_bien,
            'travail_excellent': travail_excellent,
            'student': student,
            'reussite':reussite,
            'academic_year': academic_year,
            'sequence': sequence,
            'classroom': classroom,
            'report_card': report_card,
            'coeff_total': coeff_total,
            'coeff_total2': coeff_total2,
            'notes_total': notes_total,
            'greate_total': greate_total,
            'greate_total2': greate_total2,
            'courses': Course.objects.filter(classroom=classroom),
            'remark': remark,
            'encouragement': encouragement,
            'felicitations':felicitations,
            'table': table,
            'avert_travail': avert_travail,
            'blame_travail': blame_travail,
            'blame_conduite': blame_conduite,
            'avert_conduite': avert_conduite
        }
        return render(request, 'administration/student_report_card.html', context)

    if sequence == '1 ere Sequence' or sequence == '3 eme Sequence' or sequence == '5 eme Sequence':
        for result in report_card.results.all():
            coeff_total = int(result.course.coeff) + coeff_total
            notes_total = int(result.mark) + int(notes_total)
            greate_total = int(result.total) + int(greate_total)

        average = int(greate_total) / int(coeff_total)
        average = average.__round__(2)
        report_card.average = average
        report_card.save()
        # calculating the rank
        average_list = []
        for report in student.report_card.all():
            if report.sequence == sequence and report.academic_year == academic_year:
                report_card.average = report.average
                report_card.save()



        sequence_results = Report_card.objects.filter(sequence=sequence, academic_year=academic_year,classroom=classroom)
        for a in sequence_results:
            average_list.append(a.average)

        data = list(sorted(average_list, reverse=True))
        #average_list = average_list.sort(reverse=True)
        report_card.rank = int (data.index(report_card.average)) + 1
        report_card.save()

        report_card.first_average = max(average_list)
        report_card.last_average = min(average_list)
        report_card.save()

        sequence_results = Report_card.objects.filter(sequence=sequence, academic_year=academic_year, classroom=classroom)
        for res in sequence_results:
            average_list.append(res.average)

        for a in average_list:
            print(a)

        for b in average_list:
            total_class_average = int(b) + total_class_average

        report_card.class_average = (total_class_average / int(len(average_list))).__round__(2)
        report_card.save()

        encouragement = ClassCouncil.objects.get(name='encouragements')
        table = ClassCouncil.objects.get(name="tableau d'honneur")
        avert_travail = ClassCouncil.objects.get(name='avertissement travail')
        blame_travail = ClassCouncil.objects.get(name='blame travail')
        blame_conduite = ClassCouncil.objects.get(name='blame conduite')
        avert_conduite = ClassCouncil.objects.get(name='avertissement conduite')
        felicitations = ClassCouncil.objects.get(name='felicitations')
        reussite = ClassCouncil.objects.get(name='reussite')

        travail_null = ClassCouncil.objects.get(name='travail null')
        travail_mauvais = ClassCouncil.objects.get(name="travail mauvais")
        travail_passable = ClassCouncil.objects.get(name='travail passable')
        travail_assez_bien = ClassCouncil.objects.get(name='travail assez bien')
        travail_bien = ClassCouncil.objects.get(name='travail bien')
        travail_tres_bien = ClassCouncil.objects.get(name='travail tres bien')
        travail_excellent = ClassCouncil.objects.get(name='travail excellent')

        if report_card.average >= table.average and remark.hours_no <= table.hours:
            num = int(len(student.honor_rolls.all()))
            if num >= 1:
                for a_roll in student.honor_rolls.all():
                    if a_roll.year != academic_year and a_roll.sequence != sequence:
                        roll = HonorRoll.objects.create()
                        roll.year = academic_year
                        roll.rank = report_card.rank
                        roll.class_average = report_card.class_average
                        roll.main_teacher = str(classroom.main_teacher.first_name) + " " + str(
                            classroom.main_teacher.last_name)
                        roll.stud_no = len(classroom.students.all())
                        roll.sequence = sequence
                        if report_card.average >= encouragement.average and remark.hours_no <= encouragement.hours:
                            roll.encouragement = True
                        if report_card.average >= felicitations.average and remark.hours_no <= felicitations.hours:
                            roll.congrats = True
                        roll.save()
                        student.honor_rolls.add(roll)
                        student.save()
            else:
                roll = HonorRoll.objects.create()
                roll.year = academic_year
                roll.sequence = sequence
                roll.first_name = student.first_name
                roll.last_name = student.last_name
                roll.class_average = report_card.class_average
                roll.stud_no = len(classroom.students.all())
                roll.main_teacher = str(classroom.main_teacher.first_name) + " " + str(classroom.main_teacher.last_name)
                if sequence == '2 eme Sequence':
                    roll.sequence = 'Trimestre 1'
                    roll.average = report_card.sem_average

                if  sequence == '4 eme Sequence':
                    roll.sequence = 'Trimestre 2'
                    roll.average = report_card.sem_average

                if sequence == '6 eme Sequence':
                    roll.sequence = 'Trimestre 3'
                    roll.average = report_card.sem_average

                roll.date_of_birth = student.date_of_birth
                roll.place_of_birth = student.place_of_birth
                roll.classroom = classroom.name
                roll.rank = report_card.rank

                if sequence == '1 ere Sequence' or '3 eme Sequence' or '5 eme Sequence':
                    roll.average = report_card.average
                if report_card.average >= encouragement.average and remark.hours_no <= encouragement.hours:
                    roll.encouragement = True
                if report_card.average >= felicitations.average and remark.hours_no <= felicitations.hours:
                    roll.congrats = True
                roll.save()
                student.honor_rolls.add(roll)
                student.save()

        context={
            'travail_null':travail_null,
            'travail_mauvais':travail_mauvais,
            'travail_passable':travail_passable,
            'travail_assez_bien':travail_assez_bien,
            'travail_bien':travail_bien,
            'travail_tres_bien':travail_tres_bien,
            'travail_excellent':travail_excellent,
            'student':student,
            'academic_year':academic_year,
            'sequence':sequence,
            'classroom':classroom,
            'report_card': report_card,
            'coeff_total': coeff_total,
            'notes_total':notes_total,
            'greate_total':greate_total,
            'greate_total2':greate_total2,
            'courses':Course.objects.filter(classroom=classroom),
            'remark': remark,
            'felicitations': felicitations,
            'encouragement':encouragement,
            'table':table,
            'reussite':reussite,
            'avert_travail':avert_travail,
            'blame_travail':blame_travail,
            'blame_conduite':blame_conduite,
            'avert_conduite':avert_conduite
        }
        return render(request,'administration/student_report_card.html',context)

def download_reportcard(request):
    global classroom, remark
    global report_card
    coeff_total = 0
    coeff_total2 = 0
    notes_total = 0
    notes_total2 = 0
    greate_total = 0
    greate_total2 = 0
    average_mark = 0
    average = 0
    average2 = 0
    academic_year = request.GET.get('academic_year')
    sequence = request.GET.get('sequence')
    student_id = request.GET.get('student_id')
    student = Student.objects.get(id=student_id)

    for a in student.absent_hours.all():
        if a.sequence == sequence and a.year == academic_year:
            remark = a

    for report in student.report_card.all():
        if report.sequence == sequence and report.academic_year == academic_year:
            report_card = report

    for new_classroom in Classroom.objects.all():
        for new_student in new_classroom.students.all():
            if student == new_student:
                classroom = new_classroom
    coeff_total = 0
    notes_total = 0
    greate_total = 0
    if sequence != '1 ere Sequence' and sequence != '3 eme Sequence' and sequence != '5 eme Sequence':
        for result in report_card.results.all():
            coeff_total2 = int(result.course.coeff) + coeff_total2
            notes_total2 = int(result.mark2) + int(notes_total2)
            greate_total2 = int(result.total2) + int(greate_total)
            notes_total = int(result.mark) + int(notes_total)
            greate_total = int(result.total) + int(greate_total)

        average2 = int(greate_total2) / int(coeff_total2)
        average2 = average2.__round__(2)
        average_list = []
        if sequence == '2 eme Sequence':
            for report in student.report_card.all():
                if report.sequence == '1 ere Sequence' and report.academic_year == academic_year:
                    report_card.average = report.average
                    report_card.save()

        if sequence == '4 eme Sequence':
            for report in student.report_card.all():
                if report.sequence == '3 eme Sequence' and report.academic_year == academic_year:
                    report_card.average = report.average
                    report_card.save()

        if sequence == '6 eme Sequence':
            for report in student.report_card.all():
                if report.sequence == '5 eme Sequence' and report.academic_year == academic_year:
                    report_card.average = report.average
                    report_card.save()

            sequence_results = Report_card.objects.filter(sequence='2 eme Sequence', academic_year=academic_year,
                                                          classroom=classroom)
            for a in sequence_results:
                average_list.append(a.average2)
                print(a)

            data = list(sorted(average_list, reverse=True))
            report_card.rank = int(data.index(report_card.average2)) + 1
            report_card.save()

        report_card.average2 = average2
        report_card.first_average = max(average_list)
        report_card.last_average = min(average_list)
        report_card.save()
        sem_average = (float(report_card.average) + float(report_card.average2)) / 2
        sem_average = sem_average.__round__(2)
        report_card.sem_average = sem_average
        report_card.save()



        encouragement = ClassCouncil.objects.get(name='encouragements')
        felicitations = ClassCouncil.objects.get(name='felicitations')
        table = ClassCouncil.objects.get(name="tableau d'honneur")
        avert_travail = ClassCouncil.objects.get(name='avertissement travail')
        blame_travail = ClassCouncil.objects.get(name='blame travail')
        blame_conduite = ClassCouncil.objects.get(name='blame conduite')
        avert_conduite = ClassCouncil.objects.get(name='avertissement conduite')
        reussite = ClassCouncil.objects.get(name='reussite')
        travail_null = ClassCouncil.objects.get(name='travail null')
        travail_mauvais = ClassCouncil.objects.get(name="travail mauvais")
        travail_passable = ClassCouncil.objects.get(name='travail passable')
        travail_assez_bien = ClassCouncil.objects.get(name='travail assez bien')
        travail_bien = ClassCouncil.objects.get(name='travail bien')
        travail_tres_bien = ClassCouncil.objects.get(name='travail tres bien')
        travail_excellent = ClassCouncil.objects.get(name='travail excellent')

        context = {
            'travail_null': travail_null,
            'travail_mauvais': travail_mauvais,
            'travail_passable': travail_passable,
            'travail_assez_bien': travail_assez_bien,
            'travail_bien': travail_bien,
            'travail_tres_bien': travail_tres_bien,
            'travail_excellent': travail_excellent,
            'student': student,
            'reussite': reussite,
            'academic_year': academic_year,
            'sequence': sequence,
            'classroom': classroom,
            'report_card': report_card,
            'coeff_total': coeff_total,
            'coeff_total2': coeff_total2,
            'notes_total': notes_total,
            'greate_total': greate_total,
            'greate_total2': greate_total2,
            'courses': Course.objects.filter(classroom=classroom),
            'remark': remark,
            'encouragement': encouragement,
            'felicitations': felicitations,
            'table': table,
            'avert_travail': avert_travail,
            'blame_travail': blame_travail,
            'blame_conduite': blame_conduite,
            'avert_conduite': avert_conduite
        }
        pdf = render_to_pdf('administration/download_student_reportcard.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

    if sequence == '1 ere Sequence' or '3 eme Sequence' or '5 eme Sequence':
        for result in report_card.results.all():
            coeff_total = int(result.course.coeff) + coeff_total
            notes_total = int(result.mark) + int(notes_total)
            greate_total = int(result.total) + int(greate_total)

        average = int(greate_total) / int(coeff_total)
        average = average.__round__(2)
        report_card.average = average
        report_card.save()
        # calculating the rank
        average_list = []
        for report in student.report_card.all():
            if report.sequence == sequence and report.academic_year == academic_year:
                report_card.average = report.average
                report_card.save()

        sequence_results = Report_card.objects.filter(sequence=sequence, academic_year=academic_year,classroom=classroom)
        for a in sequence_results:
            average_list.append(a.average)

        data = list(sorted(average_list, reverse=True))
        #average_list = average_list.sort(reverse=True)
        report_card.rank = int (data.index(report_card.average)) + 1
        report_card.save()

        report_card.first_average = max(average_list)
        report_card.last_average = min(average_list)
        report_card.save()

        sequence_results = Report_card.objects.filter(sequence=sequence, academic_year=academic_year, classroom=classroom)
        for res in sequence_results:
            average_list.append(res.average)

        for a in average_list:
            print(a)

        encouragement = ClassCouncil.objects.get(name='encouragements')
        table = ClassCouncil.objects.get(name="tableau d'honneur")
        avert_travail = ClassCouncil.objects.get(name='avertissement travail')
        blame_travail = ClassCouncil.objects.get(name='blame travail')
        blame_conduite = ClassCouncil.objects.get(name='blame conduite')
        avert_conduite = ClassCouncil.objects.get(name='avertissement conduite')
        felicitations = ClassCouncil.objects.get(name='felicitations')
        reussite = ClassCouncil.objects.get(name='reussite')

        travail_null = ClassCouncil.objects.get(name='travail null')
        travail_mauvais = ClassCouncil.objects.get(name="travail mauvais")
        travail_passable = ClassCouncil.objects.get(name='travail passable')
        travail_assez_bien = ClassCouncil.objects.get(name='travail assez bien')
        travail_bien = ClassCouncil.objects.get(name='travail bien')
        travail_tres_bien = ClassCouncil.objects.get(name='travail tres bien')
        travail_excellent = ClassCouncil.objects.get(name='travail excellent')
        context={
            'travail_null':travail_null,
            'travail_mauvais':travail_mauvais,
            'travail_passable':travail_passable,
            'travail_assez_bien':travail_assez_bien,
            'travail_bien':travail_bien,
            'travail_tres_bien':travail_tres_bien,
            'travail_excellent':travail_excellent,
            'student':student,
            'academic_year':academic_year,
            'sequence':sequence,
            'classroom':classroom,
            'report_card': report_card,
            'coeff_total': coeff_total,
            'notes_total':notes_total,
            'greate_total':greate_total,
            'greate_total2':greate_total2,
            'courses':Course.objects.filter(classroom=classroom),
            'remark': remark,
            'felicitations': felicitations,
            'encouragement':encouragement,
            'table':table,
            'reussite':reussite,
            'avert_travail':avert_travail,
            'blame_travail':blame_travail,
            'blame_conduite':blame_conduite,
            'avert_conduite':avert_conduite
        }
        pdf = render_to_pdf('administration/download_student_reportcard.html',context)
        return HttpResponse(pdf, content_type='application/pdf')

def assign_teacher_sorted_list(request):
    category = request.GET.get('cathegory')
    class_id = request.GET.get('class_id')
    classroom = Classroom.objects.get(id=class_id)
    courses = []
    print(category)
    all_courses = []
    for a_course in Course.objects.all():
        if a_course.classroom == classroom:
            all_courses.append(a_course)

    if category != 'all':
        for course in all_courses:
            for dep in course.department.all():
                if dep.group_type == category:
                    courses.append(course)
        context = {
            'courses':courses,
            'classroom':classroom
        }
        return render(request,'administration/assign_teacher_done.html',context)

    if category == 'all':
        courses = all_courses
        context = {
            'courses':courses,
            'classroom':classroom
        }
        return render(request,'administration/assign_teacher_done.html',context)


def modify_class(request):
    class_id = request.GET.get('class_id')
    classroom = Classroom.objects.get(id=class_id)

    context = {
        'classroom': classroom
    }
    return render(request, 'administration/modify_class.html',context)

def modify_class_done(request):
    class_id = request.GET.get('class_id')

    section = request.GET.get('section')
    studies_type = request.GET.get('studies_type')
    group_type = request.GET.get('group_type')
    name = request.GET.get('name')

    classroom = Classroom.objects.get(id=class_id)
    classroom.name = name
    classroom.studies_type = studies_type
    classroom.group_type = group_type
    classroom.section = section

    classroom.save()

    all_courses = Course.objects.all()
    courses = []
    for course in all_courses:
        if course.classroom == classroom:
            courses.append(course)

    course_num = len(courses)

    context={
        'classroom': classroom,
        'courses':courses,
        'course_num':course_num
    }
    return render(request, 'administration/class_detail.html', context)


def dates(request):
    date = request.POST.get('date')
    name = request.POST.get('name')
    status = request.POST.get('status')
    if status == 'date':
        new_date = Date.objects.create()
        new_date.date = date
        new_date.name = name
        new_date.save()

        notify.send(sender=request.user, recipient=recipient, verb='a aprouvee votre demande de rendez vous', level='success',
                    description=message)
    dates = Date.objects.all()
    context = {
        'dates':dates,
    }
    return render(request, 'administration/dates.html',context)

def add_date(request):
    date = request.POST.get('date')
    name = request.POST.get('name')
    status = request.POST.get('status')
    if status == 'date':
        new_date = Date.objects.create()
        new_date.date = date
        new_date.name = name
        new_date.save()

    dates = Date.objects.all()
    context= {
        'dates':dates,
    }
    messages.success(request, 'Date strategique enregistree avec succes !', extra_tags='success')
    return render(request, 'administration/dates.html',context)

def delete_date(request):
    date = request.POST.get('date')
    name = request.POST.get('name')
    status = request.POST.get('status')
    if status == 'date':
        new_date = Date.objects.create()
        new_date.date = date
        new_date.name = name
        new_date.save()

    date_id = request.GET.get('date_id')
    date = Date.objects.get(id=date_id)
    date.delete()
    messages.error(request, 'Date suprimee avec success !', extra_tags='error')
    dates = Date.objects.all()
    context = {
        'dates':dates,
    }
    return render(request, 'administration/dates.html',context)

def assign_main_teacher(request):
    classrooms = Classroom.objects.all()
    context = {
        'classrooms': classrooms
    }
    return render(request,'administration/assign_main_teacher_chose_class.html',context)

def chose_main_teacher(request):
    class_id = request.GET.get('class_id')
    classroom = Classroom.objects.get(id=class_id)
    all_courses = Course.objects.all()
    courses = []
    for course in all_courses:
        if course.classroom == classroom:
            courses.append(course)
    teachers = []

    for new_course in courses:
        if new_course.teacher in teachers:
            pass
        else:
            teachers.append(new_course.teacher)
    context = {
        'classroom':classroom,
        'teachers':teachers
    }
    return render(request, 'administration/chose_main_teacher.html', context)

def assign_main_teacher_done(request):
    classrooms = Classroom.objects.all()
    class_id = request.GET.get('class_id')
    teacher_id = request.GET.get('teacher_id')

    classroom = Classroom.objects.get(id=class_id)
    teacher = Teacher.objects.get(id=teacher_id)

    classroom.main_teacher = teacher
    classroom.save()

    context = {
        'classrooms': classrooms
    }
    messages.success(request,'Profeseur principal assigne avec success !', extra_tags='success')
    return render(request, 'administration/assign_main_teacher_chose_class.html', context)

def assign_headmaster(request):
    headmasters = Teacher.objects.filter(groups__name='surveillant general')
    context = {
        'headmasters' : headmasters
    }
    return render(request, 'administration/assign_headmaster.html', context)

def add_headmaster_class(request):
    object_list = Classroom.objects.all()
    headmaster_id = request.GET.get('headmaster_id')
    headmaster = Teacher.objects.get(id=headmaster_id)
    context = {
        'headmaster':headmaster,
        'object_list':object_list
    }
    return render(request, 'administration/add_headmaster_class.html',context)

def assign_headmaster_done(request):
    headmasters = Teacher.objects.filter(groups__name='surveillant general')
    headmaster_id = request.GET.get('headmaster_id')
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)
    headmaster = Teacher.objects.get(id=headmaster_id)

    for headmas in headmasters:
        for a_class in headmas.classrooms.all():
            if a_class == classroom:
                messages.error(request, 'Le surveillant General' +str(headmas.first_name) + ' est deja en charge de la '+ str(classroom.name), extra_tags='error')
                context = {
                    'headmasters': headmasters
                }
                return render(request, 'administration/assign_headmaster.html', context)
        else:
            headmaster.classrooms.add(classroom)
            messages.success(request, 'Le surveillant ' +str(headmaster.first_name)+ ' est maintenant en charge de la '+ str(classroom.name), extra_tags='success')
            context = {
                'headmasters': headmasters
            }
            return render(request, 'administration/assign_headmaster.html',context)

def remove_classroom(request):
    headmasters = Teacher.objects.filter(groups__name='surveillant general')
    headmaster_id = request.GET.get('headmaster_id')
    classroom_id = request.GET.get('classroom_id')

    classroom = Classroom.objects.get(id=classroom_id)
    headmaster = Teacher.objects.get(id=headmaster_id)

    for a_class in headmaster.classrooms.all():
        if a_class == classroom:
            headmaster.classrooms.remove(a_class)

    context = {
        'headmasters': headmasters
    }
    messages.error(request, str(classroom.name)+ ' a ete enlevee a la liste des classes de ' +str(headmaster.first_name), extra_tags='error')
    return render(request, 'administration/assign_headmaster.html',context)



def disciplinary_council(request):
    status = request.POST.get('status')
    hours = request.POST.get('hours')
    hours2 = request.POST.get('hours2')
    ex_hours = request.POST.get('ex_hours')
    ex_days = request.POST.get('ex_days')
    if status == 'avertissement conduite':
        council = DisciplinaryCouncil.objects.filter(name='avertissement conduite')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe avertissement travail deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/disciplinary_council.html', context)

        else:
            obj = DisciplinaryCouncil.objects.create()
            obj.name = "avertissement conduite"
            obj.hours = hours
            obj.hours2 = hours2
            obj.save()

    if status == 'blame conduite':
        council = DisciplinaryCouncil.objects.filter(name='blame conduite')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe blame condute deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/disciplinary_council.html', context)
        else:
            obj = DisciplinaryCouncil.objects.create()
            obj.name = "blame conduite"
            obj.hours = hours
            obj.hours2 = hours2
            obj.save()

    if status == 'conseil de discipline':
        council = DisciplinaryCouncil.objects.filter(name='conseil de discipline')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe conseil de discipline deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/disciplinary_council.html', context)
        else:
            obj = DisciplinaryCouncil.objects.create()
            obj.name = "conseil de discipline"
            obj.hours = hours
            obj.hours2 = hours2
            obj.save()

    if status == 'exclusion definitive':
        council = DisciplinaryCouncil.objects.filter(name='exclusion definitive')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe exclusion definitive deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/disciplinary_council.html', context)
        else:
            obj = DisciplinaryCouncil.objects.create()
            obj.name = "exclusion definitive"
            obj.hours = hours
            obj.save()
    if status == "heures d'exclusions":
        obj = ExclusionHours.objects.create()
        obj.name = "heures d'exclusions"
        obj.hours = hours
        obj.hours2 = hours2
        obj.ex_hours = ex_hours
        obj.save()

    if status == "jours d'exclusions":
        obj = ExclusionDays.objects.create()
        obj.name = "jours d'exclusions"
        obj.hours = hours
        obj.hours2 = hours2
        obj.ex_days = ex_days
        obj.save()
    context = {
        'exclusion_days':ExclusionDays.objects.all(),
        'exclusion_hours': ExclusionHours.objects.all(),
        'disciplines':DisciplinaryCouncil.objects.all()
    }
    return render(request, 'administration/disciplinary_council.html',context)

def delete_discipline(request):
    discipline_id = request.GET.get('discipline_id')
    hour_id = request.GET.get('hour_id')
    day_id = request.GET.get('day_id')
    delete_status = request.GET.get('delete_status')
    print(delete_status)
    if delete_status == 'hour':
        hour = ExclusionHours.objects.get(id=hour_id)
        hour.delete()

    if delete_status == 'day':
        hour = ExclusionDays.objects.get(id=day_id)
        hour.delete()

    if delete_status == ' ':
        discipline = DisciplinaryCouncil.objects.get(id=discipline_id)
        discipline.delete()
        messages.error(request, 'Scenario supprime avec succes !', extra_tags='error')

    context = {
        'disciplines': DisciplinaryCouncil.objects.all(),
        'exclusion_hours':ExclusionHours.objects.all()
    }
    return render(request, 'administration/disciplinary_council.html',context)


def class_council(request):
    status = request.POST.get('status')
    hours = request.POST.get('hours')
    hours2 = request.POST.get('hours2')
    average = request.POST.get('average')
    average2 = request.POST.get('average2')
    if status == 'encouragements':
        council = ClassCouncil.objects.filter(name='encouragements')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe encouragement deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)
        else:
            obj = ClassCouncil.objects.create()
            obj.name = 'encouragements'
            obj.average = average
            obj.hours = hours
            obj.save()
    if status == 'tableau':
        council = ClassCouncil.objects.filter(name="tableau d'honeur")
        if len(council) >= 1:
            messages.error(request, "Conseil de classe tableau d'honeur deja ajoute", extra_tags='error')
            councils = ClassCouncil.objects.all()
            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)

        else:
            obj = ClassCouncil.objects.create()
            obj.name = "tableau d'honneur"
            obj.average = average
            obj.hours = hours
            obj.save()

    if status == 'reussite':
        council = ClassCouncil.objects.filter(name='reussite')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe reussite deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)

        else:
            obj = ClassCouncil.objects.create()
            obj.name = "reussite"
            obj.average = average
            obj.hours = hours
            obj.save()

    if status == 'blame travail':
        council = ClassCouncil.objects.filter(name='blame travail')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe blame travail deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)
        else:
            obj = ClassCouncil.objects.create()
            obj.name = "blame travail"
            obj.average = average
            obj.save()
    if status == 'avertissement travail':
        council = ClassCouncil.objects.filter(name='avertissement travail')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe avertissement deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)

        else :
            obj = ClassCouncil.objects.create()
            obj.name = "avertissement travail"
            obj.average = average
            obj.average2 = average2
            obj.save()

    if status == 'felicitations':
        council = ClassCouncil.objects.filter(name='felicitations')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe felicitations deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)
        else:
            obj = ClassCouncil.objects.create()
            obj.name = "felicitations"
            obj.average = average
            obj.hours = hours
            obj.save()

    if status == 'travail null':
        council = ClassCouncil.objects.filter(name='travail null')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe travail null deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)
        else:
            obj = ClassCouncil.objects.create()
            obj.name = "travail null"
            obj.average = average
            obj.save()

    if status == 'travail mauvais':
        council = ClassCouncil.objects.filter(name='travail mauvais')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe mauvais deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)
        else:
            obj = ClassCouncil.objects.create()
            obj.name = "travail mauvais"
            obj.average = average
            obj.average2 = average2
            obj.save()

    if status == 'travail passable':
        council = ClassCouncil.objects.filter(name='travail passable')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe travail passable deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)
        else:
            obj = ClassCouncil.objects.create()
            obj.name = "travail passable"
            obj.average = average
            obj.average2 = average2
            obj.save()
    if status == 'travail assez bien':
        council = ClassCouncil.objects.filter(name='trvail assez bien')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe travail assez bien deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)
        else:
            obj = ClassCouncil.objects.create()
            obj.name = "travail assez bien"
            obj.average = average
            obj.average2 = average2
            obj.save()
    if status == 'travail bien':
        council = ClassCouncil.objects.filter(name='travail bien')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe tres bien deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)
        else:
            obj = ClassCouncil.objects.create()
            obj.name = "travail bien"
            obj.average = average
            obj.average2 = average2
            obj.save()
    if status == 'travail tres bien':
        council = ClassCouncil.objects.filter(name='travail tres bien')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe travail tres bien deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)
        else:
            obj = ClassCouncil.objects.create()
            obj.name = "travail tres bien"
            obj.average = average
            obj.average2 = average2
            obj.save()
    if status == 'travail excellent':
        council = ClassCouncil.objects.filter(name='travail excellent')
        if len(council) >= 1:
            messages.error(request, 'Conseil de classe excellent deja ajoute', extra_tags='error')
            councils = ClassCouncil.objects.all()

            context = {
                'councils': councils
            }
            return render(request, 'administration/class_council.html', context)
        else:
            obj = ClassCouncil.objects.create()
            obj.name = "travail excellent"
            obj.average = average
            obj.average2 = average2
            obj.save()
    councils = ClassCouncil.objects.all()

    context = {
        'councils':councils
    }
    return render(request, 'administration/class_council.html',context)

def delete_council(request):
    council_id = request.POST.get('council_id')
    status = request.POST.get('status')

    council =ClassCouncil.objects.get(id=council_id)
    council.delete()
    messages.error(request, 'Conseil supprime avec succes !', extra_tags='error')

    context = {
        'councils': ClassCouncil.objects.all(),
    }
    return render(request, 'administration/class_council.html',context)

def honor_roll_list(request):
    class_id = request.GET.get('class_id')
    sequence = request.GET.get('sequence')
    academic_year = request.GET.get('academic_year')
    classroom = Classroom.objects.get(id=class_id)
    list = classroom.students.all()
    object_list = []
    for stud in list:
        for roll in stud.honor_rolls.all():
            if roll.sequence == sequence and roll.year == academic_year:
                object_list.append(stud)

    academic_year = request.GET.get('academic_year')
    sequence = request.GET.get('sequence')
    context = {
        'object_list': object_list,
        'classroom': classroom,
        'academic_year': academic_year,
        'sequence': sequence
    }
    return render(request, 'administration/honor_roll_list.html',context)

def modify_department(request):
    dep_id = request.GET.get('dep_id')
    department = Department.objects.get(id=dep_id)

    context = {
        'department':department
    }
    return render(request,'administration/modify_department.html', context)

def save_department(request):
    id = request.GET.get('id')

    name = request.GET.get('name')
    section = request.GET.get('section')
    group_type = request.GET.get('group_type')
    studies_type = request.GET.get('studies_type')

    department = Department.objects.get(id=id)
    department.name = name
    department.section = section
    department.group_type = group_type
    department.studies_type = studies_type
    department.save()

    all_courses = Course.objects.all()
    all_teachers = Teacher.objects.all()
    courses = []
    teachers = []
    for teacher in all_teachers:
        for dep in teacher.department.all():
            if dep == department:
                teachers.append(teacher)

    for course in all_courses:
        for dep in course.department.all():
            if dep == department:
                courses.append(course)

    course_num = len(courses)
    teacher_num = len(teachers)
    context = {
        'department': department,
        'courses': courses,
        'course_num': course_num,
        'teacher_num': teacher_num,
        'teachers': teachers
    }
    return render(request,'administration/department_detail.html',context)

def delete_course(request):
    id = request.GET.get('id')
    course_id = request.GET.get('course_id')
    classroom = Classroom.objects.get(id=id)
    all_courses = Course.objects.all()
    course = Course.objects.get(id=course_id)
    course.delete()
    messages.success(request, str(course.name) + ' a ete supprimee avec succes a la liste des matieres de la '+ str(course.classroom.name), extra_tags='success')
    courses = []
    for course in all_courses:
        if course.classroom == classroom:
            courses.append(course)

    course_num = len(courses)
    context = {
        'classroom': classroom,
        'courses': courses,
        'course_num': course_num
    }
    return render(request, 'administration/class_detail.html',context)

def delete_class(request):
    object_list = Classroom.objects.all()
    class_id = request.GET.get('class_id')
    classroom = Classroom.objects.get(id=class_id)
    classroom.delete()
    messages.success(request, 'La '+str(classroom.name)+' a ete suprimmer avec succes a la liste des matieres !', extra_tags='success')
    context = {
        'object_list': object_list
    }
    return render(request,'administration/class_list.html',context)

def modify_course(request):
    course_id = request.GET.get('course_id')
    course = Course.objects.get(id=course_id)
    departments = Department.objects.all()
    context = {
        'course':course,
        'departments':departments
    }
    return render(request, 'administration/modify_course.html',context)

def save_course(request):
    id = request.GET.get('id')
    course_id = request.GET.get('course_id')
    dep_name = request.GET.get('department')
    department = Department.objects.get(name = dep_name)
    name = request.GET.get('name')
    coeff = request.GET.get('coeff')

    id = request.GET.get('id')

    course = Course.objects.get(id=course_id)
    classroom = Classroom.objects.get(id=id)
    for dep in course.department.all():
        course.department.remove(dep)
    course.save()
    course.coeff = coeff
    course.name = name
    course.department.add(department)
    course.save()

    all_courses = Course.objects.all()
    courses = []
    for course in all_courses:
        if course.classroom == classroom:
            courses.append(course)

    course_num = len(courses)
    context = {
        'classroom': classroom,
        'courses': courses,
        'course_num': course_num
    }
    return render(request,'administration/class_detail.html',context)