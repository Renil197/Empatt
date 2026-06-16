from django.urls import path
from .views import UserLoginView, UserLogoutView, dashboard_redirect

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('dashboard/', dashboard_redirect, name='dashboard_redirect'), 
]