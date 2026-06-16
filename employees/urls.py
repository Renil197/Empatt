from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/add/', views.employee_create, name='employee_create'),
    path('employee/edit/<int:pk>/', views.employee_update, name='employee_update'),
    path('employee/delete/<int:pk>/', views.employee_delete, name='employee_delete'),
]