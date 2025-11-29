from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dashboard/', include('dashboard.urls')),
    path('schools/', include('schools.urls')),
    path('student/', include('student.urls')),
    path('', include('auth.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
