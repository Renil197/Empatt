from django.db import models
from django.contrib.auth.models import User

class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(auto_now_add=True)  # Automatically captures today's date
    status = models.CharField(max_length=20, default='Present')  # Simple string status
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.status}"
# Create your models here.
