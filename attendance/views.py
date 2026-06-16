from django.shortcuts import redirect
from django.contrib import messages  # <-- Import messages
from django.contrib.auth.decorators import login_required
from .models import Attendance
from datetime import date

@login_required
def check_in(request):
    if request.method == 'POST':
        already_checked_in = Attendance.objects.filter(user=request.user, date=date.today()).exists()
        
        if not already_checked_in:
            Attendance.objects.create(user=request.user, status='Present')
            messages.success(request, "⚡ Attendance logged successfully! Have a great shift.")
        else:
            messages.warning(request, "⚠️ You have already punched in for today!")
            
    return redirect('employee_dashboard')