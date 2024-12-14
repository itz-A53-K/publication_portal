from django.shortcuts import render, redirect
from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


from faculty import models

import secrets
import string

# Create your views here.

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'dept_admin/dashboard.html')



def loginView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        admin = authenticate(request, email=email, password=password, is_admin=True)

        if admin is not None:
            login(request, admin)
            return redirect('dashboard')
        else:
            return redirect('login')
    return render(request, 'dept_admin/login.html')




@login_required(login_url='login')
def logoutView(request):
    logout(request)
    return render(request, 'dept_admin/logout.html')




@login_required(login_url='login')
def addFaculty(request):

    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        dasignation = request.POST.get('designation')
        password = request.POST.get('password')

        dept = models.Department.objects.get(id = request.user.dept_id)

        if models.Faculty.objects.filter(email=email).exists():
            return JsonResponse({'status': 'email_exists'})
        
        faculty = models.Faculty(
            email=email,
            name=name,
            dept = dept,
            designation=dasignation,
        )
        faculty.set_password(password)
        faculty.save()

        faculty_details = models.Faculty_details(
            faculty = faculty,
            phone = phone,
        )
        faculty_details.save()

        return JsonResponse({'status': 'success'})


    return render(request, 'dept_admin/addFaculty.html')

