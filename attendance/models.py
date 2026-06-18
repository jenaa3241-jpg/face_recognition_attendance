from django.db import models
from students.models import Student

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    image = models.ImageField(upload_to="attendance/", null=True, blank=True)

    status = models.CharField(max_length=20, default="Present")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        
        return f"{self.student.name}"