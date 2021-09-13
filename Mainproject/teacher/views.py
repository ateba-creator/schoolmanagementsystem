from django.shortcuts import render, redirect
from administration.models import Department, Course, Classroom
from accounts.models import Teacher
from student.models import Student
from django.views.generic import DetailView, ListView
from Mainproject.utils import render_to_pdf
from academic.models import Result, TeacherSequence, Report_card, GeneralSequence, AbsentHours, GeneralAbsentHours,\
    DisciplinaryCouncil,ExclusionHours, ExclusionDays
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Q


# Create your views here.

def my_departments(request):
    departments = request.user.department.all()
    all_teachers = Teacher.objects.all()
    teachers = []
    for depp in departments:
        for teacher in all_teachers:
            for dep in teacher.department.all():
                if dep == depp:
                    teachers.append(teacher)

    teacher_num = len(teachers)
    context = {
        'departments': departments,
        'teacher_num': teacher_num
    }
    return render(request, 'teacher/my_departments.html', context)


def my_classes(request):
    all_courses = Course.objects.all()
    classrooms = []
    for course in all_courses:
        if course.teacher == request.user:
            if course.classroom in classrooms:
                pass
            else:
                classrooms.append(course.classroom)

    context = {
        'classrooms': classrooms
    }
    return render(request, 'teacher/my_classes.html', context)



