import urllib.parse
import random
import string
import hmac
import hashlib
from django.urls import reverse
import base64
import os
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from models.models import User , Application , Result , Student , Payment , Admission , School , Notification
from models.models import Student
from student.forms import AdmissionForm , PaymentForm
from reportlab.lib.pagesizes import letter
from django.db import transaction
import urllib.parse
from reportlab.pdfgen import canvas
from django.utils import timezone
from django.http import HttpResponse

def application_list(request):
    student_id = request.session.get('student_id')

    if not student_id:
        messages.error(request, "You need to log in to view your applications.")
        return redirect('/dashboard/') 

    try:
        student = Student.objects.get(id=student_id)
    except Student.DoesNotExist:
        messages.error(request, "Student record not found!")
        return redirect('/dashboard/') 

    applications = Application.objects.filter(student=student)

    for application in applications:
        application.has_results = Result.objects.filter(application=application).exists()
        
    for application in applications:
        application.has_admission = Admission.objects.filter(application=application).exists()

    context = {
        'applications': applications,
    }
    return render(request, 'admin/students/application_list.html', context)

def admission_list(request):
    user_id = request.session.get('user_id') 

    if not user_id:
        messages.error(request, "You need to log in to view admissions.")
        return redirect('/dashboard/')  

    student = get_object_or_404(Student, user_id=user_id)

    admissions = Admission.objects.filter(application__student=student)

    context = {
        'admissions': admissions,
    }
    return render(request, 'admin/students/admission_list.html', context)

def admission_detail(request, admission_id):
    admission = get_object_or_404(Admission, id=admission_id)

    context = {
        'admission': admission
    }
    return render(request, 'admin/students/admission_detail.html', context)


def result_list(request, application_id):
    """View to list results for a given application, ensuring the student owns the application."""
    user_id = request.session.get('user_id') 

    if not user_id:
        messages.error(request, "You need to log in to view your results.")
        return redirect('/dashboard/')  

    student = get_object_or_404(Student, user_id=user_id)

    application = get_object_or_404(Application, id=application_id, student=student)

    results = Result.objects.filter(application=application)

    context = {
        'application': application,
        'results': results,
    }
    return render(request, 'admin/students/result_list.html', context)


def show_result(request, result_id):
    """View to display a specific result by result_id."""
    result = get_object_or_404(Result, id=result_id)

    context = {
        'result': result,
    }
    return render(request, 'admin/students/show_result.html', context)

def download_result_pdf(request, result_id):
    """Generate a PDF for the result and return as a response."""
    result = get_object_or_404(Result, id=result_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Result_{result.id}.pdf"'

    buffer = canvas.Canvas(response, pagesize=letter)
    buffer.setTitle(f"Result_{result.id}")

    buffer.setFont("Helvetica-Bold", 16)
    buffer.drawString(200, 750, "Entrance Exam Result")

    buffer.setFont("Helvetica", 12)
    y_position = 720 
    data = [
        ("Result ID:", result.id),
        ("Application ID:", result.application.id),
        ("Student Name:", f"{result.application.student.first_name} {result.application.student.last_name}"),
        ("Email:", result.application.student.user.email),
        ("Exam Name:", result.exam_name),
        ("Total Marks:", result.total_marks),
        ("Pass Marks:", result.pass_marks),
        ("Obtained Marks:", result.obtained_marks),
        ("Status:", result.status),
        ("Published Date:", result.published_at.strftime("%Y-%m-%d")),
    ]

    for label, value in data:
        buffer.drawString(100, y_position, f"{label} {value}")
        y_position -= 20 

    buffer.showPage()
    buffer.save()

    return response

def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)

def show_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            student = Student.objects.get(user_id=user_id)  
        except Student.DoesNotExist:
            return redirect('/dashboard/') 
        
        if application.student.id == student.id:
            return render(request, 'admin/students/show_application.html', {'application': application})
        else:
            return redirect('/dashboard/')
    else:
        return redirect('/dashboard/')

    
