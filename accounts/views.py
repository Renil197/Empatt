from django.shortcuts import redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .models import Profile

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

@login_required
def dashboard_redirect(request):
    """ Simple check: if the profile role is admin, send to admin dashboard """
    try:
        if request.user.profile.role == 'admin':
            return redirect('admin_dashboard')
    except Profile.DoesNotExist:
        pass
        
    return redirect('employee_dashboard')

class UserLogoutView(LogoutView):
    next_page = 'login'