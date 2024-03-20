import math
import uuid

from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save, post_delete

# Create your models here.
GENDER = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Other', 'Other')
)

TIME_SLOTS = (
    ('7:00 - 10:00', '7:00 - 10:00'),
    ('10:00 - 1:00', '10:00 - 1:00'),
    ('1:00 - 4:00', '1:00 - 4:00'),
    ('4:00 - 7:00', '4:00 7:00'),
)

DAYS_OF_WEEK = (
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
)

TEST_NAME = (
    ('Internal test 1', 'Internal test 1'),
    ('Internal test 2', 'Internal test 2'),
    ('Internal test 3', 'Internal test 3'),
    ('Event 1', 'Event 1'),
    ('Event 2', 'Event 2'),
    ('Semester End Exam', 'Semester End Exam'),
)


class User(AbstractUser):
    
    @property
    def is_student(self):
        if hasattr(self, 'student'):
            return True
        return False
    
    @property
    def is_lecturer(self):
        if hasattr(self, 'lecturer'):
            return True
        return False
    

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name 
    

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department  = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    shortname = models.CharField(max_length=50, default='X')

    def __str__(self):
        return self.name
    
class Class(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    department  = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = models.CharField(max_length=255)
    semester = models.IntegerField()

    class Meta:
        verbose_name_plural = 'classes'

    def __str__(self):
        d = Department.objects.get(name=self.department)
        return '%s : %d %s' % (d.name, self.semester, self.section)
    

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE, default=1)
    USN = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    sex = models.CharField(max_length=50, choices=GENDER, default='Male')
    DOB = models.DateField(default='1998-01-01')

    def __str__(self):
        return self.name
    

class Teacher(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, choices=GENDER, default='Male')
    DOB = DOB = models.DateField(default='1980-01-01')

    def __str__(self):
        return self.name
    

class Assign(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('course', 'class_id', 'lecturer'),)

    def __str__(self):
        cl = Class.objects.get(id=self.class_id_id)
        cr = Course.objects.get(id=self.course_id)
        te = Teacher.objects.get(id=self.lecturer_id)

        return '%s : %s : %s' % (te.name, cr.shortname, cl)
    
class AssignTime(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    period = models.CharField(max_length=50, choices=TIME_SLOTS, default='10:00 - 1:00')
    day = models.CharField(max_length=15, choices=DAYS_OF_WEEK)


class AttendanceClass(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'


class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendanceclass = models.ForeignKey(AttendanceClass, on_delete=models.CASCADE, default=1)
    date = models.DateField(default='2018-10-23')
    status = models.BooleanField(default='True')

    def __str__(self):
        sname = Student.objects.get(name=self.student)
        cname = Course.objects.get(name=self.course)

        return '%s : %s' % (sname.name, cname.shortname)
    

class AttendanceTotal(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = (
            ('student', 'course'),
            )

    @property
    def att_class(self):
        stud = Student.objects.get(name=self.student)
        cr = Course.objects.get(name=self.course)
        att_class = Attendance.objects.filter(course=cr, student=stud, status='True').count()
        
        return att_class
    
    @property
    def total_class(self):
        stud = Student.objects.get(name=self.student)
        cr = Course.objects.get(name=self.course)
        total_class = Attendance.objects.filter(course=cr, student=stud).count()

        return total_class

    @property
    def attendance(self):
        stud = Student.objects.get(name=self.student)
        cr = Course.objects.get(name=self.course)
        total_class = Attendance.objects.filter(course=cr, student=stud).count()
        att_class = Attendance.objects.filter(course=cr, student=stud, status='True').count()
        if total_class == 0:
            attendance = 0
        else:
            attendance = round(att_class / total_class * 100, 2)
        return attendance
    
    @property
    def classes_to_attend(self):
        stud = Student.objects.get(name=self.student)
        cr = Course.objects.get(name=self.course)
        total_class = Attendance.objects.filter(course=cr, student=stud).count()
        att_class = Attendance.objects.filter(course=cr, student=stud, status='True').count()
        cta = math.ceil((0.75 * total_class - att_class) / 0.25)
        if cta < 0:
            return 0
        return cta


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('student', 'course'),)
        verbose_name_plural = 'Marks'

    def __str__(self):
        sname = Student.objects.get(name=self.student)
        cname = Course.objects.get(name=self.course)

        return '%s : %s' % (sname.name, cname.shortname)
    
    def get_cie(self):
        marks_list = self.marks_set.all()
        m = []
        for mk in marks_list:
            m.append(mk.marks1)
        cie = math.ceil(sum(m[:5]) / 2)
        return cie
    
    def get_attendance(self):
        a = AttendanceTotal.objects.get(student=self.student, course=self.course)

        return a.attendance
    

class Marks(models.Model):
    studentcourse = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=TEST_NAME, default='Internal test 1')
    marks1 = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    class Meta:
        unique_together = (
            ('studentcourse', 'name'),
            )
        
    @property
    def total_marks(self):
        if self.name == 'Semester End Exam':
            return 100
        return 20
    

class MarksClass(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=TEST_NAME, default='Internal test 1')
    status = models.BooleanField(default='False')

    class Meta:
        unique_together = (('assign', 'name'),)

    @property
    def total_marks(self):
        if self.name == 'Semester End Exam':
            return 100
        return 20


class AttendanceRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()


# Triggers
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


days = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
}

