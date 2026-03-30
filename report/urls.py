from django.urls import path
from . import views

urlpatterns = [
    path('', views.report_issue, name='report_issue'),
    path('api/reports/', views.get_reports, name='get_reports'),
]