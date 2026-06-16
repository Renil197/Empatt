from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Columns to display in the admin table list
    list_display = ('user', 'role', 'first_name', 'last_name', 'created_at')
    
    # Allows filtering users by their roles in the right sidebar
    list_filter = ('role',)
    
    # Adds a search bar to look up profiles by username or email
    search_fields = ('user__username', 'user__email', 'first_name', 'last_name')
# Register your models here.
