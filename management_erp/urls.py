from django.urls import path 

from . import views


urlpatterns = [ 
    path('', views.index, name='index'),
    # STUDENT VIEWS URLS
    path('student/<uuid:student_id>/attendance/', views.attendance, name='attendance'),
    path('student/<uuid:student_id>/<uuid:course_id>/attendance/', views.attendance_detail, name='attendance_detail'),
    path('student/<uuid:student_id>/marks_list/', views.marks_list, name='marks_list'),

    # 
    path('student/<uuid:class_id>/timetable/', views.timetable, name='timetable'),

    # TEACHERS VIEWS URLS
    path('teacher/<uuid:teacher_id>/<int:choice>/Classes/', views.t_class, name='t_clas'),
    path('teacher/<uuid:assign_id>/Students/attendance/', views.t_student, name='t_student'),

    path('teacher/<uuid:assign_id>/marks_list/', views.t_marks_list, name='t_marks_list'),
    path('teacher/<uuid:marks_c_id>/marks_entry/', views.t_marks_entry, name='t_marks_entry'),
    path('teacher/<uuid:marks_c_id>/marks_entry/confirm/', views.marks_confirm, name='marks_confirm'),
    path('teacher/<uuid:marks_c_id>/Edit_marks/', views.edit_marks, name='edit_marks'),
    path('teacher/<uuid:assign_id>/Students/Marks/', views.student_marks, name='t_student_marks'),

]