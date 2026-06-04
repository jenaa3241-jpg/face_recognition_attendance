from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

   path(
        '',
        lambda request: redirect('/accounts/login/')
    ),

    path( 'dashboard/', include('dashboard.urls')),

    path(
        'accounts/',
        include('accounts.urls')
    ),

    path(
        'students/',
        include('students.urls')
    ),

    path(
        'attendance/',
        include('attendance.urls')
    ),

    path(
        'reports/',
        include('reports.urls')
    ),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )