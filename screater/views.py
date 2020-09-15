from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

from .forms import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django_filters.views import FilterView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from qwestion.models import Survey, Qwestion, Answer
from .filter import QwestionTitleFilter, AnswerQwestionFilter






# Create your views here.

class SurveyListView(ListView):
    """
    Список подготовленных тестов
    """

    model = Survey
    paginate_by = 10  # if pagination is desired
    template_name = 'screater/surveys.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(SurveyListView, self).dispatch(request, *args, **kwargs)


class SurveyCreateView(CreateView):
    """
    Создание теста
    """
    model = Survey
    form_class = SurveyCreateForm
    template_name = 'screater/survey_form.html'
    success_url = reverse_lazy('screater:survey-list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(SurveyCreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        проверяем в поле author залогиненого пользователя
        :param form:
        :return:
        """
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_initial(self, *args, **kwargs):
        initial = super(SurveyCreateView, self).get_initial(**kwargs)
        # initial['title'] = 'My Title'
        return initial

    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(SurveyCreateView, self).get_form_kwargs(*args, **kwargs)
        kwargs['user'] = self.request.user
        return kwargs


class SurveyUpdateView(UpdateView):
    """
    Обновляем тест
    """
    model = Survey
    form_class = AddSurveyForm
    template_name_suffix = '_update_form'
    template_name = 'screater/survey_form.html'
    success_url = reverse_lazy('screater:survey-list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(SurveyUpdateView, self).dispatch(request, *args, **kwargs)


class QwestionCreate(CreateView):
    """
    пока  работает
    """""
    model = Qwestion
    template_name = 'screater/add_qwestion.html'
    form_class = QwestionCreateForm
    success_url = reverse_lazy('screater:qwestion-list')



    def get(self, request, *args, **kwargs):
         """
         Get request
         :param request:
         :param args:
         :param kwargs:
         :return:
         """
         self.object = None
         form_class = self.get_form_class()
         form = self.get_form(form_class)
         answer_form = AnswerFormset()
         return self.render_to_response(self.get_context_data(form=form,
                                                              answer_form=answer_form))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(QwestionCreate, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
          """
          Handles POST requests, instantiating a form instance and its inline
          formsets with the passed POST variables and then checking them for
          validity.
          """
          self.object = None
          form_class = self.get_form_class()
          form = self.get_form(form_class)
          answer_form = AnswerFormset(self.request.POST)
          if (form.is_valid() and answer_form.is_valid()):
              return  self.form_valid(form,  answer_form)
          else:
              return self.form_invalid(form,  answer_form)

    def form_valid(self, form,  answer_form):
          """
          Called if all forms are valid. Creates a Recipe instance along with
          associated Ingredients and Instructions and then redirects to a
          success page.
          """
          form.author = self.request.user
          self.object = form.save()
          answer_form.instance = self.object
          answer_form.save()

          return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form,  answer_form):
          """
          Called if a form is invalid. Re-renders the context data with the
          data-filled forms and errors.
          """
          return self.render_to_response(
              self.get_context_data(form=form,
                                    answer_form=answer_form))



class QwestionListView(FilterView):
    """
    Вывод список вопросов
    """
    model = Qwestion
    paginate_by = 10  # if pagination is desired
    filterset_class = QwestionTitleFilter
    template_name = 'screater/qwestions.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(QwestionListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Забираем параметры фильтра из строки запроса
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        survey = self.request.GET.get('survey','')
        survey = survey.replace(" ", "+")
        context['survey_id']=survey
        return context

class QwestionUpdateView(UpdateView):
    model = Qwestion
    form_class = QwestionForm
    template_name_suffix = '_update_form'
    template_name = 'screater/qwestion_form.html'
    success_url = reverse_lazy('screater:qwestion-list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(QwestionUpdateView, self).dispatch(request, *args, **kwargs)

class QwestionCreateView(CreateView):
    model = Qwestion
    template_name = 'screater/qwestion_form.html'
    success_url = reverse_lazy('screater:qwestion-list')
    form_class = QwestionCreateForm

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(QwestionCreateView, self).dispatch(request, *args, **kwargs)

class QwestionDeleteView(DeleteView):
    """
    Удаляем вопрос
    """
    model = Qwestion
    success_message = "Deleted Successfully"
    success_url = reverse_lazy('screater:qwestion-list')
    template_name = 'screater/qwestion_confirm_delete.html'



    def get_queryset(self):
        qs = super(QwestionDeleteView, self).get_queryset()
        return qs.filter(pk=self.kwargs['pk'])

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(QwestionDeleteView, self).dispatch(request, *args, **kwargs)

class AnswerListView(FilterView):
    """
    Список вопросов
    """
    model = Answer
    paginate_by = 10  # if pagination is desired
    filterset_class = AnswerQwestionFilter
    template_name = 'screater/answers.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(AnswerListView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Забираем параметры фильтра из строки запроса
        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        qwestion = self.request.GET.get('qwestion', '')
        qwestion = qwestion.replace(" ", "+")
        context['qwestion_id'] = qwestion
        return context


class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerCreateForm
    template_name = 'screater/answer_form.html'
    success_url = reverse_lazy('screater:answer-list')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(AnswerCreateView, self).dispatch(request, *args, **kwargs)


class AnswerUpdateView(UpdateView):
    model = Answer
    form_class = AnswerCreateForm
    template_name_suffix = '_update_form'
    template_name = 'screater/answer_form.html'
    success_url = reverse_lazy('screater:answer-list')


@method_decorator(login_required)
def dispatch(self, request, *args, **kwargs):
    """
    Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
    пользователями
    """
    return super(AnswerUpdateView, self).dispatch(request, *args, **kwargs)


class AnswerDeleteView(DeleteView):
    """
    Удаляем вопрос
    """
    model = Answer
    success_message = "Deleted Successfully"
    success_url = reverse_lazy('screater:answer-list')
    template_name = 'screater/answer_confirm_delete.html'



    def get_queryset(self):
        qs = super(AnswerDeleteView, self).get_queryset()
        return qs.filter(pk=self.kwargs['pk'])

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        """
        Декорируем диспетчер функцией login_required, чтобы запретить просмотр отображения неавторизованными
        пользователями
        """
        return super(AnswerDeleteView, self).dispatch(request, *args, **kwargs)
