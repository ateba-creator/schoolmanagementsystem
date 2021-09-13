from django.shortcuts import render,redirect
from django.contrib import messages
from student.forms import AddStudentForm
from accounts.models import Teacher
from student.models import Student
from administration.models import Classroom,Course,Fee
from  django.views.generic import ListView,View
from academic.models import Date,Remark,Card
from django.db.models import Q
from django.contrib.auth.models import Group


from django.template.loader import get_template
from Mainproject.utils import render_to_pdf
from django.http import HttpResponse
# Create your views here.

def add_student(request):
    classes = Classroom.objects.all()
    form = AddStudentForm()
    all_teachers = Teacher.objects.all()
    dates = Date.objects.all()

    if request.method == 'POST':
        form = AddStudentForm(request.POST)
        year = request.POST.get('year')
        date_of_birth = request.POST.get('date_of_birth')
        if form.is_valid():
            class_name = request.POST.get('classroom_name')
            print(class_name)
            phone_no = form.cleaned_data.get('phone_no')
            first_name = request.POST.get('first_name')
            status = request.POST.get('status')
            first_name = first_name.upper()

            parent_name = request.POST.get('parent_name')
            parent_address = request.POST.get('parent_address')
            remark = request.POST.get('remark')

            last_name = request.POST.get('last_name')
            last_name = last_name.upper()
            student_class = Classroom.objects.get(name=class_name)
            for classroom in Classroom.objects.all():
                for stud in classroom.students.all():
                    if stud.first_name == first_name and stud.last_name == last_name:
                        context={
                            'student':stud,
                            'dates':dates
                        }
                        messages.error(request, first_name + " " + last_name + ' a deja ete inscrit en '+ str(classroom.name),extra_tags='error')
                        return render(request,'student/pay_fee_home.html',context)

            remark_obj = Remark.objects.create()
            remark_obj.remark = remark
            remark_obj.save()

            student = form.save()
            student.first_name = first_name
            student.last_name = last_name

            student.remark.add(remark_obj)
            student.status = status
            for course in Course.objects.all():
                if course.classroom == student_class:
                    student.course.add(course)
                    student.save()

            student.date_of_birth = date_of_birth
            new_fee = Fee.objects.create()
            new_fee.year = year
            new_year = Date.objects.create()
            new_year.date = year
            new_year.save()
            student.year.add(new_year)
            student.fee.add(new_fee)
            student.save()
            parent_group = Group.objects.get_or_create(name='parent')
            parentteacher = Group.objects.get_or_create(name='parentteacher')
            intendparent = Group.objects.get_or_create(name='intendparent')
            adminparent = Group.objects.get_or_create(name='adminparent')
            censeurparent = Group.objects.get_or_create(name='censeurparent')
            censeurparentteacher = Group.objects.get_or_create(name='censeurparentteacher')
            adminparentteacher = Group.objects.get_or_create(name='adminparentteacher')
            surveillantparent = Group.objects.get_or_create(name='surveillantparent')

            for teacher in all_teachers:
                if teacher.phone_no == phone_no:
                    for group in teacher.groups.all():
                        if group.name == 'administrateur':
                            group.user_set.remove(teacher)
                            adminparent[0].user_set.add(teacher)
                            teacher.save()
                            student.save()
                        if group.name == 'censeur':
                            group.user_set.remove(teacher)
                            censeurparent[0].user_set.add(teacher)
                            teacher.save()
                            student.save()
                        if group.name == 'enseignant':
                            group.user_set.remove(teacher)
                            parentteacher[0].user_set.add(teacher)
                            teacher.save()
                            student.save()
                        if group.name == 'intendant':
                            group.user_set.remove(teacher)
                            intendparent[0].user_set.add(teacher)
                            teacher.save()
                            student.save()

                        if group.name == 'adminteacher':
                            group.user_set.remove(teacher)
                            adminparentteacher[0].user_set.add(teacher)
                            teacher.save()
                            student.save()

                        if group.name == 'censeurteacher':
                            group.user_set.remove(teacher)
                            censeurparentteacher[0].user_set.add(teacher)
                            teacher.save()
                            student.save()

                        if group.name == 'surveillant general':
                            group.user_set.remove(teacher)
                            surveillantparent[0].user_set.add(teacher)
                            teacher.save()
                            student.save()

                        if group.name == 'adminparent' or 'parentteacher' or 'intendparent' or 'parent' or 'censeurparent':
                            student.parent = teacher
                            teacher.save()
                            student.save()

                    student.address = teacher.address
                    student.save()
                    student_class.students.add(student)
                    student_class.save()

                    context = {
                        'student': student,
                        'dates':dates
                    }
                    messages.success(request,"L'eleve "+first_name + " "+ last_name+ " a ete inscript avec succes en "+ class_name,extra_tags='success')
                    return render(request,'student/pay_fee_home.html',context)

            parent = Teacher.objects.create_user(phone_no,'00000000')
            parent_group[0].user_set.add(parent)
            parent.is_authorized = True
            parent.first_name = parent_name
            parent.address = parent_address
            parent.save()
            student.parent = parent
            student.fee.add(new_fee)
            student.save()
            student_class.students.add(student)
            student_class.save()

            messages.success(request, "L'eleve "+str(student.first_name) + ' ' + str(student.last_name)+' a ete inscript avec succes en '+class_name,extra_tags='success')
            context = {
                'student': student,
                'dates':dates
            }
            return render(request,'student/pay_fee_home.html',context)
        else:
            print(form.errors)

    context = {
        'form':form,
        'classes':classes
    }
    return render(request,'student/add_student.html',context)


