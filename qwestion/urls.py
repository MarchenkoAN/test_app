from django.urls import path
from . import views
app_name = 'qwestion'
urlpatterns = [
   # и т.д. пишешшь више чем нижняя строка
    path('', views.index, name='index'),
    path('s/<int:pk>/', views.start, name='survey-start'),
    path('survey/<int:pk>/', views.survey_view, name='survey_detail'),
    path('stop/', views.survey_stop, name='survey-stop'),
    path('pause/', views.pause, name='survey-pause'),
]
