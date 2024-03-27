import random

from django.core.management.base import BaseCommand
from faker import Faker

from management_erp.models import *


class Command(BaseCommand):
    help = "Seed database with sample data for management_erp.models"

    def add_arguments(self, parser):
        parser.add_argument("num_students", type=int, help="Number of students to create")
        parser.add_argument("num_courses", type=int, help="Number of courses to create")
        parser.add_argument("num_classes", type=int, help="Number of classes to create")
        parser.add_argument("num_departments", type=int, help="Number of departments to create")

    def handle(self, *args, **kwargs):
        num_students = kwargs["num_students"]
        num_courses = kwargs["num_courses"]
        num_classes = kwargs["num_classes"]
        num_departments = kwargs["num_departments"]

        self.stdout.write(self.style.SUCCESS("Seeding database..."))

        fake = Faker()

        # Create sample departments
        for _ in range(num_departments):
            department_name = fake.company()
            Department.objects.create(name=department_name)

        # Create sample courses
        departments = Department.objects.all()
        for _ in range(num_courses):
            department = random.choice(departments)
            course_name = fake.word()
            course_shortname = fake.word()
            Course.objects.create(department=department, name=course_name, shortname=course_shortname)

        # Create sample classes
        for _ in range(num_classes):
            department = random.choice(departments)
            section = fake.word()
            semester = random.randint(1, 8)
            Class.objects.create(department=department, section=section, semester=semester)

        # Create sample students
        classes = Class.objects.all()
        for _ in range(num_students):
            class_obj = random.choice(classes)
            name = fake.name()
            sex = random.choice(['Male', 'Female', 'Other'])
            dob = fake.date_of_birth()
            Student.objects.create(class_id=class_obj, name=name, sex=sex, DOB=dob)

        self.stdout.write(self.style.SUCCESS("Database seeding completed."))