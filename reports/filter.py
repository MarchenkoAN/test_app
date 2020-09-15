import django_filters
from qwestion.models import Rating
class RatintSurveyFilter(django_filters.FilterSet):
    class Meta:
         model = Rating
         fields = {
             'survey',
         }

    # def __init__(self, *args, **kwargs):
    #     super(RatintSurveyFilter, self).__init__(*args, **kwargs)
    #     # at sturtup user doen't push Submit button, and QueryDict (in data) is empty
    #     if self.data == {}:
    #         self.queryset = self.queryset.none()