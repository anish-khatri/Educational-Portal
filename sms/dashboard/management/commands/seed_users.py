import random  
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from models.models import User, School, Student, Subscription, Application, Course
from django.db import IntegrityError
from datetime import date

class Command(BaseCommand):
    help = 'Seeds the User, School, Student, Subscription, and Application tables with sample data'

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        School.objects.all().delete()
        Student.objects.all().delete()
        Subscription.objects.all().delete()
        Application.objects.all().delete()
        Course.objects.all().delete()

        subscription_basic = Subscription.objects.create(
            name="Basic", price=100.00, start_date=date(2025, 1, 1), end_date=date(2025, 12, 31)
        )
        subscription_premium = Subscription.objects.create(
            name="Premium", price=200.00, start_date=date(2025, 1, 1), end_date=date(2025, 12, 31)
        )

        superadmin = User.objects.create(
            email="admin@edu.com",
            username="superadmin",
            role="super_admin",
            password=make_password("admin123"),
        )
        
        schools = []
        for i in range(2):  
            user = User.objects.create(
                email=f"school{i}@edu.com",
                username=f"school{i}",
                role="school",
                password=make_password("password123"),
            )

            school = School.objects.create(
                user=user,
                subscription=subscription_basic if i % 2 == 0 else subscription_premium,
                name=f"School {i}"[:10],
                address=f"Addr {i}"[:10],
                contact=f"98765432{i}"[:10],
            )
            schools.append(school)

        course_names = ["Management", "Science", "Arts"]
        school_courses = {} 
        
        for school in schools:
            school_courses[school] = []
            for course_name in course_names:
                course = Course.objects.create(
                    school=school,
                    name=course_name,
                    description=f"{course_name} course at {school.name}",
                    duration="3 years",
                    admission_fees= 5000,
                    status=True
                )
                school_courses[school].append(course)
                
        for i in range(8):  
            try:
                user = User.objects.create(
                    email=f"student{i}@edu.com",
                    username=f"student{i}",
                    role="student",
                    password=make_password("password123"),
                )

                student = Student.objects.create(
                    user=user,
                    first_name=f"FName{i}"[:10],
                    middle_name=f"MName{i}"[:10],
                    last_name=f"LName{i}"[:10],
                    phone=f"123456789{i}"[:10],
                    address=f"Address {i}"[:10],
                    dob=date(2010, 1, i+1),
                    enrollment_date=date(2025, 3, 1)
                )

                assigned_school = schools[i % len(schools)]
                assigned_course = random.choice(school_courses[assigned_school]) 

                Application.objects.create(
                    student=student,
                    school=assigned_school,
                    course=assigned_course,
                    status="Pending"
                )

            except IntegrityError:
                self.stdout.write(self.style.WARNING(f'User "{user.email}" already exists. Skipping.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating student {i}: {e}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded Users, Schools, Students, Applications, and Courses!'))
