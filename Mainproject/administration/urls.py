from django.urls import path,include
from administration.views import (add_department,add_classroom,add_course,assign_teacher,display_class_course_list,assign_choose_teacher,assign_teacher_done,
    course_detail,department_list,department_sorted_list,department_search_results,department_detail,
    class_list,class_search_results,chose_class_search_results,class_sorted_list,chose_class_sorted_list,
    class_detail,view_result_chose_class,reportcard_chose_class,chose_course,
    reportcard_class_sorted_list,reportcard_chose_class_search_results,class_reportcards,report_card_list,
    report_card_sorted_list,report_card_list_search_results,student_report_card,download_reportcard,
    assign_teacher_sorted_list,modify_class,modify_class_done,dates,add_date,delete_date,assign_main_teacher,chose_main_teacher,
    assign_main_teacher_done,assign_headmaster,remove_classroom, add_headmaster_class, assign_headmaster_done,headmaster_class_sorted_list,
    headmaster_class_search_results, class_council, disciplinary_council, delete_discipline, delete_council, results_sorted_list,
    honor_roll_list,search_result,modify_department,save_department,delete_course,delete_class, modify_course,save_course)

urlpatterns = [
    path('add_department/', add_department, name='add department'),
    path('add_classroom/', add_classroom, name='add classroom'),
    path('add_course/', add_course, name='add course'),
    path('assign_teacher/', assign_teacher, name='assign teacher'),
    path('display_class_course_list/', display_class_course_list, name='display class course list'),
    path('assign_choose_teacher/', assign_choose_teacher, name='assign choose teacher'),
    path('assign_teacher_done/', assign_teacher_done, name='assign teacher done'),
    path('course_detail/', course_detail, name='course detail'),
    path('department_list/', department_list, name='department list'),
    path('department_sorted_list/', department_sorted_list, name='department sorted list'),
    path('department_search_results/', department_search_results.as_view(), name='department search results'),
    path('department_detail/', department_detail, name='department detail'),
    path('class_list/', class_list, name='class list'),
    path('class_search_results/', class_search_results.as_view(), name='class search results'),
    path('chose_class_search_results/', chose_class_search_results.as_view(), name='chose class search results'),
    path('class_sorted_list/', class_sorted_list, name='class sorted list'),
    path('chose_class_sorted_list/', chose_class_sorted_list, name='chose class sorted list'),
    path('reportcard_class_sorted_list/', reportcard_class_sorted_list, name='reportcard chose class sorted list'),
    path('class_detail/', class_detail, name='class detail'),
    path('view_result_chose_class/', view_result_chose_class, name='view result chose class'),
    path('reportcard_chose_class/', reportcard_chose_class, name='reportcard chose class'),
    path('chose_course/', chose_course, name='chose course'),
    path('results_sorted_list/', results_sorted_list, name='results sorted list'),
    path('search_result/', search_result, name='search result'),
    path('reportcard_chose_class_search_results',reportcard_chose_class_search_results.as_view(), name='reportcard chose class search results'),
    path('class_reportcards/', class_reportcards, name='class reportcards'),
    path('report_card_list/', report_card_list, name='report card list'),
    path('report_card_sorted_list/', report_card_sorted_list, name='report card sorted list'),
    path('report_card_list_search_results',report_card_list_search_results, name='report card list search results'),
    path('student_report_card/',student_report_card, name='student report card'),
    path('download_student_report_card/', download_reportcard, name='download student report card'),
    path('assign_teacher_sorted_list/', assign_teacher_sorted_list, name='assign teacher sorted list'),
    path('modify_class',modify_class, name='modify class'),
    path('modify_class_done/', modify_class_done, name='modify class done'),
    path('dates/', dates, name='dates'),
    path('add_date/', add_date, name='add date'),
    path('delete_date/', delete_date, name='delete date'),
    path('assign_main_teacher/', assign_main_teacher, name='assign main teacher'),
    path('chose_main_teacher/', chose_main_teacher, name='chose main teacher'),
    path('assign_main_teacher_done/', assign_main_teacher_done, name='assign main teacher done'),
    path('assign_headmaster/', assign_headmaster, name='assign head master'),
    path('remove_class/', remove_classroom, name='remove class'),
    path('add_headmaster_class/', add_headmaster_class, name='add headmaster class'),
    path('assign_headmaster_done/', assign_headmaster_done, name='assign headmaster done'),
    path('headmaster_class_sorted_list/', headmaster_class_sorted_list, name='headmaster class sorted list'),
    path('headmaster_class_search_results/',headmaster_class_search_results.as_view(), name='headmaster class search results'),
    path('class_council/', class_council, name='class council'),
    path('disciplinary_council/', disciplinary_council, name='disciplinary council'),
    path('delete_discipline/', delete_discipline, name='delete discipline'),
    path('delete_council/', delete_council, name='delete council'),
    path('honor_roll_list/', honor_roll_list, name='honor roll list'),
    path('modify_department/', modify_department, name='modify department'),
    path('save_department/', save_department, name='save department'),
    path('delete_course/', delete_course, name='delete course'),
    path('delete_class/', delete_class, name='delete class'),
    path('modify_course/',modify_course, name='modify course'),
    path('save_course/', save_course, name='save course')
]