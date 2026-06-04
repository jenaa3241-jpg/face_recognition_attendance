from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from students.models import Student
from attendance.models import Attendance
from datetime import date
@login_required(login_url='/accounts/login/')
def dashboard(request):

    total_students = Student.objects.count()

    present_today = Attendance.objects.filter(
        date=date.today()
    ).count()

    absent_today = total_students - present_today

    attendance_percentage = 0

    if total_students > 0:
        attendance_percentage = round(
            (present_today / total_students) * 100,
            2
        )

    recent_attendance = Attendance.objects.order_by(
        '-id'
    )[:10]

    context = {

        'total_students': total_students,
        'present_today': present_today,
        'absent_today': absent_today,
        'attendance_percentage': attendance_percentage,
        'recent_attendance': recent_attendance,

    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )