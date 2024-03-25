from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse
from django.utils import timezone

from .models import *

# Create your views here.
@login_required
def index(request):
    if request.user.is_lecturer:
        return render(request, 'info/t_homepage.html')
    if request.user.is_student:
        return render(request, 'info/homepage.html')
    return render(request, 'info/logout.html')

def logout_view(request):
    logout(request)
    # Redirect to a success page, or anywhere you want
    return redirect('index')

'''
ATTENDANCE VIEWS
'''

@login_required
def attendance(request, student_id):
    student = Student.objects.get(USN=student_id)
    assigned_list = Assign.objects.filter(class_id_id=student.class_id)
    attendance_list = []

    for assigned in assigned_list:
        try:
            attendance = AttendanceTotal.objects.get(student=student, course=assigned.course)
        except AttendanceTotal.DoesNotExist:
            attendance = AttendanceTotal(student=student, course=assigned.course)
            attendance.save()

        attendance_list.append(attendance)

    context = {
        'attendance_list': attendance_list,
    }
    
    return render(request, 'info/attendance.html', context)


@login_required
def attendance_detail(request, student_id, course_id):
    student = get_object_or_404(Student, USN=student_id)
    course = get_object_or_404(Course, id=course_id)
    attendance_list = Attendance.objects.filter(course=course, student=student).order_by('date')

    context = {
        'attendance_list': attendance_list, 
        'course': course,
    }

    return render(request, 'info/att_detail.html', context)
    

'''
TEACHER VIEWS
'''

@login_required
def t_class(request, teacher_id, choice):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    context = {
        'teacher': teacher, 
        'choice': choice
        }

    return render(request, 'info/t_clas.html', context)


@login_required
def t_student(request, assign_id):
    assigned = Assign.objects.get(id=assign_id)
    attendance_list = []

    for student in assigned.class_id.student_set.all():
        try:
            a = AttendanceTotal.objects.get(student=student, course=assigned.course)
        except AttendanceTotal.DoesNotExist:
            a = AttendanceTotal(student=student, course=assigned.course)
            a.save()
        attendance_list.append(a)

    context = {
        'attendance_list': attendance_list,
    }

    return render(request, 'info/t_students.html', context)


@login_required
def t_class_date(request, assign_id):
    now = timezone.now()
    assigned = get_object_or_404(Assign, id=assign_id)
    attendance_list = assigned.attendanceclass_set.filter(date__lte=now).order_by('-date')

    context = {
        'attendance_list': attendance_list
        }

    return render(request, 'info/t_class_date.html', context)


@login_required
def cancel_class(request, ass_c_id):
    assigned_class = get_object_or_404(AttendanceClass, id=ass_c_id)
    assigned_class = 2
    assigned_class.save()

    return HttpResponseRedirect(reverse('t_class_date', args=(assigned_class.assign_id,)))


@login_required
def t_attendance(request, ass_c_id):
    assigned_class = get_object_or_404(AttendanceClass, id=ass_c_id)
    assigned = assigned_class.assign
    c = assigned.class_id       # <---- Class assigned

    context = {
        'assigned_class': assigned_class,
        'c': c,
        'assigned': assigned
    }

    return render(request, 'info/t_attendance.html', context)

@login_required
def edit_att(request, ass_c_id):
    assigned_class = get_object_or_404(AttendanceClass, id=ass_c_id)
    course = assigned_class.assign.course
    attendance_list = Attendance.objects.filter(attendanceclass=assigned_class, course=course)

    context = {
        'assigned_class': assigned_class,
        'attendance_list': attendance_list
    }

    return render(request, 'info/t_edit_att.html', context)

