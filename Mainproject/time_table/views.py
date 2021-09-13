from django.shortcuts import render, redirect
from django.views.generic import ListView
from. forms import *
from django.contrib import messages
from.models import Room, MeetingTime, Lecture
from administration.models import Course, Department, Classroom
from accounts.models import Teacher
from django.db.models import Q


POPULATION_SIZE = 9
NUMB_OF_ELITE_SCHEDULES = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.05


class Data:
    def __init__(self):
        self._rooms = Room.objects.all()
        self._meetingTimes = MeetingTime.objects.all()
        self._teachers = Teacher.objects.all()
        self._courses = Course.objects.all()
        self._depts = Department.objects.all()

    def get_rooms(self): return self._rooms

    def get_teachers(self): return self._teachers

    def get_courses(self): return self._courses

    def get_depts(self): return self._depts

    def get_meetingTimes(self): return self._meetingTimes


class Schedule:
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNumb = 0
        self._isFitnessChanged = True

    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes

    def get_numbOfConflicts(self): return self._numberOfConflicts

    def get_fitness(self):
        if self._isFitnessChanged:
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness

    def initialize(self):
        lectures = Lecture.objects.all()
        for lecture in lectures:
            dept = lecture.department
            n = lecture.num_class_in_week
            if n <= len(MeetingTime.objects.all()):
                class_courses = []
                courses = []
                for course in Course.objects.all():
                    if course.classroom == lecture.classroom:
                        class_courses.append(course)
                for course in class_courses:
                    for dep in course.department.all():
                        if dep == dept:
                            courses.append(course)

                for course in courses:
                    print(course.name)
                    for i in range(n // len(courses)):
                        newClass = Class(self._classNumb, dept, lecture.id, course)
                        self._classNumb += 1
                        newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, len(MeetingTime.objects.all()))])
                        newClass.set_room(course.classroom.room)
                        newClass.set_teacher(course.teacher)
                        self._classes.append(newClass)

            else:
                n = len(MeetingTime.objects.all())
                courses = []
                for course in Course.objects.all():
                    if course.classroom == lecture.classroom:
                        courses.append(course)

                for course in courses:
                    for i in range(n // len(courses)):
                        newClass = Class(self._classNumb, dept, lecture.id, course)
                        self._classNumb += 1
                        newClass.set_meetingTime(data.get_meetingTimes()[rnd.randrange(0, len(MeetingTime.objects.all()))])
                        newClass.set_room(course.classroom.room)
                        newClass.set_teacher(course.teacher)
                        self._classes.append(newClass.lecture)

        return self

    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(len(classes)):
            for j in range(len(classes)):
                if j >= i:
                    if (classes[i].meeting_time == classes[j].meeting_time) and (classes[i].lecture_id != classes[j].lecture_id) and (classes[i].lecture == classes[j].lecture):
                        if (classes[i].room == classes[j].room) and (classes[i].lecture_id != classes[j].lecture_id) and (classes[i].lecture == classes[j].lecture):
                            self._numberOfConflicts += 1
                        if classes[i].room == classes[j].room:
                            self._numberOfConflicts += 1
                        if classes[i].teacher == classes[j].teacher:
                            self._numberOfConflicts += 1

        return 1 / (1.0 * self._numberOfConflicts + 1)


class Population:
    def __init__(self, size):
        self._size = size
        self._data = data
        self._schedules = [Schedule().initialize() for i in range(size)]

    def get_schedules(self):
        return self._schedules


class GeneticAlgorithm:
    def evolve(self, population):
        return self._mutate_population(self._crossover_population(population))

    def _crossover_population(self, pop):
        crossover_pop = Population(0)
        for i in range(NUMB_OF_ELITE_SCHEDULES):
            crossover_pop.get_schedules().append(pop.get_schedules()[i])
        i = NUMB_OF_ELITE_SCHEDULES
        while i < POPULATION_SIZE:
            schedule1 = self._select_tournament_population(pop).get_schedules()[0]
            schedule2 = self._select_tournament_population(pop).get_schedules()[0]
            crossover_pop.get_schedules().append(self._crossover_schedule(schedule1, schedule2))
            i += 1
        return crossover_pop

    def _mutate_population(self, population):
        for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
            self._mutate_schedule(population.get_schedules()[i])
        return population

    def _crossover_schedule(self, schedule1, schedule2):
        crossoverSchedule = Schedule().initialize()
        for i in range(0, len(crossoverSchedule.get_classes())):
            if rnd.random() > 0.5:
                crossoverSchedule.get_classes()[i] = schedule1.get_classes()[i]
            else:
                crossoverSchedule.get_classes()[i] = schedule2.get_classes()[i]
        return crossoverSchedule

    def _mutate_schedule(self, mutateSchedule):
        schedule = Schedule().initialize()
        for i in range(len(mutateSchedule.get_classes())):
            if MUTATION_RATE > rnd.random():
                mutateSchedule.get_classes()[i] = schedule.get_classes()[i]
        return mutateSchedule

    def _select_tournament_population(self, pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_schedules().append(pop.get_schedules()[rnd.randrange(0, POPULATION_SIZE)])
            i += 1
        tournament_pop.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        return tournament_pop


class Class:
    def __init__(self, id, dept, lecture, course):
        self.lecture_id = id
        self.department = dept
        self.course = course
        self.teacher = None
        self.meeting_time = None
        self.room = None
        self.lecture = lecture

    def get_id(self): return self.lecture.id

    def get_dept(self): return self.department

    def get_course(self): return self.course

    def get_teacher(self): return self.teacher

    def get_meetingTime(self): return self.meeting_time

    def get_room(self): return self.room

    def set_teacher(self, teacher): self.teacher = teacher

    def set_meetingTime(self, meetingTime): self.meeting_time = meetingTime

    def set_room(self, room): self.room = room


data = Data()

def context_manager(schedule):
    classes = schedule.get_classes()
    context = []
    cls = {}
    for i in range(len(classes)):
        cls["lecture"] = classes[i].lecture.id
        cls['dept'] = classes[i].department.name
        cls['course'] = f'{classes[i].course.name} ({classes[i].course.id}, ' \
                        f'{classes[i].course.max_numb_students}'
        cls['room'] = f'{classes[i].room.r_number} ({classes[i].room.seating_capacity})'
        cls['teacher'] = f'{classes[i].teacher.first_name} ({classes[i].teacher.id})'
        cls['meeting_time'] = [classes[i].meeting_time.pid, classes[i].meeting_time.day, classes[i].meeting_time.time]
        context.append(cls)
    return context


def timetable(request):
    schedule = []
    population = Population(POPULATION_SIZE)
    generation_num = 0
    population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
    geneticAlgorithm = GeneticAlgorithm()
    while population.get_schedules()[0].get_fitness() != 1.0:
        generation_num += 1
        print('\n> Generation #' + str(generation_num))
        population = geneticAlgorithm.evolve(population)
        population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)
        schedule = population.get_schedules()[0].get_classes()

    present_timetables = Timetable.objects.all()
    for a_tb in present_timetables:
        if a_tb == None:
            pass
        else:
            a_tb.delete()
    for data in schedule:
        new_timetable = Timetable.objects.create()
        new_timetable.class_id = data.lecture_id
        new_timetable.course = data.course.name
        new_timetable.room = data.room.room_name
        new_timetable.teacher = data.teacher.first_name
        new_timetable.day = data.meeting_time.day
        new_timetable.time = data.meeting_time.time
        new_timetable.save()

    context = {
        'schedule': schedule,
        'lectures': Lecture.objects.all(),
        'times': MeetingTime.objects.all(),
        'classrooms': Classroom.objects.all()
    }
    return render(request, 'timetable/timetable.html', context)

def fill_hours_chose_class(request):
    object_list = Classroom.objects.all()
    context = {
        'object_list':object_list
    }
    return render(request, 'timetable/fill_hours_chose_class.html', context)

class fill_hours_class_search_results(ListView):
    model = Classroom
    template_name = 'timetable/fill_hours_chose_class.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Classroom.objects.filter(
            Q(name__icontains=query) | Q(section__icontains=query) | Q(group_type__icontains=query) | Q(
                studies_type__icontains=query)
        )
        return object_list


