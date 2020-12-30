from django.shortcuts import render

from .models import Schema

# Create your views here.


def DashboardView(request):

    return render(request=request, template_name="schemas/dashboard.html")
