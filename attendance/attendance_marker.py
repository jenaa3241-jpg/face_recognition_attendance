from datetime import date
from datetime import datetime

from students.models import Student
from attendance.models import Attendance


def mark_attendance(student_name):

    try:

        student = Student.objects.get(
            name=student_name
        )

        attendance_exists = Attendance.objects.filter(
            student=student,
            date=date.today()
        ).exists()

        if not attendance_exists:

            Attendance.objects.create(
                student=student,
                date=date.today(),
                check_in=datetime.now().time(),
                status="Present"
            )

            print(
                f"{student.name} marked present"
            )

    except Student.DoesNotExist:

        pass