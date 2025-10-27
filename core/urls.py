from django.urls import path
from .views import *


urlpatterns = [
    path('',landingpageview,name='home'),
    # path('create/',create_linkview,name='create_link'),
    path('<str:short_code>/', redirect_to_original, name='redirect-anon'),
]