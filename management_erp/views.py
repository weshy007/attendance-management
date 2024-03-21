from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .models import *

# Create your views here.
@login_required
def index(request):
    if request.user.is_lecturer:
        return render(request, 'info/t_homepage.html')
    if request.user.is_student:
        return render(request, 'info/homepage.html')
    return render(request, 'info/logout.html')


def attendance(request, student_id):
    student = Student.objects.get(USN=student_id)
    assigned_list = Assign.objects.get(class_id_id=student.class_id)
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


'''
TEACHERS MARKS
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