def Download_studentlist(request):
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)

    context = {
        'classroom': classroom
    }
    pdf = render_to_pdf('teacher/download_student_list.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def teacher_results(request):
    all_courses = Course.objects.all()
    courses = []
    for course in all_courses:
        if course.teacher == request.user:
            courses.append(course)

    context = {
        'courses': courses
    }
    return render(request, 'teacher/teacher_results.html', context)


def teacher_results_detail(request):
    course_id = request.GET.get('id')
    course = Course.objects.get(id=course_id)
    results = []
    for result in TeacherSequence.objects.all():
        if result.course == course:
            results.append(result)

    context = {
        'course': course,
        'results':results
    }
    return render(request, 'teacher/teacher_results_detail.html', context)

def get_notes(request):
    sequence = request.GET.get('sequence')
    academic_year = request.GET.get('academic_year')
    class_id = request.GET.get('class_id')
    course_id = request.GET.get('course_id')
    course = Course.objects.get(id=course_id)

    results = []
    all_teacher_results = TeacherSequence.objects.all()
    for result in all_teacher_results:
        if result.academic_year == academic_year and result.sequence == sequence and result.course == course:
            results.append(result)
    context = {
        'course':course,
        'results':results
    }
    return render(request, 'teacher/teacher_results_detail.html',context)

def upload_notes(request):
    course_id = request.GET.get('course_id')
    sequence = request.GET.get('sequence')
    academic_year = request.GET.get('academic_year')

    course = Course.objects.get(id=course_id)
    classroom = course.classroom
    all_students = classroom.students.all()
    all_results = Result.objects.all()
    results = []

    #for creating a general sequence
    all_courses = Course.objects.all()

    for result in all_results:
        if sequence == '2 eme Sequence' or sequence == '4 eme Sequence' or sequence =='6 eme Sequence':
            if result.course == course and result.sequence2 == sequence and result.academic_year == academic_year:
                messages.error(request,"Les resultats de "+str(course.name)+" de la "+sequence+" - ("+academic_year+") ont deja ete enregistres !" ,extra_tags='error')
                results.append(result)
                context = {
                    'course': course,
                }
                return render(request, 'teacher/teacher_results_detail.html', context)

        if sequence != '2 eme Sequence' and sequence != '4 eme Sequence' and sequence != '6 eme Sequence':
            if result.course == course and result.sequence == sequence and result.academic_year == academic_year:
                messages.error(request,"Les resultats de "+str(course.name)+" de la "+sequence+" - ("+academic_year+") ont deja ete enregistres !" ,extra_tags='error')
                results.append(result)
                context = {
                    'course': course,
                }
                return render(request, 'teacher/teacher_results_detail.html', context)

    students = []
    for std in all_students:
        for crs in std.course.all():
            if crs == course:
                students.append(std)

    if sequence == '2 eme Sequence':
        for student in students:
            a_result = Result.objects.filter(sequence='1 ere Sequence', academic_year=academic_year, student=student, course=course)
            for res in a_result:
                res.sequence2 = sequence
                res.save()
                results.append(res)
    if sequence == '4 eme Sequence':
        for student in students:
            a_result = Result.objects.filter(sequence='3 eme Sequence', academic_year=academic_year, student=student, course=course)
            for res in a_result:
                res.sequence2 = sequence
                res.save()
                results.append(res)
    if sequence == '6 eme Sequence':
        for student in students:
            a_result = Result.objects.filter(sequence='5 eme Sequence', academic_year=academic_year, student=student, course=course)
            for res in a_result:
                res.sequence2 = sequence
                res.save()
                results.append(res)

    if sequence != '2 eme Sequence' and sequence != '4 eme Sequence' and sequence != '6 eme Sequence':
        for student in all_students:
            new_result = Result.objects.create()
            new_result.sequence = sequence
            new_result.academic_year = academic_year
            new_result.course = course
            new_result.student = student
            new_result.student_name = str(student.first_name) + " " + str(student.last_name)
            new_result.save()
            results.append(new_result)


    teacher_sequence = TeacherSequence.objects.create()
    teacher_sequence.sequence = sequence
    teacher_sequence.academic_year = academic_year
    teacher_sequence.course = course
    teacher_sequence.course_name = course.name
    request.user.sequence.add(teacher_sequence)
    teacher_sequence.save()
    request.user.save()

    context ={
        'sequence':sequence,
        'academic_year':academic_year,
        'course':course,
        'results':results,
        'teacher_sequence':teacher_sequence
    }
    coeff_total2=0,
    notes_total2=0
    notes_total=0,
    greate_total2=0,
    greate_total=0,
    coeff_total=0
    all_teacher_sequences = TeacherSequence.objects.all()
    classroom_courses = []
    classroom_results = []
    for new_course in all_courses:
        if new_course.classroom == course.classroom:
            classroom_courses.append(new_course)

    for course in classroom_courses:
        for result in all_teacher_sequences:
            if result.course == course and result.sequence == sequence and result.academic_year == academic_year:
                classroom_results.append(result)

    i = 0
    if len(classroom_results) == len(classroom_courses):
        general_sequence = GeneralSequence.objects.create()
        general_sequence.academic_year = academic_year
        general_sequence.sequence = sequence
        general_sequence.classroom = classroom
        general_sequence.save()

        if sequence != '2 eme Sequence' and sequence != '4 eme Sequence' and sequence != '6 eme Sequence':
            print('here too')
            for stud in students:
                report_card = Report_card.objects.create()
                report_card.sequence = sequence
                report_card.academic_year = academic_year
                report_card.classroom = classroom
                report_card.student_name = str(stud.first_name)
                report_card.save()
                stud.report_card.add(report_card)
                stud.save()

                for res in Result.objects.all():
                    if res.student == stud and res.sequence == sequence and res.academic_year == academic_year:
                        for rep in stud.report_card.all():
                            if rep.sequence == sequence and rep.academic_year == academic_year:
                                rep.results.add(res)
                                rep.save()
                                stud.save()

        if sequence == '2 eme Sequence' or sequence == '4 eme Sequence' or sequence == '6 eme Sequence':
            print('here')
            for stud in students:
                report_card = Report_card.objects.create()
                report_card.sequence = sequence
                report_card.academic_year = academic_year
                report_card.student_name = str(stud.first_name)
                report_card.classroom = classroom
                report_card.save()
                stud.report_card.add(report_card)
                stud.save()
                for res in Result.objects.all():
                    if res.student == stud and res.sequence2 == sequence and res.academic_year == academic_year:
                        for rep in stud.report_card.all():
                            if rep.sequence == sequence and rep.academic_year == academic_year:
                                rep.results.add(res)
                                rep.save()
                                stud.save()

    else:
        pass

    return render(request, 'teacher/upload_notes.html', context)


def student_results_detail(request):
    course_id = request.GET.get('course_id')
    sequence = request.GET.get('sequence')
    teacher_sequence_id = request.GET.get('teacher_sequence_id')
    academic_year = request.GET.get('academic_year')
    all_students = Student.objects.all()
    course = Course.objects.get(id=course_id)
    all_results = Result.objects.all()
    results = []

    if sequence != '2 eme Sequence' and sequence != '4 eme Sequence' and sequence != '6 eme Sequence':
        for result in all_results:
            if result.course == course and result.sequence == sequence and result.academic_year == academic_year:
                messages.success(request, "Les resultats de " + str(
                    course.name) + " de la " + sequence + " - (" + academic_year + ") !",
                                 extra_tags='success')
                results.append(result)

    if sequence == '2 eme Sequence' or '4 eme Sequence' or '6 eme Sequence':
        for result in all_results:
            if result.course == course and result.sequence2 == sequence and result.academic_year == academic_year:
                messages.success(request, "Les resultats de " + str(
                    course.name) + " de la " + sequence + " - (" + academic_year + ") !",
                                 extra_tags='success')
                results.append(result)

    context = {
        'course': course,
        'results':results,
        'sequence':sequence,
        'academic_year':academic_year,
        'teacher_sequence_id':teacher_sequence_id
            }
    return render(request,'teacher/student_results_detail.html',context)

def save_student_notes(request):
    coeff_total2=0
    greate_total=0
    greate_total2=0
    coeff_total=0
    course_id = request.GET.get('course_id')
    course = Course.objects.get(id=course_id)
    print(course)
    all_students = course.classroom.students.all()
    sequence = request.GET.get('sequence')
    academic_year = request.GET.get('academic_year')
    marks = request.GET.getlist('mark')
    teacher_sequence_id = request.GET.get('teacher_sequence_id')
    teacher_sequence = TeacherSequence.objects.get(id=teacher_sequence_id)

    students = []
    all_results = Result.objects.all()
    results = []
    a = -1
    average_mark = 0
    if sequence != '1 ere Sequence' and sequence != '3 eme Sequence' and sequence != '5 eme Sequence':
        for result in all_results:
            if result.course == course and result.academic_year == academic_year and result.sequence2 == sequence:
                a = a + 1
                minimum = min(marks)
                maximum = max(marks)
                avg = (float(minimum) + float(maximum)) / 2

                data = list(enumerate(marks, start=1))
                data = list(sorted(data, key=lambda x: x[1], reverse=True))
                data = list(enumerate(data, start=1))
                data = list(sorted(data, key=lambda x: x[1][0]))
                rank_list = []
                for x in data:
                    rank_list.append(x[0])

                result.rank2 = rank_list[a]
                result.mark2 = marks[a]
                result.total2 = float(result.mark2) * float(result.course.coeff)
                average_mark = (float(result.mark) + float(result.mark2))/2 
                result.average_mark = average_mark
                total2 = float(average_mark) * float(result.course.coeff)
                result.total2 = total2
                result.max2 = maximum
                result.min2 = minimum
                result.avg2 = avg
                result.save()
                results.append(result)

        for student in all_students:
            for rep in student.report_card.all():
                print(rep.sequence)
                print(rep.academic_year)
                if sequence != '1 ere Sequence' and sequence != '3 eme Sequence' and sequence != '5 eme Sequence':
                    if rep.sequence == sequence and rep.academic_year == academic_year and rep.classroom == course.classroom:
                        print('loop 2')
                        for result in rep.results.all():
                            print('loop 3')
                            coeff_total2 = float(result.course.coeff) + coeff_total2
                            greate_total2 = float(result.total2) + float(greate_total2)
                        average2 = float(greate_total2) / float(coeff_total2)
                        average2 = average2.__round__(2)
                        rep.average2 = average2
                        rep.save()


    if sequence == '1 ere Sequence' or '3 eme Sequence' or '5 eme Sequence':
        for result in all_results:
            if result.course == course and result.academic_year == academic_year and result.sequence == sequence:
                a = a + 1
                minimum = min(marks)
                maximum = max(marks)
                avg = (float(minimum) + float(maximum)) / 2

                result.mark = marks[a]
                result.max = maximum
                result.min = minimum
                result.avg = avg
                result.save()

                data = list(enumerate(marks, start=1))
                data = list(sorted(data, key=lambda x: x[1], reverse=True))
                data = list(enumerate(data, start=1))
                data = list(sorted(data, key=lambda x: x[1][0]))
                rank_list = []
                for x in data:
                    rank_list.append(x[0])

                result.rank = rank_list[a]
                total = float(result.mark) * float(result.course.coeff)
                result.total = total
                result.save()
                results.append(result)

        for student in all_students:
            for rep in student.report_card.all():
                if rep.sequence == sequence and rep.academic_year == academic_year and rep.classroom == course.classroom:
                    for result in rep.results.all():
                        coeff_total = float(result.course.coeff) + coeff_total
                        greate_total = float(result.total) + float(greate_total)

                    average = int(greate_total) / int(coeff_total)
                    average = average.__round__(2)
                    rep.average = average
                    rep.save()
    messages.success(request,'Les notes on ete enregistrees avec succes !', extra_tags='success')
    context = {
        'results': results,
        'sequence': sequence,
        'academic_year': academic_year,
        'teacher_sequence': teacher_sequence,
        'course': course
    }

    return render(request, 'teacher/upload_notes.html', context)

def download_student_result(request):
    global course
    result_id = request.GET.get('teacher_sequence_id')
    teacher_result = TeacherSequence.objects.get(id=result_id)
    all_results = Result.objects.all()
    sequence = request.GET.get('sequence')
    academic_year = request.GET.get('academic_year')
    print(sequence)
    print(academic_year)

    results = []
    for result in all_results:
        if sequence == '1 ere Sequence' or '3 eme Sequence' or '5 eme Sequence':
            if result.sequence == teacher_result.sequence and result.academic_year == teacher_result.academic_year:
                if result.course == teacher_result.course:
                    results.append(result)
                    academic_year = result.academic_year
                    sequence = result.sequence
                    course = result.course

        if sequence != '1 ere Sequence' and sequence != ' 3 eme Sequence' or sequence != '5 eme Sequence':
            if result.sequence2 == teacher_result.sequence and result.academic_year == teacher_result.academic_year:
                if result.course == teacher_result.course:
                    results.append(result)
                    academic_year = result.academic_year
                    sequence = result.sequence2
                    course = result.course

    context = {
        'results': results,
        'academic_year':academic_year,
        'sequence':sequence,
        'course':course
        }
    pdf = render_to_pdf('teacher/download_student_result.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def download_sorted_student_result(request):
    global course
    result_id = request.GET.get('teacher_sequence_id')
    choice = request.GET.get('choice')
    teacher_result = TeacherSequence.objects.get(id=result_id)
    all_results = Result.objects.all()
    sequence = ''
    academic_year = ''
    class_name = ''

    results = []
    if choice == 'ordre alphabetique':
        for result in all_results.order_by('student_name'):
            if result.sequence == teacher_result.sequence and result.academic_year == teacher_result.academic_year:
                if result.course == teacher_result.course:
                        results.append(result)
                        academic_year = result.academic_year
                        sequence = result.sequence
                        course = result.course
        context = {
            'results': results,
            'academic_year': academic_year,
            'sequence': sequence,
            'course': course,
        }
        pdf = render_to_pdf('teacher/download_student_result.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

    if choice == 'ordre de merit':
        for result in all_results.order_by('-mark'):
            if result.sequence == teacher_result.sequence and result.academic_year == teacher_result.academic_year:
                if result.course == teacher_result.course:
                    results.append(result)
                    academic_year = result.academic_year
                    sequence = result.sequence
                    course = result.course


        context = {
            'results': results,
            'academic_year':academic_year,
            'sequence':sequence,
            'course':course,
        }
        pdf = render_to_pdf('teacher/download_student_result.html', context)
        return HttpResponse(pdf, content_type='application/pdf')

def t_reportcard_chose_class(request):
    object_list = []
    for course in Course.objects.all():
        if course.teacher == request.user:
            if course.classroom in object_list:
                pass
            else:
                object_list.append(course.classroom)

    context = {
        'object_list': object_list
    }
    return render(request, 'teacher/t_reportcard_chose_class.html',context)

def reportcard_class_sorted_list(request):
    cathegory = request.GET.get('cathegory')
    print(cathegory)
    context = {}
    if cathegory == 'anglophone' or 'francophone':
        object_list = Classroom.objects.filter(section=cathegory)
        context = {'object_list': object_list}
    else:
        pass
    return render(request,'teacher/t_reportcard_chose_class.html',context)


def s_classes(request):
    return render(request, 'teacher/s_classes.html')

def add_hours(request):
    return render(request, 'teacher/add_hours.html')

def upload_hours_home(request):
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)
    context = {
        'classroom' : classroom
    }
    return render(request, 'teacher/upload_hours_home.html', context)

def upload_hours(request):
    sequence = request.GET.get('sequence')
    year = request.GET.get('year')
    class_id = request.GET.get('class_id')
    classroom = Classroom.objects.get(id=class_id)

    for generalhours in GeneralAbsentHours.objects.all():
        if generalhours.sequence == sequence and generalhours.year == year and generalhours.classroom == classroom:
            messages.error(request, "Les heures d'absences de la "+str(classroom.name)+ " * "+str(sequence)+ " ( "+ str(year)+" ) ont deja ete ajoutees !")
            context = {
                'sequence': sequence,
                'year': year,
                'classroom': classroom
            }
            return render(request, 'teacher/upload_hours.html', context)
        else:
            pass

    generalhours = GeneralAbsentHours.objects.create()
    generalhours.year = year
    generalhours.sequence = sequence
    generalhours.classroom = classroom
    generalhours.save()
    for student in classroom.students.all():
        hour = AbsentHours.objects.create()
        hour.year = year
        hour.sequence = sequence
        hour.save()
        student.absent_hours.add(hour)
        student.save()

    context = {
        'sequence':sequence,
        'year':year,
        'classroom':classroom
    }
    return render(request, 'teacher/upload_hours.html',context)

def save_hours(request):
    sequence = request.GET.get('sequence')
    year = request.GET.get('year')
    class_id = request.GET.get('class_id')
    classroom = Classroom.objects.get(id=class_id)
    hours = request.GET.getlist('hours')
    hr = request.GET.getlist('hr')
    jr = request.GET.getlist('jr')
    consignes = request.GET.getlist('conclusions')
    i = 0

    for student in classroom.students.all():
        for hour in student.absent_hours.all():
            if hour.year == year and hour.sequence == sequence:
                hour.hours_no = hours[i]
                hour.save()
                student.save()

                for des in ExclusionHours.objects.all():
                    if int(hour.hours_no) >= int(des.hours) and int(hour.hours_no) <= int(des.hours2):
                        hour.hr_exclusions = des.ex_hours
                        hour.save()
                for des in ExclusionDays.objects.all():
                    if int(hour.hours_no) >= int(des.hours) and int(hour.hours_no) <= int(des.hours2):
                        hour.jr_exclusions = des.ex_days
                        hour.save()

                council = DisciplinaryCouncil.objects.get(name='exclusion definitive')
                if int(hour.hours_no) >= int(council.hours):
                    hour.def_exclusion = True
                    hour.save()

                council = DisciplinaryCouncil.objects.get(name='convocation')
                if int(hour.hours_no) >= int(council.hours):
                    hour.convocation = True
                    hour.save()

                i = i+1
    messages.success(request, "Les heures d'absences ont ete enregistrees avec succes ! ", extra_tags='success')
    context = {
        'sequence': sequence,
        'year': year,
        'classroom': classroom
    }
    return render(request, 'teacher/hour_list.html', context)

def class_hour_list(request):
    return render(request, 'teacher/class_hour_list.html')

def class_hours(request):
    all_hours = GeneralAbsentHours.objects.all()
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)
    context = {
        'all_hours' : all_hours,
        'classroom': classroom
    }
    return render(request, 'teacher/class_hours.html', context)

def hour_list(request):
    class_id = request.GET.get('id')
    year = request.GET.get('year')
    sequence = request.GET.get('sequence')
    classroom = Classroom.objects.get(id=class_id)

    context = {
        'classroom':classroom,
        'year' :year,
        'sequence':sequence
    }
    return render(request, 'teacher/hour_list.html', context)

def download_hour_list(request):
    class_id = request.GET.get('id')
    year = request.GET.get('year')
    sequence = request.GET.get('sequence')
    classroom = Classroom.objects.get(id=class_id)

    context = {
        'classroom': classroom,
        'year': year,
        'sequence': sequence
    }
    pdf = render_to_pdf('teacher/download_hour_list.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

def delete_result(request):
    course_id = request.GET.get('id')
    result_id = request.GET.get('result_id')
    print(result_id)
    try:
        Teacherseq = TeacherSequence.objects.get(id=result_id)

    except ValueError:
        pass
    course = Course.objects.get(id=course_id)
    sequence = Teacherseq.sequence
    year = Teacherseq.academic_year

    if sequence == '1 ere Sequence' or sequence == '3 eme Sequence' or sequence == '5 eme Sequence':
        for result in Result.objects.all():
            if result.course == course and result.academic_year == year and Teacherseq.sequence == sequence:
                result.delete()

    if sequence != '1 ere Sequence' and sequence != '3 eme Sequence' and sequence != '5 eme Sequence':
        for result in Result.objects.all():
            if result.course == course and result.academic_year == year and result.sequence2 == sequence:
                result.delete()
    if sequence == '1 ere Sequence' or sequence == '3 eme Sequence' or sequence == '5 eme Sequence':
        messages.success(request, "Les resultats de "+str(Teacherseq.course.name)+" de la "+str(Teacherseq.sequence)+" ont ete suprimmes avec success", extra_tags='success')

    if sequence != '1 ere Sequence' and sequence != '3 eme Sequence' and sequence != '5 eme Sequence':
        messages.success(request, "Les resultats de "+str(Teacherseq.course.name)+" de la "+str(Teacherseq.sequence2)+" ont ete suprimmes avec success", extra_tags='success')

    Teacherseq.delete()
    results = []
    for result in TeacherSequence.objects.all():
        if result.course == course:
            results.append(result)

    context = {
        'course': course,
        'results': results
    }
    return render(request,'teacher/teacher_results_detail.html',context)

