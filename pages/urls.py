from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),                    # Single-page homepage
    path('contact-submit/', views.contact_form_submit, name='contact_submit'),  # Form submission
    path('set-language/<str:lang_code>/', views.set_language, name='set_language'),
]