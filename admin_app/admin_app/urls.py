from django.contrib import admin
from django.urls import include
from django.views.generic import RedirectView
from .forms import CustomLoginForm
from django.urls import path
from django.contrib.auth.views import LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
    path('deck/', include('admin_app.deck.urls')),
    path('bridge/', include('admin_app.bridge.urls')),
    path('catering/', include('admin_app.catering.urls')),
    path('electrical/', include('admin_app.electrical.urls')),
    path('engine/', include('admin_app.engine.urls')),
    path('login/', LoginView.as_view(template_name='admin_app/login.html', form_class=CustomLoginForm), name='login'),
    path('dashboard/', include('admin_app.dashboard.urls')),
]
