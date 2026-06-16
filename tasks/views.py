from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Task
from accounts.models import Profile

def admin_only(view_func):
    """ Custom decorator to restrict task assignments to Admins only """
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
def create_task(request):
    """ Create: Admin view to assign a task structure to an employee """
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        user_id = request.POST.get('assigned_to')
        due_date = request.POST.get('due_date')
        
        assigned_user = get_object_or_404(User, id=user_id)
        
        Task.objects.create(
            title=title, 
            description=description, 
            assigned_to=assigned_user, 
            due_date=due_date
        )
        return redirect('admin_dashboard')
        
    # Gather workforce targets with the matching simple profile string
    employees = User.objects.filter(profile__role='employee')
    return render(request, 'tasks/create_task.html', {'employees': employees})

@login_required
def complete_task(request, task_id):
    """ Update: Employee flags an assignment module object as finished """
    task = get_object_or_404(Task, id=task_id, assigned_to=request.user)
    task.status = 'Completed'
    task.save()
    return redirect('employee_dashboard')