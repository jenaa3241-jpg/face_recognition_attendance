from django.shortcuts import render

def daily_report(request):
    return render(
        request,
        'reports/daily_report.html'
    )

def monthly_report(request):
    return render(
        request,
        'reports/monthly_report.html'
    )