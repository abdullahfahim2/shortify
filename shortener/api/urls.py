from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('apis/',Shorturlcreate.as_view()),
    path('<pk>/',ShortUrlDetail.as_view()),
]