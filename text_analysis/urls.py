# text_analysis/urls.py
from django.urls import path
from .views import home, download_report

urlpatterns = [
    path('', home, name='home'),
    path('download/<path:url>/', download_report, name='download_report'),
]
