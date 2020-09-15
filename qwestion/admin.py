from django.contrib import admin
from .models import Qwestion, Survey, Answer, Rating
@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'author',  'timedelta', 'created', 'updated')
    fields = ['title', 'author','timedelta','public']
    list_filter = ('title','author','timedelta','public')
@admin.register(Qwestion)
class QwestionAdmin(admin.ModelAdmin):
    list_display = ('survey','title', 'input')
    list_filter = ('survey','title',)

@admin.register(Answer)
class OtvetAdmin(admin.ModelAdmin):
    list_display = ('qwestion', 'title', 'truefild')
    list_filter = ('qwestion',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('created','username','email','result','sessionid')
    list_filter = ('sessionid','username','created')