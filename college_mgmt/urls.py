from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),

    # Root → dashboard (login_required redirects to /login/ automatically)
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),

    # All app URLs
    path('accounts/', include('accounts.urls')),
    path('dashboard/', include('core.urls')),
    path('students/',  include('students.urls')),
    path('attendance/', include('attendance.urls')),
    path('results/',   include('results.urls')),
    path('finance/',   include('finance.urls')),
    path('bonafide/',  include('bonafide.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
