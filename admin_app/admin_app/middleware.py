# admin_app/middleware.py

from django.shortcuts import redirect
from django.urls import reverse

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path_info != reverse('login'):
            return redirect('login')
        response = self.get_response(request)
        return response