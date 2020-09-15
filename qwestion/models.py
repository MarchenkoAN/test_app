from django.db import models
from django.contrib.auth.admin import User
from django.urls import reverse


class Survey(models.Model):
    title = models.CharField(max_length=255, verbose_name='Наименование теста')
    author = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name=' Автор')
    timedelta = models.IntegerField(default=0, verbose_name='Время выполнения теста')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    public = models.BooleanField(default=False, verbose_name="Опубликовано")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('qwestion:survey_detail', kwargs={"pk": self.id})

    class Meta:
        ordering = ['title', 'created']


class Qwestion(models.Model):
    Q_CHOICES = (
        ('ch', 'checkbox'),
        ('rd', 'radio'),
    )
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, verbose_name='Наименование теста')
    title = models.CharField(max_length=755, verbose_name='Вопрос')
    input = models.CharField(max_length=2, choices=Q_CHOICES, default='ch', verbose_name='Тип поля')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("qwestion:survey-start", kwargs={"pk": self.id})

    class Meta:
        ordering = ['pk']


class Answer(models.Model):
    qwestion = models.ForeignKey(Qwestion, on_delete=models.CASCADE, verbose_name='Вопрос')
    title = models.CharField(max_length=555, verbose_name='Ответ')
    truefild = models.BooleanField(default=False, verbose_name='Правильный ответ')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['pk']


class Rating(models.Model):
    username = models.CharField(max_length=55, db_index=True, verbose_name='Имя пользователя')
    email = models.CharField(max_length=55, verbose_name='Email')
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT, verbose_name='Наменование теста')
    sessionid = models.CharField(max_length=200, db_index=True)
    qwestion = models.ForeignKey(Qwestion, on_delete=models.PROTECT, verbose_name='Вопрос')
    answer = models.CharField(max_length=100, verbose_name='Список номеров ответов пользователя')
    true_answer = models.CharField(max_length=100, verbose_name='Список номеров правильных ответов')
    result = models.BooleanField(default=False, verbose_name='Результат')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата ответа')

    def __str__(self):
        return self.sessionid

    class Meta:
        ordering = ['sessionid', '-created']
