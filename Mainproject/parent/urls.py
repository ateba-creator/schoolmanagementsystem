from django.urls import path
from parent.views import (my_children,children_detail,results_home,student_results,course_mark_detail,children_report_card,
                          contact_teacher,report_card_home)
urlpatterns = [
    path('my_children/', my_children, name='my children'),
    path('children_detail/', children_detail, name='children detail'),
    path('results_home/', results_home, name='results home'),
    path('student_results/', student_results, name='student results'),
    path('course_mark_detail/',course_mark_detail,name='course mark detail'),
    path('children_report_card/',children_report_card,name='children report card'),
    path('contact_teacher/',contact_teacher,name='contact teacher'),
    path('report_card_home/',report_card_home,name='report card home')
]
