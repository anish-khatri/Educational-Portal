from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from models.models import Application, School, User, Result , Course , Admission , Student , Notification
from schools.forms import ResultForm  , CourseForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.core.mail import send_mail
from reportlab.lib import colors

def application_list(request):
    """View to list all applications for a given school."""
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "You need to log in to view applications.")
        return redirect('/dashboard/')

    user = get_object_or_404(User, id=user_id)

    if not user.is_school():
        messages.error(request, "You are not authorized to view applications.")
        return redirect('/dashboard/')

    school = get_object_or_404(School, user=user)

    applications = Application.objects.filter(school=school, status="Pending").select_related("student__user")

    context = {
        'applications': applications,
        'school': school,
    }
    return render(request, 'admin/schools/application_list.html', context)

def result_list(request, application_id):
    """View to list all results for a given application."""
    application = get_object_or_404(Application, id=application_id)
    
    results = Result.objects.filter(application=application)
    
    context = {
        'application': application,
        'results': results,
    }
    return render(request, 'admin/schools/result_list.html', context)

def approved_application_list(request):
    """View to list all applications for a given school."""
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "You need to log in to view applications.")
        return redirect('/dashboard/')

    user = get_object_or_404(User, id=user_id)

    if not user.is_school():
        messages.error(request, "You are not authorized to view applications.")
        return redirect('/dashboard/')

    school = get_object_or_404(School, user=user)

    applications = Application.objects.filter(school=school, status="Approved").select_related("student__user")

    for application in applications:
        application.has_results = Result.objects.filter(application=application).exists()

        
    context = {
        'applications': applications,
        'school': school,
    }
    return render(request, 'admin/schools/approved_application_list.html', context)

def waiting_application_list(request):
    """View to list all applications for a given school."""
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "You need to log in to view applications.")
        return redirect('/dashboard/')

    user = get_object_or_404(User, id=user_id)

    if not user.is_school():
        messages.error(request, "You are not authorized to view applications.")
        return redirect('/dashboard/')

    school = get_object_or_404(School, user=user)

    applications = Application.objects.filter(school=school, status="Waiting").select_related("student__user")

    for application in applications:
        application.has_results = Result.objects.filter(application=application).exists()

        
    context = {
        'applications': applications,
        'school': school,
    }
    return render(request, 'admin/schools/waiting_application_list.html', context)

def show_application(request, application_id):
    """View to display a single application in detail."""
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "You need to log in to view this application.")
        return redirect('/dashboard/')

    user = get_object_or_404(User, id=user_id)

    school = get_object_or_404(School, user=user)

    application = get_object_or_404(Application.objects.select_related("student__user"), id=application_id, school=school)

    context = {
        'application': application,
        'student': application.student,
    }
    return render(request, 'admin/schools/show_application.html', context)

def convert_waiting_exam(request, application_id):
    """Create a StudentEntranceExam and send ID card PDF via email."""
    application = get_object_or_404(Application, id=application_id)

    school_id = request.session.get('school_id')

    if application.school.id != school_id:
        messages.error(request, "Unauthorized access to this application.")
        return redirect('/dashboard/')  

    application.status = 'Waiting'
    application.save()

    messages.success(request, "Entrance exam created and application status updated to 'Waiting'. ID card sent to email.")
    
    return redirect('waiting_application_list')

def create_student_entrance_exam(request, application_id):
    """Create a StudentEntranceExam and send ID card PDF via email."""
    application = get_object_or_404(Application, id=application_id)

    school_id = request.session.get('school_id')

    if application.school.id != school_id:
        messages.error(request, "Unauthorized access to this application.")
        return redirect('/dashboard/')  

    application.status = 'Approved'
    application.save()

    create_notification(
        user=application.student.user,
        title="Application Approved",
        message="Your application has been approved, and your entrance exam details have been sent to your email."
    )
    
    pdf = generate_id_card_pdf(application, application.student)

    send_id_card_email(pdf, application.student.user.email)

    messages.success(request, "Entrance exam created and application status updated to 'Approved'. ID card sent to email.")
    
    return redirect('approved_application_list')

def generate_id_card_pdf(application, student):
    """Generate a PDF ID card for the student with enhanced design."""
    buffer = BytesIO() 
    c = canvas.Canvas(buffer, pagesize=letter)

    c.setFont("Helvetica", 10)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(230, 750, "Student ID Card")

    c.setStrokeColor(colors.black)
    c.setLineWidth(1)
    c.line(30, 720, 580, 720)

    c.setStrokeColor(colors.black)
    c.setFillColor(colors.lightgrey)
    c.roundRect(30, 600, 550, 150, 10, stroke=1, fill=1)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(100, 650, f"Student ID: {student.user.username}")
    
    c.setFont("Helvetica", 10)
    c.drawString(100, 630, f"Name: {student.first_name} {student.last_name}")
    c.drawString(100, 610, f"Date of Birth: {student.dob}")
    c.drawString(100, 590, f"Enrollment Date: {student.enrollment_date}")

    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawString(100, 540, "student Name | Contact Info | Website")

    c.setFont("Helvetica", 14)
    c.drawString(100, 590, f"Symbol Number: {application.symbol_number}")

    c.showPage()
    c.save()

    buffer.seek(0)
    return buffer

