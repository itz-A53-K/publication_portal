
from django.urls import path
from dept_admin import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('addFaculty/', views.addFaculty, name='addFaculty'),
]
