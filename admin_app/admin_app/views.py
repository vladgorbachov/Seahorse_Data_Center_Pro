# views.py в папке admin_app
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import CustomLoginForm


class CustomLoginView(LoginView):
    template_name = 'admin_app/login.html'  # Путь к шаблону страницы логина
    form_class = CustomLoginForm
    success_url = reverse_lazy('dashboard')  # Перенаправление на dashboard после успешного логина


@login_required
def dashboard_view(request):
    # Логика для отображения dashboard
    return render(request, 'admin_app/dashboard.html')