def fill_hours_class_sorted_list(request):
    cathegory = request.GET.get('cathegory')
    print(cathegory)
    context = {}
    if cathegory == 'anglophone' or 'francophone':
        object_list = Classroom.objects.filter(section=cathegory)
        context = {'object_list': object_list}
    else:
        pass
    return render(request,'timetable/fill_hours_chose_class.html',context)

def class_course_list(request):
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)

    courses = []
    for course in Course.objects.all():
        if course.classroom == classroom:
            courses.append(course)
    lectures = []

    for course in courses:
        for lecture in Lecture.objects.all():
            if lecture.classroom == course.classroom:
                pass
            else:
                new_lecture = Lecture.objects.create()
                for depart in course.department.all():
                    new_lecture.department = depart
                new_lecture.classroom = classroom
                new_lecture.save()
                for lecture in lectures:
                    if lecture.classroom != new_lecture.classroom:
                        lectures.append(new_lecture)
                    elif lecture.classroom == new_lecture.classroom:
                        pass

    context = {
        'courses': courses,
        'classroom': classroom,
        'lectures':lectures
    }
    return render(request, 'timetable/class_course_list.html',context)


def save_class_hours(request):
    class_id = request.GET.get('id')
    classroom = Classroom.objects.get(id=class_id)

    courses = []
    for course in Course.objects.all():
        if course.classroom == classroom:
            courses.append(course)
    lectures = []

    for lecture in Lecture.objects.all():
        if lecture.classroom == classroom:
            lectures.append(lecture)
            pass
        else:
            for course in courses:
                new_lecture = Lecture.objects.create()
                for depart in course.department.all():
                    new_lecture.department = depart

                new_lecture.classroom = classroom
                new_lecture.save()
                lectures.append(new_lecture)

    hours = request.GET.getlist('hours')
    a = 0
    for a_lecture in lectures:
        a_lecture.num_class_in_week = hours[a]
        a = a+1
        a_lecture.save()
    messages.success(request, 'Les heures de cours de la '+str(classroom.name) + ' ont ete enregistre avec succes !', extra_tags='success')
    context = {
        'courses': courses,
        'classroom': classroom,
        'lectures': lectures
    }
    return render(request, 'timetable/class_course_list.html',context)