
from django.urls import path
from user import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.searchResult, name='searchResult'),
    path('view/<pubID>', views.viewPublication, name='viewPublication'),
    path('profile/<id>', views.userProfile, name='userProfile'),
]
