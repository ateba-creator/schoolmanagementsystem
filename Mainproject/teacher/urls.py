from django.urls import path
from teacher.views import (my_departments,my_classes,Download_studentlist,teacher_results,teacher_results_detail,
        upload_notes,save_student_notes,get_notes,download_student_result,student_results_detail,download_sorted_student_result,
         t_reportcard_chose_class, s_classes, add_hours, upload_hours, upload_hours_home, save_hours, class_hour_list,
        class_hours,hour_list,download_hour_list,delete_result)

urlpatterns = [
    path('my_departments/', my_departments, name='my departments'),
    path('my_classes/', my_classes, name='my classes'),
    path('download_studentlist/', Download_studentlist, name='download studentlist'),
    path('teacher_results/', teacher_results, name='teacher results'),
    path('teacher_results_detail/', teacher_results_detail, name='teacher results detail'),
    path('upload_notes/', upload_notes, name='upload notes'),
    path('get_notes/', get_notes, name='get notes'),
    path('save_student_notes/', save_student_notes, name='save student notes'),
    path('download_student_result/', download_student_result, name='download student result'),
    path('student_results_detail/', student_results_detail, name='student results detail'),
    path('download_sorted_student_result/', download_sorted_student_result, name='download sorted student result'),
    path('t_reportcard_chose_class/', t_reportcard_chose_class, name='t reportcard chose class'),
    path('s_classes/',s_classes, name='s classes'),
    path('add_hours/',add_hours, name='add hours'),
    path('upload_hours/',upload_hours, name='upload hours'),
    path('upload_hours_home/', upload_hours_home, name='upload hours home'),
    path('save_hours/', save_hours, name='save hours'),
    path('class_hour_list/', class_hour_list, name='class hour list'),
    path('class_hours/', class_hours, name='class hours'),
    path('hour_list/', hour_list, name='hour list'),
    path('download_hour_list/', download_hour_list, name='download hour list'),
    path('delete_result/',delete_result, name='delete result')
]