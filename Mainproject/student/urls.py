from django.urls import path
from student.views import (add_student,pay_fee_home,student_class_list,student_detail,modify_student,modify_student_done,
        student_class_search_results,student_class_sorted_list,student_list,Download_studentlist, student_card, honor_roll,
                           restore_student,deleted_students,delete_student,download_student_card)

urlpatterns = [
    path('add_student/', add_student, name='add student'),
    path('pay_fee_home/', pay_fee_home, name='pay fee home'),
    path('student_class_list/', student_class_list, name='student class list'),
    path('student_class_search_results/', student_class_search_results, name='student class search results'),
    path('student_class_sorted_list/', student_class_sorted_list, name='student class sorted list'),
    path('student_list/', student_list, name='student list'),
    path('student_detail/', student_detail, name='student detail'),
    path('student_list_pdf/',Download_studentlist,name='student list pdf'),
    path('modify_student/',modify_student, name='modify student'),
    path('student_card/',student_card, name='student card'),
    path('modify_student_done/', modify_student_done, name='modify student done'),
    path('honor_roll/', honor_roll, name='honor roll'),
    path('delete_student/', delete_student, name='delete student'),
    path('download_student_card/', download_student_card, name='download student card'),
    path('deleted_students/', deleted_students, name='deleted students'),
    path('restore_student/', restore_student, name='restore student'),
]
