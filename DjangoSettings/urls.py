"""
Here the URLs for the webpage are added
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from Dashboard.views import DashboardView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", DashboardView.as_view()),
    path("dashboard/", DashboardView.as_view())
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