@login_required
def confirm(request, ass_c_id):
    assigned_class = get_object_or_404(AttendanceClass, id=ass_c_id)
    assigned = assigned_class.assign
    course = assigned.course
    cl = assigned.class_id

    for i, s in enumerate(cl.student_set.all()):
        status = request.POST[s.USN]
        if status == 'present':
            status =  'True'
        else: 
            status = 'False'
        
        if assigned_class.status == 1:
            try:
                a = Attendance.objects.get(course=course, student=s, date=assigned_class.date, attendanceclass=assigned_class)
                a.status = status
                a.save()
            except Attendance.DoesNotExist:
                a = Attendance(course=course, student=s, status=status, date=assigned_class.date, attendanceclass=assigned_class)
                a.save()
                assigned_class.status = 1
                assigned_class.save()
        else:
            a = Attendance(course=course, student=s, status=status, date=assigned_class.date, attendanceclass=assigned_class)
            a.save()
            assigned_class.status = 1
            assigned_class.save()

    return HttpResponseRedirect(reverse('t_class_date', args=(assigned.id,)))


@login_required
def t_attendance_detail(request, student_id, course_id):
    student = get_object_or_404(Student, USN=student_id)
    course = get_object_or_404(Course, id=course_id)
    attendance_list = Attendance.objects.filter(course=course, student=student).order_by('date')

    context = {
        'attendance_list': attendance_list,
        'course': course
    }

    return render(request, 'info/t_att_detail.html', context)


@login_required
def change_att(request, att_id):
    attendance = get_object_or_404(Attendance, id=att_id)
    attendance = not attendance.status
    attendance.save()

    return HttpResponseRedirect(reverse('t_attendance_detail', args=(attendance.student.USN, attendance.course_id)))


@login_required
def t_extra_class(request, assign_id):
    assigned = get_object_or_404(Assign, id=assign_id)
    c = assigned.class_id

    context = {
        'assigned': assigned,
        'c': c
    }
    
    return render(request, 'info/t_extra_class.html', context)
    

@login_required
def e_confirm(request, assign_id):
    assinged = get_object_or_404(Assign, id=assign_id)
    course = assinged.course
    cl = assinged.class_id
    assigned_class = assinged.attendanceclass_set.create(status=1, date=request.POST['date'])
    assigned_class.save()

    for i, s in enumerate(cl.student_set.all()):
        status = request.POST[s.USN]
        if status == 'present':
            status = 'True'
        else:
            status = 'False'
        date = request.POST['date']
        a = AttendanceClass(course=course, student=s, status=status, date=date, attendanceclass=assigned_class)
        a.save()

    return HttpResponseRedirect(reverse('t_clas', args=(assinged.lecturer_id, 1)))


@login_required
def t_report(request, assign_id):
    assigned = get_object_or_404(Assign, id=assign_id)

    sc_list = []

    for student in assigned.class_id.student_set.all():
        a = StudentCourse.objects.get(student=student, course=assigned.course)
        sc_list.append(a)

    context = {
        'sc_list': sc_list
        }

    return render(request, 'info/t_report.html', context)


@login_required
def t_timetable(request, lecturer_id):
    assigned_time = AssignTime.objects.filter(assign__lecturer_id=lecturer_id)
    class_matrix = [[True for i in range(12)] for j in range(6)]

    for i, d in enumerate(DAYS_OF_WEEK):
        t = 0
        for j in range(12):
            if j == 0:
                class_matrix[i][0] = d[0]
                continue
            if j == 4 or j == 8:
                continue
            try:
                a = assigned_time.get(period=TIME_SLOTS[t][0], day=d[0])
                class_matrix[i][j] = a
            except AssignTime.DoesNotExist:
                pass
            t += 1

    context = {
        'class_matrix': class_matrix,
    }
    return render(request, 'info/t_timetable.html', context)


@login_required
def free_teachers(request, asst_id):
    assigned_time = get_object_or_404(AssignTime, id=asst_id)

    ft_list = []
    t_list = Teacher.objects.filter(assign__class_id__id=assigned_time.assign.class_id_id)

    for t in t_list:
        at_list = AssignTime.objects.filter(assign__teacher=t)
        if not any([True if at.period == assigned_time.period and at.day == assigned_time.day else False for at in at_list]):
            ft_list.append(t)

    context = {
        'ft_list': ft_list
        }

    return render(request, 'info/free_teachers.html', context)


