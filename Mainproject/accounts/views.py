from django.shortcuts import render,redirect
from django.contrib.auth.models import Group
from accounts.forms import AddTeacherForm,AddcollegueForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponse
from accounts.models import Teacher
from administration.models import Department,Classroom,Course
from django.views.generic import DetailView
# Create your views here.

def register_home(request):
    return render(request,'accounts/register_home.html')

def register(request):
    group_name = request.GET.get('group_name')
    print(group_name)
    form = AddTeacherForm()
    departments = Department.objects.all()
    if request.method == 'POST':
        form = AddTeacherForm(request.POST)
        if form.is_valid():
            date_of_birth = request.POST.get('date_of_birth')
            department_names = request.POST.getlist('department')
            department_list = []

            if department_list == []:
                pass
            else:
                for name in department_names:
                    department = Department.objects.get(name=name)
                    department_list.append(department)

            user = form.save()
            for dep in department_list:
                user.department.add(dep)
                user.save()

            user.date_if_birth = date_of_birth
            user.is_authorized = False
            user_group = Group.objects.get_or_create(name=group_name)
            user_group[0].user_set.add(user)
            user.save()
            messages.info(request, 'Attendez que votre compte soit valide par le principal !', extra_tags='info')
            return redirect('login')
    context = {
        'form': form,
        'departments': departments,
        'group_name':group_name
    }
    return render(request, 'accounts/register_teacher.html', context)

def loginview(request):
    phone_no = request.POST.get('phone_no')
    password = request.POST.get('password')
    user = authenticate(request, phone_no=phone_no, password=password)
    if user is not None:
        login(request, user)
        if user.is_authorized == False:
            messages.info(request,"Desole! Votre compte n'a pas encore valide par le principal!",extra_tags="info")
            return redirect('login')
        else:
            gender = user.gender
            name = user.first_name
            name = name.upper()
            if gender == 'masculin':
                messages.success(request,'Bienvenue Monsieur. '+str(name)+' sur PURPLE', extra_tags='success')
                return redirect('home')
            elif gender == 'feminin':
                messages.success(request,'Bienvenue Madamme. '+str(name)+' sur PURPLE', extra_tags='success')
                return redirect('home')
    else:
        messages.error(request, "Verifiez votre nom d'utilisateur et votre mot de passe, puis reessayez !" ,extra_tags='error')
    return render(request,'accounts/login.html')

def logoutview(request):
    logout(request)
    return render(request,'index.html')

def add_collegue(request):
    form = AddcollegueForm()
    group_name = request.GET.get('group_name')
    departments = Department.objects.all()
    if request.method == 'POST':
        form = AddcollegueForm(request.POST)
        if form.is_valid():
            department = request.POST.getlist('department')
            censeur_group = Group.objects.get_or_create(name='censeur')
            teacher_group = Group.objects.get_or_create(name='enseignant')
            intendant_group = Group.objects.get_or_create(name='intendant')
            surveillant_group = Group.objects.get_or_create(name='surveillant')
            user = form.save()
            user.is_authorized = True
            user.save()
            if group_name == 'censeur':
                for dep in department:
                    depart = Department.objects.get(name=dep)
                    user.department.add(depart)
                    user.save()

                censeur_group[0].user_set.add(user)
                messages.success(request, 'Le compte ' + group_name + ' à été créé avec succès.',extra_tags='success')
                return redirect('collegue list')

            elif group_name == 'enseignant':
                for dep in department:
                    depart = Department.objects.get(name=dep)
                    user.department.add(depart)
                    user.save()

                user.save()
                teacher_group[0].user_set.add(user)
                messages.success(request, 'Le compte ' + group_name + ' à été créé avec succès.', extra_tags='success')
                return redirect('collegue list')

            elif group_name == 'intendant':
                intendant_group[0].user_set.add(user)
                messages.success(request, 'Le compte ' + group_name + ' à été créé avec succès.', extra_tags='success')
                return redirect('collegue list')

            elif group_name == 'surveillant general':
                surveillant_group[0].user_set.add(user)
                messages.success(request, 'Le compte ' + group_name + ' à été créé avec succès.', extra_tags='success')
                return redirect('collegue list')

            else:
                pass

            user.is_authorized = True
            user.save()
            messages.success(request,'Compte cree avec succes !',extra_tags='success')
            return redirect('add collegue home')

    context={
        'form':form,
        'departments':departments,
        'group_name':group_name
    }
    return render(request,'accounts/add_collegue.html',context)

def add_collegue_home(request):
    teachers = Teacher.objects.filter(is_authorized=False)
    context = {
        'teachers': teachers
    }
    return render(request,'accounts/add_collegue_home.html',context)

def add_collegue_detail(request):
    id=request.GET.get('id')
    teacher=Teacher.objects.get(id=id)
    context={
        'teacher':teacher
    }
    return render(request,'accounts/add_collegue_detail.html',context)

def confirm_success(request):
    id = request.GET.get('id')
    teacher = Teacher.objects.get(id=id)
    teacher.is_authorized = True
    teacher.save()
    messages.success(request,"Compte comfirme avec succes !",extra_tags='success')
    return redirect('add collegue')

def collegue_list(request):
    teachers = Teacher.objects.filter(is_authorized = True)
    context = {
        'teachers':teachers
    }
    return render(request,'accounts/collegue_list.html',context)

def collegue_sorted_list(request):
    cathegory = request.GET.get('cathegory')
    context ={}
    if cathegory == 'enseignant' or 'surveillant general' or 'intendant':
        teachers = Teacher.objects.filter(groups__name=str(cathegory))
        context = {
            'teachers': teachers
        }
    if cathegory == 'masculin':
        teachers = Teacher.objects.filter(gender='masculin')
        context = {
            'teachers': teachers
        }
    if cathegory == 'feminin':
        teachers = Teacher.objects.filter(gender='feminin')
        context = {
            'teachers': teachers
        }
    return render(request, 'accounts/collegue_list.html', context)


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

def my_account(request):
    all_courses = Course.objects.all()
    teacher_courses = []
    for course in all_courses:
        if course.teacher == request.user:
            teacher_courses.append(course)

    context={
        'teacher_courses':teacher_courses
    }
    return render(request,'accounts/my_account.html',context)

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')

    else:
        form = PasswordChangeForm(request.user)
        return render(request, 'accounts/change_password.html', {'form': form})

def test(request):
    return render(request,'accounts/test.html')