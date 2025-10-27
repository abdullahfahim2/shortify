from django.urls import path
from .views import *


urlpatterns = [
    path('register/',registerview,name='register'),
    path('sign-in/',loginview,name='login'),
    path('logout/',logoutview,name='logout'),
    path('dashboard/',dashboardview,name='dashboard')
]