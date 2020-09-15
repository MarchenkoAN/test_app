import django_filters
from qwestion.models import Qwestion, Answer
class QwestionTitleFilter(django_filters.FilterSet):
    class Meta:
         model = Qwestion
         fields = {
             'survey',
         }

class AnswerQwestionFilter(django_filters.FilterSet):
    class Meta:
        model = Answer
        fields = {
            'qwestion',

        }

