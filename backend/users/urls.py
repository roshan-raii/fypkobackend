from django.urls import path
from .views import *
urlpatterns=[
    path('login/',AdminLogin.as_view()),
    path('createTeacher/',CreateTeacher.as_view()),
    path('createStudent/',CreateStudent.as_view()),
    path('allUsers/',ViewUsers.as_view()),
    path('yearSection/',ViewYearSection.as_view()),
    path('allTeacher/', TeacherView.as_view())
]