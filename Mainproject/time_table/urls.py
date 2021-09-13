from django.contrib import admin
from django.urls import path, include
from. import views

urlpatterns = [
    path('fill_hours_chose_class', views.fill_hours_chose_class, name='fill hours chose class'),
    path('timetable_generation/', views.timetable, name='timetable'),
    path('fill_hours_class_search_results/', views.fill_hours_class_search_results.as_view(), name='fill hours class search results'),
    path('fill_hours_class_sorted_list/', views.fill_hours_class_sorted_list, name='fill hours class sorted list'),
    path('course_course_list/',views.class_course_list, name='class course list'),
    path('save_class_hours/', views.save_class_hours, name='save class hours')
]
