import cv2

from django.shortcuts import render, redirect
from django.contrib import messages

from attendance.camera import start_attendance
from .models import Attendance
from students.models import Student

from django.core.files.base import ContentFile

import os

def capture_attendance(request):

    camera = cv2.VideoCapture(0)

    ret, frame = camera.read()

    camera.release()

    if ret:

        student = Student.objects.first()

        filename = f"{student.id}.jpg"

        path = os.path.join(
            "media/attendance",
            filename
        )

        cv2.imwrite(path, frame)

        Attendance.objects.create(
            student=student,
            attendance_image=f'attendance/{filename}',
            status='Present'
        )

    return redirect(
        'attendance:attendance_history'
    )

from django.shortcuts import render
from .models import Attendance


def attendance_history(request):

    records = Attendance.objects.all().order_by('-date')

    return render(
        request,
        'attendance/attendance_history.html',
        {
            'records': records
        }
    )
def attendance_report(request):
    return render(
        request,
        'attendance/attendance_report.html'
    )
def recognition_logs(request):
    return render(
        request,
        'attendance/recognition_logs.html'
    )
def live_attendance(request):

    success = start_attendance()

    if success:
        return redirect("attendance_history")

    return redirect("attendance_history")