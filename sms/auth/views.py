from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from models.models import User , School
from auth.forms import StudentRegistrationForm , LoginForm , SchoolRegistrationForm
from models.models import Student
from applications.forms import ApplicationForm

def home(request):
    return render(request, 'home/index.html')

def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)

def home_school_list(request):
    """Read: List all schools"""
    schools = School.objects.all()
    return render(request, 'home/school_list.html', {'schools': schools})

def home_school_detail(request, pk):
    school = get_object_or_404(School, pk=pk)
    return render(request, 'home/school_detail.html', {'school': school})

def apply_to_school(request, pk):
    school = get_object_or_404(School, pk=pk)

    student_id = request.session.get('student_id')
    if not student_id:
        messages.error(request, "Oops Something went wrong!")
        return redirect('login')  
    try:
        student = Student.objects.get(id=student_id) 
    except Student.DoesNotExist:
        messages.error(request, "Oops Something went wrong!")
        return redirect('login')

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.student = student  
            application.school = school 
            application.course = form.cleaned_data['course']
            application.save()
            messages.success(request, "Application submitted successfully!")
            return redirect('dashboard')  
        else:
            messages.error(request, "Error submitting application. Please check your inputs.")
    else:
        form = ApplicationForm()

    return render(request, 'home/apply.html', {'form': form, 'school': school})

def registerHome(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your registration. Please check the form.")
    else:
        form = StudentRegistrationForm()

    return render(request, 'home/student_register.html', {'form': form})

def registerSchool(request):
    if request.method == 'POST':
        form = SchoolRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful!")
            return redirect('/')
        else:
            messages.error(request, "There was an error with your registration. Please check the form.")
    else:
        form = SchoolRegistrationForm()

    return render(request, 'home/school_register.html', {'form': form})

def loginHome(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            login_input = form.cleaned_data['email_or_username']
            password = form.cleaned_data['password']

            user = User.objects.filter(email=login_input).first() or User.objects.filter(username=login_input).first()

            if user and check_password(password, user.password):
                request.session['user_id'] = user.id  
                request.session['role'] = user.role

                request.session.pop('student_id', None)
                request.session.pop('school_id', None)

                if user.role == 'student':
                    student = Student.objects.filter(user=user).first()  
                    if student:
                        request.session['student_id'] = student.id  
                    return render(request, 'home/login.html', {
                        'form': form, 
                        'login_success': True, 
                        'redirect_url': '/'
                    })

                elif user.role == 'school':
                    school = School.objects.filter(user=user).first()
                    if school:
                        if school.status:
                            request.session['school_id'] = school.id
                            return render(request, 'home/login.html', {
                                'form': form,
                                'login_success': True,
                                'redirect_url': '/'
                            })
                        else:
                            messages.error(request, "Your school account is under review.")
                            return render(request, 'home/login.html', {
                                'form': form,
                                'login_success': False
                            })
                    else:
                        messages.error(request, "School account not found.")
                        return render(request, 'home/login.html', {
                            'form': form,
                            'login_success': False
                        })


                elif user.role == 'super_admin':
                    return render(request, 'home/login.html', {
                        'form': form, 
                        'login_success': True, 
                        'redirect_url': '/'
                    })

                messages.error(request, "Invalid role or permission")
                return render(request, 'home/login.html', {
                    'form': form, 
                    'login_success': False
                })

            else:
                messages.error(request, "Invalid Email/Username or Password")
                return render(request, 'home/login.html', {
                    'form': form, 
                    'login_success': False
                })

    return render(request, 'home/login.html', {
        'form': form, 
        'login_success': False
    })
    
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

    return render(request, 'admin/update-profile.html', {'user': user})


def logout(request):
    request.session.flush() 
    return render(request, 'home/index.html')

def profile(request):
    if 'user_id' not in request.session:
        return redirect('/')

    user_id = request.session.get('user_id')
    user = User.objects.get(id=user_id)

    return render(request, 'admin/update-profile.html', {'user': user})
