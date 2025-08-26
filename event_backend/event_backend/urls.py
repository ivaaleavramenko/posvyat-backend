from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home_view(request):
    return HttpResponse("""
        <h1>Event Registration API</h1>
        <p>Доступные endpoints:</p>
        <ul>
            <li><a href="/admin/">Admin panel</a></li>
            <li><a href="/api/visitors/">Visitors API</a></li>
            <li><a href="/api/waves/">Event Waves API</a></li>
        </ul>
    """)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('registration.urls')),
]
