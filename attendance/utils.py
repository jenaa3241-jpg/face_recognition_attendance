from datetime import date
from .models import Attendance

def mark_attendance(student, frame, confidence):

    today = date.today()

    if Attendance.objects.filter(
        student=student,
        date=today
    ).exists():

        return False

    import cv2
    import os

    filename = f"{student.student_id}_{today}.jpg"

    folder = "media/attendance"

    os.makedirs(folder, exist_ok=True)

    path = os.path.join(folder, filename)

    cv2.imwrite(path, frame)

    Attendance.objects.create(
        student=student,
        attendance_image=f"attendance/{filename}",
        status="Present"
    )

    return True