def pay_fee_home(request):
    return render(request,'student/pay_fee_home.html')

def student_class_list(request):
    object_list = Classroom.objects.all()

    context={
        'object_list':object_list
    }
    return render(request,'student/student_class_list.html',context)


def student_class_search_results(request):
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)
    query = request.GET.get('q')
    students = classroom.students.filter(is_delete=False)
    object_list = students.filter(
        Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(date_of_birth__icontains=query) | Q(gender__icontains=query)
    )
    context={
        'object_list':object_list,
        'classroom':classroom
        }
    return render(request,'student/student_list.html',context)

def student_class_sorted_list(request):
    cathegory = request.GET.get('cathegory')
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)
    print(cathegory)
    context = {}
    students = classroom.students.filter(is_delete=False)
    if cathegory == 'masculin' or 'feminin':
        object_list = students.filter(gender=cathegory)
        context = {
            'object_list': object_list,
            'classroom':classroom
        }
    if cathegory == 'ordre alphabetique':
        object_list = students.all().order_by('first_name','last_name')
        context = {
            'object_list': object_list,
            'classroom': classroom
        }
    if cathegory == "pension non-paye":
        all_students = classroom.students.filter(is_delete=False)
        object_list = []
        for stud in all_students:
            for fee in stud.fee.all():
                print(fee.paid_fee)
                if fee.paid_fee == False:
                    object_list.append(stud)

        context = {
            'object_list': object_list,
            'classroom': classroom
        }
    if cathegory == 'pension paye':
        all_students = classroom.students.filter(is_delete=False)
        object_list = []
        for stud in all_students:
            for fee in stud.fee.all():
                if fee.paid_fee == True:
                    object_list.append(stud)

        context = {
            'object_list': object_list,
            'classroom': classroom
        }

    if cathegory == 'tous':
        object_list = classroom.students.filter(is_delete=False)
        context = {
            'object_list': object_list,
            'classroom': classroom
        }
    return render(request,'student/student_list.html',context)


def student_list(request):
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)
    object_list = classroom.students.filter(is_delete=False).order_by("first_name")

    context = {
        'object_list':object_list,
        'classroom': classroom
    }
    return render(request,'student/student_list.html',context)

