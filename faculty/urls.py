
from django.urls import path
from faculty import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.loginView, name='loginView'),
    path('logout/', views.logoutView, name='logoutView'),
    path('myProfile', views.myProfile, name='myProfile'),
    path('upload/article/', views.upload_article, name='upload_article'),
]
