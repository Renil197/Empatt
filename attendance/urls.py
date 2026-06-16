from django.urls import path
from . import views

urlpatterns = [
    # The URL pattern that matches the check-in form action button
    path('check-in/', views.check_in, name='check_in'),
]