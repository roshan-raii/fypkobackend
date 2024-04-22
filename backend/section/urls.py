from django.urls import path
from .views import *

urlpatterns = [
    path('',SectionView.as_view()),
    path('assign/',YearSectionView.as_view()),
    path('all/',ViewAllSections.as_view()),
    path('yearFac/',FacultyYearView.as_view())

]