def Download_studentlist(request):
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)
    object_list = classroom.students.filter(is_delete=False).order_by('first_name', 'last_name')
    context = {
        'object_list': object_list,
        'classroom': classroom
    }
    pdf = render_to_pdf('student/download_student_list.html', context)
    return HttpResponse(pdf, content_type='application/pdf')


def collegue_sorted_list(request):
    cathegory = request.GET.get('cathegory')
    if cathegory == 'tous':
        teachers = Teacher.objects.all()
        pass
    else:
        teachers = Teacher.objects.filter(groups__name = cathegory)
        pass
    context={
            'teachers':teachers
        }
    return render(request,'accounts/collegue_list.html',context)

def collegue_detail(request):
    teacher_id = request.GET.get('teacher_id')
    teacher = Teacher.objects.get(id=teacher_id)
    courses = Course.objects.all()
    teacher_courses=[]

    for course in courses.all():
        if course.teacher == teacher:
            teacher_courses.append(course)


    context={
        'teacher_courses':teacher_courses,
        'teacher':teacher
    }
    return render(request,'accounts/collegue_detail.html',context)

def student_detail(request):
    student_id = request.GET.get('student_id')
    student = Student.objects.get(id=student_id)
    global classroom
    all_classes = Classroom.objects.all()
    for new_class in all_classes:
        if student in new_class.students.all():
            classroom = new_class

    for fee in student.fee.all():
        if fee.paid_fee == True:
            num = int(len(student.cards.all()))
            if num >= 1:
                print('OK')
                for card in student.cards.all():
                    if card.year != fee.year:
                        print('OK')
                        student_card = Card.objects.create()
                        student_card.first_name = student.first_name
                        student_card.last_name = student.last_name
                        student_card.date_of_birth = student.date_of_birth
                        student_card.place_of_birth = student.place_of_birth
                        student_card.father_name = student.father_name
                        student_card.mother_name = student.mother_name
                        student_card.department = student.department
                        student_card.locality = student.locality
                        student_card.year = fee.year
                        student_card.nationality = student.nationality
                        student_card.parent_address = student.parent.address
                        student_card.classroom = classroom.name
                        student_card.matricule = student.matricule
                        student_card.save()
                        student.cards.add(student_card)
            else:
                student_card = Card.objects.create()
                student_card.first_name = student.first_name
                student_card.last_name = student.last_name
                student_card.date_of_birth = student.date_of_birth
                student_card.place_of_birth = student.place_of_birth
                student_card.father_name = student.father_name
                student_card.mother_name = student.mother_name
                student_card.department = student.department
                student_card.locality = student.locality
                student_card.year = fee.year
                student_card.nationality = student.nationality
                student_card.parent_address = student.parent.address
                student_card.classroom = classroom.name
                student_card.matricule = student.matricule
                student_card.save()
                student.cards.add(student_card)

    context = {
        'student':student,
        'classroom':classroom
    }
    return render(request,'student/student_detail.html',context)

def modify_student(request):
    student_id = request.GET.get('student_id')
    student = Student.objects.get(id=student_id)
    global classroom
    courses = []
    for new_class in Classroom.objects.all():
        if student in new_class.students.all():
            classroom = new_class
            classroom.save()
    print(classroom)
    for course in Course.objects.all():
        if course.classroom == classroom:
            courses.append(course)

    classrooms = Classroom.objects.all()
    context={
        'student':student,
        'classrooms': classrooms,
        'courses':courses,
        'classroom':classroom
    }
    return render(request,'student/modify_student.html',context)


