from django.urls import path
from . import views
app_name = "attendance"
urlpatterns = [
    path(
        'capture/',
        views.capture_attendance,
        name='capture_attendance'
    ),
    path(
        'live/',
        views.live_attendance,
        name='live_attendance'
    ),

    path(
        'history/',
        views.attendance_history,
        name='attendance_history'
    ),

]