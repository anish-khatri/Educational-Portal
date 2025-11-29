from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
import random
import string

class User(models.Model):
    ROLE_CHOICES = [
        ('super_admin', 'Super Admin'),
        ('school', 'School'),
        ('student', 'Student'),
    ]

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='student')
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username

    def is_super_admin(self):
        return self.role == 'super_admin'

    def is_school(self):
        return self.role == 'school'

    def is_student(self):
        return self.role == 'student'
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password) 
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def clean(self):
        # Ensure user role is one of the defined roles
        if self.role not in dict(self.ROLE_CHOICES).keys():
            raise ValueError("Invalid role assigned.")

    class Meta:
        db_table = 'users'


class Subscription(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'subscriptions'


class School(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="schools")
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, null=True, blank=True, related_name="schools")
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='school_images/', null=True)
    address = models.TextField()
    contact = models.CharField(max_length=20)
    status = models.BooleanField(default=False) 
    
    subscription_start_date = models.DateField(null=True, blank=True)
    subscription_end_date = models.DateField(null=True, blank=True)
    is_subscription_manual = models.BooleanField(default=False) 

    def __str__(self):
        return self.name

    @property
    def is_subscription_active(self):
        today = timezone.now().date()
        if self.subscription_end_date and self.subscription_end_date >= today:
            return "Active"
        return "Inactive"

    class Meta:
        db_table = 'schools'

class Course(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="courses")
    name = models.CharField(max_length=255)
    admission_fees = models.PositiveIntegerField()
    description = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'courses'
        
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=10, null=True)
    address = models.TextField()
    documents = models.FileField(upload_to="student_documents/", blank=True, null=True)
    dob = models.DateField(null=True, blank=True)
    enrollment_date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'students'

class Application(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Waiting", "Waiting"),
        ("Rejected", "Rejected"),
    ]

    student = models.ForeignKey("Student", on_delete=models.CASCADE, related_name="applications")
    school = models.ForeignKey("School", on_delete=models.CASCADE, related_name="applications")
    application_date = models.DateField(auto_now_add=True)
    course = models.ForeignKey("Course", on_delete=models.CASCADE, related_name="applications") 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    applied_at = models.DateTimeField(auto_now_add=True)
    symbol_number = models.CharField(max_length=12, unique=True, blank=True, null=True)

    supporting_documents = models.FileField(upload_to="applications/documents/", blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if not self.symbol_number:
            self.symbol_number = self.generate_symbol_number()
        super().save(*args, **kwargs)

    def generate_symbol_number(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    class Meta:
        db_table = "applications"


class Result(models.Model):
    application = models.OneToOneField("Application", on_delete=models.CASCADE, related_name="result")
    obtained_marks = models.PositiveIntegerField()
    exam_name = models.CharField(max_length=255, default="entrance_exams")
    total_marks = models.PositiveIntegerField()
    pass_marks = models.PositiveIntegerField()
    status = models.CharField(
        max_length=20,
        choices=[("Pass", "Pass"), ("Fail", "Fail")],
        default="Fail"
    )
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Result for {self.application.user.username}"

    class Meta:
        db_table = "results"


class Admission(models.Model):
    application = models.OneToOneField("Application", on_delete=models.CASCADE, related_name="admission")
    admission_date = models.DateTimeField(auto_now_add=True)
    
    admission_number = models.CharField(max_length=15, unique=True, blank=True, null=True)

    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    due_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payment_method = models.CharField(
        max_length=50,
        choices=[("Esewa", "Esewa"), ("Onsite", "Onsite")],
        default="Esewa"
    )
    payment_status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Completed", "Completed"), ("Partial", "Partial")],
        default="Pending"
    )

    def generate_admission_number(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def generate_student_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    class Meta:
        db_table = "admissions"
        
        
class Payment(models.Model):
    admission = models.OneToOneField("Admission", on_delete=models.CASCADE, related_name="payment") 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("Pending", "Pending"), ("Completed", "Completed"), ("Failed", "Failed")],
        default="Pending"
    )
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        super().save(*args, **kwargs)

    def generate_transaction_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.application.user.username}"

    class Meta:
        db_table = "payments"
        
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.title}"

    class Meta:
        db_table = "notifications"
        ordering = ['-created_at']