def create_attendance(sender, instance, **kwargs):
    if kwargs['created']:
        start_date = AttendanceRange.objects.all()[:1].get().start_date
        end_date = AttendanceRange.objects.all()[:1].get().end_date

        for single_date in daterange(start_date, end_date):
            if single_date.isoweekday() == days[instance.day]:
                try:
                    AttendanceClass.objects.get(date=single_date.strftime("%Y-%m-%d"), assign=instance.assign)
                except AttendanceClass.DoesNotExist:
                    a = AttendanceClass(date=single_date.strftime("%Y-%m-%d"), assign=instance.assign)
                    a.save()


def create_marks(sender, instance, **kwargs):
    if kwargs['created']:
        if hasattr(instance, 'name'):
            ass_list = instance.class_id.assign_set.all()
            
            for ass in ass_list():
                try:
                    StudentCourse.objects.get(student=instance, course=ass.course)
                except StudentCourse.DoesNotExist:
                    sc = StudentCourse(student=instance, course=ass.course)
                    sc.save()
                    sc.marks_set.create(name='Internal test 1')
                    sc.marks_set.create(name='Internal test 2')
                    sc.marks_set.create(name='Internal test 3')
                    sc.marks_set.create(name='Event 1')
                    sc.marks_set.create(name='Event 2')
                    sc.marks_set.create(name='Semester End Exam')
                
        elif hasattr(instance, 'course'):
            stud_list = instance.class_id.student_set.all()
            cr = instance.course
            for s in stud_list:
                try:
                    StudentCourse.objects.get(student=s, course=cr)
                except StudentCourse.DoesNotExist:
                    sc = StudentCourse(student=s, course=cr)
                    sc.save()
                    sc.marks_set.create(name='Internal test 1')
                    sc.marks_set.create(name='Internal test 2')
                    sc.marks_set.create(name='Internal test 3')
                    sc.marks_set.create(name='Event 1')
                    sc.marks_set.create(name='Event 2')
                    sc.marks_set.create(name='Semester End Exam')


def create_marks_class(sender, instance, **kwargs):
    if kwargs['created']:
        for name in TEST_NAME:
            try:
                MarksClass.objects.get(assign=instance, name=name[0])
            except MarksClass.DoesNotExist:
                m = MarksClass(assign=instance, name=name[0])
                m.save()


def delete_marks(sender, instance, **kwargs):
    stud_list = instance.class_id.student_set.all()
    StudentCourse.objects.filter(course=instance.course, student__in=stud_list).delete()



post_save.connect(create_marks, sender=Student)
post_save.connect(create_marks, sender=Assign)
post_save.connect(create_marks_class, sender=Assign)
post_save.connect(create_attendance, sender=AssignTime)
post_delete.connect(delete_marks, sender=Assign)