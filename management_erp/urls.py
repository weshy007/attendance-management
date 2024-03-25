from django.urls import path 

from . import views


urlpatterns = [ 
    path('', views.index, name='index'),
    path('accounts/logout/', views.logout_view, name='logout'),

    # STUDENT VIEWS URLS
    path('student/<uuid:student_id>/attendance/', views.attendance, name='attendance'),
    path('student/<uuid:student_id>/<uuid:course_id>/attendance/', views.attendance_detail, name='attendance_detail'),
    path('student/<uuid:student_id>/marks-list/', views.marks_list, name='marks_list'),

    # 
    path('student/<uuid:class_id>/timetable/', views.timetable, name='timetable'),

    # TEACHERS VIEWS URLS
    path('teacher/<uuid:teacher_id>/<uuid:choice>/classes/', views.t_class, name='t_clas'),
    path('teacher/<uuid:assign_id>/students/attendance/', views.t_student, name='t_student'),
    path('teacher/<uuid:assign_id>/class-dates/', views.t_class_date, name='t_class_date'),
    path('teacher/<uuid:ass_c_id>/cancel/', views.cancel_class, name='cancel_class'),
    path('teacher/<uuid:ass_c_id>/attendance/', views.t_attendance, name='t_attendance'),
    path('teacher/<uuid:ass_c_id>/edit-att/', views.edit_att, name='edit_att'),
    path('teacher/<uuid:ass_c_id>/attendance/confirm/', views.confirm, name='confirm'),
    path('teacher/<uuid:student_id>/<uuid:course_id>/attendance/', views.t_attendance_detail, name='t_attendance_detail'),
    path('teacher/<uuid:assign_id>/extra-class/', views.t_extra_class, name='t_extra_class'),
    path('teacher/<uuid:assign_id>/report/', views.t_report, name='t_report'),

    #
    path('teacher/<uuid:teacher_id>/t-timetable/', views.t_timetable, name='t_timetable'),
    path('teacher/<uuid:asst_id>/free-teachers/', views.free_teachers, name='free_teachers'),

    path('teacher/<uuid:assign_id>/marks-list/', views.t_marks_list, name='t_marks_list'),
    path('teacher/<uuid:marks_c_id>/marks-entry/', views.t_marks_entry, name='t_marks_entry'),
    path('teacher/<uuid:marks_c_id>/marks-entry/confirm/', views.marks_confirm, name='marks_confirm'),
    path('teacher/<uuid:marks_c_id>/edit-marks/', views.edit_marks, name='edit_marks'),
    path('teacher/<uuid:assign_id>/students/marks/', views.student_marks, name='t_student_marks'),
]