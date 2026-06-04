from django.urls import path
from . import views

from .views import logout_view

urlpatterns = [
    
    path(
        'logout/',
        logout_view,
        name='logout'
    ),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('users/', views.users_view, name='users'),
]