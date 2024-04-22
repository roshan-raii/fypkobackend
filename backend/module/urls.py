from rest_framework.urls import path
from .views import *
urlpatterns = [
    path('',ModuleView.as_view()),
    path('teacher/',ModuleTeacherView.as_view())
    # path('modYear/',ModuleYear.as_view())
]