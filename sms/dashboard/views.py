from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from models.models import School , Student
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from models.models import User  
from django.utils import timezone
from datetime import timedelta
def dashboard(request):
    if 'user_id' not in request.session:
        return redirect('/') 

    user_id = request.session.get('user_id')
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, "User not found")
        return redirect('/')

    
    student_count = Student.objects.count()
    school_count = School.objects.count()
    approved_school_count = School.objects.filter(status=True).count()

    today = timezone.now().date()
    next_week = today + timedelta(days=7)

    expiring_soon_schools = School.objects.filter(
        status=True,
        subscription_end_date__range=[today, next_week]
    )

    return render(request, 'admin/dashboard.html', {
        'user': user,
        'student_count': student_count,
        'school_count': school_count,
        'approved_school_count': approved_school_count,
        'expiring_soon_schools': expiring_soon_schools,
    })

def accept_school_subscription(request, school_id):
    school = get_object_or_404(School, id=school_id)

    school.status = True

    school.subscription_start_date = timezone.now().date()

    if school.subscription and school.subscription.end_date:
        school.subscription_end_date = school.subscription.end_date
    else:
        school.subscription_end_date = timezone.now().date() + timedelta(days=30)

    school.save()

    context = {
        'school': school,
        'success_message': 'School subscription has been accepted and started.'
    }
    return redirect('school_list')

def school_detail_view(request, school_id):
    school = get_object_or_404(School, id=school_id)
    
    context = {
        'school': school
    }
    return render(request, 'admin/schools/school_detail.html', context)