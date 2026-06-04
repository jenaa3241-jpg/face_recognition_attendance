from django.urls import path
from . import views
app_name = "students" 
urlpatterns = [
    path('', views.student_list, name='student_list'),
    path('add/', views.add_student, name='add_student'),
    path('edit/<int:id>/', views.edit_student, name='edit_student'),
    path('profile/<int:id>/', views.student_profile, name='student_profile'),
     path('delete/<int:id>/', views.delete_student, name='delete_student'),
]