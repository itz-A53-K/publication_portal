
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.

def home(request):
    return render(request, 'user/index.html')