def edit_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if request.method == 'POST':
        new_document = request.FILES.get('supporting_documents', None)
        if new_document:
            application.supporting_documents = new_document
            application.save()  
            messages.success(request, "Supporting document updated successfully!")
        else:
            messages.warning(request, "No document uploaded. No changes were made.")

        return redirect('application_list')

    context = {
        'application': application,
    }
    return render(request, 'admin/students/edit_application.html', context)

def delete_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    if application.student.id == request.session.get('student_id'):
        application.delete()
        messages.success(request, "Application deleted successfully!")
    else:
        messages.error(request, "You cannot delete an application that doesn't belong to you.")
        
def generate_transaction_id():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

def generate_esewa_signature(params):
    secret_key = "8gBm/:&EnhH.1/q" 
    
    signed_fields = params["signed_field_names"].split(",")
    message = ",".join(f"{field}={params[field]}" for field in signed_fields)
    
    digest = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    signature = base64.b64encode(digest).decode()
    
    return signature

@transaction.atomic
def admission_create(request, application_id):
    application = get_object_or_404(Application, id=application_id)

    if request.method == "POST":
        form = AdmissionForm(request.POST)
        if form.is_valid():
            admission = form.save(commit=False)
            admission.application = application

            amount_paid = form.cleaned_data.get("amount_paid", 0)
            total_fees = application.course.admission_fees
            admission.due_amount = total_fees - amount_paid

            if amount_paid == 0:
                admission.payment_status = "Pending"
            elif amount_paid < total_fees:
                admission.payment_status = "Partial"
            else:
                admission.payment_status = "Completed"

            admission.save()  

            if form.cleaned_data.get("payment_method") == "Esewa":
                transaction_id = generate_transaction_id()

                payment = Payment.objects.create(
                    admission=admission,
                    amount=amount_paid,
                    payment_date=timezone.now(),
                    transaction_id=transaction_id,
                    status="Pending",
                )

                return redirect("payment_form", admission_id=admission.id)

            messages.success(request, "Admission created successfully!")
            return redirect("admission_list")

    else:
        form = AdmissionForm()

    return render(request, "admin/students/admission_form.html", {"form": form, "application": application})

def create_notification(user, title, message):
    if user and title and message:
        Notification.objects.create(
            user=user,
            title=title,
            message=message
        )

def mark_all_notifications_as_read(request):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect('/dashboard/')

    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('/dashboard/')

    
    Notification.objects.filter(user=user, is_read=False).update(is_read=True)
    return redirect('/dashboard/')


def mark_notification_as_read(request, notification_id):
    user_id = request.session.get('user_id')
    
    if not user_id:
        messages.error(request, "You must be logged in to perform this action.")
        return redirect('/dashboard/')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('/dashboard/')

    
    Notification.objects.filter(id=notification_id, user=user).update(is_read=True)
    return redirect('/dashboard/')
                                                           
def payment_form(request, admission_id):
    admission = get_object_or_404(Admission, id=admission_id)
    payment = get_object_or_404(Payment, admission=admission)

    esewa_url = "https://rc-epay.esewa.com.np/api/epay/main/v2/form"

    amount = int(admission.amount_paid)
    txAmt = 10
    psc = 0
    pdc = 0
    total = amount + txAmt

    transaction_uuid = generate_transaction_id()

    su_url = f"http://127.0.0.1:8000{reverse('esewa_payment_success', kwargs={'transaction_id': payment.transaction_id})}"
    fu_url = f"http://127.0.0.1:8000{reverse('esewa_payment_failure', kwargs={'transaction_id': payment.transaction_id})}"

    params = {
        "amount": f"{amount}",
        "tax_amount": f"{txAmt}",
        "psc": f"{psc}",
        "pdc": f"{pdc}",
        "total_amount": f"{total}",
        "transaction_uuid": transaction_uuid,
        "product_code": "EPAYTEST",  
        "success_url": su_url,
        "failure_url": fu_url,
        "signed_field_names": "total_amount,transaction_uuid,product_code",
    }

    signature = generate_esewa_signature(params)

    params['signature'] = signature

    context = {
        "admission": admission,
        "payment": payment,
        "esewa_url": esewa_url,
        "params": params,
        "signature": signature,
    }

    return render(request, "admin/students/payment_form.html", context)