def modify_student_done(request):
    student_id = request.GET.get('student_id')
    student = Student.objects.get(id=student_id)
    classroom_name = request.GET.get('classroom_name')
    classroom = Classroom.objects.get(name=classroom_name)
    all_classes = Classroom.objects.all()

    for a_class in all_classes:
        if student in a_class.students.all():
            a_class.students.remove(student)
            a_class.save()

    for new_class in all_classes:
        if student in new_class.students.all():
            classroom = new_class

    classroom.students.add(student)
    student.save()
    classroom.save()

    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    phone_no = request.GET.get('phone_no')
    address = request.GET.get('address')
    religion = request.GET.get('religion')
    date_of_birth = request.GET.get('date_of_birth')
    place_of_birth = request.GET.get('place_of_birth')
    parent_address = request.GET.get('parent_address')
    parent_first_name = request.GET.get('parent_first_name')
    parent_phone_no = request.GET.get('parent_phone_no')
    gender = request.GET.get('gender')
    school_of_origin = request.GET.get('school_of_origin')
    matricule = request.GET.get('matricule')
    department = request.GET.get('department')
    locality = request.GET.get('locality')
    status = request.GET.get('status')
    course_id = request.GET.getlist('course_id')

    for id in course_id:
        new_course = Course.objects.get(id=id)
        student.course.add(new_course)
        student.save()

    student.phone_no = phone_no
    student.address = address
    student.religion = religion
    student.first_name = first_name
    student.last_name = last_name
    student.date_of_birth = date_of_birth
    student.place_of_birth = place_of_birth
    student.parent.address = parent_address
    student.parent.first_name = parent_first_name
    student.parent.phone_no = parent_phone_no

    student.gender = gender
    student.school_of_origin = school_of_origin
    student.matricule = matricule
    student.department = department
    student.locality = locality
    student.status = status

    student.save()
    context={
        'student':student,
        'classroom':classroom
    }
    messages.success(request, 'Modifications enregistrees avec success !', extra_tags='success')
    return render(request, 'student/student_detail.html',context)

def student_card(request):
    card_id = request.GET.get('card_id')
    card = Card.objects.get(id=card_id)
    context = {
        'card':card
    }
    return render(request, 'student/student_card.html', context)

def honor_roll(request):
    student_id = request.GET.get('student_id')
    academic_year = request.GET.get('academic_year')
    sequence = request.GET.get('sequence')
    student = Student.objects.get(id=student_id)
    global roll
    for a_roll in student.honor_rolls.all():
        if a_roll.year == academic_year and a_roll.sequence == sequence:
            roll = a_roll
    context = {
        'roll':roll
    }
    return render(request, 'student/honor_roll.html',context)

def download_student_card(request):
    card_id = request.GET.get('card_id')
    card = Card.objects.get(id=card_id)
    context = {
        'card': card
    }
    pdf = render_to_pdf('student/download_student_card.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

def delete_student(request):
    class_id = request.GET.get('id')
    stud_id = request.GET.get('stud_id')
    student = Student.objects.get(id=stud_id)
    student.is_delete = True
    student.save()
    classroom = Classroom.objects.get(id=class_id)
    object_list = classroom.students.filter(is_delete=False).order_by("first_name")

    messages.info(request, "l'eleve "+str(student.first_name)+" "+str(student.last_name)+" a ete suprimme avec succes !", extra_tags='info')

    context = {
        'object_list': object_list,
        'classroom': classroom
    }
    return render(request,'student/student_list.html',context)

def deleted_students(request):
    object_list = Student.objects.filter(is_delete=True)
    context= {
        'object_list':object_list
    }
    return render(request, 'student/deleted_students.html',context)

def restore_student(request):
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)
    object_list = classroom.students.filter(is_delete=False).order_by("first_name")
    student_id = request.GET.get('student_id')
    student = Student.objects.get(id=student_id)
    student.is_delete = False
    student.save()
    messages.success(request, "L'eleve "+str(student.first_name)+ " "+ str(student.last_name)+" a ete retaure avec succes !",extra_tags='success')
    context = {
        'object_list': object_list,
        'classroom': classroom
    }
    return render(request, 'student/student_list.html', context)


