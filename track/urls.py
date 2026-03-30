from django.urls import path
from . import views

urlpatterns = [
    path('', views.track_issue, name='track_issue'),
]