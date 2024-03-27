from django.test import TestCase
from psycopg2 import IntegrityError
from .models import *

# Create your tests here.

class MarksClassTestCase(TestCase):
    def setUp(self):
        # Create a Department
        self.department = Department.objects.create(name='Your Department')

        # Create a Class
        self.c = Class.objects.create(department=self.department, section='A', semester=1)

        # Create a Course
        self.course = Course.objects.create(department=self.department, name='Your Course', shortname='YC')

        # Create a Teacher
        self.teacher = Teacher.objects.create(department=self.department, name='Teacher Name', gender='Male')

        # Create an Assign object with a valid class_id
        self.assign = Assign.objects.create(class_id=self.c, course=self.course, lecturer=self.teacher)

    def test_marks_class_uniqueness(self):
        # Test uniqueness of MarksClass instances
        MarksClass.objects.create(assign=self.assign, name='Internal test 1')
        MarksClass.objects.create(assign=self.assign, name='Event 1')

        # Attempt to create a duplicate MarksClass instance
        with self.assertRaises(IntegrityError):
            MarksClass.objects.create(assign=self.assign, name='Internal test 1')

    def test_marks_class_creation(self):
        # Test creation of MarksClass instances
        initial_count = MarksClass.objects.count()

        # Create a new MarksClass instance
        MarksClass.objects.create(assign=self.assign, name='Internal test 2')

        # Check if the count of MarksClass instances increased by 1
        self.assertEqual(MarksClass.objects.count(), initial_count + 1)
