
from django.urls import path
from .views import *
app_name = 'screater'

urlpatterns = [
    path('', SurveyListView.as_view(), name='survey-list'),
    path('survey/<int:pk>/edit/', SurveyUpdateView.as_view(), name='survey-edit'),
    path('survey/new/', SurveyCreateView.as_view(), name='survey-new'),
    path('qwestion/', QwestionListView.as_view(), name='qwestion-list'),
    path('qwestion/<int:pk>/edit/', QwestionUpdateView.as_view(), name='qwestion-update'),
    path('qwestion/new/', QwestionCreateView.as_view(), name='qwestion-new'),
    path('qwestion/new/answers/', QwestionCreate.as_view(), name='qwestions-answers'),
    path('qwestion/<int:pk>/delete/', QwestionDeleteView.as_view(), name='qwestion-delete'),
    path('answer/', AnswerListView.as_view(), name='answer-list'),
    path('answer/new/', AnswerCreateView.as_view(), name='answer-new'),
    path('answer/<int:pk>/edit/', AnswerUpdateView.as_view(), name='answer-update'),
    path('answer/<int:pk>/delete/',AnswerDeleteView.as_view(), name='answer-delete'),

]