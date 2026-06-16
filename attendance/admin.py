from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'status', 'created_at')
    list_filter = ('status', 'date')
    search_fields = ('user__username', 'status')
# Register your models here.
