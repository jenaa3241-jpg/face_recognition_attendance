from django.db import models


class Student(models.Model):

    student_id = models.CharField(
        max_length=20,
        unique=True
    )

    name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    department = models.CharField(
        max_length=100
    )

    photo = models.ImageField(
    upload_to='students/',
    blank=True,
    null=True,
    default='students/photo.jpg'
    )

    embedding = models.JSONField(
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.name