'''
GENERAL VIEWS
'''
@login_required
def timetable(request, class_id):
    assigned_time = AssignTime.objects.filter(assign__class_id=class_id)
    matrix = [['' for i in range(5)] for j in range(5)]

    for i, (day, _) in enumerate(DAYS_OF_WEEK):
        t = 0

        for j in range(12):
            if j == 0:
                matrix[i][0] = day 
                continue
            if j == 4 or j == 8:
                continue
            try:
                a = assigned_time.get(period=TIME_SLOTS[t % len(TIME_SLOTS)][0], day=day) 
                matrix[i][j] = a.assign.course_id
            except AssignTime.DoesNotExist:
                pass
            t += 1

    context = {
        'matrix': matrix,
        }

    return render(request, 'info/timetable.html', context)


'''
STUDENT MARKS VIEWS
'''
@login_required
def marks_list(request, student_id):
    student = Student.objects.get(USN=student_id)
    assinged_list = Assign.objects.filter(class_id_id=student.class_id)
    student_c_list = []

    for assigned in assinged_list:
        try: 
            sc = StudentCourse.objects.get(student=student, course=assigned.course)
        except StudentCourse.DoesNotExist:
            sc =StudentCourse(student=student, course=assigned.course)
            sc.save()
            sc.marks_set.create(type='I', name='Internal test 1')
            sc.marks_set.create(type='I', name='Internal test 2')
            sc.marks_set.create(type='I', name='Internal test 3')
            sc.marks_set.create(type='E', name='Event 1')
            sc.marks_set.create(type='E', name='Event 2')
            sc.marks_set.create(type='S', name='Semester End Exam')

        student_c_list.append(sc)

    context = {
        'student_c_list': student_c_list,
        }

    return render(request, 'info/marks_list.html', context)


'''
TEACHERS MARKS VIEWS
'''
@login_required
def t_marks_list(request, assign_id):
    assigned = get_object_or_404(Assign, id=assign_id)
    marks_list = MarksClass.objects.filter(assign=assigned)

    context = {
        'marks_list': marks_list
        }

    return render(request, 'info/t_marks_list.html', context)


@login_required
def t_marks_entry(request, marks_c_id):
    marks_class = get_object_or_404(MarksClass, id=marks_c_id)
    assigned = marks_class.assign
    c = assigned.class_id

    context = {
        'ass': assigned,
        'c': c,
        'marks_class': marks_class,
    }
    return render(request, 'info/t_marks_entry.html', context)


@login_required
def marks_confirm(request, marks_c_id):
    marks_class = get_object_or_404(MarksClass, id=marks_c_id)
    assigned =  marks_class.assign
    cr = assigned.course
    cl = assigned.class_id

    for s in cl.student_set.all():
        mark = request.POST[s.USN]
        sc = StudentCourse.objects.get(course=cr, student=s)
        m = sc.marks_set.get(name=marks_class.name)
        m.marks1 = mark
        m.save()

        return HttpResponseRedirect(reverse('t_marks_list', args=(assigned.id,)))


@login_required
def edit_marks(request, marks_c_id):
    marks_class = get_object_or_404(MarksClass, id=marks_c_id)
    cr = marks_class.assign.course
    student_list =marks_class.assign.class_id.student_set.all()
    
    marks_list = []

    for student in student_list:
        sc = StudentCourse.objects.get(course=cr, student=student)
        marks = sc.marks_set.get(name=marks_class.name)
        
        marks_list.append(marks)

        context ={
            'marks_class': marks_class,
            'marks_list': marks_list
        }

        return render(request, 'info/edit_marks.html', context)
    

@login_required
def student_marks(request, assign_id):
    assined = Assign.objects.get(id=assign_id)
    sc_list = StudentCourse.objects.filter(student__in=assined.class_id.student_set.all(), course=assined.course)

    context = {
        'sc_list': sc_list,
        }

    return render(request, 'info/t_student_marks.html', context)