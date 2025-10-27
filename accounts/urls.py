from django.urls import path
from .views import *


urlpatterns = [
    path('register/',registerview,name='register'),
    path('sign-in/',loginview,name='login'),
    path('logout/',logoutview,name='logout'),
    path('dashboard/',dashboardview,name='dashboard'),
    path('profile/',profileview,name='userprofile'),
    path('manage/',managelinksview,name='managelinks'),
    path('analytics/',analyticsview,name='analytics'),
]