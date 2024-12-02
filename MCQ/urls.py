
from django.urls import path

from .import views

app_name = 'quiz'

urlpatterns = [
    path('', views.Question_View, name="mcq"),
    path('quiz/' , views.quiz , name="quiz"),
    path('quiz/results/', views.quiz_results, name='quiz_results'),
]

