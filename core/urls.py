from django.urls import path
from .views import *


urlpatterns = [
    path('',landingpageview,name='home'),
    path('create-link/', createlink, name='createlink'),
    path('<str:short_code>/', redirect_short_url, name='redirect-anon'),
]