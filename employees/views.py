from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Profile
from attendance.models import Attendance
from .forms import EmployeeForm
from datetime import date

def admin_only(view_func):
    """ Custom decorator to restrict access to Admins only """
    def wrapper(request, *args, **kwargs):
        try:
            if request.user.profile.role == 'admin':
                return view_func(request, *args, **kwargs)
        except Profile.DoesNotExist:
            pass
        return redirect('employee_dashboard')
    return wrapper

@login_required
@admin_only
def admin_dashboard(request):
    """ Read: Displays workforce data and calculated attendance analytics """
    # 1. Fetch all standard employees
    employees = User.objects.filter(profile__role='employee')
    total_employees = employees.count()
    
    # 2. Calculate today's attendance stats
    today = date.today()
    present_today = Attendance.objects.filter(date=today, status='Present').count()
    
    # Avoid dividing by zero if there are no employees registered yet
    absent_today = max(0, total_employees - present_today)
    
    if total_employees > 0:
        attendance_rate = round((present_today / total_employees) * 100, 1)
    else:
        attendance_rate = 0.0

    # 3. Pack everything into the context dictionary for the frontend
    context = {
        'employees': employees,
        'total_employees': total_employees,
        'present_today': present_today,
        'absent_today': absent_today,
        'attendance_rate': attendance_rate,
        'today_date': today.strftime("%B %d, %Y")
    }
    return render(request, 'employees/admin_dashboard.html', context)

@login_required
def employee_dashboard(request):
    """ Read: Individual portal for logged-in staff member """
    return render(request, 'employees/employee_dashboard.html')

@login_required
@admin_only
def employee_create(request):
    """ Create: Admin adds a new employee account and Profile """
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():  
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Create corresponding Profile record automatically
            Profile.objects.create(
                user=user,
                role=form.cleaned_data['role'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            return redirect('admin_dashboard')
    else:
        form = EmployeeForm()
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Add Employee'})

@login_required
@admin_only
def employee_update(request, pk):
    """ Update: Admin edits an existing employee profile """
    employee_user = get_object_or_404(User, pk=pk)
    profile = employee_user.profile
    
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee_user)
        if form.is_valid():
            user = form.save(commit=False)
            if form.cleaned_data['password']:
                user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Save corresponding Profile details
            profile.role = form.cleaned_data['role']
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.save()
            
            return redirect('admin_dashboard')
    else:
        initial_data = {
            'role': profile.role,
            'first_name': profile.first_name,
            'last_name': profile.last_name
        }
        form = EmployeeForm(instance=employee_user, initial=initial_data)
        
    return render(request, 'employees/employee_form.html', {'form': form, 'title': 'Edit Employee'})

@login_required
@admin_only
def employee_delete(request, pk):
    """ Delete: Admin removes an employee from the system """
    employee_user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        employee_user.delete()
        return redirect('admin_dashboard')
    return render(request, 'employees/employee_confirm_delete.html', {'employee': employee_user})