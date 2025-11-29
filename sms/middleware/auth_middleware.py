from django.shortcuts import redirect
from django.urls import reverse
from models.models import User

class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Defining routes that require authentication
        self.protected_routes = [
            '/dashboard/',
            '/students/',
            '/school/',
            '/subscription/',
        ]

    def __call__(self, request):
        if any(request.path.startswith(route) for route in self.protected_routes):
            user_id = request.session.get('user_id')

            if not user_id:
                return redirect(reverse('home'))

            try:
                user = User.objects.get(id=user_id)
                request.user = user  

                if user.role == 'student' and not request.path.startswith('/student/'):
                    return redirect(reverse('student_dashboard')) 
                elif user.role == 'school' and not request.path.startswith('/school/'):
                    return redirect(reverse('school_dashboard')) 
                elif user.role == 'super_admin' and not request.path.startswith(''):
                    return redirect(reverse('dashboard')) 

            except User.DoesNotExist:
                del request.session['user_id']
                return redirect(reverse('home'))

        response = self.get_response(request)

        if hasattr(request, 'user'):
            response.context_data = response.context_data if hasattr(response, 'context_data') else {}
            response.context_data['user'] = request.user

        return response
