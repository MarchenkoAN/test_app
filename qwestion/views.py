from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
# from django.core.signing import Signer
from .form import ContactForm
import uuid

import datetime

from .models import *


# Create your views here.


def index(request):
    """
    Список тестов
    :param request:
    :return:
    """
    survey = Survey.objects.filter(public=True)
    return render(request, 'qwestion/index.html', context={'survey': survey})


def pause(request):
    """
    Отсрочка ответа на вопрос
    :param request:
    :return:
    """
    if request.method == 'POST':
        qwestion_id = request.POST.get("qwestion_id")
        qwestions = list(request.session['qwestions'])
        qwestions.append(qwestion_id)
        qwestions.reverse()
        value = qwestions.pop()
        print(value)
        request.session['qwestions'] = qwestions
        request.session.modified = True

    return HttpResponseRedirect(reverse('qwestion:survey-start', kwargs={'pk': value}))


def start(request, pk):
    """
    Страница вопросов
    :param request:
    :param pk:
    :return:
    """
    if request.method == 'POST':
        sessionid = request.session['sessionkey']
        name = request.session['username']
        email = request.session['email']
        answers = [entry for entry in request.POST.values()][1:-2]
        answers = list(map(int, answers))
        survey_id = request.POST.get("survey_id")
        qwestion_id = request.POST.get("qwestion_id")
        answers_true = list(Answer.objects.filter(qwestion=qwestion_id, truefild=True).values_list('id', flat=True))
        if len(list(set(answers) ^ set(answers_true))) == 0:
            result = True
        else:
            result = False

        rating = Rating(username=name,email=email, survey=Survey.objects.get(pk=survey_id), sessionid=sessionid, qwestion=Qwestion.objects.get(pk=qwestion_id),
                        answer=answers,
                        true_answer=answers_true, result=result)
        rating.save()
        qwestions = list(request.session['qwestions'])
        if len(qwestions) == 0:
            #delete_session(request)
            return HttpResponseRedirect(reverse('qwestion:survey-stop'))

        else:
            value = qwestions.pop()
            request.session['qwestions'] = qwestions
            request.session.modified = True
            return HttpResponseRedirect(reverse('qwestion:survey-start', kwargs={'pk': value}))

    else:
        try:
            request.session['username']
        except:
            return HttpResponseRedirect(reverse('qwestion:index'))
        if stop_time(request):
            return HttpResponseRedirect(reverse('qwestion:survey-stop'))

            #return render(request, 'qwestion/stop.html', context={})
        qwestion = get_object_or_404(Qwestion, pk=pk)
        answers = Answer.objects.order_by('?').filter(qwestion=qwestion)
        mytimer = my_timer(request)
        return render(request, 'qwestion/start.html', context={'qwestion': qwestion, 'answers': answers, 'mytimer': mytimer})


def survey_view(request, pk):
    """
    Страница регистрации пользователей
    :param request:
    :param pk:
    :return:
    """
    form = ContactForm()
    if request.method == "GET":
        survey = get_object_or_404(Survey, pk=pk)
        return render(request, 'qwestion/survey_detail.html', {'survey': survey, 'form': form})

    if request.method == 'POST':
        request.session['username'] = request.POST.get("name")
        request.session['email'] = request.POST.get("email")
        request.session['timedelta'] = request.POST.get("timedelta")
        request.session['start_time'] = str(datetime.datetime.now())
        # signer = Signer()
        # request.session['sessionkey'] = signer.sign(request.POST.get("name") + ':' + request.POST.get("email") + ':' + str(datetime.datetime.now()))
        request.session['sessionkey'] = uuid.uuid4().hex
        survey_id = request.POST.get("surveyId")
        request.session['survey_id']  = survey_id
        qwestions = list(Qwestion.objects.order_by('?').filter(survey__id=survey_id).values_list('id', flat=True))
        value = qwestions.pop()
        request.session['qwestions'] = qwestions
        request.session.modified = True
        # return HttpResponse("UserName: {0} Qwestions: {1} value:{2}".format(request.session['username'], request.session['qwestion'], value))
        return HttpResponseRedirect(reverse('qwestion:survey-start', kwargs={'pk': value}))


def survey_stop(request):
    """
    Формируем последнюю страницу теста- результаты
    :param request:
    :return:
    """
    username = None
    try:

        survey_id = request.session['survey_id']
        sessionid = request.session['sessionkey']
        username =  request.session['username']


    except:
        # return render(request, 'qwestion/stop.html')
        pass

    survey = Survey.objects.get(pk=int(survey_id))
    countQwestion = Qwestion.objects.filter(survey=survey).count()
    rightAnswer = Rating.objects.filter(sessionid=sessionid,result=True).count()
    procent = rightAnswer/countQwestion*100

    delete_session(request)
    return render(request, 'qwestion/stop.html', context={'survey': survey, 'count': countQwestion, 'right': rightAnswer,'procent': procent,
                                                          'username':username})

def delete_session(request):
    """
    Удаляем данные сессии
    :param request:
    :return:
    """
    try:
        del request.session['qwestions']
        del request.session['username']
        del request.session['email']
        del request.session['timedelta']
        del request.session['start_time']
        del request.session['sessionid']
        del request.session['survey_id']
        del request.session['sessionkey']
        request.session.modified = True

    except KeyError:
        pass


def stop_time(request):
    try:
        timedelta = datetime.timedelta(minutes=int(request.session['timedelta']))
        start_time = datetime.datetime.strptime(request.session['start_time'], '%Y-%m-%d %H:%M:%S.%f')
        now = datetime.datetime.now()
        delta = start_time + timedelta

        if delta > now:
            return False
    except:
        return True
        # return render(request, 'qwestion/stop.html', context={})
    # return render(request, 'qwestion/stop.html', context={})
    return True


def my_timer(request):
    """
    Возвращаем время до окончания теста
    :param request:
    :return:
    """
    try:
        timedelta = datetime.timedelta(minutes=int(request.session['timedelta']))
        start_time = datetime.datetime.strptime(request.session['start_time'], '%Y-%m-%d %H:%M:%S.%f')
        now = datetime.datetime.now()
        delta = start_time + timedelta

        if delta > now:
            return delta
    except:
        return 0
        # return render(request, 'qwestion/stop.html', context={})
    # return render(request, 'qwestion/stop.html', context={})
    return 0