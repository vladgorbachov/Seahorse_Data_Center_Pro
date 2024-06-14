from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('deck/', include('admin_app.deck.urls')),
    path('', include('admin_app.dashboard.urls')),  # Главная страница
]