@transaction.atomic
def esewa_payment_success(request, transaction_id):
    payment = get_object_or_404(Payment, transaction_id=transaction_id)
    
    status = request.GET.get("status") 

    if status == "Success":
        payment.status = "Completed"
        payment.save()
        
        admission = Admission.objects.get(payment=payment)
        admission.payment_status = "Completed"
        admission.status = "Enrolled"
        admission.save()

        return HttpResponse("Payment Successful! Your admission is confirmed.")
    else:
        return HttpResponse("Payment was unsuccessful. Please try again.")
    
@transaction.atomic
def esewa_payment_failure(request, transaction_id):
    payment = get_object_or_404(Payment, transaction_id=transaction_id)

    payment.status = "Failed"
    payment.save()

    admission = Admission.objects.get(payment=payment)
    admission.payment_status = "Failed"
    admission.status = "Pending"
    admission.save()

    api_url = "https://rc.esewa.com.np/api/epay/transaction/status/"
    params = {
        "product_code": "EPAYTEST",
        "transaction_uuid": payment.transaction_id,
        "total_amount": payment.amount,
    }

    response = requests.get(api_url, params=params)

    print("Response Status Code:", response.status_code)  
    print("Response Content:", response.text)  

    if response.status_code == 200:
        data = response.json()
        
        status = data.get("status", "")
        if status == "COMPLETE":
            payment.status = "Completed"
            admission.payment_status = "Completed"
            admission.status = "Confirmed"
        elif status == "PENDING":
            return render(request, 'admin/students/payment_failure.html', {"payment": payment, "admission": admission})
        elif status == "CANCELED" or status == "NOT_FOUND" or status == "AMBIGUOUS":
            return render(request, 'admin/students/payment_failure.html', {"payment": payment, "admission": admission})
        else:
            return render(request, 'admin/students/payment_failure.html', {"payment": payment, "admission": admission})
        
        payment.save()
        admission.save()
        
        return render(request, 'admin/students/payment_failure.html', {"payment": payment, "admission": admission})

    return render(request, 'admin/students/payment_failure.html', {"payment": payment, "admission": admission, "error": "eSewa service is currently unavailable."})

def show_application_full_data(request, application_id):
    """Display full data for a given student's application in an ID card style."""
    application = get_object_or_404(Application, id=application_id)

    user_id = request.session.get('user_id')
    
    if user_id:
        try:
            student = Student.objects.get(user_id=user_id)  
        except Student.DoesNotExist:
            return redirect('/dashboard/') 
        
        if application.student.id == student.id:
            context = {
                'application': application,
                'student': application.student,
                'course': application.course,
                'school': application.school,
            }
            return render(request, 'admin/students/application_full_data.html', context)
        else:
            return redirect('/dashboard/')
    else:
        return redirect('/dashboard/')
    
def dashboard(request):
    user_id = request.session.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('/')

    student = get_object_or_404(Student, user_id=user_id)

    accepted_apps = Application.objects.filter(student=student, status="Approved")
    rejected_apps = Application.objects.filter(student=student, status="Rejected")

    accepted_schools = [app.school.name for app in accepted_apps]
    rejected_schools = [app.school.name for app in rejected_apps]

    schools_with_results = []
    for app in accepted_apps:
        if Result.objects.filter(application=app).exists():
            schools_with_results.append(app.school.name)

    school_count = School.objects.count()
    notifications = Notification.objects.filter(user=user_id, is_read=False)
    allNotifications = Notification.objects.filter(user=user_id, is_read=True)
    unread_count = notifications.filter(user=user_id, is_read=False).count()

    context = {
        'user': user,
        'notifications': notifications, 
        'allNotifications': allNotifications, 
        'unread_count': unread_count,
        'school_count': school_count,
        'accepted_applications_count': accepted_apps.count(),
        'rejected_applications_count': rejected_apps.count(),
        'accepted_schools': accepted_schools,
        'rejected_schools': rejected_schools,
        'schools_with_results': schools_with_results,
        'accepted_apps': accepted_apps,  
    }

    return render(request, 'admin/students/dashboard.html', context)

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

    return render(request, 'admin/students/update-profile.html', {'user': user})


def profile(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    return render(request, 'admin/students/update-profile.html', {'user': user})