def send_id_card_email(pdf_buffer, student_email):
    """Send the ID card PDF via email."""
    
    try:
        if not student_email:
            raise Http404("Invalid email address")

        email_subject = "Your Entrance Exam ID Card"
        email_body = """
        Dear Student,

        Your entrance exam ID card is attached to this email.

        Best Regards,
        Your School
        """

        email = EmailMessage(
            subject=email_subject,
            body=email_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[student_email]
        )

        pdf_buffer.seek(0) 
        email.attach('student_id_card.pdf', pdf_buffer.read(), 'application/pdf')

        email.send()
        print("Email sent successfully")

    except Exception as e:
        print(f"Error sending email: {e}")
        raise

def publish_result(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    school_id = request.session.get('school_id')

    if application.school.id != school_id:
        messages.error(request, "Unauthorized access.")
        return redirect('/dashboard/')

    create_notification(
        user=application.student.user,
        title="Result Published",
        message="Your result has been published."
    )
    
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            result = form.save(commit=False)
            result.application = application
            result.published_at = timezone.now() 
            result.save()

            messages.success(request, "Result published successfully.")
            return redirect('approved_application_list')  
    else:
        form = ResultForm()

    return render(request, 'admin/schools/publish_result.html', {'form': form, 'application': application})


def create_course(request):
    """View to create a new course."""
    school_id = request.session.get('school_id')

    if not school_id:
        messages.error(request, "You need to be logged in to create a course.")
        return redirect('/dashboard/')

    school = get_object_or_404(School, id=school_id)

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.school = school  
            course.save()
            messages.success(request, "Course created successfully.")
            return redirect('course_list')  
    else:
        form = CourseForm()

    return render(request, 'admin/schools/courses/create_course.html', {'form': form})

def admission_list(request):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "You need to log in to view applications.")
        return redirect('/dashboard/')

    user = get_object_or_404(User, id=user_id)

    if not user.is_school():
        messages.error(request, "You are not authorized to view applications.")
        return redirect('/dashboard/')

    school = get_object_or_404(School, user=user)

    admissions = Admission.objects.filter(application__school=school)

    context = {
        'admissions': admissions,
    }
    return render(request, 'admin/schools/admission_list.html', context)

def admission_detail(request, admission_id):
    admission = get_object_or_404(Admission, id=admission_id)

    context = {
        'admission': admission
    }
    return render(request, 'admin/schools/admission_detail.html', context)

def update_course(request, course_id):
    """View to update an existing course."""
    course = get_object_or_404(Course, id=course_id)

    if course.school.id != request.session.get('school_id'):
        messages.error(request, "You are not authorized to edit this course.")
        return redirect('/dashboard/')

    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect('course_list')  
    else:
        form = CourseForm(instance=course)

    return render(request, 'admin/schools/courses/update_course.html', {'form': form, 'course': course})

def course_list(request):
    school_id = request.session.get('school_id')

    if not school_id:
        messages.error(request, "You need to be logged in to view courses.")
        return redirect('/dashboard/')

    school = get_object_or_404(School, id=school_id)

    courses = Course.objects.filter(school=school)

    context = {
        'courses': courses,
        'school': school,
    }
    return render(request, 'admin/schools/courses/course_list.html', context)


def delete_course(request, course_id):
    """View to delete a course."""
    school_id = request.session.get('school_id')

    if not school_id:
        messages.error(request, "You need to be logged in to delete a course.")
        return redirect('/dashboard/')

    school = get_object_or_404(School, id=school_id)

    course = get_object_or_404(Course, id=course_id, school=school)

    course.delete()

    messages.success(request, "Course deleted successfully.")
    return redirect('course_list')


def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user_id = request.session.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('/')

    if not user.is_school():
        messages.error(request, "Unauthorized access.")
        return redirect('/dashboard/')

    school = get_object_or_404(School, user=user)

    student_count = Student.objects.count()
    course_count = Course.objects.filter(school=school).count()
    application_total = Application.objects.filter(school=school).count()
    approved_applications = Application.objects.filter(school=school, status='Approved').count()
    pending_applications = Application.objects.filter(school=school, status='Pending').count()
    waiting_applications = Application.objects.filter(school=school, status='Waiting').count()
    admission_count = Admission.objects.filter(application__school=school).count()

    recent_applications = Application.objects.filter(school=school).select_related('student__user')[:5]

    context = {
        'user': user,
        'student_count': student_count,
        'course_count': course_count,
        'application_total': application_total,
        'approved_applications': approved_applications,
        'pending_applications': pending_applications,
        'waiting_applications': waiting_applications,
        'admission_count': admission_count,
        'recent_applications': recent_applications,
    }

    return render(request, 'admin/schools/dashboard.html', context)

    
def updateProfile(request):
    user_id = request.session.get('user_id')

    if not user_id:
        messages.error(request, "User not logged in")
        return redirect('/')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('/')  

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        current_password = request.POST.get('current_password') 
        confirm_password = request.POST.get('confirm_password')
        email = request.POST.get('email')

        if current_password and current_password != user.password:
            messages.error(request, "Current password is incorrect")
            if password and password != confirm_password:
                messages.error(request, "New passwords do not match")

        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = make_password(password) 

        user.save()

        messages.success(request, "Profile updated successfully")

    return render(request, 'admin/schools/update-profile.html', {'user': user})


def create_notification(user, title, message):
    if user and title and message:
        Notification.objects.create(
            user=user,
            title=title,
            message=message
        )


def profile(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    return render(request, 'admin/schools/update-profile.html', {'user': user})