from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('admin_app.dashboard.urls')),
    path('deck/', include('admin_app.deck.urls')),
    path('bridge/', include('admin_app.bridge.urls')),
    path('catering/', include('admin_app.catering.urls')),
    path('electrical/', include('admin_app.electrical.urls')),
    path('engine/', include('admin_app.engine.urls')),
]
