from django.urls import path
from .views import *

urlpatterns = [
    path('',YearView.as_view())
    
]
